import os
import streamlit as st
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openrouter import OpenRouterResponses
from agno.tools.github import GithubTools
from agno.team.mode import TeamMode
from agno.team.team import Team

class Replica:
    def __init__(self, model_id = "nvidia/nemotron-3.5-super-vl:free"):
        self.model_id = model_id

        self.model_provider = OpenRouterResponses(
            id=self.model_id,
            api_key=st.secrets.get("OPENROUTER_API_KEY"),
        )

        self.GITHUB_TOKEN = st.secrets.get("GITHUB_ACCESS_TOKEN")
        if not self.GITHUB_TOKEN:
            raise ValueError("GITHUB_ACCESS_TOKEN is not set in .env")

        os.makedirs("tmp", exist_ok=True)
        self.db = SqliteDb(db_file="tmp/memory.db")
        if not self.db:
             raise ValueError("Cannot access tmp folder")

        instruction_path = os.path.join(os.getcwd(), "AgenticAI/Instructions")

        self.analyst_instructions = open(os.path.join(instruction_path, "analyst_agent.txt"), "r", encoding="utf-8").read()
        self.written_instructions = open(os.path.join(instruction_path, "writer_agent.txt"), "r", encoding="utf-8").read()
        self.manager_instructions = open(os.path.join(instruction_path, "manager_agent.txt"), "r", encoding="utf-8").read()

    def _analyst_agent(self, session_id=None):
        return Agent(
                    name = "Analyst",
                    model = self.model_provider,
                    instructions = [self.analyst_instructions],
                    tools = [GithubTools(
                                access_token = self.GITHUB_TOKEN,
                                include_tools = 
                                    [
                                        "get_repository",
                                        "get_repository_languages",
                                        "list_branches",
                                        "get_directory_content",
                                        "get_file_content",
                                    ]
                                )
                            ],
                    tool_call_limit=15,
                    add_datetime_to_context = True,
                    markdown = True,
                    db = self.db,
                    session_id=session_id,
                    update_memory_on_run = True,
                    add_history_to_context=True,
                    read_chat_history=True
                )
        
    def _writer_agent(self, session_id=None):
            return Agent(
                    name = "Writer",
                    model = self.model_provider,
                    instructions = [self.written_instructions],
                    tools = [
                            GithubTools(
                                    access_token = self.GITHUB_TOKEN,
                                    include_tools = ["create_file",
                                                        "update_file",
                                                        "delete_file"
                                                    ]
                                        )
                            ],
                    tool_call_limit=5,
                    add_datetime_to_context = True,
                    db = self.db,
                    session_id=session_id,
                    update_memory_on_run=True,
                    add_history_to_context=True,
                    read_chat_history=True
                )

    def manager(self, session_id=None):
            analyst = self._analyst_agent(session_id=session_id)
            writer = self._writer_agent(session_id=session_id)

            return Team(
                name = "Manager",
                members = [analyst, writer],
                model = self.model_provider,
                mode = TeamMode.coordinate,
                instructions =[self.manager_instructions],
                show_members_responses = True,
                db = self.db,
                update_memory_on_run = True,
                add_history_to_context=True,
                add_datetime_to_context = True,
                read_chat_history=True
            )