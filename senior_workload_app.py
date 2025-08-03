# senior_school_workload_app.py

import math
import streamlit as st
from collections import defaultdict

st.set_page_config(layout="wide")
st.title("🏫 TSC Teacher Workload Calculator (Senior School)")
st.caption("Author: Paul Gabriel")

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

TSC_COMBINATIONS = {
    "SCI001": ["Chemistry", "Biology"],
    "SCI002": ["Chemistry", "Physics"],
    "SCI003": ["Agriculture", "Geography"],
    "SCI004": ["Biology", "Geography"],
    "SCI005": ["Home Science", "Biology"],
    "SCI006": ["Physics", "Computer Studies"],
    "SCI007": ["Agriculture", "Biology"],
    "SCI008": ["Agriculture", "Chemistry"],
    "LANG009": ["English", "English Literature"],
    "LANG010": ["Kiswahili", "CRE"],
    "LANG011": ["Kiswahili", "History"],
    "LANG012": ["Kiswahili", "Geography"],
    "LANG013": ["German", "Geography"],
    "LANG014": ["German", "CRE"],
    "LANG015": ["Kiswahili", "IRE"],
    "LANG016": ["Kiswahili", "Home Science"],
    "LANG017": ["Kiswahili", "P.E."],
    "LANG018": ["French", "Geography"],
    "LANG019": ["French", "Business Studies"],
    "LANG020": ["French", "CRE"],
    "LANG021": ["French", "History"],
    "LANG022": ["Arabic", "IRE"],
    "LANG023": ["German", "History"],
    "MATH024": ["Mathematics", "Business Studies"],
    "MATH025": ["Mathematics", "Geography"],
    "MATH026": ["Mathematics", "Computer Studies"],
    "MATH027": ["Mathematics", "Chemistry"],
    "MATH028": ["Mathematics", "Biology"],
    "MATH029": ["Mathematics", "Physics"],
    "HUM030": ["Geography", "CRE"],
    "HUM031": ["History", "CRE"],
    "HUM032": ["Geography", "History"],
    "HUM033": ["Geography", "IRE"],
    "HUM034": ["History", "IRE"],
    "HUM035": ["History", "P.E."],
    "HUM036": ["Geography", "P.E."],
    "HUM037": ["Geography", "Business Studies"],
    "HUM038": ["Home Science", "History"],
    "HUM039": ["Home Science", "CRE"],
    "HUM040": ["Special Needs Education", "P.E."],
    "HUM041": ["Music", "P.E."],
    "TECH042": ["Metal Work", "Mathematics"],
    "TECH043": ["Metal Work", "Physics"],
    "TECH044": ["Woodwork", "Mathematics"],
    "TECH045": ["Woodwork", "Physics"],
    "TECH046": ["Electricity", "Mathematics"],
    "TECH047": ["Electricity", "Physics"],
    "TECH048": ["Art & Design", "History"],
    "TECH049": ["Art & Design", "Geography"],
    "TECH050": ["Art & Design", "History"],
    "TECH051": ["Art & Design", "Geography"],
}

LESSONS_PER_TEACHER = 27


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


# === UI COMPONENTS ===

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

st.success(f"Streams:\nForm 1: {streams['Form 1']} | Form 2: {streams['Form 2']} | Form 3: {streams['Form 3']} | Form 4: {streams['Form 4']}")

# === Combination Section ===
st.header("📚 Teaching Combinations")

department = st.selectbox("Select Department", ["SCIENCES", "LANGUAGES", "MATHEMATICS", "HUMANITIES", "TECHNICAL"])

prefix = {
    "SCIENCES": "SCI",
    "LANGUAGES": "LANG",
    "MATHEMATICS": "MATH",
    "HUMANITIES": "HUM",
    "TECHNICAL": "TECH"
}[department]

filtered_combos = {k: v for k, v in TSC_COMBINATIONS.items() if k.startswith(prefix)}

combo_display = [f"{code}: {' + '.join(subjects)}" for code, subjects in filtered_combos.items()]
selected_display = st.selectbox("Select Combination", combo_display)

selected_code = selected_display.split(":")[0]
subjects = filtered_combos[selected_code]

available_teachers = st.number_input("Number of Available Teachers", min_value=0, step=1)

if st.button("🔍 Analyze Workload"):
    subject_loads = {subject: calculate_subject_load(subject, streams) for subject in subjects}
    total_load = sum(subject_loads.values())
    required_teachers = math.ceil(total_load / LESSONS_PER_TEACHER)

    st.subheader("📊 Workload Summary")
    st.write(f"**Total Weekly Lessons:** {total_load}")
    st.write(f"**Required Teachers (27 lessons/week):** {required_teachers}")

    st.subheader("🧾 Subject Breakdown")
    st.table([
        {"Subject": subject, "Department": get_department(subject), "Weekly Lessons": load}
        for subject, load in subject_loads.items()
    ])

    st.subheader("✅ Staffing Evaluation")
    if available_teachers > required_teachers:
        st.success(f"You have {available_teachers - required_teachers} extra teacher(s).")
    elif available_teachers == required_teachers:
        st.info("Perfect staffing! You have exactly the number of teachers needed.")
    else:
        st.error(f"You need {required_teachers - available_teachers} more teacher(s).")

    shared_subjects = {
        s for s in sum(TSC_COMBINATIONS.values(), []) if s in subjects and s not in subjects
    }
    if shared_subjects:
        st.warning(f"Note: Shared subjects with other combinations include: {', '.join(shared_subjects)}")

