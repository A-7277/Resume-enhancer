import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from docx import Document
from langchain.document_loaders import PyPDFLoader
from io import BytesIO
# from exceptions import PendingDeprecationWarning
from old import resume_score,chat

load_dotenv()
genai.configure(api_key=os.getenv('api_key'))

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
    
}


st.subheader('Upload your resume here! format(.pdf,.docx,doc)')
doc=st.file_uploader('Upload here!',type=['pdf','docx'])


document=0

if doc:
    with open('temp.pdf', 'wb') as f:
        f.write(doc.read())
    
    
    loader = PyPDFLoader('./temp.pdf') 
    data = loader.load()
    
    
    if len(data[0].page_content) > 2900:
        st.text('Tokens greater than 3000')
    else:
        para = data 

   
    role = st.text_input("For which role do you want to know your resume score?")
    
   
    if len(role) > 0:
       
        res=resume_score(para,role,generation_config)
        
        doc_code=''    
        if st.session_state.get('resume_scored', False):
          if st.button('Make resume better'):
              question = "Provide Python code to create a Word document without explanation to improve the resume."
              
              llm = genai.GenerativeModel(
                  model_name="gemini-1.5-flash",
                  generation_config=generation_config,
                  system_instruction=f"Find the answer to this question: {question} from this resume: {para} based on this context:{res}",
              )
              res = llm.generate_content(question)
              
              
              doc_code = res.text.replace("```python", "").replace("```", "").strip()
              doc_code=doc_code.split('document.save')[0]
              exec(doc_code)
              
            
              if 'document' in locals():  
                  buffer = BytesIO()
                  document.save(buffer)
                  buffer.seek(0)
                  
                  
                  st.download_button(
                      label="Download Resume as DOCX",
                      data=buffer,
                      file_name="resume.docx",
                      mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                  )
                  st.text("This resume has been improved")
                  st.session_state.resume_updated=True
                  question = "Now rate this updated resume out of 10 for the same role and return only the score"
                  st.header("score of this new updated resume for the same role is:")  
                  res = llm.generate_content(question)
                  st.subheader(res.text)
                #   st.subheader("##Please do check the resume")
                  
                  st.session_state.chat=True
 
                       
              else:
                  st.error("The document was not created. Check the generated code for issues.")
              
        if st.session_state.get('chat',False):
            chat(para,doc_code,generation_config)
            
                               
        
    

            
                    

        
        
    
  
