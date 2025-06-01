import sqlite3

def init_db():
    conn = sqlite3.connect('database/plates.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS plate_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate_text TEXT,
            timestamp TEXT,
            image_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(plate_text, timestamp, image_path):
    conn = sqlite3.connect('database/plates.db')
    c = conn.cursor()
    c.execute("INSERT INTO plate_data (plate_text, timestamp, image_path) VALUES (?, ?, ?)", 
              (plate_text, timestamp, image_path))
    conn.commit()
    conn.close()
