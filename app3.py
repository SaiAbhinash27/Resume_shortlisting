from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import system_prompt
import os
import smtplib
from email.message import EmailMessage
import ssl
import smtplib
load_dotenv()
gmail_password = os.getenv('gmail_password')

class RESUME_SHORTLISTER:
    def __init__(self,path,model):
        self.path = path
        self.model = model
        if  self.model == 'groq':
            groq_api_key = os.getenv('GROQ_API_KEY')            
            self.llm = ChatGroq(groq_api_key=groq_api_key,model_name= 'Gemma2-9b-It')

        elif self.model == 'openai':
            os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
            self.llm = ChatOpenAI(model="gpt-3.5-turbo")
        else: 
            print("model you specified is not available")
        self.prompt = system_prompt.systemPrompt
        self.output_parser = StrOutputParser()
    def text_extractor(self):
        pdf_loader = PyPDFLoader(file_path=self.path)
        text = pdf_loader.load()
        complete_text_content = ''
        for page in text:
            complete_text_content = complete_text_content+page.page_content
        return complete_text_content
    
    def chatbot(self):
        chain = self.prompt|self.llm|self.output_parser
        output = chain.invoke({'resume_content':self.text_extractor()})
        return output
    def mail_sender(self):
        try:
            email_id = 'msaiabhinash@gmail.com'
            email_password = os.getenv('gmail_password')
            subject = 'shortlisted message'
            body = self.chatbot()
            em = EmailMessage()
            em['From'] = email_id
            em['To'] = email_id
            em['Subject'] = subject
            em.set_content(body)
            context  = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(email_id,email_password)
                smtp.sendmail(email_id,email_id,em.as_string())
        except Exception as e:
            print("error sendinf email:", e)


   


