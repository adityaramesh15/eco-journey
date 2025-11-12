from flask import Flask
from flask_cors import CORS
from routes import auth_bp, users_bp, cities_bp, trips_bp 


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.secret_key = "supersecretkey"  

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(cities_bp)
    app.register_blueprint(trips_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()


    # app.run(host='localhost', port=5050, debug=True)
    app.run(host='0.0.0.0', port=5050, debug=True)