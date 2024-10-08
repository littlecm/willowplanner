import streamlit as st
import pandas as pd
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="High School Class Planner",
    page_icon=":notebook:",
    layout="wide"
)

# Custom CSS for modern styling with Inter font
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #f5f5f5;
        color: #333;
    }

    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 8px 16px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
    }

    .stButton>button:hover {
        background-color: #0056b3;
    }

    .stTextArea textarea, .stTextInput input {
        border-radius: 10px;
    }

    .stDateInput>div>div>div {
        border-radius: 10px;
    }

    .stDataFrame {
        border-radius: 10px;
        background-color: white;
        padding: 10px;
    }

    footer {
        text-align: center;
        padding: 20px 0;
        font-size: 14px;
        color: #888;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Pre-loaded class schedule for Willow
preloaded_classes = [
    {"Class Name": "Algebra 1 Seminar", "Period/Hour": 1},
    {"Class Name": "Biology", "Period/Hour": 2},
    {"Class Name": "Algebra", "Period/Hour": 3},
    {"Class Name": "World History", "Period/Hour": 4},
    {"Class Name": "English 9 A", "Period/Hour": 5},
    {"Class Name": "Lifelong Fitness", "Period/Hour": 6},
]

# Initialize session state to store classes and tasks
if 'classes' not in st.session_state:
    st.session_state['classes'] = preloaded_classes
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []

# Function to add a new task
def add_task(selected_class, task, due_date, priority, notes):
    st.session_state['tasks'].append({
        "Class": selected_class,
        "Task": task,
        "Due Date": due_date,
        "Priority": priority,
        "Completed": False,
        "Notes": notes,
        "Reminder": due_date <= datetime.now().date()
    })

# Function to mark a task as completed
def mark_task_completed(index):
    st.session_state['tasks'][index]["Completed"] = True

# Function to remove a task
def remove_task(index):
    del st.session_state['tasks'][index]

# Function to clear all tasks
def clear_tasks():
    st.session_state['tasks'] = []

# Title and introduction
st.title("High School Class Planner")
st.write("### Welcome, Willow! Stay organized with your classes, homework, projects, and more.")

# Sidebar for adding a new task
st.sidebar.header("Add a New Task")
if st.session_state['classes']:
    selected_class = st.sidebar.selectbox("Select Class", [cls["Class Name"] for cls in st.session_state['classes']])
    task = st.sidebar.text_area("Task")
    due_date = st.sidebar.date_input("Due Date", datetime.now())
    priority = st.sidebar.selectbox("Priority", ["Low", "Medium", "High"])
    notes = st.sidebar.text_area("Notes")

    if st.sidebar.button("Add Task"):
        if selected_class and task and due_date:
            add_task(selected_class, task, due_date, priority, notes)
            st.sidebar.success("Task added successfully!")
        else:
            st.sidebar.error("Please fill in all the fields.")
else:
    st.sidebar.write("Please add a class first!")

# Task search functionality
st.header("Search Tasks")
search_query = st.text_input("Search for a task...")

# Display classes
st.header("Your Classes")
if st.session_state['classes']:
    classes_df = pd.DataFrame(st.session_state['classes'])
    st.table(classes_df)
else:
    st.write("You haven't added any classes yet.")

# Display and manage tasks
st.header("Your Tasks")
filtered_tasks = [task for task in st.session_state['tasks'] if search_query.lower() in task['Task'].lower()]
if filtered_tasks:
    sorted_tasks = sorted(filtered_tasks, key=lambda x: x['Priority'], reverse=True)
    for i, task in enumerate(sorted_tasks):
        task_status = "✅ Completed" if task["Completed"] else "⏳ Incomplete"
        reminder = "🔔 Reminder!" if task["Reminder"] else ""
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])
        with col1:
            st.write(f"**{task['Class']}**: {task['Task']}")
        with col2:
            st.write(f"Due: {task['Due Date'].strftime('%b %d, %Y')} {reminder}")
        with col3:
            st.write(f"Priority: {task['Priority']}")
        with col4:
            st.write(f"Notes: {task['Notes']}")
        with col5:
            st.write(f"Status: {task_status}")
        with col6:
            if not task["Completed"]:
                if st.button(f"Complete", key=f"complete_{i}"):
                    mark_task_completed(i)
            else:
                if st.button(f"Remove", key=f"remove_{i}"):
                    remove_task(i)

    # Clear all tasks option
    if st.button("Clear All Tasks"):
        clear_tasks()
        st.success("All tasks cleared successfully!")
else:
    st.write("No tasks match your search criteria." if search_query else "You don't have any tasks yet. Add a task from the sidebar!")

# Task progress tracking
st.header("Your Progress")
completed_tasks = sum(task["Completed"] for task in st.session_state['tasks'])
total_tasks = len(st.session_state['tasks'])
progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
st.progress(progress)
st.write(f"Completed {completed_tasks} out of {total_tasks} tasks ({progress:.2f}%).")

# Footer with credit to Dad
st.write("---")
st.markdown("<footer>Designed with ❤️ by Chris Little (aka Dad)</footer>", unsafe_allow_html=True)
