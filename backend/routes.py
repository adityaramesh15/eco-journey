from flask import Blueprint, jsonify, request
from database import db
import ranking

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
users_bp = Blueprint('users', __name__, url_prefix='/users')
cities_bp = Blueprint('cities', __name__, url_prefix='/cities')
trips_bp = Blueprint('trips', __name__, url_prefix='/trips')


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Route: POST /auth/login
    Logs a user in.
    """
    # Get username/password from the request body
    # data = request.json
    # username = data.get('username')
    # password = data.get('password')
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400
    
    # Get username/password from the request body
    username = data.get('username')
    password = data.get('password')
    
    # --- Add logic to validate user ---
    pass
    # ---
    
    # Example response
    return jsonify({"user_id": 123, "token": "a-secure-token-placeholder"}), 200


# --- 2. User Routes ---
@users_bp.route('', methods=['POST'])
def create_user():
    """
    Route: POST /users
    Creates a new user.
    """
    # Get data from the request body
    # data = request.json
    # username = data.get('username')
    # password = data.get('password')
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400

    username = data.get('username')
    password = data.get('password') # hash or nah? 
    
    # --- Add logic to create user in database ---
    pass
    # ---
    
    # On success:
    # return jsonify({"user_id": 123, "username": username}), 201
    # On failure (user exists):
    # return jsonify({"error": "User already exists"}), 409

@users_bp.route('/<int:user_id>/trips/count', methods=['GET'])
def get_trip_count(user_id):
    """
    Route: GET /users/<user_id>/trips/count
    Gets the trip count for a specific user.
    """
    # The user_id is passed from the URL
    
    # --- Add logic to query database for user's trip count ---
    pass
    # ---
    
    # Example response
    # return jsonify({"count": 3}), 200

@users_bp.route('/<int:user_id>/trips', methods=['DELETE'])
def delete_all_user_trips(user_id):
    """
    Route: DELETE /users/<user_id>/trips
    Deletes all trips for a specific user.
    """
    # The user_id is passed from the URL
    
    # --- Add logic to delete all trips for this user ---
    pass
    # ---
    
    # On success, return no content
    return '', 204


# --- 3. City Routes ---

@cities_bp.route('/check', methods=['GET'])
def check_city():
    """
    Route: GET /cities/check?city=...&state=...
    Checks if a city exists in the database.
    """
    # Get data from query parameters
    # city = request.args.get('city')
    # state = request.args.get('state')
    city = request.args.get('city')
    state = request.args.get('state')

    if not city or not state:
        return jsonify({"error": "city and state parameters are required"}), 400
    
    # --- Add logic to check database ---
    pass
    # ---
    
    # Example response
    return jsonify({"exists": True}), 200


# --- 4. Trip Routes ---

@trips_bp.route('/rank', methods=['POST'])
def get_trip_ranks():
    """
    Route: POST /trips/rank
    Calculates and returns location rankings for a new trip.
    """
    # Get the complex trip details from the request body
    # data = request.json
    data = request.json
    if not data:
        return jsonify({"error": "Missing request body"}), 400
    
    locations = data.get('locations')
    if not locations or not isinstance(locations, list) or len(locations) == 0:
        return jsonify({"error": "Missing or invalid 'locations' list"}), 400
    
    prefs = data.get('preferences')
    if not prefs or not isinstance(prefs, dict):
        return jsonify({"error": "Missing or invalid 'preferences' object"}), 400
        
    pref_temp = prefs.get('temp')
    pref_precp = prefs.get('precp')
    bad_days = prefs.get('check_bad_days', False)
    rainy_days = prefs.get('check_rainy_days', False)

    if pref_temp is None or pref_precp is None:
        return jsonify({"error": "Missing 'temp' or 'precp' in preferences"}), 400
    
    date_range = data.get('date_range')
    if not date_range or not isinstance(date_range, dict):
        return jsonify({"error": "Missing or invalid 'date_range' object"}), 400
        
    start_month = date_range.get('start_month')
    start_day = date_range.get('start_day')
    end_month = date_range.get('end_month')
    end_day = date_range.get('end_day')
    
    if None in [start_month, start_day, end_month, end_day]:
        return jsonify({"error": "Missing one or more date_range fields"}), 400
    
    ### ADD SQL QUERY CALL HERE
    input_data = []

    ranked_data = ranking.create_ranking(
        input_data, 
        int(pref_temp), int(pref_precp), bool(bad_days), bool(rainy_days), 
        int(start_month), int(start_day), int(end_month), int(end_day)
    )
    
    return jsonify(ranked_data), 200

@trips_bp.route('', methods=['POST'])
def save_new_trip():
    """
    Route: POST /trips
    Saves a new trip to the database.
    """
    # Get trip data from the request body
    # data = request.json
    data = request.json
    if not data:
        return jsonify({"error": "Missing request body"}), 400
    
    user_id = data.get('user_id')
    trip_name = data.get('trip_name')

    ranking_data = data.get('ranking_data') 
    preferences = data.get('preferences')
    date_range = data.get('date_range')
    locations = data.get('locations')

    if not user_id or not trip_name or not ranking_data:
        return jsonify({"error": "Missing user_id, trip_name, or ranking_data"}), 400
    
    # --- Add logic to save trip (and handle 5-trip limit) ---
    # 1. Check trip count for user_id
    # 2. If count < 5, save the new trip.
    #    (You'd probably save trip_name, user_id, and JSON-serialized
    #     ranking_data, preferences, date_range, and locations)
    # This is where we run the trigger
    pass
    # ---
    
    # Example response
    # new_trip = { "trip_id": 456, ... }
    # return jsonify(new_trip), 201

@trips_bp.route('', methods=['GET'])
def get_trip_list():
    """
    Route: GET /trips?user_id=...
    Gets the list of saved trips for a user.
    """
    # Get user_id from query parameters
    # user_id = request.args.get('user_id')
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"error": "user_id query parameter is required"}), 400
    
    
    # --- Add logic to fetch trip list for the user ---
    pass
    # ---
    
    # Example response
    # trip_list = [
    #   { "id": 123, "name": "Trip to NY" },
    #   { "id": 456, "name": "Summer Vacation" }
    # ]
    # return jsonify(trip_list), 200

@trips_bp.route('/<int:trip_id>', methods=['GET'])
def view_trip(trip_id):
    """
    Route: GET /trips/<trip_id>
    Gets the full details for a single trip.
    """
    # The trip_id is passed from the URL
    
    # --- Add logic to fetch specific trip details ---
    pass
    # ---
    
    # Example response
    # trip_details = { "trip_name": "...", ... }
    # return jsonify(trip_details), 200
    # On failure:
    # return jsonify({"error": "Trip not found"}), 404

@trips_bp.route('/<int:trip_id>', methods=['PUT'])
def edit_trip(trip_id):
    """
    Route: PUT /trips/<trip_id>
    Updates an existing trip.
    """
    # The trip_id is passed from the URL
    # Get the new trip data from the request body
    # data = request.json
    data = request.json
    if not data:
        return jsonify({"error": "Missing request body"}), 400

    new_trip_name = data.get('trip_name')
    new_preferences = data.get('preferences')
    new_date_range = data.get('date_range')
    
    if not new_trip_name and not new_preferences and not new_date_range:
        return jsonify({"error": "No updateable fields provided (e.g., trip_name, preferences, date_range)"}), 400
    
        
    
    # --- Add logic to update the trip in the database ---
    # --- Re-calculate ranks if necessary ---
    pass
    # ---
    
    # Example response
    # updated_ranks = { ... }
    # return jsonify(updated_ranks), 200

@trips_bp.route('/<int:trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    """
    Route: DELETE /trips/<trip_id>
    Deletes a single trip.
    """
    # The trip_id is passed from the URL
    
    # --- Add logic to delete the specific trip ---
    pass
    # ---
    
    # On success, return no content
    # return '', 204