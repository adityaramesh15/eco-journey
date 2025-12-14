# Eco-Journey (Team 095 - OAR)

Eco-Journey is a full-stack web application designed to help users compare tourist destinations in the United States using historical weather data rather than unreliable forecasts. The application allows users to create trips, rank locations based on temperature and precipitation preferences, and manage saved itineraries.

## Team Information

**Team:** 095 (OAR)

* **Aditya Ramesh** (Captain) - Backend / Data Engineering
* **Ojas Bankhele** - Frontend / State Management
* **Ali Hussain** - Backend / Ranking Algorithms
* **Michael Kirylau** - Frontend / UI & Visualization

## Features

* **Historical Weather Analysis:** Utilizes NOAA GHCNd data to provide accurate weather expectations.
* **Trip Ranking Algorithm:** Compares 3 locations side-by-side and ranks them based on user-defined preferences for temperature and precipitation.
* **Advanced Filtering:** Detects "Bad Days" (extreme temps/heavy rain) and "Rainy Days" within a specified date range.
* **User Accounts:** Secure login and registration system.
* **Trip Management:** Save, load, edit, and delete trip plans (CRUD functionality).
* **Trip Constraints:** Implements business logic (max 5 trips per user) using database Stored Procedures.

## Tech Stack

* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Backend:** Python, Flask, Flask-CORS
* **Database:** MySQL
* **Data Processing:** Pandas, Scikit-learn, NumPy

## Project Structure

```text
├── backend/                # Flask API and database logic
│   ├── app.py              # Application entry point
│   ├── database.py         # Database connection class
│   ├── queries.py          # SQL query functions
│   ├── ranking.py          # Ranking algorithm (Scikit-learn)
│   └── routes.py           # API endpoints
├── frontend/               # Static UI files
│   ├── *.html              # UI Pages (Login, Home, Create, Load)
│   ├── style.css           # Styling
│   └── script.js           # Client-side logic and API calls
├── raw_data/               # Data processing scripts
│   ├── preprocess.py       # Script to parse NOAA CSVs
│   └── generate_users.py   # Script to generate dummy user data
├── indexing_scripts/       # SQL scripts for performance optimization
└── doc/                    # Project documentation
