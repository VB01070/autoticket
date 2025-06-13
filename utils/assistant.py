import openai
import google.generativeai  as genai
from utils.manage_keys import get_credential
import json

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
        try:
            genai.configure(api_key=api_key)
            gemini_model_name = "gemini-2.0-flash"
            model = genai.GenerativeModel(gemini_model_name)
            generation_config = genai.GenerationConfig(temperature=0.4)
            response = model.generate_content(prompt, generation_config=generation_config)
            raw_content = response.text.strip()

            if raw_content.startswith('```json') and raw_content.endswith('```'):
                content = raw_content[len('```json'):-len('```')].strip()
            elif raw_content.startswith('```') and raw_content.endswith('```'):
                content = raw_content[len('```'):-len('```')].strip()
            else:
                content = raw_content

            try:
                json_object = json.loads(content)
                return json.dumps(json_object)
            except json.JSONDecodeError:
                print(f"Warning: Gemini response was not valid JSON after stripping markdown: {content[:200]}...")
                return f'{{"error": "Gemini response was malformed JSON.", "raw_response": {json.dumps(content)}}}'
        except Exception as e:
            print(f"Error calling Gemini API with model '{gemini_model_name}': {e}")
            return f'{{"error": "Gemini API Error: {e}"}}'

    return '{"error": "Unsupported AI model type"}'
