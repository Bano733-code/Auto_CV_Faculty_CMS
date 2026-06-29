from groq import Groq
import json
import re

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def extract_structured_data(cv_text):

    prompt = f"""
Extract structured academic data from this CV.

Return ONLY valid JSON:

{{
  "projects": [],
  "publications": [],
  "skills": []
}}

CV:
{cv_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def safe_json_parse(text):
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                return {"projects": [], "publications": [], "skills": []}

        return {"projects": [], "publications": [], "skills": []}


def generate_slug(name):
    return name.lower().strip().replace(" ", "-")
