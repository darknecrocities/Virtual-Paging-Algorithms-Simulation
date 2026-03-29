from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

def generate_ai_insights(reference_string, results):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        return "⚠️ Please configure a valid GEMINI_API_KEY in the .env file to enable AI insights."

    client = genai.Client(api_key=api_key)

    prompt = f"""
    Analyze the following page reference string and algorithm results:

    Reference String: {reference_string}

    Results:
    {results}

    Provide the analysis strictly in the following JSON format. DO NOT INCLUDE ANY MARKDOWN BLOCK WRAPPERS, JUST RAW JSON TEXT:
    {{
        "best_algorithm": "Name of best algorithm here",
        "best_why": "Concise 1-2 sentence explanation here",
        "locality": "Highly concise status of locality here",
        "performance_explanation": "Concise 1-2 sentences explaining performance here",
        "os_relevance": "Concise 1-2 sentences on real-world OS relevance here"
    }}
    """

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
        )
        clean_json = response.text.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:]
        elif clean_json.startswith("```"):
            clean_json = clean_json[3:]
        if clean_json.endswith("```"):
            clean_json = clean_json[:-3]
        return clean_json.strip()
    except Exception as e:
        return f"Error generating AI insights: {str(e)}"
