import openai
import os
import google.generativeai  as genai
from utils.manage_keys import get_credential

api_key = get_credential("AiAPIKey")


def generate_ai_suggestion(title, severity, notes, model, template=None):
    base_sections = {
        "description": "",
        "impact": "",
        "recommendation": ""
    }

    if isinstance(template, dict):
        for key in base_sections:
            if template.get(key):
                base_sections[key] = template[key].strip()

    prompt = f"""
You are a security expert. Analyze the following vulnerability and enhance or complete the missing fields.

Use the template (if provided) as a baseline — do not contradict it.
Fill only missing or weak sections, and generate useful references.

Return a JSON object like this:

{{
  "description": "...",
  "impact": "...",
  "recommendation": "...",
  "references": [
    {{ "source": "CWE", "url": "https://..." }},
    {{ "source": "OWASP", "url": "https://..." }}
  ]
}}

----

Template:
Description: {base_sections['description'] or '[missing]'}
Impact: {base_sections['impact'] or '[missing]'}
Recommendation: {base_sections['recommendation'] or '[missing]'}

----

Title: {title}
Severity: {severity}
Note: {notes}

Always respond with only valid JSON. Do not include labels, explanations, or extra formatting.
"""
    if model == "GPT":
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        content = response.choices[0].message.content.strip()
        return content or '{"error": "Empty AI Response"}'
    elif model == "Gemini":
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        content = response.choices[0].message.content.strip()
        return content or '{"error": "Empty AI Response"}'
