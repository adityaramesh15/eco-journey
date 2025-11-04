import json
import sys
import numpy as np  
from sklearn.preprocessing import MinMaxScaler  



def create_ranking(input_data, pref_temp, pref_precp, bad_days, rainy_days, 
                   start_month, start_day, end_month, end_day, conn):
    """
    Ranks three input locations based on normalized distance from user preferences,
    using scikit-learn's MinMaxScaler.
    """
    
    if pref_precp == 0:
        translated_pref_precp = 0
    elif pref_precp == 1:
        translated_pref_precp = 50
    else:
        translated_pref_precp = 100

    # 2. Calculate raw distances and store city info
    city_info_list = []
    distances_to_scale = []

    for city_data in input_data:
        city, state, avg_tavg, avg_prcp = city_data
        
        # Calculate the raw distance (difference) from preference
        temp_distance = abs(avg_tavg - pref_temp)
        prcp_distance = abs(avg_prcp - translated_pref_precp)
        
        # Store city info to be used after scaling
        city_info_list.append({
            'city': city,
            'state': state
        })
        
        # Store distances in a format for the scaler
        distances_to_scale.append([temp_distance, prcp_distance])

    # 3. Use MinMaxScaler to normalize both distance columns (features)
    
    # Convert to numpy array
    distances_array = np.array(distances_to_scale)
    
    # Create and fit the scaler
    scaler = MinMaxScaler()
    normalized_distances = scaler.fit_transform(distances_array)
    
    # normalized_distances is now a numpy array like:
    # [[norm_temp_dist_1, norm_prcp_dist_1],
    #  [norm_temp_dist_2, norm_prcp_dist_2],
    #  [norm_temp_dist_3, norm_prcp_dist_3]]
    # where values are scaled from 0 (best, min distance) to 1 (worst, max distance)

    # 4. Calculate final scores and apply penalties
    city_scores = []
    for i, city_info in enumerate(city_info_list):
        
        norm_temp_dist = normalized_distances[i][0]
        norm_prcp_dist = normalized_distances[i][1]
        
        # The final score is the sum of normalized distances. Lower is better.
        score = norm_temp_dist + norm_prcp_dist
        
        city = city_info['city']
        state = city_info['state']
        has_bad_days = False
        has_rainy_days = False
        
        # Apply penalties if user requested checks
        if bad_days:
            has_bad_days = check_bad_days(start_month, start_day, end_month, end_day, city, state, conn)
            if has_bad_days:
                score += 1000  # Add large penalty
                
        if rainy_days:
            has_rainy_days = check_rainy_days(start_month, start_day, end_month, end_day, city, state, conn)
            if has_rainy_days:
                score += 1000  # Add large penalty

        # Store results
        city_scores.append({
            'city': city,
            'state': state,
            'score': score,
            'bad_days': has_bad_days,
            'rainy_days': has_rainy_days
        })

    # 5. Sort cities by score (lowest to highest)
    ranked_cities = sorted(city_scores, key=lambda x: x['score'])

    # 6. Format the final output dictionary
    output = {}
    for i, city_info in enumerate(ranked_cities):
        rank_key = f"rank_{i+1}_location"
        output[rank_key] = {
            "city": city_info['city'],
            "state": city_info['state'],
            "bad_days": city_info['bad_days'],
            "rainy_days": city_info['rainy_days']
        }
            
    return output



def check_bad_days(start_month, start_day, end_month, end_day, city, state, conn):
    """
    Checks if a location has ANY "bad days" (TAVG < 150 or > 270, or PRCP > 1000)
    in the given date range.
    Returns True if bad days EXIST, False otherwise.
    """
    sql = f"""
        SELECT EXISTS (
            SELECT 1
            FROM LOCATIONS L
            WHERE L.CITY = '{city}'
                AND L.STATE = '{state}'
                AND NOT EXISTS (
                SELECT 1
                FROM (
                    SELECT RND_LAT, RND_LNG
                    FROM HISTORICAL_WEATHER
                    WHERE (
                        (H_MONTH = {start_month} AND H_DAY >= {start_day} AND ({start_month} = {end_month} OR H_DAY <= {end_day}))
                        OR
                        ({start_month} <> {end_month} AND H_MONTH = {end_month} AND H_DAY <= {end_day})
                    )
                    AND (TAVG < 150 OR TAVG > 270 OR PRCP > 1000)
                ) S
                WHERE S.RND_LAT = L.RND_LAT
                    AND S.RND_LNG = L.RND_LNG
                )
            ) AS good_weather;
    """
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()[0]  # This is True if weather is good
    return not bool(result)     # Return True if weather is bad


def check_rainy_days(start_month, start_day, end_month, end_day, city, state, conn):
    """
    Checks if a location has ANY "rainy days" (PRCP > 200)
    in the given date range.
    Returns True if rainy days EXIST, False otherwise.
    """
    sql = f"""
        SELECT EXISTS (
          SELECT 1
          FROM LOCATIONS L
          WHERE L.CITY = '{city}'
            AND L.STATE = '{state}'
            AND EXISTS (
              SELECT 1
              FROM (
                SELECT RND_LAT, RND_LNG
                FROM HISTORICAL_WEATHER
                WHERE (
                        (H_MONTH = {start_month} AND H_DAY >= {start_day} AND ({start_month} = {end_month} OR H_DAY <= {end_day}))
                        OR
                        ({start_month} <> {end_month} AND H_MONTH = {end_month} AND H_DAY <= {end_day})
                      ) AND PRCP > 200
              ) S
              WHERE S.RND_LAT = L.RND_LAT
                AND S.RND_LNG = L.RND_LNG
            )
        ) AS rainy_flag;
    """
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()[0]
    return bool(result)