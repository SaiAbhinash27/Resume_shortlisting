from flask import Flask,request
from flask_restx import Api,Resource,reqparse,Namespace
from werkzeug.datastructures import FileStorage
import os
import app3

app = Flask(__name__)
api = Api(app,title="My Api",description="Building an api to shortlist the resume")


namespace_1 = Namespace('resume',description='shortlisting the resumes')
upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file',type=FileStorage,location='files',required = True)
upload_parser.add_argument('model', type=str, required=True, choices=("groq", "ollama",'openai','gemini'), location='form')


@namespace_1.route('/')
class resume_shoertlist(Resource):
    @namespace_1.expect(upload_parser)
    def post(self):
        file_dict = request.files.to_dict() # converting uploaded data to dictionary format
        file  = file_dict['file'] #geting the file out from the dictionary
        model= request.form.get('model') # geting the model name
        file_name = file.filename # getting filename
        file_extension = accepted_file(file_name) #finding the type of file uploaded with help of accepted_file function which splits the file name and extension and return in tuple format
        path = os.getcwd()
        if file_extension[1]=='.pdf':
            folder_path = path+'/uploadedfile' # created path to folder
        else:
            return 'file you uploaded in not correct'
        os.makedirs(folder_path,exist_ok=True) # creating folder as per path entioned in folder_path
        file.save(os.path.join(folder_path,file_name))
        file_path = (os.path.join(folder_path,file_name)).replace('\\','\\\\')
        r_s = app3.RESUME_SHORTLISTER(file_path,model) # creating the instance
        result = r_s.chatbot() # calling the chatbot method from the app3 which retuen the analysed data from the resume
        r_s.mail_sender() # sending mail by using mail_sender method
        return {'Candidate Info': result,
                'File_name': file_name}






def accepted_file(name):
    n = os.path.splitext(name)
    return n
api.add_namespace(namespace_1,path='/resume')

if __name__=='__main__':
    app.run(debug=True)