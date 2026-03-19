
from dotenv import load_dotenv
load_dotenv()


from langchain_groq import ChatGroq 
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
import streamlit as st



# We use SQLDatabase.from_uri to connect to our local 'my_tasks.db' file
db = SQLDatabase.from_uri("sqlite:///my_tasks.db")

# Automatically create the 'tasks' table if it doesn't already exist
db.run("""
    CREATE TABLE IF NOT EXISTS tasks (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       title TEXT NOT NULL,
       description TEXT,
       status TEXT CHECK(status IN ('pending', 'in_progress', 'completed')) DEFAULT 'pending',
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
       );
""")

print("Database and 'tasks' table verified successfully.")



model = ChatGroq(model="openai/gpt-oss-20b")
toolkit = SQLDatabaseToolkit(db=db, llm=model)
tools = toolkit.get_tools()
# InMemorySaver tracks our conversation history, so the AI remembers past tasks
memory = InMemorySaver()
# This tells the agent EXACTLY how to behave and what the database structure looks like
system_prompt = """
 You are a task management assistant that interacts with a SQL database containing a 'tasks' table.

 TASK RULES:
 1. Limit SELECT queries to 10 results max with ORDER BY created_at DESC.
 2. After performing CREATE/UPDATE/DELETE, confirm by showing the updated status with a SELECT query.
 3. Ensure task lists are displayed clearly in a structured format for the user.

 CRUD OPERATIONS GUIDE:
    CREATE: INSERT INTO tasks(title, description, status)
    READ: SELECT * FROM tasks WHERE ... LIMIT 10
    UPDATE: UPDATE tasks SET status=? WHERE id=? OR title=?
    DELETE: DELETE FROM tasks WHERE id=? OR title=?

 Table Schema: [id, title, description, status (pending, in_progress, completed), created_at]
"""

# Efficiently cache the agent creation so it doesn't reload unnecessarily
@st.cache_resource
def get_agent():
    agent = create_agent(
        model=model,
        tools=tools,
        checkpointer=memory,
        system_prompt=system_prompt
    )
    return agent

agent = get_agent()



st.subheader("📋 TaskBot - Manage Your Tasks with AI Power")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ex: 'Add a high priority task to finish my project' or 'List all my pending tasks'")

if prompt:

    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    
    with st.chat_message("ai"):
        with st.spinner("Analyzing your request and updating tasks..."):
        
            response = agent.invoke(
                {"messages": [{"role": "user", "content": prompt}]},
                {"configurable": {"thread_id": "1"}}
            )
            
            result = response["messages"][-1].content
            st.markdown(result)
            st.session_state.messages.append({"role": "ai", "content": result})






