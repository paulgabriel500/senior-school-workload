# senior_school_workload_app.py

import math
import streamlit as st
from collections import defaultdict

# ===== APP CONFIGURATION =====
st.set_page_config(
    layout="wide",
    page_title="TSC Teacher Workload Calculator | Senior School",
    page_icon="🏫"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .header-style {
        font-size: 20px;
        font-weight: bold;
        color: #2c3e50;
        padding: 10px;
        border-radius: 5px;
        margin-top: 20px;
    }
    .highlight-box {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 20px;
        border-left: 4px solid #3498db;
    }
    .result-box {
        background-color: #e8f4fd;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .subject-table {
        width: 100%;
        border-collapse: collapse;
    }
    .subject-table th {
        background-color: #3498db;
        color: white;
        padding: 10px;
        text-align: left;
    }
    .subject-table td {
        padding: 8px 10px;
        border-bottom: 1px solid #ddd;
    }
    .subject-table tr:nth-child(even) {
        background-color: #f2f2f2;
    }
</style>
""", unsafe_allow_html=True)

# ===== APP HEADER =====
st.title("🏫 TSC Teacher Workload Calculator")
st.subheader("Senior School Edition")
st.markdown("""
<div style="background-color: #e8f4fd; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
    <p style="margin: 0;">This tool helps school administrators calculate teacher workload requirements based on student enrollment and available teaching staff.</p>
    <p style="margin: 10px 0 0 0; font-size: 0.9em;"><strong>Author:</strong> Paul Gabriel | <strong>TSC Guidelines:</strong> 27 lessons/week per teacher</p>
</div>
""", unsafe_allow_html=True)

# ===== DATA DEFINITIONS =====
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
STUDENTS_PER_STREAM = 50

# ===== HELPER FUNCTIONS =====
def get_department(subject):
    """Returns the department for a given subject."""
    for dept, subjects in DEPARTMENT_DATA.items():
        if subject in subjects:
            return dept
    return "Unknown"

def calculate_subject_load(subject, streams):
    """Calculates weekly lesson load for a subject based on streams."""
    total = 0
    for form, stream_count in streams.items():
        form_group = "Form 1 & 2" if form in ["Form 1", "Form 2"] else "Form 3 & 4"
        lesson_count = DEPARTMENT_DATA[get_department(subject)][subject].get(form_group, 0)
        total += lesson_count * stream_count
    return total

def display_stream_info(form1, form2, form3, form4):
    """Displays detailed stream information in a user-friendly way."""
    total_students = form1 + form2 + form3 + form4
    total_streams = sum(streams.values())
    
    st.markdown(f"""
    <div class="highlight-box">
        <h4 style="margin-top: 0;">Stream Calculation Details</h4>
        <p><strong>Total Students:</strong> {total_students}</p>
        <p><strong>Stream Capacity:</strong> {STUDENTS_PER_STREAM} students per stream</p>
        <p><strong>Calculated Streams:</strong> {total_streams} (Form 1: {streams['Form 1']}, Form 2: {streams['Form 2']}, Form 3: {streams['Form 3']}, Form 4: {streams['Form 4']})</p>
    </div>
    """, unsafe_allow_html=True)

# ===== MAIN APP INTERFACE =====
with st.expander("📋 Student Enrollment Information", expanded=True):
    st.markdown("""
    <div style="margin-bottom: 15px;">
        <p>Enter the number of students in each form to calculate the required streams. 
        The system automatically calculates streams based on TSC guidelines (max 50 students per stream).</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    form1 = col1.number_input("Form 1 Students", min_value=0, step=1, key="form1")
    form2 = col2.number_input("Form 2 Students", min_value=0, step=1, key="form2")
    form3 = col3.number_input("Form 3 Students", min_value=0, step=1, key="form3")
    form4 = col4.number_input("Form 4 Students", min_value=0, step=1, key="form4")

    # Calculate streams
    streams = {
        "Form 1": math.ceil(form1 / STUDENTS_PER_STREAM) if form1 else 0,
        "Form 2": math.ceil(form2 / STUDENTS_PER_STREAM) if form2 else 0,
        "Form 3": math.ceil(form3 / STUDENTS_PER_STREAM) if form3 else 0,
        "Form 4": math.ceil(form4 / STUDENTS_PER_STREAM) if form4 else 0,
    }
    
    display_stream_info(form1, form2, form3, form4)

# ===== TEACHING COMBINATION SECTION =====
with st.expander("📚 Teaching Combination Analysis", expanded=True):
    st.markdown("""
    <div style="margin-bottom: 15px;">
        <p>Select a teaching combination to analyze the workload requirements. The system will calculate the total 
        weekly lessons and required teachers based on TSC standards (27 lessons per teacher per week).</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    department = col1.selectbox(
        "Select Department", 
        ["SCIENCES", "LANGUAGES", "MATHEMATICS", "HUMANITIES", "TECHNICAL"],
        key="dept_select"
    )
    
    prefix = {
        "SCIENCES": "SCI",
        "LANGUAGES": "LANG",
        "MATHEMATICS": "MATH",
        "HUMANITIES": "HUM",
        "TECHNICAL": "TECH"
    }[department]
    
    filtered_combos = {k: v for k, v in TSC_COMBINATIONS.items() if k.startswith(prefix)}
    combo_display = [f"{code}: {' + '.join(subjects)}" for code, subjects in filtered_combos.items()]
    
    selected_display = col2.selectbox(
        "Select Combination", 
        combo_display,
        key="combo_select"
    )
    
    available_teachers = st.number_input(
        "Number of Available Teachers for This Combination", 
        min_value=0, 
        step=1,
        key="teachers_input"
    )

# ===== ANALYSIS BUTTON AND RESULTS =====
if st.button("🔍 Analyze Workload", type="primary", use_container_width=True):
    if not any(streams.values()):
        st.error("Please enter student numbers to calculate streams first.")
        st.stop()
    
    selected_code = selected_display.split(":")[0]
    subjects = filtered_combos[selected_code]
    
    with st.spinner("Calculating workload requirements..."):
        # Calculate subject loads
        subject_loads = {subject: calculate_subject_load(subject, streams) for subject in subjects}
        total_load = sum(subject_loads.values())
        required_teachers = math.ceil(total_load / LESSONS_PER_TEACHER)
        
        # Display main results
        st.markdown(f"""
        <div class="result-box">
            <h3 style="margin-top: 0;">Workload Summary for {selected_display}</h3>
            <p><strong>Total Weekly Lessons:</strong> {total_load}</p>
            <p><strong>Required Teachers (27 lessons/week):</strong> {required_teachers}</p>
            <p><strong>Available Teachers:</strong> {available_teachers}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Staffing evaluation with more detailed feedback
        staffing_diff = available_teachers - required_teachers
        if staffing_diff > 0:
            st.success(f"""
            **Staffing Status:** You have {staffing_diff} extra teacher(s) for this combination.
            These teachers could potentially cover {staffing_diff * LESSONS_PER_TEACHER} additional lessons.
            """)
        elif staffing_diff == 0:
            st.info("""
            **Staffing Status:** Perfect match! You have exactly the number of teachers needed for this combination.
            """)
        else:
            st.error(f"""
            **Staffing Status:** You're short by {abs(staffing_diff)} teacher(s) for this combination.
            This creates a deficit of {abs(staffing_diff) * LESSONS_PER_TEACHER} lessons that need to be covered.
            """)
        
        # Subject breakdown in a styled table
        st.markdown("""
        <div style="margin-top: 20px;">
            <h4>Subject Breakdown</h4>
        </div>
        """, unsafe_allow_html=True)
        
        subject_data = [
            {"Subject": subject, "Department": get_department(subject), "Weekly Lessons": load}
            for subject, load in subject_loads.items()
        ]
        
        # Create a styled HTML table
        table_html = """
        <table class="subject-table">
            <tr>
                <th>Subject</th>
                <th>Department</th>
                <th>Weekly Lessons</th>
                <th>% of Total</th>
            </tr>
        """
        
        for row in subject_data:
            percentage = (row["Weekly Lessons"] / total_load) * 100 if total_load > 0 else 0
            table_html += f"""
            <tr>
                <td>{row["Subject"]}</td>
                <td>{row["Department"]}</td>
                <td>{row["Weekly Lessons"]}</td>
                <td>{percentage:.1f}%</td>
            </tr>
            """
        
        table_html += "</table>"
        st.markdown(table_html, unsafe_allow_html=True)
        
        # Additional recommendations
        st.markdown("""
        <div style="margin-top: 30px;">
            <h4>Recommendations</h4>
            <ul>
                <li>Consider cross-departmental teaching assignments for shared subjects</li>
                <li>Review timetabling to optimize teacher utilization</li>
                <li>Check for teachers who might handle additional lessons within their capacity</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown("""
<div style="margin-top: 50px; padding: 15px; background-color: #f8f9fa; border-radius: 5px; text-align: center;">
    <p style="margin: 0; font-size: 0.9em;">TSC Teacher Workload Calculator v2.0 | For official use only</p>
    <p style="margin: 5px 0 0 0; font-size: 0.8em;">© 2023 Ministry of Education | All rights reserved</p>
</div>
""", unsafe_allow_html=True)
