import pymysql
import os

# Default XAMPP MySQL configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "smart_agri"

def initialize_database():
    print(f"Connecting to MySQL at {DB_HOST}...")
    try:
        # Connect without selecting a database to create it first
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        with connection.cursor() as cursor:
            # Create the database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
            print(f"Database '{DB_NAME}' checked/created successfully.")
            
        connection.close()

        # Connect to the created database to set up tables
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # Table: crops
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS crops (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    category VARCHAR(100),
                    planted_date DATE,
                    expected_harvest_date DATE,
                    status VARCHAR(50) DEFAULT 'growing'
                );
            """)

            # Table: irrigation_schedules
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS irrigation_schedules (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    crop_id INT,
                    date DATE NOT NULL,
                    duration_minutes INT NOT NULL,
                    water_amount DECIMAL(10,2),
                    status VARCHAR(50) DEFAULT 'scheduled',
                    FOREIGN KEY (crop_id) REFERENCES crops(id) ON DELETE CASCADE
                );
            """)

            # Table: chemical_logs (fertilizers & pesticides)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chemical_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    crop_id INT,
                    chem_type ENUM('fertilizer', 'pesticide') NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    application_date DATE NOT NULL,
                    quantity DECIMAL(10,2), /* quantity in kg/liters */
                    FOREIGN KEY (crop_id) REFERENCES crops(id) ON DELETE CASCADE
                );
            """)
            print("Tables checked/created successfully.")
            
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL or inserting data: {e}")
        print("Please ensure your XAMPP MySQL server is running.")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    initialize_database()
