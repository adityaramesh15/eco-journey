import pandas as pd
import glob
import os

# --- Configuration ---

# Define file paths
DATA_DIR = "raw_data/NOAA/"
STATIONS_FILE_NAME = "ghcnd-stations.csv"
OUTPUT_FILE_NAME = "formatted_weather_data.csv"

# Define column names for the data files based on user's example
# (Station, Date, Element, Value, ...)
DATA_COLS_TO_USE = [0, 1, 2, 3]
DATA_COL_NAMES = ['Station', 'Date', 'Element', 'Value']

# Define column names for stations file based on user's example
# (Station, LAT, LONG, ...)
STATION_COLS_TO_USE = [0, 1, 2]
STATION_COL_NAMES = ['Station', 'LAT', 'LONG']

# Define the elements we want to keep
ELEMENTS_TO_KEEP = ['TMAX', 'TMIN', 'PRCP']

# --- Main Script ---

def main():
    """
    Main function to load, process, and save the NOAA GHCN data.
    """
    
    # --- Step 1: Find and combine all data CSVs ---
    
    stations_file_path = os.path.join(DATA_DIR, STATIONS_FILE_NAME)
    
    # Find all CSV files in the directory
    all_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))

    # Exclude the stations file
    data_files = [f for f in all_files if os.path.normpath(f) != os.path.normpath(stations_file_path)]

    if not data_files:
        print(f"Error: No data CSV files (excluding {STATIONS_FILE_NAME}) found in {DATA_DIR}")
        return

    print(f"Found {len(data_files)} data files to combine.")
    
    # Load and combine files
    li = []
    for filename in data_files:
        try:
            df = pd.read_csv(
                filename,
                header=None,
                usecols=DATA_COLS_TO_USE,
                names=DATA_COL_NAMES,
                dtype={'Date': str} # Keep Date as string for proper pivot
            )
            li.append(df)
        except Exception as e:
            print(f"Warning: Error reading {filename}: {e}. Skipping file.")

    if not li:
        print("Error: No data was successfully loaded from the CSV files.")
        return

    master_df = pd.concat(li, axis=0, ignore_index=True)
    print(f"Combined data has {len(master_df):,} rows before filtering.")

    # --- Step 2: Filter the master DataFrame ---

    # Filter for "US" stations
    master_df = master_df[master_df['Station'].str.startswith('US')]
    print(f"Filtered for 'US' stations: {len(master_df):,} rows remaining.")

    # Filter for required elements
    master_df = master_df[master_df['Element'].isin(ELEMENTS_TO_KEEP)]
    print(f"Filtered for TMAX, TMIN, PRCP: {len(master_df):,} rows remaining.")

    # --- Step 3: Load Station Data ---
    try:
        stations_df = pd.read_csv(
            stations_file_path,
            header=None,
            usecols=STATION_COLS_TO_USE,
            names=STATION_COL_NAMES,
            skipinitialspace=True # Handle spaces after delimiters
        )
        print(f"Loaded {len(stations_df):,} stations from {STATIONS_FILE_NAME}.")
    except FileNotFoundError:
        print(f"Error: The stations file was not found at {stations_file_path}")
        return
    except Exception as e:
        print(f"Error: Could not load stations file. {e}")
        return

    # --- Step 4: Pivot the data ---
    
    # Ensure 'Value' is numeric before pivoting
    master_df['Value'] = pd.to_numeric(master_df['Value'], errors='coerce')
    
    # Drop any rows where Value couldn't be converted
    master_df.dropna(subset=['Value'], inplace=True)

    print("Pivoting data from long to wide format...")
    pivoted_df = master_df.pivot_table(
        index=['Station', 'Date'],
        columns='Element',
        values='Value'
    ).reset_index()
    
    # Clean up column names after pivot
    pivoted_df.columns.name = None
    
    # After pivoting, TMAX or TMIN could be missing for a given day.
    # Drop rows where TMAX or TMIN is missing, as TAVG cannot be calculated.
    pivoted_df.dropna(subset=['TMAX', 'TMIN'], inplace=True)
    
    # For PRCP, missing (NaN) means "no precipitation". We'll fill with 0.
    pivoted_df['PRCP'] = pivoted_df['PRCP'].fillna(0)

    print(f"Pivoted data has {len(pivoted_df):,} rows (days with TMAX and TMIN).")

    # --- Step 5: Calculate TAVG ---
    pivoted_df['TAVG'] = (pivoted_df['TMAX'] + pivoted_df['TMIN']) / 2
    print("Calculated TAVG.")

    # --- Step 6: Merge with station data ---
    # Use 'inner' join to only keep rows that have a matching station
    merged_df = pd.merge(
        pivoted_df,
        stations_df,
        on='Station',
        how='inner'
    )
    print(f"Merged with station data. Final dataset has {len(merged_df):,} rows.")

    # --- Step 7: Format final table and save ---
    final_columns = ['LAT', 'LONG', 'Date', 'TAVG', 'PRCP']
    
    # Check if all final columns are present
    if not all(col in merged_df.columns for col in final_columns):
        print("Error: Missing one of the final columns after merge. Aborting.")
        print(f"Expected: {final_columns}")
        print(f"Got: {list(merged_df.columns)}")
        return

    final_df = merged_df[final_columns]
    
    # Rename 'Date' column to 'DATE' as in the user's final requested format
    final_df = final_df.rename(columns={'Date': 'DATE'})

    final_df.to_csv(OUTPUT_FILE_NAME, index=False)
    
    print("\n--- Success! ---")
    print(f"Successfully created '{OUTPUT_FILE_NAME}'")
    print(f"Final columns: {list(final_df.columns)}")
    print(f"Total rows written: {len(final_df):,}")

# This allows the script to be run from the command line
if __name__ == "__main__":
    main()