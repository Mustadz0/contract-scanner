import json
import os
import re
import time
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are a contract analysis expert. Analyze the following contract/clause and identify potential risks, red flags, and unusual terms.

For each clause you identify as problematic, provide:
1. Severity (HIGH / MEDIUM / LOW)
2. The specific clause text
3. Why it's a red flag (in simple language)
4. What to ask a lawyer or how to negotiate it better

Also provide:
- An overall risk score (0-100)
- 3 key things to watch out for
- Suggested next steps

Respond ONLY in valid JSON format without markdown wrapping:
{
  "overall_risk_score": 0-100,
  "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "summary": "2-3 sentence summary of the contract",
  "red_flags": [
    {
      "severity": "HIGH|MEDIUM|LOW",
      "clause": "exact clause text",
      "why_risky": "explanation",
      "negotiation_tip": "what to ask for instead"
    }
  ],
  "key_watchpoints": ["point1", "point2", "point3"],
  "next_steps": ["step1", "step2", "step3"]
}
"""


class ContractAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        self.groq_key = api_key or os.getenv("GROQ_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    def analyze(self, text: str, language: str = "en") -> dict:
        lang_instruction = {
            "en": "Analyze in English.",
            "ar": "حلل باللغة العربية.",
            "fr": "Analysez en français.",
            "es": "Analice en español.",
            "de": "Analysieren Sie auf Deutsch.",
            "tr": "Türkçe analiz yapın.",
        }.get(language, "Analyze in English.")

        prompt = f"{SYSTEM_PROMPT}\n\n{lang_instruction}\n\nCONTRACT TEXT:\n{text[:15000]}"

        if self.groq_key:
            try:
                return self._analyze_groq(prompt)
            except Exception as e:
                print(f"[WARN] Groq failed: {e}, falling back to Gemini")

        if self.gemini_key:
            try:
                return self._analyze_gemini(prompt)
            except Exception as e:
                print(f"[WARN] Gemini failed: {e}")

        raise ValueError("No API key available. Set GROQ_API_KEY or GEMINI_API_KEY in .env")

    def _analyze_groq(self, prompt: str) -> dict:
        import httpx

        resp = httpx.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.groq_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.groq_model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
                "max_tokens": 4096,
            },
            timeout=60,
        )
        resp.raise_for_status()
        raw = resp.json()["choices"][0]["message"]["content"]
        return self._parse_json(raw)

    def _analyze_gemini(self, prompt: str) -> dict:
        import google.genai as genai

        client = genai.Client(api_key=self.gemini_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt,
        )
        return self._parse_json(response.text)

    def _parse_json(self, raw: str) -> dict:
        raw = raw.strip()
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {
                "overall_risk_score": 50,
                "risk_level": "MEDIUM",
                "summary": "Could not parse analysis. Manual review recommended.",
                "red_flags": [],
                "key_watchpoints": ["Manual review recommended"],
                "next_steps": ["Consult a lawyer"],
                "_raw": raw[:500],
            }
