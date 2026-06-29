import streamlit as st
import json

from db import create_tables, save_or_update_teacher, get_teacher_by_slug, get_universities
from parser import extract_text
from ai import extract_structured_data, safe_json_parse, generate_slug

# initialize DB
create_tables()

# UI config
st.set_page_config(page_title="AutoCV Faculty CMS", layout="wide")

st.title("🧠 AutoCV Faculty CMS")
st.caption("AI-powered CV → Faculty Profile Generator")

menu = st.sidebar.radio("Navigation", [
    "🏠 Dashboard",
    "📄 Create Profile",
    "👤 View Profile",
    "🏫 University Directory"
])

# ---------------- DASHBOARD ----------------
if menu == "🏠 Dashboard":
    st.subheader("Welcome 👋")

    st.markdown("""
    ### 🚀 System Features
    - Upload CV (PDF)
    - AI extracts Projects, Publications, Skills
    - Editable CMS (NEW ✨)
    - University-based directory
    """)

# ---------------- CREATE PROFILE ----------------
elif menu == "📄 Create Profile":

    st.subheader("Upload CV to Generate & Edit Profile")

    name = st.text_input("Full Name")
    university = st.text_input("University")
    uploaded_file = st.file_uploader("Upload CV (PDF)", type=["pdf"])

    if uploaded_file and name and university:

        # -------- AI PIPELINE --------
        text = extract_text(uploaded_file)
        ai_output = extract_structured_data(text)

        st.subheader("🤖 AI Raw Output")
        st.code(ai_output)

        data = safe_json_parse(ai_output)

        slug = generate_slug(name)

        # -------- SESSION STATE INIT (IMPORTANT) --------
        if "projects" not in st.session_state:
            st.session_state.projects = data.get("projects", [])

        if "publications" not in st.session_state:
            st.session_state.publications = data.get("publications", [])

        if "skills" not in st.session_state:
            st.session_state.skills = data.get("skills", [])

        # ---------------- EDITABLE UI ----------------

        st.markdown("## 📌 Projects")

        new_project = st.text_input("Add New Project")
        if st.button("➕ Add Project"):
            if new_project:
                st.session_state.projects.append(new_project)

        updated_projects = []
        for i, p in enumerate(st.session_state.projects):
            edited = st.text_input(f"Project {i+1}", value=p, key=f"proj_{i}")
            updated_projects.append(edited)
        st.session_state.projects = updated_projects

        st.markdown("## 📄 Publications")

        new_pub = st.text_input("Add New Publication")
        if st.button("➕ Add Publication"):
            if new_pub:
                st.session_state.publications.append(new_pub)

        updated_pubs = []
        for i, p in enumerate(st.session_state.publications):
            edited = st.text_input(f"Publication {i+1}", value=p, key=f"pub_{i}")
            updated_pubs.append(edited)
        st.session_state.publications = updated_pubs

        st.markdown("## 🧠 Skills")

        new_skill = st.text_input("Add New Skill")
        if st.button("➕ Add Skill"):
            if new_skill:
                st.session_state.skills.append(new_skill)

        updated_skills = []
        for i, s in enumerate(st.session_state.skills):
            edited = st.text_input(f"Skill {i+1}", value=s, key=f"skill_{i}")
            updated_skills.append(edited)
        st.session_state.skills = updated_skills

        # ---------------- FINAL SAVE ----------------
        final_data = {
            "projects": st.session_state.projects,
            "publications": st.session_state.publications,
            "skills": st.session_state.skills
        }

        st.markdown("---")

        if st.button("💾 Save Final Profile"):
            save_or_update_teacher(name, university, slug, final_data)
            st.success(f"✅ Profile saved successfully! Slug: {slug}")

# ---------------- VIEW PROFILE ----------------
elif menu == "👤 View Profile":

    st.subheader("Faculty Profile Viewer")

    slug = st.text_input("Enter profile slug (e.g. john-doe)")

    if slug:
        teacher = get_teacher_by_slug(slug)

        if teacher:
            st.success("Profile Found")

            st.markdown(f"## 👨‍🏫 {teacher['name']}")
            st.markdown(f"🏫 {teacher['university']}")

            data = teacher["data"]

            def show(title, items):
                st.markdown(f"### {title}")
                if items:
                    for i in items:
                        st.write("📌", i)
                else:
                    st.info("No data available")

            show("Projects", data.get("projects"))
            show("Publications", data.get("publications"))
            show("Skills", data.get("skills"))

        else:
            st.error("Profile not found")

# ---------------- UNIVERSITY DIRECTORY ----------------
elif menu == "🏫 University Directory":

    st.subheader("Universities")

    universities = get_universities()

    for uni in universities:
        st.markdown(f"## 🏫 {uni}")
