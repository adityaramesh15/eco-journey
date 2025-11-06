from flask import Blueprint, jsonify, request
import ranking
import queries
from datetime import date

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
users_bp = Blueprint('users', __name__, url_prefix='/users')
cities_bp = Blueprint('cities', __name__, url_prefix='/cities')
trips_bp = Blueprint('trips', __name__, url_prefix='/trips')


def format_date(month, day):
    year = date.today().year
    return f"{year}-{int(month):02d}-{int(day):02d}"


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400
    
    user = queries.login_user(data['username'], data['password'])
    
    if user:
        return jsonify({"user_id": user['user_id'], "token": "demo-token"}), 200
    return jsonify({"error": "Invalid credentials"}), 401


@users_bp.route('', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400

    user = queries.create_user(data['username'], data['password'])

    if user:
        return jsonify(user), 201
    return jsonify({"error": "User already exists"}), 409

@users_bp.route('/<int:user_id>/trips/count', methods=['GET'])
def get_trip_count(user_id):
    count = queries.get_user_trip_count(user_id)
    return jsonify({"count": count}), 200

@users_bp.route('/<int:user_id>/trips', methods=['DELETE'])
def delete_all_user_trips(user_id):
    queries.delete_all_user_trips(user_id)
    return '', 204


@cities_bp.route('/check', methods=['GET'])
def check_city():
    city = request.args.get('city')
    state = request.args.get('state')
    if not city or not state:
        return jsonify({"error": "City and state required"}), 400
    
    return jsonify({"exists": queries.check_city_exists(city, state)}), 200


@trips_bp.route('/rank', methods=['POST'])
def get_trip_ranks():
    data = request.json
    if not data or 'locations' not in data or 'date_range' not in data:
         return jsonify({"error": "Missing locations or date_range"}), 400

    locs = data['locations']
    dr = data['date_range']
    prefs = data.get('preferences', {})

    city_tuples = [(l['city'], l['state']) for l in locs]

    ranking_input = queries.get_ranking_data(
        city_tuples,
        dr['start_month'], dr['start_day'],
        dr['end_month'], dr['end_day']
    )

    
    formatted_input = [(r['CITY'], r['STATE'], r['avg_temp'], r['avg_precipitation']) for r in ranking_input]

    ranked = ranking.create_ranking(
        formatted_input,
        int(prefs.get('temp', 70)), int(prefs.get('precp', 0)),
        prefs.get('check_bad_days', False), prefs.get('check_rainy_days', False),
        dr['start_month'], dr['start_day'], dr['end_month'], dr['end_day']
    )
    return jsonify(ranked), 200

@trips_bp.route('', methods=['POST'])
def save_new_trip():
    data = request.json
    required = ['user_id', 'trip_name', 'date_range', 'preferences', 'locations']
    if not data or not all(k in data for k in required):
        return jsonify({"error": "Missing required trip data"}), 400

    dr = data['date_range']
    
    start_year = date.today().year
    end_year = start_year
    if dr['end_month'] < dr['start_month']:
        end_year += 1

    start_date = f"{start_year}-{dr['start_month']:02d}-{dr['start_day']:02d}"
    end_date = f"{end_year}-{dr['end_month']:02d}-{dr['end_day']:02d}"

    result = queries.save_new_trip(
        data['user_id'], data['trip_name'],
        start_date, end_date,
        data['preferences'].get('precp', 0), data['preferences'].get('temp', 70),
        data['locations']
    )

    if result:
        return jsonify({**data, "trip_id": result['trip_id']}), 201
    return jsonify({"error": "Failed to save trip"}), 500

@trips_bp.route('', methods=['GET'])
def get_trip_list():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    return jsonify(queries.get_user_trips(user_id)), 200

@trips_bp.route('/<int:trip_id>', methods=['GET'])
def view_trip(trip_id):
    trip = queries.view_trip(trip_id)
    if trip:
        response = {
            "trip_name": trip['trip_name'],
            "date_start": {
                "month": trip['startDate'].month,
                "day": trip['startDate'].day
            },
            "date_end": {
                "month": trip['endDate'].month,
                "day": trip['endDate'].day
            },
            "preferences": {
                "precipitation": trip['precipitation'],
                "temperature": trip['temperature']
            }
        }

        for loc in trip['locations']:
             rank_key = f"rank_{loc['rank_order']}_location"
             response[rank_key] = {"city": loc['city'], "state": loc['state']}
             
        return jsonify(response), 200
    return jsonify({"error": "Trip not found"}), 404

@trips_bp.route('/<int:trip_id>', methods=['PUT'])
def edit_trip(trip_id):
    data = request.json
    if not data: return jsonify({"error": "No data provided"}), 400
    
    dr = data['date_range']
    success = queries.edit_trip(
        trip_id, data['trip_name'],
        format_date(dr['start_month'], dr['start_day']),
        format_date(dr['end_month'], dr['end_day']),
        data['preferences'].get('precp'), data['preferences'].get('temp'),
        data['locations']
    )
    
    if success:
        return jsonify({"status": "success", "locations": data['locations']}), 200
    return jsonify({"error": "Update failed"}), 500

@trips_bp.route('/<int:trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    queries.delete_trip(trip_id)
    return '', 204