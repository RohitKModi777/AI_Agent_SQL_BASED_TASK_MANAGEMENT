# 🤖 AI Agent: SQL-Based Task Management System

Welcome to the **AI SQL Task Management Agent**, a smart chat assistant designed for efficient task management. This application converts your natural language prompts into SQL queries to perform CRUD (Create, Read, Update, Delete) operations on a local SQLite database.

## 🌟 Features
- **Natural Language Interaction**: Manage tasks with simple English prompts.
- **SQLite Integration**: Robust local database storage for tasks.
- **AI-Powered Execution**: Uses LangChain and ChatGroq for intelligent SQL generation.
- **Memory Management**: Remembers context within the session using `InMemorySaver`.
- **Streamlit UI**: A clean, interactive chat interface for real-time task management.

---

## 🛠️ How It Works

### 1. Database Connection & Schema
The project uses **SQLite** through the `SQLDatabase` utility in LangChain. 
- **DB Path**: `sqlite:///my_tasks.db`
- **Schema**:
  - `id`: Primary key (Auto-increment).
  - `title`: Task title (Text).
  - `description`: Task description (Text).
  - `status`: Task state (`pending`, `in_progress`, `completed`).
  - `created_at`: Timestamp for task creation.

### 2. Major Functions & Components

#### `app.py` Logic:
- **`SQLDatabaseToolkit`**: Provides the AI agent with tools to query and manipulate the database.
- **`create_agent()`**: Initializes the LangChain agent with:
    - `ChatGroq`: Using the `openai/gpt-oss-20b` model for natural language processing.
    - `tools`: SQL database tools for CRUD operations.
    - `checkpointer`: Using `InMemorySaver` to maintain chat history and memory.
- **System Prompt**: Defines strict rules for the agent, ensuring queries are efficient (max 10 results) and data is presented in a structured format.

### 3. Task Management Workflow
1. **User Prompt**: "Add a task called 'Buy groceries' with a pending status."
2. **AI Processing**: The agent analyzes the intent and generates the SQL command: `INSERT INTO tasks (title, status) VALUES ('Buy groceries', 'pending');`.
3. **Execution**: The database is updated, and the agent confirms the action with a success message.
4. **Memory**: The agent can reference previous tasks thanks to the `InMemorySaver` session management.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- A [Groq Cloud API Key](https://console.groq.com/keys)

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/RohitKModi777/AI_Agent_SQL_BASED_TASK_MANAGEMENT.git
   cd AI_Agent_SQL_BASED_TASK_MANAGEMENT
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add your API key:
   ```env
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

4. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

---

## 🌎 Deployment Steps (Streamlit Cloud)

To deploy this assistant:
1. Push your code to GitHub (as we are doing now).
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Connect your GitHub repository.
4. Add your `GROQ_API_KEY` in the **Secrets Management** section of Streamlit Cloud settings.
5. Deploy!

---

### Graduate/Student Notes 🎓
*This project demonstrates the power of AI-to-SQL agents. By decoupling natural language from raw SQL, we create accessible data management tools for everyone.*

**Happy Tasking!** 🚀
