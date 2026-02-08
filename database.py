# Database module for TaskFlow
# Author: Ahmed (Backend Developer)

import sqlite3
import os

DB_FILE = 'taskflow.db'

def init_db():
    """Create the database and tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            completed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            assigned_to TEXT DEFAULT ''
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            role TEXT DEFAULT 'developer'
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized!")

def add_task(title, description='', assigned_to=''):
    """Add a new task to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO tasks (title, description, assigned_to) VALUES (?, ?, ?)',
        (title, description, assigned_to)
    )
    conn.commit()
    conn.close()

def get_all_tasks():
    """Get all tasks from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

if __name__ == '__main__':
    init_db()
    add_task("Set up CI/CD pipeline", "Configure GitHub Actions", "Ahmed")
    add_task("Write API tests", "Unit tests for all endpoints", "Ahmed")
    print("Sample tasks added!")
    print("All tasks:", get_all_tasks())
