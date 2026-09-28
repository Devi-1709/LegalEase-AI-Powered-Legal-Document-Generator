# ⚖️ LegalEase: AI-Powered Legal Document Generator

**LegalEase** is a full-stack Generative AI application that automates the drafting of formal, customizable, and legally structured documents. Built with a **FastAPI** microservice backend, **Google Gemini AI** core, and an interactive **Streamlit** frontend, LegalEase empowers founders, freelancers, landlords, and professionals to generate contracts, NDAs, and agreements without requiring a legal background.

---

## ✨ Key Features

* **AI-Powered Legal Drafting:** Dynamically generates formal legal agreements (Employment Contracts, Freelance Work Contracts, NDAs, Residential Leases) tailored to specific parties, effective dates, and custom terms.
* **Auto-Model Discovery Engine:** Automatically queries the Google Gemini REST API (`v1beta/models`) to select active high-speed models (`gemini-2.5-flash`, `gemini-3.5-flash`, `gemini-3.8-flash`) without gRPC timeout bottlenecks.
* **Dark-Mode Live HTML Preview:** Renders generated Markdown into a clean, scrollable semantic HTML preview card.
* **Inline Document Editor:** Allows instant in-browser modification of clauses and wording prior to export.
* **Multi-Format Branded Exports:**
  * **`.TXT`:** Clean plain-text contract for quick copying and archival.
  * **`.DOCX`:** Microsoft Word document formatted in Times New Roman with centered company branding, structured headings, an auto-generated **Summary of Specific Clauses & Terms** table, and page footers.
  * **`.PDF`:** Print-ready Adobe PDF document with embedded header logos, section dividers, and paginated legal footers.

---

## 🏗️ System Architecture

```text
+-----------------------+        HTTP POST /generate         +-----------------------+
|   Streamlit Frontend  | ---------------------------------> |    FastAPI Backend    |
|    (frontend/app.py)  | <--------------------------------- |  (legalEaseAPI/main)  |
+-----------------------+         JSON {"document"}          +-----------------------+
           |                                                             |
           v                                                             v
+-----------------------+                                    +-----------------------+
|   Formatting Engine   |                                    |    Gemini AI Core     |
| (ai_core/generator.py)|                                    | (gemini_generator.py) |
|  - HTML Dark Preview  |                                    |  - Dynamic Model List |
|  - Branded .DOCX      |                                    |  - Legal Prompting    |
|  - Paginated .PDF     |                                    |  - Google Gemini API  |
+-----------------------+                                    +-----------------------+
```

---

## 📂 Project Directory Structure

```text
LEGALEASE/
├── ai_core/
│   ├── __init__.py
│   ├── gemini_generator.py    # Gemini REST API integration & dynamic model discovery
│   └── generator.py           # Text sanitizer & HTML, DOCX, and PDF formatting engine
├── docs/                      # Project documentation & reference assets
├── frontend/
│   └── app.py                 # Streamlit web interface, live editor & download buttons
├── Image/
│   ├── Logo.png               # Standard brand logo for DOCX and PDF headers
│   └── inverseLogo.png        # Light-on-dark logo for the Streamlit UI
├── legalEaseAPI/
│   ├── __init__.py
│   ├── main.py                # FastAPI application entry point & CORS setup
│   └── routes.py              # Pydantic validation & POST /generate endpoint
├── .env                       # Local environment variables (GEMINI_API_KEY)
├── .env.example               # Template for environment variables
├── .gitignore                 # Git exclusion rules
├── config.py                  # Centralized configuration & path management
├── requirements.txt           # Python package dependencies
├── run.bat                    # One-click launcher for Windows
└── run.sh                     # One-click launcher for Linux / macOS / Git Bash
```

---

## 🚀 Getting Started

### Prerequisites
* **Python 3.10+** (Compatible up to Python 3.14)
* **Google Gemini API Key** from [Google AI Studio](https://aistudio.google.com/)

### 1. Clone or Open the Repository
Open the `LEGALEASE` folder in **VS Code** and launch a terminal (`Ctrl + ~`).

### 2. Configure Environment Variables
Create a `.env` file in the project root directory:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
BACKEND_URL=[http://127.0.0.1:8000](http://127.0.0.1:8000)
GEMINI_MODEL_NAME=gemini-2.5-flash
```

### 3. Quick Launch (One-Click Scripts)
* **Windows:** Double-click `run.bat` or run `.\run.bat` in PowerShell/CMD.
* **Linux / macOS / Git Bash:** Run `chmod +x run.sh && ./run.sh`.

### 4. Manual Launch (Two Terminals)

**Terminal 1 — Setup & Start FastAPI Backend:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install --prefer-binary -r requirements.txt
python -m uvicorn legalEaseAPI.main:app --reload --port 8000
```

**Terminal 2 — Start Streamlit Frontend:**
```powershell
.\venv\Scripts\Activate.ps1
python -m streamlit run frontend/app.py
```

Access the web application at:
* **Streamlit Web UI:** [http://localhost:8501](http://localhost:8501)
* **FastAPI Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Usage Scenarios & Sample Inputs

| Scenario | Document Type | Parties Involved | Terms & Conditions (Semicolon-Separated) | Effective Date |
| :--- | :--- | :--- | :--- | :--- |
| **1. Freelance Project** | `Freelance Work Contract` | `Jane Doe (Service Provider), TechNova Inc. (Client)` | `Work must be delivered by May 15, 2026; Payment will be made within 7 days of invoice; The client retains intellectual property rights` | `April 15, 2026` |
| **2. Startup Hiring** | `Employment Contract` | `Apex Labs Pvt Ltd (Employer), Rahul Sharma (Senior Software Engineer)` | `Base salary of $120,000 per annum; 90-day probation period; Strict confidentiality of proprietary source code; 30 days notice period` | `May 1, 2026` |
| **3. Client Pitch NDA** | `Non-Disclosure Agreement` | `Alpha Ventures (Disclosing Party), Studio X (Receiving Party)` | `Confidentiality obligations last for 3 years; No reverse engineering of shared prototypes; Immediate return of materials upon request` | `June 1, 2026` |
| **4. Property Rental** | `Residential Lease Agreement` | `XYZ Realty (Landlord), Alice Smith (Tenant)` | `Monthly rent of $1,500 due on the 1st of each month; Security deposit of $3,000; Lease term of 12 months; No subletting without written consent` | `July 1, 2026` |

---

## 🔌 API Reference

### `GET /`
Health-check endpoint verifying that the FastAPI backend service is online.

### `POST /generate`
Generates a structured legal contract using the Gemini AI Core.

**Request Body (`application/json`):**
```json
{
  "document_type": "Freelance Work Contract",
  "parties": "Jane Doe (Service Provider), TechNova Inc. (Client)",
  "terms": "Work must be delivered by May 15, 2026; Payment within 7 days of invoice",
  "dates": "April 15, 2026"
}
```

**Success Response (`200 OK`):**
```json
{
  "document": "## Freelance Work Contract\n\n**PREAMBLE**\nThis Freelance Work Contract..."
}
```