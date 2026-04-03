import streamlit as st
import json
from datetime import datetime

# =========================
# Questions
# =========================
questions = [
    {"question":"How often do you re-watch lecture recordings?", "options":[("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"question":"How much does replaying reinforce your understanding?", "options":[("Strongly reinforces",0),("Moderately reinforces",1),("Slightly reinforces",2),("Little",3),("Not at all",4)]},
    {"question":"Do you pause or rewind recordings to check your understanding?", "options":[("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"question":"How often do you use recordings to revise before exams?", "options":[("Every lecture",0),("Most lectures",1),("Some lectures",2),("Rarely",3),("Never",4)]},
    {"question":"How confident are you in understanding topics after replaying?", "options":[("Very confident",0),("Confident",1),("Neutral",2),("Slightly confident",3),("Not confident",4)]},
    {"question":"How often do you combine notes with replays?", "options":[("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"question":"How helpful are replays for missed lectures?", "options":[("Very helpful",0),("Helpful",1),("Somewhat helpful",2),("Slightly helpful",3),("Not helpful",4)]},
    {"question":"How often do you replay confusing parts of lectures?", "options":[("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"question":"How well do replays help you retain knowledge?", "options":[("Extremely well",0),("Well",1),("Moderately",2),("Poorly",3),("Very poorly",4)]},
    {"question":"Do replays help you complete assignments more easily?", "options":[("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"question":"How often do you rewatch lectures before quizzes?", "options":[("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"question":"How much do replays improve your overall learning?", "options":[("Significantly",0),("Moderately",1),("Slightly",2),("Little",3),("Not at all",4)]},
    {"question":"Do replays reduce study stress?", "options":[("Significantly",0),("Moderately",1),("Slightly",2),("Little",3),("Not at all",4)]},
    {"question":"How often do you recommend using replays to peers?", "options":[("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"question":"Overall, how effective are lecture recordings for understanding?", "options":[("Extremely effective",0),("Very effective",1),("Moderately effective",2),("Slightly effective",3),("Not effective",4)]}
]

# =========================
# Validation
# =========================
ALLOWED_CHARS = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-' ")

def validate_name(name):
    return all(c in ALLOWED_CHARS for c in name.strip()) and len(name.strip())>0

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
# Streamlit App
# =========================
st.title("Online Lecture Replay Usage Survey")

# User info
given = st.text_input("Given Name")
surname = st.text_input("Surname")
dob = st.text_input("Date of Birth (YYYY-MM-DD)")
student_id = st.text_input("Student ID")

if st.button("Start Survey"):
    errors = []
    if not validate_name(given):
        errors.append("Invalid given name")
    if not validate_name(surname):
        errors.append("Invalid surname")
    if not validate_dob(dob):
        errors.append("Invalid DOB format")
    if not validate_student_id(student_id):
        errors.append("Student ID must be digits only")
    
    if errors:
        st.warning("\n".join(errors))
    else:
        st.success("User info validated! Answer the questions below:")

        # Survey
        answer_vars = []
        for i in range(len(questions)):
            q = questions[i]
            options = [opt[0] for opt in q["options"]]
            choice = st.radio(f"Q{i+1}. {q['question']}", options, key=i)
            answer_vars.append(choice)

        if st.button("Submit Survey"):
            total_score = 0
            answers = []
            for i, choice in enumerate(answer_vars):
                for text, score in questions[i]["options"]:
                    if text == choice:
                        total_score += score
                        answers.append({"question": questions[i]["question"], "score": score})
            avg_score = float(total_score)/len(questions)
            state = get_psych_state(total_score)

            st.write(f"**Total Score:** {total_score}")
            st.write(f"**Average Score:** {avg_score}")
            st.write(f"**Psychological State:** {state}")

            # JSON download
            result_json = json.dumps({
                "user_info": {"given": given, "surname": surname, "dob": dob, "sid": student_id},
                "answers": answers,
                "total_score": total_score,
                "avg_score": avg_score,
                "state": state
            }, indent=4)

            st.download_button("Download Results (JSON)", data=result_json, file_name="survey_result.json")