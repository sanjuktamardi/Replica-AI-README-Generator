import streamlit as st
import mysql.connector
from dotenv import load_dotenv
load_dotenv()

class Login():
        def get_connection(self):
            return mysql.connector.connect(
                host=st.secrets["connections"]["login"]["host"],
                port=int(st.secrets["connections"]["login"]["port"]),
                user=st.secrets["connections"]["login"]["username"],
                password=st.secrets["connections"]["login"]["password"],
                database=st.secrets["connections"]["login"]["database"],
    )

        
        def verify_login(self, username, emailid, password):
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(
                    "SELECT id, username, password, emailid FROM users WHERE username=%s AND emailid=%s",
                    (username, emailid),
                )
                user_row = cursor.fetchone()
                if user_row and user_row["password"] == password:
                    st.success(f"Welcome back {username}!!")
                    return user_row
                else:
                    st.warning(f"username {username} did not exists!! Please create an accout first or check your username and password")
                    return None
            finally:
                cursor.close()
                conn.close()
            
        def interface(self):
            st.set_page_config(
                page_title="Replica",
                page_icon = "💻",
                layout = "centered",
                initial_sidebar_state="expanded",
            )

            
            if "logged_in" not in st.session_state: 
                st.session_state["logged_in"] = False 
            if "id" not in st.session_state:
                st.session_state["id"] = None
            if "user" not in st.session_state: 
                st.session_state["user"] = None
            if "email" not in st.session_state:
                st.session_state["email"] = None

            if st.session_state["logged_in"]:
                user = st.session_state["user"]
                email = st.session_state["email"]
                st.toast(f"Welcome {user}!")
                st.write(f"Email {email}")
                if st.button("Logout"):
                    st.session_state["logged_in"] = False
                    st.session_state["user"] = None
                    st.session_state["email"] = None
                    st.rerun()
                return 

            # Login form
            log_in = st.form("login form", border=True)
            with log_in:
                st.subheader(" :orange[_Login Form_] :pen:", divider="green")
                username = st.text_input(f"Enter your username", placeholder="sanjukta")
                emailid = st.text_input(f"Enter your Email-id", placeholder="sanjukta@gmal.com")
                password = st.text_input(f"Enter your password", type="password", placeholder="Sanjukta_2026")
                done = st.form_submit_button("submit", type="primary", width="stretch")

            if done:
                if not username or not password or not emailid:
                    st.warning("Please enter your username and password")
                else:
                    user = self.verify_login(username, emailid, password)
                    if user:
                        st.session_state["logged_in"] = True
                        st.session_state["user_id"] = user["id"]
                        st.session_state["user"] = user["username"]
                        st.session_state["email"] = user["emailid"]
                        st.success(f"user succesflly logged in succesfuly")
                        st.switch_page("pages/chat.py")
                    
            col, col1, col2, col3, col4 = st.columns(5)
            with col2:
                    # st.html("<br>")
                    signup_button = st.button(label=":orange[Set up an Account] :red[Signup]", type="tertiary", use_container_width=True)
                    # st.button(label=":orange[Signup]", type="tertiary")
                    if signup_button:
                        st.switch_page("pages/signup.py")

            

if __name__ == "__main__":
    app = Login()
    app.interface()
       
# streamlit run UI/login.py