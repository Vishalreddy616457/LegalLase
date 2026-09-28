import os
from dotenv import load_dotenv

load_dotenv()

class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
        self.model = None

        if self.api_key:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)

    def build_prompt(self, document_type, parties, terms, dates):
        return f"""
You are the AI document-generation engine for LegalEase.

Create a professional, structured legal-document DRAFT.

Document type: {document_type}
Parties involved: {parties}
Terms and conditions: {terms}
Effective date: {dates}

Requirements:
1. Use a clear title.
2. Include the parties and effective date.
3. Create numbered sections and clauses appropriate for the document type.
4. Include signature blocks.
5. Use plain, professional language.
6. Preserve the supplied facts and terms.
7. Do not invent important personal or financial facts.
8. Add this notice at the beginning:
"DEMO DRAFT - NOT LEGAL ADVICE. Review by a qualified legal professional before use."
9. Return plain text only.
"""

    def fallback_document(self, document_type, parties, terms, dates):
        terms_list = [x.strip() for x in terms.split(";") if x.strip()]
        terms_text = "\n".join(
            f"{i}. {term}" for i, term in enumerate(terms_list, 1)
        ) or "The parties will agree the detailed terms in writing."

        return f"""DEMO DRAFT - NOT LEGAL ADVICE
Review by a qualified legal professional before use.

{document_type.upper()}

Effective Date: {dates}

PARTIES
{parties}

1. PURPOSE
The parties enter into this {document_type} for the purpose described by them.

2. TERMS AND CONDITIONS
{terms_text}

3. GENERAL PROVISIONS
Any amendment should be made in writing and agreed by the parties.

4. SIGNATURES

Party 1: ______________________________
Name: _________________________________
Date: __________________________________

Party 2: ______________________________
Name: _________________________________
Date: __________________________________
"""

    def generate_document(self, document_type, parties, terms, dates):
        if not self.model:
            return self.fallback_document(document_type, parties, terms, dates)

        response = self.model.generate_content(
            self.build_prompt(document_type, parties, terms, dates)
        )
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned no text.")
        return text.strip()
