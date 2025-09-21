#Legal Document Demystifier (Gemini + Colab)
#Install Gemini API library
!pip install -q -U google-generativeai PyPDF2

#Import required libraries
import google.generativeai as genai
from IPython.display import display, Markdown
from google.colab import userdata, files
import textwrap
import PyPDF2

#Helper function:
def to_markdown(text):
    text = text.replace('•', ' *')  # replace bullet characters
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

#Configure API key(must be saved in Colab secrets beforehand)
try:
    GEMINI_API_KEY = userdata.get('GEMINI_API_KEY')
    genai.configure(api_key=GEMINI_API_KEY)
except KeyError:
    raise ValueError("API key 'GEMINI_API_KEY' not found in Colab secrets. Please add it.")

#Choose Input Method
choice = input("Do you want to (1) Paste text or (2) Upload file? Enter 1 or 2: ")

# Use Python 3.10+ match-case (switch alternative)
match choice.strip():
    case "1":
        # Copy-paste option
        user_input = input(" Paste the legal document text here:\n")

    case "2":
        # File upload option
        print("Upload your .txt or .pdf file:")
        uploaded = files.upload()
        filename = list(uploaded.keys())[0]

        if filename.endswith(".txt"):
            with open(filename, "r", encoding="utf-8") as f:
                user_input = f.read()

        elif filename.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(filename)
            text_list = [page.extract_text() for page in pdf_reader.pages if page.extract_text()]
            user_input = "\n".join(text_list)
        else:
            raise ValueError("Only .txt and .pdf files are supported!")

    case _:
        raise ValueError("Invalid choice! Please enter 1 or 2.")

#prompt
prompt = f"""
You are an expert legal document simplifier. Your task is to take a section of a legal document
and translate it into clear, simple language that a non-expert can easily understand.

**Important Instructions:**
- Use bullet points to break down key concepts.
- Avoid legal jargon.
- Do not add or remove any terms; only rephrase them.
- Begin your response with "In simple terms, this means:"

Given the following legal text:
---
{user_input}
---

Provide the simplified explanation.
"""
# Run Gemini model
model = genai.GenerativeModel('gemini-1.5-flash-latest')
response = model.generate_content(prompt)
print("Simplified Legal Document:")
display(to_markdown(response.text))
