import streamlit as st
import json
from datetime import datetime

# =========================
# Load questions from same file as Spyder/Tkinter
# =========================
DEFAULT_QUESTIONS_FILE = "questions.json"

try:
    with open(DEFAULT_QUESTIONS_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)

        # Support both:
        # 1) [ {...}, {...} ]
        # 2) { "questions": [ {...}, {...} ] }
        if isinstance(questions, dict) and "questions" in questions:
            questions = questions["questions"]

except Exception as e:
    st.error(f"Could not load questions.json: {e}")
    st.stop()

# =========================
# Validation
# =========================
ALLOWED_CHARS = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-' ")

def validate_name(name):
    return all(c in ALLOWED_CHARS for c in name.strip()) and len(name.strip()) > 0

def validate_dob(dob):
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except:
        return False

def validate_student_id(sid):
    return sid.isdigit()

# =========================
# Psychological state
# (KEEP SAME RANGES AS YOUR SPYDER PROGRAM)
# =========================
def get_psych_state(score):
    if 0 <= score <= 10:
        return "The person is in an excellent state; strong reinforcement of understanding."
    elif 11 <= score <= 20:
        return "The person is in a good state; generally effective reinforcement."
    elif 21 <= score <= 30:
        return "The person is in a moderate state; could use improvement."
    elif 31 <= score <= 40:
        return "The person is in a limited reinforcement state; review strategy suggested."
    elif 41 <= score <= 50:
        return "The person is in a low reinforcement state; effectiveness is weak."
    else:
        return "The person is in minimal learning support; needs significant improvement."

# =========================
# Session state
# =========================
if "survey_started" not in st.session_state:
    st.session_state.survey_started = False

if "survey_submitted" not in st.session_state:
    st.session_state.survey_submitted = False

if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)

if "user_info" not in st.session_state:
    st.session_state.user_info = {}

# =========================
# App UI
# =========================
st.title("Online Lecture Replay Usage and Understanding Reinforcement Survey")

# --- User details ---
given = st.text_input("Given Name")
surname = st.text_input("Surname")
dob = st.text_input("Date of Birth (YYYY-MM-DD)")
student_id = st.text_input("Student ID")

# --- Start survey ---
if st.button("Start Survey"):
    errors = []

    if not validate_name(given):
        errors.append("Invalid given name. Use only letters, spaces, hyphens, and apostrophes.")

    if not validate_name(surname):
        errors.append("Invalid surname. Use only letters, spaces, hyphens, and apostrophes.")

    if not validate_dob(dob):
        errors.append("Invalid date of birth. Use YYYY-MM-DD format.")

    if not validate_student_id(student_id):
        errors.append("Student ID must contain digits only.")

    if errors:
        for err in errors:
            st.warning(err)
    else:
        st.session_state.survey_started = True
        st.session_state.survey_submitted = False
        st.session_state.user_info = {
            "given_name": given,
            "surname": surname,
            "date_of_birth": dob,
            "student_id": student_id
        }

# --- Show survey ---
if st.session_state.survey_started and not st.session_state.survey_submitted:
    st.success("User details validated. Please complete the questionnaire below.")

    for i in range(len(questions)):
        q = questions[i]
        option_labels = [opt[0] for opt in q["options"]]

        # Set current selected option index safely
        current_value = st.session_state.answers[i]
        if current_value in option_labels:
            default_index = option_labels.index(current_value)
        else:
            default_index = 0
            st.session_state.answers[i] = option_labels[0]

        selected = st.radio(
            f"Q{i+1}. {q['question']}",
            option_labels,
            index=default_index,
            key=f"q_{i}"
        )

        st.session_state.answers[i] = selected

    # --- Submit survey ---
    if st.button("Submit Survey"):
        st.session_state.survey_submitted = True

# --- Results ---
if st.session_state.survey_submitted:
    total_score = 0
    answers_with_scores = []

    for i, selected_option in enumerate(st.session_state.answers):
        q = questions[i]

        for option_text, option_score in q["options"]:
            if option_text == selected_option:
                total_score += option_score
                answers_with_scores.append({
                    "question": q["question"],
                    "selected_option": option_text,
                    "score": option_score
                })
                break

    avg_score = float(total_score) / len(questions)
    state = get_psych_state(total_score)

    st.subheader("Survey Results")
    st.write(f"**Total Score:** {total_score}")
    st.write(f"**Average Score:** {avg_score:.2f}")
    st.write(f"**Psychological State:** {state}")

    result_data = {
        "user_info": st.session_state.user_info,
        "answers": answers_with_scores,
        "total_score": total_score,
        "average_score": avg_score,
        "psychological_state": state
    }

    # JSON download
    result_json = json.dumps(result_data, indent=4, ensure_ascii=False)
    st.download_button(
        label="Download Results (JSON)",
        data=result_json,
        file_name="survey_result.json",
        mime="application/json"
    )