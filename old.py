import streamlit as st
import google.generativeai as genai



def resume_score(para,role,generation_config):
            if st.button('Get resume score '):
                st.text(f"Assessing for role: {role}")
                
                
                question = f"What rate this resume out of 10 for this {role} role"
                
            
                llm = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    generation_config=generation_config,
                    system_instruction=f"Answer this question - {question} from this paragraph: {para}",
                )
                res = llm.generate_content(question)
                st.subheader(res.text)
                st.session_state.resume_scored = True
                return res.text
              
              
              
def chat(para,doc_code,generation_config):
  if st.session_state.get('chat',False):
        with st.sidebar:
            messages=st.container(height=300)
            if prompt := st.chat_input("Say something"):
                messages.chat_message("user").write(prompt)
                llm = genai.GenerativeModel(
                        model_name="gemini-1.5-flash",
                        generation_config=generation_config,
                        system_instruction=f"Find the answer to this question: {prompt} from this is the old resume: {para} and this is the new resume :{doc_code}",
                    )
                ans=llm.generate_content(prompt)
                messages.chat_message("assistant").write(f"Echo: {ans.text}")  
                
                
                
                
                              
            
# def resume_maker(para,response1):
#           if st.button('Make resume better'):
#               document=0
              
#               question = "Provide Python code to create a Word document without explanation to improve the resume."
              
#               llm = genai.GenerativeModel(
#                   model_name="gemini-1.5-flash",
#                   generation_config=generation_config,
#                   system_instruction=f"Find the answer to this question: {question} from this resume: {para} based on this context:{response1}",
#               )
#               response2 = llm.generate_content(question)
              
              
#               doc_code = response2.text.replace("```python", "").replace("```", "")
#               doc_code=doc_code.split('document.save')
#               st.text(doc_code)
#               exec(doc_code[0])
#               if 'document' in locals():  
#                   buffer = BytesIO()
#                   document.save(buffer)
#                   buffer.seek(0)
                  
                  
#                   st.download_button(
#                       label="Download Resume as DOCX",
#                       data=buffer,
#                       file_name="resume.docx",
#                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#                   )
#                   st.text("This resume has been improved")
#                   st.session_state.resume_updated=True
#                   question = "Now rate this updated resume out of 10 for the same role and return only the score"
#                   st.header("score of this new updated resume for the same role is:")  
#                   res = llm.generate_content(question)
#                   st.subheader(res.text)
                  
#                   st.session_state.chat=True
#                   return doc_code[0]
                     
                       
#               else:
#                   st.error("The document was not created. Check the generated code for issues.")            
 
            
 


    

            
                    

        
        
    
  
