import psycopg2
import csv
import os
import pandas as pd # Optional, but often very convenient for CSVs

def create_table_if_not_exists(cursor, table_name, columns_sql):
    """
    Creates a table in PostgreSQL if it doesn't already exist.
    """
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {columns_sql}
    );
    """
    cursor.execute(create_table_query)
    print(f"Table '{table_name}' checked/created successfully.")

def load_csv_to_postgres(file_path, db_config, table_name):
    """
    Reads data from a CSV file and loads it into a PostgreSQL table.
    """
    conn = None
    try:
        # 1. Connect to PostgreSQL
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        print("Successfully connected to PostgreSQL.")

        # --- Option 1: Using pandas (Recommended for structured CSVs) ---
        # Pandas is excellent for handling various CSV quirks (headers, delimiters, missing values)
        print(f"Reading data from '{file_path}' using pandas...")
        df = pd.read_csv(file_path)

        # Infer SQL columns based on DataFrame dtypes (you might need to adjust this)
        # This is a simplified inference. For production, define your schema explicitly.
        sql_columns = []
        for col_name, dtype in df.dtypes.items():
            col_name_sanitized = col_name.replace(' ', '_').lower() # Sanitize column names for SQL
            if pd.api.types.is_integer_dtype(dtype):
                sql_columns.append(f"{col_name_sanitized} INTEGER")
            elif pd.api.types.is_float_dtype(dtype):
                sql_columns.append(f"{col_name_sanitized} NUMERIC")
            elif pd.api.types.is_bool_dtype(dtype):
                sql_columns.append(f"{col_name_sanitized} BOOLEAN")
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                sql_columns.append(f"{col_name_sanitized} TIMESTAMP")
            else: # Default to TEXT for strings and objects
                sql_columns.append(f"{col_name_sanitized} TEXT")
        columns_sql_definition = ", ".join(sql_columns)
        db_column_names = ", ".join([col.replace(' ', '_').lower() for col in df.columns])
        placeholder_string = ", ".join(["%s"] * len(df.columns))


        # 2. Create table if not exists (based on pandas DataFrame columns)
        # You should define your actual table schema if it's fixed.
        create_table_if_not_exists(cur, table_name, columns_sql_definition)

        # 3. Prepare data for insertion
        # Convert DataFrame rows to a list of tuples, handling None for NaN
        data_to_insert = [tuple(None if pd.isna(x) else x for x in row) for row in df.itertuples(index=False)]

        # 4. Insert data into the table
        insert_query = f"INSERT INTO {table_name} ({db_column_names}) VALUES ({placeholder_string})"

        print(f"Inserting {len(data_to_insert)} rows into '{table_name}'...")
        cur.executemany(insert_query, data_to_insert)
        conn.commit() # Commit the transaction
        print("Data loaded successfully using pandas and executemany.")

        # --- Option 2: Using csv module directly (more control, less abstraction) ---
        # This is uncommented if you prefer not to use pandas.
        # with open(file_path, 'r', newline='', encoding='utf-8') as f:
        #     reader = csv.reader(f)
        #     header = next(reader) # Skip header row
        #     # Dynamically create table based on header (customize this for robust schema)
        #     # For demonstration, assume all text
        #     columns_sql_csv = ", ".join([f'"{col.replace(" ", "_").lower()}" TEXT' for col in header])
        #     db_column_names_csv = ", ".join([f'"{col.replace(" ", "_").lower()}"' for col in header])
        #     placeholder_string_csv = ", ".join(["%s"] * len(header))

        #     create_table_if_not_exists(cur, table_name, columns_sql_csv)

        #     insert_query_csv = f"INSERT INTO {table_name} ({db_column_names_csv}) VALUES ({placeholder_string_csv})"
        #     data_to_insert_csv = []
        #     for row in reader:
        #         data_to_insert_csv.append(tuple(row)) # Collect all rows
        #     cur.executemany(insert_query_csv, data_to_insert_csv) # Execute all at once
        #     conn.commit()
        #     print("Data loaded successfully using csv module and executemany.")


    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback() # Rollback on error
            print("Transaction rolled back.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection closed.")

# --- Configuration and Usage ---
if __name__ == "__main__":
    # --- 1. Database Configuration ---
    # !! IMPORTANT: Replace with your actual PostgreSQL credentials and details !!
    db_config = {
        "host": "localhost",
        "database": "your_database_name",
        "user": "your_username",
        "password": "your_password",
        "port": "5432" # Default PostgreSQL port
    }

    # --- 2. File Configuration ---
    file_name = "sample_data.csv"
    # Create a dummy CSV file for demonstration if it doesn't exist
    if not os.path.exists(file_name):
        print(f"Creating a dummy CSV file: {file_name}")
        with open(file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "email", "age", "is_active", "last_login"])
            writer.writerow([1, "Alice Smith", "alice@example.com", 30, True, "2023-10-26 10:00:00"])
            writer.writerow([2, "Bob Johnson", "bob@example.com", 24, False, "2023-09-15 14:30:00"])
            writer.writerow([3, "Charlie Brown", "charlie@example.com", None, True, "2024-01-01 08:00:00"])
            writer.writerow([4, "Diana Prince", "diana@example.com", 35, True, None])
            writer.writerow([5, "Eve Adams", "eve@example.com", 29, False, "2023-11-20 16:00:00"])
            writer.writerow([6, "Frank White", "frank@example.com", 42, True, "2024-05-01 09:00:00"])

    table_to_load = "my_data_table" # The name of the table in your PostgreSQL database

    # --- 3. Run the data loading function ---
    print(f"\nAttempting to load '{file_name}' into table '{table_to_load}'...")
    load_csv_to_postgres(file_name, db_config, table_to_load)

    # You can verify the data in your PostgreSQL client:
    # SELECT * FROM my_data_table;
    # Or from Python:
    # try:
    #     conn = psycopg2.connect(**db_config)
    #     cur = conn.cursor()
    #     cur.execute(f"SELECT * FROM {table_to_load} LIMIT 5;")
    #     print("\nFirst 5 rows from the table:")
    #     for row in cur.fetchall():
    #         print(row)
    # except psycopg2.Error as e:
    #     print(f"Error verifying data: {e}")
    # finally:
    #     if 'conn' in locals() and conn:
    #         conn.close()