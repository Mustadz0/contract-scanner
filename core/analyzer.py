import json
import os
import re
import time
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are a senior contract lawyer with 20 years of experience in commercial, employment, and service agreements. Analyze the contract text below and identify risks.

For EVERY clause you flag, you MUST include:
1. Severity: HIGH (definitely dangerous - could cost significant money or rights), MEDIUM (concerning - needs attention), LOW (minor - worth noting)
2. The exact clause text that is problematic
3. A clear explanation of WHY it's risky in plain business language
4. A specific negotiation tip — what to ask for instead

Look for these common traps:
- Auto-renewal clauses without opt-out
- Indemnification that is one-sided
- Non-compete / non-solicit that is too broad
- Limitation of liability that excludes your remedies
- Termination for convenience only on their side
- Governing law / jurisdiction far from you
- Liquidated damages that seem punitive
- Data ownership / IP assignment that takes your pre-existing IP
- Payment terms that are unreasonable (net 90+, or after customer pays them)
- Force majeure that doesn't include pandemics or internet outages

Output ONLY valid JSON (no markdown, no code fences):
{
  "overall_risk_score": 0-100,
  "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "summary": "2-3 sentence summary of the contract and key concerns",
  "red_flags": [
    {
      "severity": "HIGH|MEDIUM|LOW",
      "clause": "exact clause text (max 200 chars)",
      "why_risky": "plain language explanation",
      "negotiation_tip": "specific alternative to request"
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

        prompt = f"{SYSTEM_PROMPT}\n\n{lang_instruction}\n\nCONTRACT TEXT:\n{text[:20000]}"

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
                "temperature": 0.1,
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
                "summary": "Could not parse AI analysis. Manual review recommended.",
                "red_flags": [],
                "key_watchpoints": ["Manual review recommended"],
                "next_steps": ["Consult a lawyer"],
                "_raw": raw[:500],
            }
