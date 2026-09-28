import html
import requests
import streamlit as st
from utils.exporters import format_docx, format_pdf

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")
st.title("⚖️ LegalEase")
st.caption("AI-Powered Legal Document Generator")
st.info(
    "LegalEase creates editable document drafts. "
    "Generated content is not legal advice and should be reviewed by a qualified legal professional."
)

with st.form("document_form"):
    document_type = st.selectbox(
        "Document Type",
        [
            "Employment Contract",
            "Lease Agreement",
            "Non-Disclosure Agreement (NDA)",
            "Freelance Work Contract",
            "Service Agreement",
            "General Agreement",
        ],
    )
    parties = st.text_area(
        "Parties Involved",
        placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)"
    )
    terms = st.text_area(
        "Terms & Conditions",
        placeholder="Payment within 30 days; Confidentiality required; 15 days notice"
    )
    dates = st.text_input("Effective Date", placeholder="April 10, 2026")
    submitted = st.form_submit_button("Generate Document")

if submitted:
    if not parties.strip() or not dates.strip():
        st.error("Please enter the parties and effective date.")
    else:
        with st.spinner("Generating document..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/generate",
                    json={
                        "document_type": document_type,
                        "parties": parties,
                        "terms": terms,
                        "dates": dates,
                    },
                    timeout=120,
                )
                response.raise_for_status()
                st.session_state["document"] = response.json()["document"]
            except requests.RequestException as exc:
                st.error(f"Backend connection failed: {exc}")

if "document" in st.session_state:
    st.subheader("Generated Document")
    edited = st.text_area(
        "Click here to edit the document",
        value=st.session_state["document"],
        height=500,
    )
    st.session_state["document"] = edited

    st.subheader("Preview")
    st.markdown(
        '<div style="background:#111827;color:#f9fafb;padding:24px;'
        'border-radius:12px;white-space:pre-wrap;">'
        + html.escape(edited) + "</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            "Download TXT", edited.encode("utf-8"),
            "legalease_document.txt", "text/plain"
        )
    with col2:
        st.download_button(
            "Download DOCX", format_docx(edited, document_type),
            "legalease_document.docx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    with col3:
        st.download_button(
            "Download PDF", format_pdf(edited, document_type),
            "legalease_document.pdf", "application/pdf"
        )
