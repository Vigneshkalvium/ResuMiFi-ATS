import streamlit as st
import google.generativeai as genai
import os
import PyPDF2

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        # Check if the reader has pages
        if not reader.pages:
            raise ValueError("The PDF file is empty or unreadable.")
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() if page.extract_text() else ""
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""
input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"xx%","MissingKeywords":["keyword1", "keyword2", "keyword3"],"Profile Summary":"A brief, impactful summary of the candidate's profile highlighting relevant skills and achievements."}}

"""

## streamlit app
st.title("ResuMiFi ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Job Description:")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt) 
        st.subheader(response)
