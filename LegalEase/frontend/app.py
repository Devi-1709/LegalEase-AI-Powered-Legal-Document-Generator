import streamlit as st
import requests
import re
from pathlib import Path
import sys

# Ensure root directory is on Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import BACKEND_URL, LOGO_PATH, INVERSE_LOGO_PATH
from ai_core.generator import (
    sanitize_text,
    format_html_preview,
    format_docx,
    format_pdf
)

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Dark Styling Matching PDF Specification
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 820px;
    }
    .preview-box {
        background-color: #0f172a;
        color: #f8fafc;
        padding: 24px;
        border-radius: 8px;
        border: 1px solid #334155;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 14px;
        line-height: 1.6;
        margin-top: 15px;
        margin-bottom: 20px;
        max-height: 480px;
        overflow-y: auto;
    }
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Logo Display
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if INVERSE_LOGO_PATH.exists():
        st.image(str(INVERSE_LOGO_PATH), use_container_width=True)
    elif LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)

st.markdown("<h2 style='text-align: center; margin-top: 0;'>AI Legal Document Generator</h2>", unsafe_allow_html=True)

# Initialize Session State
if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "show_edit" not in st.session_state:
    st.session_state.show_edit = False

# Input Controls
document_type = st.text_input(
    "Document Type (Ex: Agreement, Contract, NDA)",
    placeholder="Freelance Work Contract"
)

parties = st.text_area(
    "Parties Involved",
    placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)",
    height=85
)

terms = st.text_area(
    "Terms & Conditions (Use semicolons for bullet points)",
    placeholder="Work must be delivered by May 15, 2026; Payment will be made within 7 days of invoice; The client retains intellectual property rights.",
    height=110
)

dates = st.text_input(
    "Effective Date",
    placeholder="May 1, 2026"
)

# Generation Trigger
if st.button("Generate Document", type="primary"):
    if not document_type.strip() or not parties.strip():
        st.error("Please specify both the Document Type and Parties Involved.")
    else:
        with st.spinner("Synthesizing legal document via Gemini AI core..."):
            try:
                payload = {
                    "document_type": document_type,
                    "parties": parties,
                    "terms": terms,
                    "dates": dates
                }
                res = requests.post(f"{BACKEND_URL}/generate", json=payload, timeout=90)
                if res.status_code == 200:
                    raw_doc = res.json().get("document", "")
                    st.session_state.generated_text = sanitize_text(raw_doc)
                    st.session_state.show_edit = False
                    st.success("Document Generated Successfully!")
                else:
                    err_msg = res.json().get("detail", res.text)
                    st.error(f"Error {res.status_code}: {err_msg}")
            except requests.exceptions.ConnectionError:
                st.error(f"Failed to connect to FastAPI backend at {BACKEND_URL}. Ensure uvicorn is running.")
            except Exception as ex:
                st.error(f"An unexpected error occurred: {str(ex)}")

# Document Presentation, Inline Editing & Export Options
if st.session_state.generated_text:
    styled_html = format_html_preview(st.session_state.generated_text)
    st.markdown(f"<div class='preview-box'>{styled_html}</div>", unsafe_allow_html=True)

    if st.button("Click to Edit Document" if not st.session_state.show_edit else "Collapse Editor"):
        st.session_state.show_edit = not st.session_state.show_edit

    if st.session_state.show_edit:
        edited_content = st.text_area(
            "Edit Document Below:",
            value=st.session_state.generated_text,
            height=320
        )
        st.session_state.generated_text = edited_content

    # File Base Name
    safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", document_type.strip().lower()) or "legal_document"

    col_txt, col_docx, col_pdf = st.columns(3)

    # 1. Plain Text Download
    with col_txt:
        st.download_button(
            label="📄 Download as .TXT",
            data=st.session_state.generated_text,
            file_name=f"{safe_name}.txt",
            mime="text/plain",
            use_container_width=True
        )

    # 2. Microsoft Word DOCX Download
    with col_docx:
        docx_bytes = format_docx(st.session_state.generated_text, document_type, terms_input=terms)
        st.download_button(
            label="📑 Download as .DOCX",
            data=docx_bytes,
            file_name=f"{safe_name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

    # 3. Formatted PDF Download
    with col_pdf:
        pdf_bytes = format_pdf(st.session_state.generated_text, document_type)
        st.download_button(
            label="📕 Download as .PDF",
            data=pdf_bytes,
            file_name=f"{safe_name}.pdf",
            mime="application/pdf",
            use_container_width=True
        )