import math
import streamlit as st

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    layout="wide",
    page_title="TSC Teacher Workload Calculator | Senior School",
    page_icon="🏫"
)
# ===== SCHOOL NAME INPUT =====
school_name = st.text_input("🏫 Enter the School Name:", placeholder="e.g., Enrio Senior School")
if school_name:
    st.markdown(f"### 📍 School Name: **{school_name}**")

# ===== STYLING =====
st.markdown("""
    <style>
        .header-style { font-size: 20px; font-weight: bold; color: #2c3e50; margin-top: 20px; }
        .highlight-box { background-color: #f8f9fa; border-radius: 5px; padding: 15px; margin-bottom: 20px; border-left: 4px solid #3498db; }
        .result-box { background-color: #e8f4fd; border-radius: 5px; padding: 15px; margin: 10px 0; color: #333333; }
        .subject-table { width: 100%; border-collapse: collapse; }
        .subject-table th { background-color: #3498db; color: white; padding: 10px; text-align: left; }
        .subject-table td { padding: 8px 10px; border-bottom: 1px solid #ddd; color: #333333; }
        .subject-table tr:nth-child(even) { background-color: #f2f2f2; }
    </style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.title("Teachers Service Commission Kenya")
st.title("🏫 TSC Teacher Workload Calculator")
st.subheader("Senior School Edition")
st.markdown("""
<div class="highlight-box">
    <p style="color: #333333;">This tool helps school administrators calculate teacher workload based on student enrollment and subject combinations.</p>
    <p style="color: #333333;"><strong>Guideline:</strong> 27 lessons per teacher per week</p>
</div>
""", unsafe_allow_html=True)

# ===== CONSTANTS =====
LESSONS_PER_TEACHER = 27
STUDENTS_PER_STREAM = 50

# ===== SUBJECT DATA =====
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

# ===== HELPER FUNCTIONS =====
def get_department(subject):
    for dept, subjects in DEPARTMENT_DATA.items():
        if subject in subjects:
            return dept
    return "Unknown"

def calculate_subject_load(subject, streams):
    total = 0
    for form, stream_count in streams.items():
        form_group = "Form 1 & 2" if form in ["Form 1", "Form 2"] else "Form 3 & 4"
        lessons = DEPARTMENT_DATA[get_department(subject)][subject].get(form_group, 0)
        total += lessons * stream_count
    return total

# ===== STUDENT ENROLLMENT SECTION =====
with st.expander("📋 Student Enrollment Information", expanded=True):
    col1, col2, col3, col4 = st.columns(4)
    f1 = col1.number_input("Form 1 Students", min_value=0, step=1)
    f2 = col2.number_input("Form 2 Students", min_value=0, step=1)
    f3 = col3.number_input("Form 3 Students", min_value=0, step=1)
    f4 = col4.number_input("Form 4 Students", min_value=0, step=1)

    streams = {
        "Form 1": math.ceil(f1 / STUDENTS_PER_STREAM) if f1 else 0,
        "Form 2": math.ceil(f2 / STUDENTS_PER_STREAM) if f2 else 0,
        "Form 3": math.ceil(f3 / STUDENTS_PER_STREAM) if f3 else 0,
        "Form 4": math.ceil(f4 / STUDENTS_PER_STREAM) if f4 else 0,
    }

    total_students = f1 + f2 + f3 + f4
    st.markdown(f"""
    <div class="highlight-box">
        <h4 style="color: #333333;">Stream Calculation Summary</h4>
        <p style="color: #333333;"><strong>Total Students:</strong> {total_students}</p>
        <p style="color: #333333;"><strong>Stream Capacity:</strong> 50 students per stream</p>
        <p style="color: #333333;"><strong>Streams:</strong> {sum(streams.values())} (F1: {streams['Form 1']}, F2: {streams['Form 2']}, F3: {streams['Form 3']}, F4: {streams['Form 4']})</p>
    </div>
    """, unsafe_allow_html=True)

# ===== TEACHING COMBINATION SECTION =====
with st.expander("📚 Teaching Combination Analysis", expanded=True):
    col1, col2 = st.columns(2)
    dept_choice = col1.selectbox("Select Department", ["SCIENCES", "LANGUAGES", "MATHEMATICS", "HUMANITIES", "TECHNICAL"])
    prefix = {"SCIENCES": "SCI", "LANGUAGES": "LANG", "MATHEMATICS": "MATH", "HUMANITIES": "HUM", "TECHNICAL": "TECH"}[dept_choice]
    
    filtered = {k: v for k, v in TSC_COMBINATIONS.items() if k.startswith(prefix)}
    combo_options = [f"{k}: {' + '.join(v)}" for k, v in filtered.items()]
    selected_combo = col2.selectbox("Select Combination", combo_options)

    available_teachers = st.number_input("Available Teachers", min_value=0, step=1)

# ===== CALCULATE BUTTON =====
if st.button("🔍 Analyze Workload", use_container_width=True):
    if sum(streams.values()) == 0:
        st.error("Please enter student numbers.")
        st.stop()

    code = selected_combo.split(":")[0]
    subjects = filtered[code]

    subject_loads = {s: calculate_subject_load(s, streams) for s in subjects}
    total_load = sum(subject_loads.values())
    required_teachers = math.ceil(total_load / LESSONS_PER_TEACHER)

    st.markdown(f"""
    <div class="result-box">
        <h3 style="color: #333333;">Summary for {selected_combo}</h3>
        <p style="color: #333333;"><strong>Total Weekly Lessons:</strong> {total_load}</p>
        <p style="color: #333333;"><strong>Required Teachers (27/week):</strong> {required_teachers}</p>
        <p style="color: #333333;"><strong>Available Teachers:</strong> {available_teachers}</p>
    </div>
    """, unsafe_allow_html=True)

    diff = available_teachers - required_teachers
    if diff > 0:
        st.success(f"✅ Surplus: {diff} teacher(s) available ({diff * LESSONS_PER_TEACHER} extra lessons).")
    elif diff == 0:
        st.info("🎯 Perfect staffing.")
    else:
        st.error(f"⚠️ Deficit: {abs(diff)} teacher(s) needed ({abs(diff) * LESSONS_PER_TEACHER} more lessons).")

    # Subject breakdown
    st.markdown("<h4 style='color: #333333;'>Subject Breakdown</h4>", unsafe_allow_html=True)
    table = """
    <table class="subject-table">
        <tr><th>Subject</th><th>Department</th><th>Weekly Lessons</th><th>% of Total</th></tr>
    """
    for subj, lessons in subject_loads.items():
        pct = (lessons / total_load) * 100 if total_load else 0
        table += f"<tr><td>{subj}</td><td>{get_department(subj)}</td><td>{lessons}</td><td>{pct:.1f}%</td></tr>"
    table += "</table>"
    st.markdown(table, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top: 30px;">
        <h4 style="color: #333333;">Recommendations</h4>
        <ul style="color: #333333;">
            <li>Maximize use of multi-subject teachers</li>
            <li>Optimize timetabling for balance</li>
            <li>Share teachers across departments if qualified</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown("""
<div style="margin-top: 50px; padding: 15px; background-color: #f8f9fa; border-radius: 5px; text-align: center;">
    <p style="margin: 0; font-size: 0.9em; color: #333333;">TSC Workload Calculator v2.0 | For Official Use Only</p>
    <p style="margin: 5px 0 0 0; font-size: 0.8em; color: #333333;">© 2025 Paul Gabriel | All rights reserved</p>
</div>
""", unsafe_allow_html=True)


