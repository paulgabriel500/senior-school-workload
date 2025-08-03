# senior_school_workload_app.py

import math
import streamlit as st
import pandas as pd
import plotly.express as px
from collections import defaultdict

# === PAGE CONFIG ===
st.set_page_config(
    page_title="TSC Workload Calculator | Senior School",
    layout="wide",
    page_icon="🏫"
)

st.title("🏫 TSC Teacher Workload Calculator (Senior School)")
st.caption("Crafted with care by Paul Gabriel | Powered by Streamlit")

# === DATA DEFINITIONS ===

DEPARTMENT_DATA = {
    "Mathematics": {
        "Mathematics": {"Form 1 & 2": 6, "Form 3 & 4": 7},
    },
    "Sciences": {
        "Physics": {"Form 1 & 2": 4, "Form 3 & 4": 5},
        "Chemistry": {"Form 1 & 2": 4, "Form 3 & 4": 5},
        "Biology": {"Form 1 & 2": 4, "Form 3 & 4": 5},
        "Agriculture": {"Form 1 & 2": 3, "Form 3 & 4": 4},
        "Computer Studies": {"Form 1 & 2": 3, "Form 3 & 4": 4},
        "Home Science": {"Form 1 & 2": 3, "Form 3 & 4": 4},
    },
    "Languages": {
        "English": {"Form 1 & 2": 6, "Form 3 & 4": 7},
        "Kiswahili": {"Form 1 & 2": 5, "Form 3 & 4": 6},
        "English Literature": {"Form 3 & 4": 4},
        "French": {"Form 1 & 2": 3, "Form 3 & 4": 4},
        "German": {"Form 1 & 2": 3, "Form 3 & 4": 4},
        "Arabic": {"Form 1 & 2": 3, "Form 3 & 4": 4},
    },
    "Humanities": {
        "History": {"Form 1 & 2": 3, "Form 3 & 4": 4},
        "Geography": {"Form 1 & 2": 3, "Form 3 & 4": 4},
        "CRE": {"Form 1 & 2": 3, "Form 3 & 4": 4},
        "IRE": {"Form 1 & 2": 3, "Form 3 & 4": 4},
        "HRE": {"Form 1 & 2": 3, "Form 3 & 4": 4},
        "P.E.": {"Form 1 & 2": 2, "Form 3 & 4": 2},
        "Music": {"Form 1 & 2": 2, "Form 3 & 4": 2},
        "Special Needs Education": {"Form 1 & 2": 3, "Form 3 & 4": 3},
    },
    "Technical": {
        "Business Studies": {"Form 1 & 2": 4, "Form 3 & 4": 5},
        "Art & Design": {"Form 1 & 2": 3, "Form 3 & 4": 4},
        "Metal Work": {"Form 1 & 2": 3, "Form 3 & 4": 4},
        "Woodwork": {"Form 1 & 2": 3, "Form 3 & 4": 4},
        "Electricity": {"Form 1 & 2": 3, "Form 3 & 4": 4},
    }
}

TSC_COMBINATIONS = { ... }  # Leave unchanged for brevity

LESSONS_PER_TEACHER = 27

# === HELPER FUNCTIONS ===

def get_department(subject):
    for dept, subjects in DEPARTMENT_DATA.items():
        if subject in subjects:
            return dept
    return "Unknown"

def calculate_subject_load(subject, streams):
    total = 0
    for form, stream_count in streams.items():
        form_group = "Form 1 & 2" if form in ["Form 1", "Form 2"] else "Form 3 & 4"
        lesson_count = DEPARTMENT_DATA[get_department(subject)][subject].get(form_group, 0)
        total += lesson_count * stream_count
    return total

# === STUDENT ENROLLMENT ===
st.header("📋 Student Enrollment")
col1, col2, col3, col4 = st.columns(4)
form1 = col1.number_input("Form 1", min_value=0, step=1)
form2 = col2.number_input("Form 2", min_value=0, step=1)
form3 = col3.number_input("Form 3", min_value=0, step=1)
form4 = col4.number_input("Form 4", min_value=0, step=1)

streams = {
    "Form 1": math.ceil(form1 / 50) if form1 else 0,
    "Form 2": math.ceil(form2 / 50) if form2 else 0,
    "Form 3": math.ceil(form3 / 50) if form3 else 0,
    "Form 4": math.ceil(form4 / 50) if form4 else 0,
}

st.success(f"Calculated Streams → F1: {streams['Form 1']}, F2: {streams['Form 2']}, F3: {streams['Form 3']}, F4: {streams['Form 4']}")

# === COMBINATION SECTION ===
st.header("📚 Teaching Combinations")
department = st.selectbox("Select Department", list(set(code[:code.index("0")] for code in TSC_COMBINATIONS)))
filtered_combos = {k: v for k, v in TSC_COMBINATIONS.items() if k.startswith(department)}
combo_display = [f"{code}: {' + '.join(subjects)}" for code, subjects in filtered_combos.items()]
selected_combo = st.selectbox("Select Combination", combo_display)
selected_code = selected_combo.split(":")[0]
subjects = filtered_combos[selected_code]

available_teachers = st.slider("Number of Available Teachers", 0, 20, 5)

if st.button("🔍 Analyze Workload"):
    subject_loads = {s: calculate_subject_load(s, streams) for s in subjects}
    total_lessons = sum(subject_loads.values())
    required_teachers = math.ceil(total_lessons / LESSONS_PER_TEACHER)

    st.subheader("📊 Workload Summary")
    colL, colR = st.columns(2)
    colL.metric("Total Weekly Lessons", total_lessons)
    colR.metric("Required Teachers", required_teachers)

    df = pd.DataFrame([
        {"Subject": sub, "Department": get_department(sub), "Lessons/Week": load}
        for sub, load in subject_loads.items()
    ])

    st.subheader("📈 Subject Load Breakdown")
    st.dataframe(df, use_container_width=True)

    chart = px.bar(df, x="Subject", y="Lessons/Week", color="Department", barmode="group",
                   title="Weekly Lessons per Subject")
    st.plotly_chart(chart, use_container_width=True)

    st.subheader("✅ Staffing Evaluation")
    if available_teachers > required_teachers:
        st.success(f"✅ Surplus of {available_teachers - required_teachers} teacher(s).")
    elif available_teachers == required_teachers:
        st.info("Perfectly staffed! You have just enough teachers.")
    else:
        st.error(f"⚠️ Deficit of {required_teachers - available_teachers} teacher(s). Please adjust staffing.")
