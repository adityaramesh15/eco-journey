import json
import sys
import numpy as np  
from sklearn.preprocessing import MinMaxScaler  
from database import db


def create_ranking(input_data, pref_temp, pref_precp, bad_days, rainy_days, 
                   start_month, start_day, end_month, end_day):
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

    city_info_list = []
    distances_to_scale = []
    
    pref_temp *= 10

    for city_data in input_data:
        city, state, avg_tavg, avg_prcp = city_data
        
        temp_distance = abs(avg_tavg - pref_temp)
        prcp_distance = abs(avg_prcp - translated_pref_precp)
        
        city_info_list.append({
            'city': city,
            'state': state
        })
        
        distances_to_scale.append([temp_distance, prcp_distance])

    
    distances_array = np.array(distances_to_scale)
    scaler = MinMaxScaler()
    normalized_distances = scaler.fit_transform(distances_array)
    
    
    city_scores = []
    for i, city_info in enumerate(city_info_list):
        
        norm_temp_dist = normalized_distances[i][0]
        norm_prcp_dist = normalized_distances[i][1]
        
        score = norm_temp_dist + norm_prcp_dist
        
        city = city_info['city']
        state = city_info['state']
        has_bad_days = False
        has_rainy_days = False
        
        if bad_days:
            has_bad_days = check_bad_days(start_month, start_day, end_month, end_day, city, state)
        
        if rainy_days:
            has_rainy_days = check_rainy_days(start_month, start_day, end_month, end_day, city, state)

        city_scores.append({
            'city': city,
            'state': state,
            'score': score,
            'bad_days': has_bad_days,
            'rainy_days': has_rainy_days
        })

    ranked_cities = sorted(city_scores, key=lambda x: x['score'])


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



def check_bad_days(start_month, start_day, end_month, end_day, city, state): 
    """
    Checks if a location has ANY "bad days" (TAVG < 150 or > 270, or PRCP > 1000)
    in the given date range.
    Returns True if bad days EXIST, False otherwise.
    """

    sql = """
        SELECT EXISTS (
            SELECT 1
            FROM LOCATIONS L
            WHERE L.CITY = %s
                AND L.STATE = %s
                AND NOT EXISTS (
                SELECT 1
                FROM (
                    SELECT RND_LAT, RND_LNG
                    FROM HISTORICAL_WEATHER
                    WHERE (
                        (H_MONTH = %s AND H_DAY >= %s AND (%s = %s OR H_DAY <= %s))
                        OR
                        (%s <> %s AND H_MONTH = %s AND H_DAY <= %s)
                    )
                    AND (TAVG < 150 OR TAVG > 270 OR PRCP > 1000)
                ) S
                WHERE S.RND_LAT = L.RND_LAT
                    AND S.RND_LNG = L.RND_LNG
                )
            ) AS good_weather;
    """
    
    params = (
        city, state, 
        start_month, start_day, start_month, end_month, end_day,
        start_month, end_month, end_month, end_day
    )
    
    result = db.execute(sql, params, fetchone=True)
    return not bool(result['good_weather']) 


def check_rainy_days(start_month, start_day, end_month, end_day, city, state): 
    """
    Checks if a location has ANY "rainy days" (PRCP > 200)
    in the given date range.
    Returns True if rainy days EXIST, False otherwise.
    """
    
    sql = """
        SELECT EXISTS (
          SELECT 1
          FROM LOCATIONS L
          WHERE L.CITY = %s
            AND L.STATE = %s
            AND EXISTS (
              SELECT 1
              FROM (
                SELECT RND_LAT, RND_LNG
                FROM HISTORICAL_WEATHER
                WHERE (
                        (H_MONTH = %s AND H_DAY >= %s AND (%s = %s OR H_DAY <= %s))
                        OR
                        (%s <> %s AND H_MONTH = %s AND H_DAY <= %s)
                      ) AND PRCP > 200
              ) S
              WHERE S.RND_LAT = L.RND_LAT
                AND S.RND_LNG = L.RND_LNG
            )
        ) AS rainy_flag;
    """
    
    params = (
        city, state, 
        start_month, start_day, start_month, end_month, end_day,
        start_month, end_month, end_month, end_day
    )

    result = db.execute(sql, params, fetchone=True)    
    return bool(result['rainy_flag'])