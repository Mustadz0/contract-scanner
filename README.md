<div align="center">

# Contract Clause Scanner

### AI-powered contract analysis — Spot red flags before you sign

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3-F97316?logo=groq&logoColor=white)](https://groq.com)
[![Gemini](https://img.shields.io/badge/Gemini-2.0-8E75B2?logo=googlegemini&logoColor=white)](https://deepmind.google/gemini)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Mustadz0/contract-scanner/pulls)
[![CI](https://github.com/Mustadz0/contract-scanner/actions/workflows/ci.yml/badge.svg)](https://github.com/Mustadz0/contract-scanner/actions)
[![Deploy to Render](https://img.shields.io/badge/Deploy%20to%20Render-46E3B7?logo=render&logoColor=white)](https://render.com/deploy?repo=https://github.com/Mustadz0/contract-scanner)

---

[🇬🇧 English](#english) &nbsp;•&nbsp; [🇸🇦 العربية](#arabic) &nbsp;•&nbsp; [🇫🇷 Français](#francais) &nbsp;•&nbsp; [🇪🇸 Español](#espanol) &nbsp;•&nbsp; [🇩🇪 Deutsch](#deutsch) &nbsp;•&nbsp; [🇹🇷 Türkçe](#turkce)

---

</div>

---

<a name="english"></a>
## 🇬🇧 English

**Contract Clause Scanner** is a free, open-source AI tool that analyzes legal contracts and highlights risky clauses before you sign. Built for freelancers, startup founders, and anyone who needs to understand what they're signing without paying $300/hour for a lawyer.

### The Problem

Solo founders and freelancers sign contracts every week that contain hidden risks. Non-refundable payment clauses. Auto-renewal traps. Unlimited liability. Broad indemnification. Arbitration clauses that favor one side.

A lawyer costs **$300–500/hour** just to read a 5-page contract. Most people sign without knowing what they agreed to.

**This tool gives you a second pair of AI eyes — for free.**

### Features

- **AI Clause Detection** — Identifies HIGH, MEDIUM, and LOW risk clauses
- **Risk Score** — Overall contract risk assessment (0–100)
- **Negotiation Tips** — Practical suggestions for each red flag
- **Multi-Format** — Works with PDF, DOCX, and TXT files
- **6 Languages** — English, Arabic, French, Spanish, German, Turkish
- **Web UI** — Drag-and-drop interface
- **CLI** — Command-line for automation
- **100% Free** — No paid tiers, no limits (uses free Groq/Gemini APIs)

### Quick Start

```bash
# 1. Clone & install
git clone https://github.com/Mustadz0/contract-scanner.git
cd contract-scanner
pip install -r requirements.txt

# 2. Add your API keys to .env
# Get free keys at:
#   Groq: https://console.groq.com/keys
#   Gemini: https://aistudio.google.com/apikey
echo "GROQ_API_KEY=gsk_your_key_here" >> .env
echo "GEMINI_API_KEY=AIza_your_key_here" >> .env

# 3. Analyze a contract
python cli.py contract.pdf
python cli.py contract.docx --language ar
python cli.py contract.txt --language fr --output report.json

# 4. Launch Web UI
python web.py
# Open http://localhost:8000
```

### CLI Usage

```bash
# Basic analysis
python cli.py contract.pdf

# Arabic analysis
python cli.py contract.docx --language ar

# Save report as JSON
python cli.py contract.txt --output report.json

# All supported languages: en, ar, fr, es, de, tr
```

### Web UI

```bash
python web.py
```

Upload your contract (PDF, DOCX, or TXT), select the output language, and get an instant risk analysis with highlighted clauses, severity ratings, and negotiation tips.

### How It Works

```
Contract (PDF/DOCX/TXT) → Text Extraction → AI Analysis (Groq/Gemini) → Risk Report
```

1. **Upload** your contract file
2. **AI reads** every clause and compares against known risky patterns
3. **Report** shows risk score, red flags with severity, and what to negotiate

### Why This Exists

Contract review tools for businesses start at **$99–500/month**. Lawyers charge **$300/hour**. Solo founders and freelancers shouldn't have to choose between paying rent and understanding what they sign.

---

<a name="arabic"></a>
## 🇸🇦 العربية

**مدقق بنود العقود** — أداة ذكاء اصطناعي مجانية ومفتوحة المصدر لتحليل العقود القانونية واكتشاف البنود الخطيرة قبل التوقيع. صممت للمؤسسين المنفردين والمستقلين الذين يحتاجون فهم عقودهم دون دفع $300/ساعة لمحام.

### المشكلة

المؤسسون المنفردون يوقعون عقودًا أسبوعيًا تحتوي على مخاطر خفية: دفعات غير قابلة للاسترداد، شرط تجديد تلقائي، مسؤولية غير محدودة، تحكيم إجباري.

المحامي يكلف **$300–500/ساعة** فقط لقراءة عقد من 5 صفحات. معظم الناس يوقعون دون معرفة ما وافقوا عليه.

**هذه الأداة تعطيك عينًا ثانية من الذكاء الاصطناعي — مجانًا.**

### بداية سريعة

```bash
pip install -r requirements.txt
python cli.py عقد.pdf --language ar
python web.py
```

### المميزات

- **اكتشاف تلقائي** للبنود الخطرة (HIGH/MEDIUM/LOW)
- **نقاط المخاطرة** (0–100) لتقييم العقد ككل
- **اقتراحات تفاوضية** لكل بند خطر
- **دعم PDF و DOCX و TXT**
- **واجهة ويب** بالسحب والإفلات
- **واجهة أوامر** للأتمتة
- **مجاني تمامًا** — يستخدم APIs مجانية

### صيغ الإخراج

| اللغة | الأمر |
|-------|-------|
| العربية | `python cli.py عقد.pdf --language ar` |
| الإنجليزية | `python cli.py contract.pdf --language en` |
| الفرنسية | `python cli.py contrat.pdf --language fr` |

---

<a name="francais"></a>
## 🇫🇷 Français

**Analyseur de Clauses Contractuelles** — Un outil IA gratuit et open-source qui analyse les contrats juridiques et signale les clauses risquées avant signature.

### Démarrage rapide

```bash
pip install -r requirements.txt
python cli.py contrat.pdf --language fr
python web.py
```

### Fonctionnalités

- Détection des clauses à risque (HIGH/MEDIUM/LOW)
- Score de risque global (0–100)
- Conseils de négociation
- Formats supportés : PDF, DOCX, TXT
- Interface Web glisser-déposer
- 100% gratuit

---

<a name="espanol"></a>
## 🇪🇸 Español

**Escáner de Cláusulas Contractuales** — Una herramienta de IA gratuita y de código abierto que analiza contratos legales y señala cláusulas de riesgo antes de firmar.

### Inicio rápido

```bash
pip install -r requirements.txt
python cli.py contrato.pdf --language es
python web.py
```

### Características

- Detección automática de cláusulas riesgosas
- Puntuación de riesgo general (0–100)
- Consejos de negociación
- Soporte para PDF, DOCX, TXT
- 100% gratuito

---

<a name="deutsch"></a>
## 🇩🇪 Deutsch

**Vertragsklausel-Scanner** — Ein kostenloses Open-Source-KI-Tool zur Analyse von Rechtsverträgen und Erkennung riskanter Klauseln vor der Unterzeichnung.

### Schnellstart

```bash
pip install -r requirements.txt
python cli.py vertrag.pdf --language de
python web.py
```

### Funktionen

- Automatische Erkennung risikoreicher Klauseln
- Gesamtrisikobewertung (0–100)
- Verhandlungsvorschläge
- Unterstützt PDF, DOCX, TXT
- 100% kostenlos

---

<a name="turkce"></a>
## 🇹🇷 Türkçe

**Sözleşme Madde Tarayıcısı** — İmzalamadan önce yasal sözleşmeleri analiz eden ve riskli maddeleri işaretleyen ücretsiz, açık kaynaklı bir AI aracı.

### Hızlı Başlangıç

```bash
pip install -r requirements.txt
python cli.py sozlesme.pdf --language tr
python web.py
```

### Özellikler

- Riskli maddelerin otomatik tespiti
- Genel risk puanı (0–100)
- Pazarlık ipuçları
- PDF, DOCX, TXT desteği
- Tamamen ücretsiz

---

<div align="center">

**Support Development**

TRON (TRC20): `TSQt2sV6NypuXFK3mqtPCgzHeoXug6pQp4`

</div>

---

<div align="center">

**Made with ❤️ by [Mustadz0](https://github.com/Mustadz0)**

Contributions, issues, and feature requests are welcome!

[![GitHub stars](https://img.shields.io/github/stars/Mustadz0/contract-scanner?style=social)](https://github.com/Mustadz0/contract-scanner/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Mustadz0/contract-scanner?style=social)](https://github.com/Mustadz0/contract-scanner/network/members)

</div>
