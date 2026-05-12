import streamlit as st
import joblib
import PyPDF2
import matplotlib.pyplot as plt
import pandas as pd

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Career Predictor", layout="wide")

# -------------------- SESSION STATE --------------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# -------------------- SIDEBAR MENU --------------------
menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Menu", menu)

# -------------------- SIGNUP --------------------
if choice == "Signup":
    st.subheader("Create Account")

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")

    if st.button("Signup"):
        if new_user in st.session_state.users:
            st.warning("User already exists!")
        else:
            st.session_state.users[new_user] = new_pass
            st.success("Account created successfully!")

# -------------------- LOGIN --------------------
elif choice == "Login":

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔐 Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome {username} 🎉")
            else:
                st.error("Invalid credentials")

    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/295/295128.png", width=300)

# -------------------- LOGOUT --------------------
if st.session_state.logged_in:
    st.sidebar.write(f"👤 {st.session_state.username}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""

# -------------------- MAIN APP --------------------
if st.session_state.logged_in:

    # -------------------- SIDEBAR NAVIGATION --------------------
    st.sidebar.title("📌 Navigation")
    page = st.sidebar.radio("Go to", [
        "🏠 Dashboard",
        "📊 Prediction",
        "🤖 Chatbot",
        "📄 Resume Analyzer"
    ])

    # -------------------- CUSTOM CSS --------------------
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #0f172a, #1e293b);
        color: white;
    }
    h1, h2, h3 {
        color: #38bdf8;
    }
    </style>
    """, unsafe_allow_html=True)

    # -------------------- LOAD MODEL --------------------
    model = joblib.load("model/career_model.pkl")

    # ==================== DASHBOARD ====================
    if page == "🏠 Dashboard":
        st.title("🎓 Career Dashboard")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("👨‍🎓 CGPA", "7.5")
        with col2:
            st.metric("💻 Skills", "5+")
        with col3:
            st.metric("📊 Status", "Active")

        st.write("Welcome to your AI Career System 🚀")

    # ==================== PREDICTION ====================
    elif page == "📊 Prediction":

        st.title("CareerPath AI")

        # Resume Upload
        st.subheader("📄 Upload Resume (Optional)")
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

        skills_list = ["python","java","c++","machine learning","data science","web development","html","css","javascript","sql","react"]
        detected_skills = []

        if uploaded_file:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""

            for page_pdf in pdf_reader.pages:
                text += page_pdf.extract_text().lower()

            for skill in skills_list:
                if skill in text:
                    detected_skills.append(skill)

            st.write("🧠 Detected Skills:", detected_skills)

        # Role Suggestion
        if detected_skills:
            st.subheader("🎯 Recommended Roles")
            roles = []

            if "python" in detected_skills and "machine learning" in detected_skills:
                roles.append("🤖 ML Engineer")
            if "data science" in detected_skills or "sql" in detected_skills:
                roles.append("📊 Data Scientist")
            if "html" in detected_skills and "css" in detected_skills and "javascript" in detected_skills:
                roles.append("🌐 Frontend Developer")
            if "react" in detected_skills:
                roles.append("⚛️ React Developer")
            if "java" in detected_skills:
                roles.append("☕ Backend Developer")

            for r in roles:
                st.write(r)

        # Input Section
        st.subheader("🧾 Enter Details")

        col1, col2 = st.columns(2)

        with col1:
            cgpa = st.number_input("CGPA", 5.0, 10.0, 7.0)
            projects = st.number_input("Projects", 1, 5, 2)
            certifications = st.number_input("Certifications", 0, 5, 1)
            coding_hours = st.number_input("Coding Hours", 5, 40, 15)

        with col2:
            skill_count = len(detected_skills) if uploaded_file else st.number_input("Skill Count", 1, 10, 5)
            communication = st.number_input("Communication", 1, 10, 5)
            hackathons = st.number_input("Hackathons", 0, 5, 0)
            backlogs = st.number_input("Backlogs", 0, 5, 0)

        internship = 1 if st.selectbox("Internship", ["No", "Yes"]) == "Yes" else 0

        # Prediction Button
        if st.button("Predict"):

            input_data = pd.DataFrame([{
                "cgpa": cgpa,
                "skill_count": skill_count,
                "internship": internship,
                "projects": projects,
                "communication_skill": communication,
                "certifications": certifications,
                "hackathons": hackathons,
                "coding_hours": coding_hours,
                "backlogs": backlogs
            }])

            prediction = model.predict(input_data)[0]

            if prediction == "High":
                st.error("⚠️ High Risk")
            elif prediction == "Medium":
                st.warning("⚡ Medium Risk")
            else:
                st.success("✅ Low Risk")

            # Progress
            score = (cgpa/10 + skill_count/10 + coding_hours/40) / 3
            st.subheader("📊 Profile Strength")
            st.progress(score)

            # Suggestions
            st.subheader("📌 Suggestions")

            if cgpa < 7: st.write("📉 Improve CGPA")
            if skill_count < 5: st.write("🧠 Learn more skills")
            if internship == 0: st.write("🏢 Get internship")
            if projects < 3: st.write("📂 Build projects")
            if communication < 5: st.write("🗣️ Improve communication")
            if certifications < 2: st.write("📜 Do certifications")
            if hackathons == 0: st.write("🏆 Join hackathons")
            if coding_hours < 10: st.write("💻 Practice more")
            if backlogs > 0: st.write("⚠️ Clear backlogs")

            # Bar Chart
            st.subheader("📊 Profile Analysis")

            features = ["CGPA","Skills","Projects","Comm","Certs","Hack","Coding","Backlogs"]
            values = [cgpa, skill_count, projects, communication, certifications, hackathons, coding_hours, backlogs]

            fig, ax = plt.subplots(figsize=(6, 3))
            colors = ['#38bdf8','#6366f1','#22c55e','#f59e0b','#ef4444','#a855f7','#14b8a6','#eab308']
            ax.bar(features, values, color=colors)

            ax.set_facecolor("#0f172a")
            fig.patch.set_facecolor('#0f172a')

            plt.xticks(rotation=30, color="white")
            plt.yticks(color="white")

            st.pyplot(fig)

            # Pie Chart
            st.subheader("📈 Risk Distribution")

            labels = ["Low","Medium","High"]

            if prediction == "Low":
                sizes = [70,20,10]
            elif prediction == "Medium":
                sizes = [20,60,20]
            else:
                sizes = [10,20,70]

            fig2, ax2 = plt.subplots(figsize=(4, 4))
            colors = ['#22c55e','#f59e0b','#ef4444']

            ax2.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, textprops={'color': "white"})
            fig2.patch.set_facecolor('#0f172a')

            st.pyplot(fig2)

    # ==================== CHATBOT ====================
    elif page == "🤖 Chatbot":
        st.title("🤖 AI Chatbot")

        user_input = st.text_input("Ask something")

        if st.button("Send"):
            if user_input:
                msg = user_input.lower()

                if "hello" in msg:
                    st.success("Hello! 👋")
                elif "career" in msg:
                    st.success("Focus on skills + projects 🚀")
                elif "skills" in msg:
                    st.success("Python, ML, Web Dev are in demand 📊")
                else:
                    st.success("Basic chatbot only 😅")

    # ==================== RESUME ANALYZER ====================
    elif page == "📄 Resume Analyzer":
        st.title("📄 Resume Analyzer")

        uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

        skills_list = ["python","java","c++","machine learning","data science","web development","html","css","javascript","sql","react"]

        if uploaded_file:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""

            for page_pdf in pdf_reader.pages:
                text += page_pdf.extract_text().lower()

            detected_skills = [skill for skill in skills_list if skill in text]

            st.write("🧠 Detected Skills:", detected_skills)

            st.subheader("💡 Suggestions")

            if "python" not in detected_skills:
                st.write("➕ Learn Python")
            if "sql" not in detected_skills:
                st.write("➕ Learn SQL")
            if len(detected_skills) < 5:
                st.write("➕ Add more skills")