import os
import re
import requests
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

def get_gemini_api_key() -> str:
    """Finds and loads GEMINI_API_KEY from root or any project subfolder."""
    candidate_dirs = [
        BASE_DIR,
        Path.cwd(),
        BASE_DIR / "docs",
        BASE_DIR / "legalEaseAPI",
        BASE_DIR / "frontend",
        BASE_DIR / "ai_core",
    ]
    candidate_names = [".env", ".env.txt", ".env.local", ".env.example"]

    for folder in candidate_dirs:
        if not folder.exists():
            continue
        for name in candidate_names:
            env_file = folder / name
            if env_file.is_file():
                load_dotenv(dotenv_path=env_file, override=True)
                key = os.getenv("GEMINI_API_KEY", "").strip().strip('"').strip("'")
                if key and key != "your_gemini_api_key_here":
                    return key
                try:
                    raw_content = env_file.read_text(encoding="utf-8", errors="ignore")
                    match = re.search(r"(AIza[0-9A-Za-z\-_]{30,})", raw_content)
                    if match:
                        return match.group(1)
                except Exception:
                    pass

    return os.getenv("GEMINI_API_KEY", "").strip()


class GeminiDocumentGenerator:
    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = api_key or get_gemini_api_key()
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            raise ValueError(
                f"GEMINI_API_KEY not found in {BASE_DIR / '.env'}. "
                "Please set GEMINI_API_KEY=AIza... in your .env file."
            )
        self.model_name = model_name

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        prompt = (
            f"Generate a comprehensive legal document titled '{document_type}'.\n"
            f"Involved parties: {parties}\n"
            f"Effective Date: {dates}\n"
            f"Terms and conditions: {terms}\n\n"
            "Requirements:\n"
            f"1. Start with a title heading: '## {document_type}'.\n"
            "2. Ensure formal legal structure with multiple numbered sections and legal clauses "
            "(Preamble, WITNESSETH/Recitals, Services/Scope, Term and Termination, Payment, "
            "Intellectual Property Rights, Confidentiality, Independent Contractor Status, "
            "Governing Law, Entire Agreement, Severability, and Signatures).\n"
            "3. Return ONLY the formal legal document text without conversational intro or outro."
        )

        # Exact active models verified on your API key
        models_to_try = [
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
            "gemini-flash-latest",
            "gemini-flash-lite-latest",
            "gemini-3.5-flash-lite",
            "gemini-3.5-flash",
            "gemini-3.7-flash",
            "gemini-3.8-flash",
            "gemini-3.1-flash-lite",
            "gemma-4-31b-it",
        ]

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.3,
            }
        }

        errors = []
        for model in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
            try:
                res = requests.post(url, json=payload, timeout=60)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        # Extract non-thought text parts (supports Gemini 2.5/3.x thinking models)
                        output_chunks = [
                            p["text"] for p in parts
                            if "text" in p and not p.get("thought", False)
                        ]
                        if not output_chunks and parts and "text" in parts[-1]:
                            output_chunks = [parts[-1]["text"]]
                        if output_chunks:
                            return "\n".join(output_chunks).strip()
                else:
                    errors.append(f"{model} -> HTTP {res.status_code}: {res.text[:160]}")
            except Exception as e:
                errors.append(f"{model} -> {str(e)}")
                continue

        raise RuntimeError("All Gemini models failed:\n" + "\n".join(errors))