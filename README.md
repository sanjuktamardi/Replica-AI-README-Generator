# Replica

## Overview

Replica is an AI-powered assistant that analyzes GitHub repositories, generates README documentation, and helps identify and fix minor bugs in your code.

## Features

- Agentic GitHub repository analysis.
- AI-generated, editable README documentation delivered as a `.docx` file.
- Bug and error investigation with actionable fix guidance.

## How It Works

Replica is built as an Agno multi-agent team operating in coordinate mode:

- **Manager** – coordinates the Analyst and Writer agents.
- **Analyst** – investigates GitHub repositories using GitHub tools (`get_repository`, `get_repository_languages`, `list_branches`, `get_directory_content`, `get_file_content`) and gathers verified repository information for README generation and bug investigation.
- **Writer** – generates a professional README from the Analyst's verified findings and produces an editable `.docx` via file-generation tools.

## Tech Stack

- Python
- agno
- openai
- PyGithub
- greenlet
- streamlit
- reportlab
- SQLAlchemy
- python-docx
- python-dotenv
- mysql-connector-python

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run UI/login.py
```

## Project Structure

```
.
├── .streamlit/
│   └── config.toml
├── AgenticAI/
│   ├── __init__.py
│   └── agents.py
├── certs/
│   └── ca.pem
├── chat_history_db/
│   ├── chat_db.py
│   └── history_db.sql
├── UI/
│   ├── pages/
│   │   ├── chat.py
│   │   └── signup.py
│   ├── login.py
│   └── login_database.sql
├── .env.example
├── .gitignore
├── __init__.py
└── requirements.txt
```

## Limitations / Gaps

- No `README.md` was present in the repository before this draft.
- No license file is present.
- No tests, CI, docs, or contributor guide were found.
- No version pins or Python version evidence were found.
- No recorded results or metrics were found.
