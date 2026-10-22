import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
)

import streamlit as st
from chat_history_db.chat_db import new_user_chat, existing_user_chat, load_all_messages, both_conversation
from AgenticAI.agents import Replica

class Query:
    def __init__(self):
        st.set_page_config(
                        page_title="Replica",
                        page_icon = "💻",
                        layout = "centered",
                        initial_sidebar_state="auto",
                    )
        st.header("Welcome to :red[Replica💻]: :orange[_Generate your ReadME_]", divider="rainbow")
        

        self.chat_session()
        self.sidebar_ui()
        self.session_state()

    def session_state(self):
        st.sidebar.divider()
        if st.session_state.get("logged_in", False) and st.session_state.get("user_id") is not None:
            user = st.session_state.get("user")
            email= st.session_state.get("email")

            if not st.session_state.get("welcome_shown", False):
                st.toast(f"Welcome 👤 {user}", duration="short")
                st.session_state["welcome_shown"] = True

            st.sidebar.write(f"👤 {user}")
            st.sidebar.write(f"📧 {email}")

            if st.sidebar.button("logout"):
                st.session_state["logged_in"] = False
                st.session_state["user"] = None
                st.session_state["email"] = None
                st.rerun()
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.warning(f"Please log in first")
            with col2:
                if st.button("login here", type="tertiary"):
                    st.switch_page("login.py")

    def chat_session(self):
        if "current_chat_id" not in st.session_state:
            st.session_state["current_chat_id"] = None

        if "current_session" not in st.session_state:
            st.session_state["current_session"] = False

        if "messages" not in st.session_state:
            st.session_state["messages"] = []

    def sidebar_ui(self):
        if not (st.session_state.get("logged_in", False) or st.session_state.get("user")):
            return

        # New chat button
        if st.sidebar.button("➕ New Chat", use_container_width=True):
                st.session_state["current_chat_id"] = None
                st.session_state["messages"] = []
                st.rerun()

        st.sidebar.subheader("Chat history")

        # new chat title and convo
        user_id = st.session_state.get("user_id")

        if user_id:
            chats = existing_user_chat(user_id)

            user_id = 0
            chat_title = 1
            for chat in reversed(chats):
                chat_id = chat[user_id]
                title = chat[chat_title]

                if st.sidebar.button(title, key=f"chat_{chat_id}", use_container_width=True):
                    st.session_state["current_chat_id"] = chat_id
                    messages = load_all_messages(chat_id)
                    st.session_state["messages"] = messages
                    self.display_conversation()
                
    def display_conversation(self):
        messages = st.session_state.get("messages", [])

        for msg in messages:
            with st.chat_message(msg['role']):
                st.write(msg['content'])


    def interface(self):
        if not st.session_state.get("logged_in", False):
            return

        self.display_conversation()

        prompt = st.chat_input("What would you like Replica to do?", accept_file=True)
    
        if prompt:
            self.run_query(prompt)

    def run_query(self, prompt):
            
            if hasattr(prompt, "text"):
                user_query = prompt.text
            else:
                user_query = str(prompt)
            
            with st.chat_message("user"):
                st.write(user_query) 

                user_id = st.session_state.get("user_id")
                current_chat_id = st.session_state.get("current_chat_id")

                if current_chat_id is None:
                    user_title = self.title_creation(user_query)
                    current_chat_id = new_user_chat(user_id=user_id, title=user_title)
            

                    st.session_state["current_chat_id"] = current_chat_id

                both_conversation(current_chat_id, role='user', content=user_query)
                st.session_state["messages"].append({
                    "role" : "user",
                    "content" : user_query
                })
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    replica = Replica()
                    manager = replica.manager()

                    response = manager.run(user_query)

                assistant_response = response.content
                st.write(assistant_response)

                st.session_state["messages"].append({
                    "role" : "assistant",
                    "content" : assistant_response
                })

                both_conversation(current_chat_id, role='assistant', content=assistant_response)

                

    def title_creation(self, prompt):

        if not prompt:
            return "No conversatin yet"

        user_query = str(prompt).strip()

        if not user_query:
            return "No Conversation yet"

        words = user_query.split()

        title = " ".join(words[:6])

        if len(words) > 6:
            title += "..."

        return title


if __name__ == "__main__":
    app = Query()
    app.interface()
