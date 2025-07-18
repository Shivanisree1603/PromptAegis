import requests
# import os
# from dotenv import load_dotenv
# load_dotenv()

from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

def query_llama_model(user_prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Inner prompt asking the model to classify and return penalties
    system_prompt = """
You are a Prompt Safety Classifier AI with expertise in Indian cybersecurity law and international cybercrime laws.

Your job is to analyze any given user prompt and:

1. Classify it as one of:
   - "Safe": Legal and ethical.
   - "Malicious": Unethical or suspicious (e.g., bypassing security) but not illegal.
   - "Criminal": Clearly violates Indian laws (e.g., hacking, trespassing, phishing, violence).

2. Provide a brief explanation (reason).

3. If "Malicious" or "Criminal", identify all relevant legal consequences — specifically:
   - IPC (Indian Penal Code) sections (e.g., 447 for trespassing, 420 for cheating)
   - IT Act (e.g., Section 66, 66C, 66D for hacking, identity theft, phishing)
   - Describe punishment clearly (imprisonment term or fine)

⚠️ Output must ONLY be a valid JSON object in this format:

{
  "classification": "Safe" / "Malicious" / "Criminal",
  "reason": "Explain classification briefly",
  "punishment": "List all relevant IPC / IT Act sections with clear punishments. If not found, say 'Unknown'."
}

💡 Do not include extra text, formatting, markdown, or explanations outside this JSON object.
"""

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(GROQ_ENDPOINT, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]