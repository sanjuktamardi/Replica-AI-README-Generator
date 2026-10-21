from pathlib import Path

import mysql.connector
import streamlit as st

def _get_connection():
    ssl_ca = str(
                Path(__file__).resolve().parents[1] / "certs" / "ca.pem"
            )
    return mysql.connector.connect(
        host=st.secrets["connections"]["host"],
        port=int(st.secrets["connections"]["port"]),
        user=st.secrets["connections"]["username"],
        password=st.secrets["connections"]["password"],
        database=st.secrets["connections"]["database"],
        ssl_ca=ssl_ca,
        ssl_verify_cert=True,
        ssl_verify_identity=True,
    )

def existing_user_chat(user_id):
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title FROM convo_history WHERE user_id=%s",
                   (int(user_id),)
                   )
    return cursor.fetchall()

def new_user_chat(user_id, title):
    conn = _get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO convo_history(user_id, title)
                        VALUES(%s, %s)
                        """,
                        (user_id, title))
        conn.commit()
        cursor.close()
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