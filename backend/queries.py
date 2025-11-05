import MySQLdb
from database import db
from datetime import date

def create_user(username, password):
    """
    Creates a new user and returns their details.
    """
    try:

        sql_insert = "INSERT INTO USERS (username, password) VALUES (%s, %s)"
        conn = db._get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql_insert, (username, password))
            conn.commit()
            new_id = cur.lastrowid
            
            cur.execute("SELECT userID AS user_id, username FROM USERS WHERE userID = %s", (new_id,))
            return cur.fetchone()
        finally:
            conn.close()
    except MySQLdb.IntegrityError:
        return None

def login_user(username, password):
    """
    Checks credentials for login.
    """
    sql = "SELECT userID AS user_id FROM USERS WHERE username = %s AND password = %s"
    return db.execute(sql, (username, password), fetchone=True)

def check_city_exists(city, state):
    """
    Checks if a city exists in the database.
    """
    sql = "SELECT EXISTS(SELECT 1 FROM LOCATIONS WHERE CITY = %s AND STATE = %s) AS `exists`"
    result = db.execute(sql, (city, state), fetchone=True)
    return bool(result['exists']) if result else False

def get_ranking_data(cities, m1, d1, m2, d2):
    """
    Gets averaged weather data for selected locations.
    Expecting 'cities' to be a list of tuples: [(city1, state1), (city2, state2), ...]
    """

    in_placeholders = ', '.join(['(%s, %s)'] * len(cities))
    
    sql = f"""
        SELECT L.CITY, L.STATE, AVG(S.TAVG) AS avg_temp, AVG(S.PRCP) AS avg_precipitation
        FROM LOCATIONS AS L
        JOIN (
          SELECT RND_LAT, RND_LNG, TAVG, PRCP
          FROM HISTORICAL_WEATHER
          WHERE (H_MONTH = %s AND H_DAY >= %s AND (%s = %s OR H_DAY <= %s))
             OR (%s <> %s AND H_MONTH = %s AND H_DAY <= %s)
        ) AS S ON S.RND_LAT = L.RND_LAT AND S.RND_LNG = L.RND_LNG
        WHERE (L.CITY, L.STATE) IN ({in_placeholders})
        GROUP BY L.CITY, L.STATE
    """
    
    city_params = [item for sublist in cities for item in sublist]
    params = (m1, d1, m1, m2, d2, m1, m2, m2, d2, *city_params)
    
    return db.execute(sql, params, fetchall=True)

def get_user_trip_count(user_id):
    sql = "SELECT COUNT(*) AS count FROM TRIP_PLANS WHERE userID = %s"
    result = db.execute(sql, (user_id,), fetchone=True)
    return result['count'] if result else 0

def save_new_trip(user_id, trip_name, start_date, end_date, precip_pref, temp_pref, locations):
    """
    Transactional save of a new trip.
    """
    conn = db._get_connection()
    try:
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO TRIP_PLANS (userID, planName, startDate, endDate) VALUES (%s, %s, %s, %s)",
            (user_id, trip_name, start_date, end_date)
        )
        trip_id = cur.lastrowid
        
        pref_sql = "INSERT INTO PREFERENCES (tripID, featureName, preferredValue) VALUES (%s, %s, %s)"
        cur.executemany(pref_sql, [
            (trip_id, 'precipitation', precip_pref),
            (trip_id, 'temperature', temp_pref)
        ])
        

        loc_sql = "INSERT INTO TRIP_LOCATIONS (tripID, CITY, STATE) VALUES (%s, %s, %s)"
        loc_data = [(trip_id, loc['city'], loc['state']) for loc in locations]
        cur.executemany(loc_sql, loc_data)
        
        conn.commit()
        return {'trip_id': trip_id}
    except Exception as e:
        conn.rollback()
        print(f"Transaction failed: {e}")
        return None
    finally:
        conn.close()

def get_user_trips(user_id):
    sql = "SELECT tripID AS id, planName AS name FROM TRIP_PLANS WHERE userID = %s ORDER BY tripID DESC"
    return db.execute(sql, (user_id,), fetchall=True)

def view_trip(trip_id):
    sql_trip = """
        SELECT tp.planName AS trip_name, tp.startDate, tp.endDate,
               MAX(CASE WHEN p.featureName = 'precipitation' THEN p.preferredValue END) AS precipitation,
               MAX(CASE WHEN p.featureName = 'temperature' THEN p.preferredValue END) AS temperature
        FROM TRIP_PLANS tp
        LEFT JOIN PREFERENCES p ON p.tripID = tp.tripID
        WHERE tp.tripID = %s
        GROUP BY tp.tripID
    """
    trip = db.execute(sql_trip, (trip_id,), fetchone=True)
    
    if trip:
        sql_locs = "SELECT CITY AS city, STATE AS state FROM TRIP_LOCATIONS WHERE tripID = %s"
        trip['locations'] = db.execute(sql_locs, (trip_id,), fetchall=True)
        
    return trip

def edit_trip(trip_id, trip_name, start_date, end_date, precip_pref, temp_pref, locations):
    """
    Transactional update of a trip.
    """
    conn = db._get_connection()
    try:
        cur = conn.cursor()
        
        cur.execute(
            "UPDATE TRIP_PLANS SET planName=%s, startDate=%s, endDate=%s WHERE tripID=%s",
            (trip_name, start_date, end_date, trip_id)
        )
        
        cur.execute("UPDATE PREFERENCES SET preferredValue=%s WHERE tripID=%s AND featureName='precipitation'", (precip_pref, trip_id))
        cur.execute("UPDATE PREFERENCES SET preferredValue=%s WHERE tripID=%s AND featureName='temperature'", (temp_pref, trip_id))
        

        needed_locs = set((loc['city'], loc['state']) for loc in locations)
        current_locs = set()
        
        cur.execute("SELECT CITY, STATE FROM TRIP_LOCATIONS WHERE tripID = %s", (trip_id,))
        for row in cur.fetchall():
             current_locs.add((row['CITY'], row['STATE']))
             
        to_delete = current_locs - needed_locs
        to_insert = needed_locs - current_locs
        
        if to_delete:
             del_sql = "DELETE FROM TRIP_LOCATIONS WHERE tripID=%s AND CITY=%s AND STATE=%s"
             cur.executemany(del_sql, [(trip_id, c, s) for c, s in to_delete])
             
        if to_insert:
             ins_sql = "INSERT INTO TRIP_LOCATIONS (tripID, CITY, STATE) VALUES (%s, %s, %s)"
             cur.executemany(ins_sql, [(trip_id, c, s) for c, s in to_insert])

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Update failed: {e}")
        return False
    finally:
        conn.close()

def delete_trip(trip_id):
    db.execute("DELETE FROM TRIP_PLANS WHERE tripID = %s", (trip_id,), commit=True)

def delete_all_user_trips(user_id):
    db.execute("DELETE FROM TRIP_PLANS WHERE userID = %s", (user_id,), commit=True)