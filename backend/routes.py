from flask import Blueprint, jsonify, request



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
    
    # --- Add logic to validate user ---
    pass
    # ---
    
    # Example response
    # return jsonify({"user_id": 123, "token": "a-secure-token"}), 200


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
    # return '', 204


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
    
    # --- Add logic to check database ---
    pass
    # ---
    
    # Example response
    # return jsonify({"exists": True}), 200


# --- 4. Trip Routes ---

@trips_bp.route('/rank', methods=['POST'])
def get_trip_ranks():
    """
    Route: POST /trips/rank
    Calculates and returns location rankings for a new trip.
    """
    # Get the complex trip details from the request body
    # data = request.json
    
    # --- Add logic to calculate ranks ---
    pass
    # ---
    
    # Example response
    # ranked_data = { ... }
    # return jsonify(ranked_data), 200

@trips_bp.route('', methods=['POST'])
def save_new_trip():
    """
    Route: POST /trips
    Saves a new trip to the database.
    """
    # Get trip data from the request body
    # data = request.json
    
    # --- Add logic to save trip (and handle 5-trip limit) ---
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