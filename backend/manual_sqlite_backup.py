import os
import sqlite3

# Path to your database file
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'interprep.db')
print(f"Creating database at: {db_path}")

# Connect to the database (this will create it if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    bio TEXT
)
''')

# Create questions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    topic TEXT NOT NULL,
    company TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    code_template TEXT
)
''')

# Create submissions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    language TEXT NOT NULL,
    status TEXT NOT NULL,
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (question_id) REFERENCES questions (id)
)
''')

# Create favorites table
cursor.execute('''
CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (question_id) REFERENCES questions (id),
    UNIQUE(user_id, question_id)
)
''')

# Create learning categories table
cursor.execute('''
CREATE TABLE IF NOT EXISTS learning_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    order_index INTEGER NOT NULL
)
''')

# Create learning topics table
cursor.execute('''
CREATE TABLE IF NOT EXISTS learning_topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    order_index INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES learning_categories (id)
)
''')

# Create learning content table
cursor.execute('''
CREATE TABLE IF NOT EXISTS learning_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    content_type TEXT NOT NULL,
    order_index INTEGER NOT NULL,
    FOREIGN KEY (topic_id) REFERENCES learning_topics (id)
)
''')

# Create learning progress table
cursor.execute('''
CREATE TABLE IF NOT EXISTS learning_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    content_id INTEGER NOT NULL,
    completed BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (content_id) REFERENCES learning_content (id),
    UNIQUE(user_id, content_id)
)
''')

# Insert some initial learning categories
categories = [
    (1, "Arrays and Strings", "Fundamental data structures for storing collections of elements", 1),
    (2, "Linked Lists", "Linear data structures where elements are stored in nodes", 2),
    (3, "Stacks and Queues", "Abstract data types with specific access patterns", 3),
    (4, "Trees and Graphs", "Non-linear data structures representing hierarchical relationships", 4),
    (5, "Bit Manipulation", "Operations at the bit level of numeric representations", 5),
    (6, "Math and Logic Puzzles", "Mathematical problems and logical reasoning", 6),
    (7, "Object-Oriented Design", "Principles and patterns of object-oriented programming", 7),
    (8, "Recursion and Dynamic Programming", "Techniques for solving problems by breaking them down", 8),
    (9, "System Design and Scalability", "Designing large-scale distributed systems", 9)
]

cursor.executemany('''
INSERT OR IGNORE INTO learning_categories (id, name, description, order_index)
VALUES (?, ?, ?, ?)
''', categories)

# Commit changes and close connection
conn.commit()
conn.close()

print("Database tables created successfully!")
