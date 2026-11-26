import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv(".env.local")

def _get_connection():
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
def existing_user_chat(user_id):
    conn = _get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, title FROM convo_history WHERE user_id=%s",
            (int(user_id),)
        )
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def new_user_chat(user_id, title):
    conn = _get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO convo_history(user_id, title)
                        VALUES(%s, %s)
                        """,
                        (user_id, title))
        conn.commit()
        return cursor.lastrowid

    finally:
        cursor.close()
        conn.close()

# Saving every convo happened in the chat user and asssistant
def both_conversation(convo_id, role, content):
    conn = _get_connection()
    cursor = conn.cursor()

    try:
        query = """
                INSERT INTO conversation(convo_id, role, content) 
                VALUES(%s, %s, %s)"""
        
        values = (convo_id, role, content)

        cursor.execute(query,values)
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()

def load_all_messages(convo_id):
    conn = _get_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT role, content FROM conversation WHERE convo_id = %s ORDER BY created_at ASC"
        values = (convo_id,)

        cursor.execute(query, values)
        rows = cursor.fetchall()

        chats = []

        for row in rows:
            role = row[0]
            content = row[1]
            chats.append({
                "role" :role,
                "content" : content
            })
        return chats
    finally:
        cursor.close()
        conn.close()