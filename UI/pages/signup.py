import os
from pathlib import Path
import streamlit as st
import mysql.connector
import datetime

class Signup:
    def __init__(self):
        st.set_page_config(
                            page_title="Signup",
                            page_icon = "📝",
                            layout = "centered",
                            initial_sidebar_state="collapsed",
                            )
        self.ssl_ca = os.path.abspath("certs/ca.pem")
        st.write("CA certificate exists:", Path(self.ssl_ca).is_file())

    def get_connection(self):
        ssl_ca = str(
                    Path(__file__).resolve().parents[1] / "certs" / "ca.pem"
                    )
        return mysql.connector.connect(
            host=st.secrets["connections"]["host"],
            port=int(st.secrets["connections"]["port"]),
            user=st.secrets["connections"]["username"],
            password=st.secrets["connections"]["password"],
            database=st.secrets["connections"]["database"],
            ssl_ca=self.ssl_ca,
            ssl_verify_cert=True,
            ssl_verify_identity=True,
            )

    def user_exists(self, cursor, username, emaiid):
        cursor.execute("SELECT username FROM users WHERE username=%s OR emailid=%s",
                       (username, emaiid))
        return cursor.fetchone()

    def create_user(self, name, username, dob, emailid, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if  self.user_exists(cursor, username, emailid):
                st.warning(f"Account already exists, please choose another username or  emailid")
                return None
            cursor.execute(
                "INSERT INTO users(name, username, dob, emailid, password)"
                "VALUES(%s, %s, %s, %s, %s)",
                (name, username, dob, emailid, password)
            )
            conn.commit()
            return {
                "username" : username,
                "emailid" : emailid
            }
        finally:
            cursor.close()
            conn.close()

    def signup_session(self):
        # session create
        if "signin" not in st.session_state:
            st.session_state["signin"] = False
        if "user" not in st.session_state:
            st.session_state["user"] = None
        if "email" not in st.session_state:
            st.session_state["email"] = None

        # session store
        if st.session_state["signin"]:
            user = st.session_state["user"]
            email = st.session_state["email"]
            st.success(f"Welcome {user}")
            return user, email
        
        else:
            st.warning(f"Invalid session!!")
            return None

    def interface(self):
        signin = st.form("Signup Form")
        with signin:
                st.subheader(" :orange[_Signup Form_] :pen:", divider="green")
                name = st.text_input(f"Enter your Fullname")
                username = st.text_input(f"Enter your username")

                # creating only for 18+
                today = datetime.date.today()
                max_dob = datetime.date(
                    today.year-18,
                    today.month,
                    today.day
                )
                dob = st.date_input(f"Enter you Date of Birth",
                                    value = max_dob,
                                    min_value=datetime.date(1946,1,1),
                                    max_value = max_dob)

                
                emailid = st.text_input(f"Enter your Email-id")
                password = st.text_input(f"Enter your password", type="password")
                done = st.form_submit_button("submit", type="primary")

                if done:
                    if not username or not emailid or not password:
                        st.warning("Please fill the details correctly!")
                    else:
                        # self.signup_session()
                        user = self.create_user(name, username, dob, emailid, password)
                        if user:
                            st.session_state["logged_in"] = True
                            st.session_state["user"] = user["username"]
                            st.session_state["email"] = user["emailid"]
                            st.success(f"Account Created Successfully!!")
                            st.switch_page("pages/chat.py")



if __name__ == "__main__":
    app = Signup()
    app.interface()