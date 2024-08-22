import streamlit as st
import pandas as pd
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="High School Class Planner",
    page_icon=":notebook:",
    layout="wide"
)

# Initialize session state to store classes and tasks
if 'classes' not in st.session_state:
    st.session_state['classes'] = []
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []

# Function to add a new class
def add_class(class_name, period):
    st.session_state['classes'].append({"Class Name": class_name, "Period/Hour": period})

# Function to add a new task
def add_task(selected_class, task, due_date):
    st.session_state['tasks'].append({"Class": selected_class, "Task": task, "Due Date": due_date})

# Function to remove a task
def remove_task(index):
    del st.session_state['tasks'][index]

# Function to clear all tasks
def clear_tasks():
    st.session_state['tasks'] = []

# Title and introduction
st.title("High School Class Planner")
st.write("### Welcome, Willow! Use this planner to easily track your classes, homework, projects, and other tasks.")

# Sidebar for adding a new class
st.sidebar.header("Add a New Class")
class_name = st.sidebar.text_input("Class Name")
period = st.sidebar.number_input("Period/Hour", min_value=1, max_value=10, step=1)

if st.sidebar.button("Add Class"):
    if class_name and period:
        add_class(class_name, period)
        st.sidebar.success("Class added successfully!")
    else:
        st.sidebar.error("Please fill in all the fields.")

# Sidebar for adding a new task
st.sidebar.header("Add a New Task")
if st.session_state['classes']:
    selected_class = st.sidebar.selectbox("Select Class", [cls["Class Name"] for cls in st.session_state['classes']])
    task = st.sidebar.text_area("Task")
    due_date = st.sidebar.date_input("Due Date", datetime.now())

    if st.sidebar.button("Add Task"):
        if selected_class and task and due_date:
            add_task(selected_class, task, due_date)
            st.sidebar.success("Task added successfully!")
        else:
            st.sidebar.error("Please fill in all the fields.")
else:
    st.sidebar.write("Please add a class first!")

# Display classes
st.header("Your Classes")
if st.session_state['classes']:
    classes_df = pd.DataFrame(st.session_state['classes'])
    st.table(classes_df)
else:
    st.write("You haven't added any classes yet. Add a class from the sidebar!")

# Display tasks
st.header("Your Tasks")
if st.session_state['tasks']:
    tasks_df = pd.DataFrame(st.session_state['tasks'])
    st.table(tasks_df)
    
    # Remove task option
    st.write("### Manage Tasks")
    for i, task in enumerate(st.session_state['tasks']):
        if st.button(f"Remove Task {i+1}"):
            remove_task(i)
            st.success(f"Task {i+1} removed successfully!")

    # Clear all tasks option
    if st.button("Clear All Tasks"):
        clear_tasks()
        st.success("All tasks cleared successfully!")
else:
    st.write("You don't have any tasks yet. Add a task from the sidebar!")

# Footer
st.write("---")
st.write("📅 Stay organized and keep track of all your assignments with this planner!")
