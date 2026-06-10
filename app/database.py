"""
SQLite Database setup and utilities for Theme Park Accessibility Planner
"""
import sqlite3
from datetime import datetime
from config import DATABASE_PATH

def get_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database schema"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users/Queries table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        park_name TEXT NOT NULL,
        query_text TEXT NOT NULL,
        dietary_restrictions TEXT,
        allergens TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Results table - stores AI-generated plans
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query_id INTEGER NOT NULL,
        park_section TEXT NOT NULL,
        restaurant_name TEXT,
        menu_items TEXT,
        dietary_notes TEXT,
        result_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (query_id) REFERENCES queries(id)
    )
    """)
    
    # Accessibility accommodations table (for phase 2)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accessibility_accommodations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        park_name TEXT NOT NULL,
        land TEXT NOT NULL,
        ride_name TEXT NOT NULL,
        disability_type TEXT,
        accommodation_details TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

def save_query(park_name, query_text, dietary_restrictions, allergens):
    """Save a user query"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO queries (park_name, query_text, dietary_restrictions, allergens)
    VALUES (?, ?, ?, ?)
    """, (park_name, query_text, dietary_restrictions, allergens))
    conn.commit()
    query_id = cursor.lastrowid
    conn.close()
    return query_id

def save_result(query_id, park_section, restaurant_name, menu_items, dietary_notes, result_json):
    """Save a result from the dietary agent"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO results (query_id, park_section, restaurant_name, menu_items, dietary_notes, result_json)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (query_id, park_section, restaurant_name, menu_items, dietary_notes, result_json))
    conn.commit()
    conn.close()

def get_query_results(query_id):
    """Retrieve all results for a query"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM results WHERE query_id = ? ORDER BY park_section", (query_id,))
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    init_database()
