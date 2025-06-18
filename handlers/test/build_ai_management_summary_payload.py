from openai import OpenAI
import json
import flet as ft
import google.generativeai  as genai
from collections import Counter
from handlers.test.fetch_and_clean_vulns import fetch_and_clean_vulns
from utils.manage_keys import get_credential


def build_ai_management_summary_payload(page, e, test_uuid):
    vulns = fetch_and_clean_vulns(page, test_uuid)
    print(vulns)
    order = ["Critical", "High", "Medium", "Low", "Info"]
    counts = Counter(v["severity"] for v in vulns)

    data = {
        "total": len(vulns),
        "severity_counts": [counts.get(level, 0) for level in order],
        "order": order,
        "vulnerabilities": vulns,
    }

    api_key = get_credential("AiAPIKey")
    prompt = """You will receive a JSON object containing information about vulnerabilities discovered during a security assessment. Your task is to generate a compelling and comprehensive management summary suitable for executives.

    The summary must follow this strict three-part structure:

    1.  **Opening:** Start with the exact format:
        "During our most recent assessment we have identified <TOTAL> vulnerabilities: <COUNT> <SEVERITY>, <COUNT> <SEVERITY>..."
        Use the 'total', 'order', and 'severity_counts' fields. Only include severities with a count greater than zero.

    2.  **Executive Summary Paragraph:** After the opening, write a detailed paragraph of **at least 3 to 4 sentences** that synthesizes all findings into a cohesive risk narrative.
        - **First,** begin with a high-level sentence establishing the overall security posture (e.g., "This assessment has identified multiple, interconnected security weaknesses across the application and infrastructure.").
        - **Second,** group the findings into their **primary themes, giving proportional weight**. Start with the theme of the highest severity findings, and then incorporate themes from other significant findings (e.g., "The risks primarily cluster around **insecure credential management**, highlighted by the High-severity finding, but are significantly compounded by **systemic access control misconfigurations** and a **lack of input sanitization** noted in the Medium and Low-severity findings.").
        - **Third,** explain the **combined business impact** of these themes together. Describe how the different issues create a greater, more complex risk than any single finding in isolation (e.g., "This combination of weaknesses creates a tangible risk of a multi-stage attack where an initial compromise could escalate quickly, leading to a major data breach, operational disruption, and significant reputational harm.").
        - **Finally,** provide a **broader strategic recommendation** that addresses both immediate and systemic issues (e.g., "Therefore, we recommend a two-pronged strategy: immediately remediating the high-severity findings to close the most critical gaps, while initiating a thematic review to correct the underlying root causes of all identified vulnerabilities.").

    3.  **Conclusion:** Conclude with the exact sentence:
        "Addressing these issues will result in a better security posture."
        
    4.  **CRITICAL FORMATTING RULE:** The generated summary text **must be plain text only.** It absolutely **must not** contain any markdown characters for styling, such as asterisks for bolding (`**text**`) or underscores for italics. The entire output must be free of any formatting tags.

    Return your final output as a single JSON object with one key, "summary", like this:
    {"summary": "<GENERATED SUMMARY>"}
    """

    if page.app_state.ai_assistant == "GPT":
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": json.dumps(data)}
            ],
            temperature=0.7
        )

        page.app_state.info_progress.visible = False
        page.app_state.management_summary_text_field.value = response.choices[0].message.content
        page.snack_bar.content = ft.Row(
                    [
                        ft.Icon(name=ft.Icons.SMART_TOY_OUTLINED, color=ft.Colors.BLACK87),
                        ft.Text("Management summary created", color=ft.Colors.BLACK87)
                    ]
                )
        page.snack_bar.bgcolor = ft.Colors.GREEN_400

    elif page.app_state.ai_assistant == "Gemini":
        try:
            genai.configure(api_key=api_key)
            gemini_model_name = "gemini-2.0-flash"
            model = genai.GenerativeModel(gemini_model_name)
            generation_config = genai.GenerationConfig(
                temperature=0.4,
                response_mime_type="application/json"
            )

            try:
                response = model.generate_content([prompt, json.dumps(data)], generation_config=generation_config)
                json_object = json.loads(response.text)
                summary_text = json_object.get("summary", "Error: 'summary' key not found.")
                page.app_state.info_progress.visible = False
                page.app_state.management_summary_text_field.value = summary_text
                page.app_state.edit_ai_summary_button.disabled = False
                page.snack_bar.content = ft.Row(
                    [
                        ft.Icon(name=ft.Icons.SMART_TOY_OUTLINED, color=ft.Colors.BLACK87),
                        ft.Text("Management summary created", color=ft.Colors.BLACK87)
                    ]
                )
                page.snack_bar.bgcolor = ft.Colors.GREEN_400

            except Exception as e:
                print(f"Error calling or parsing Gemini API response: {e}")
                json_dump = f'{{"error": "Gemini API Error or JSON parsing failed: {e}"}}'
                page.app_state.info_progress.visible = False
                page.app_state.management_summary_text_field.value = json_dump
                page.snack_bar.content = ft.Row(
                    [
                        ft.Icon(name=ft.Icons.WARNING_OUTLINED, color=ft.Colors.BLACK87),
                        ft.Text(f"Error calling or parsing Gemini API response: {e}", color=ft.Colors.BLACK87)
                    ]
                )
                page.snack_bar.bgcolor = ft.Colors.ORANGE_400
        except Exception as e:
            print(f"Error calling Gemini API with model '{gemini_model_name}': {e}")
            json_dump =  f'{{"error": "Gemini API Error: {e}"}}'
            page.app_state.info_progress.visible = False
            page.app_state.management_summary_text_field.value = json_dump
            page.snack_bar.content = ft.Row(
                [
                    ft.Icon(name=ft.Icons.WARNING_OUTLINED, color=ft.Colors.BLACK87),
                    ft.Text(f"Error calling Gemini API with model '{gemini_model_name}': {e}", color=ft.Colors.BLACK87)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.ORANGE_400

    page.snack_bar.open = True
    page.update()