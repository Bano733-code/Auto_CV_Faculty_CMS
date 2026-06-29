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
    - Auto profile generation
    - Editable CMS
    - University-based directory
    """)

# ---------------- CREATE PROFILE ----------------
elif menu == "📄 Create Profile":

    st.subheader("Upload CV to Generate Profile")

    name = st.text_input("Full Name")
    university = st.text_input("University")
    uploaded_file = st.file_uploader("Upload CV (PDF)", type=["pdf"])

    if uploaded_file and name and university:

        text = extract_text(uploaded_file)
        ai_output = extract_structured_data(text)

        st.subheader("AI Raw Output")
        st.code(ai_output)

        data = safe_json_parse(ai_output)

        slug = generate_slug(name)

        if st.button("💾 Save Profile"):
            save_or_update_teacher(name, university, slug, data)
            st.success(f"Profile saved! URL slug: {slug}")

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
                    st.info("No data")

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
