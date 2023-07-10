from flask import Flask,request
from flask_restful import Resource, Api
from flask_cors import CORS


#Inisiasi object

app = Flask(__name__)
api = Api(app)
CORS(app)

#inisiasi variabelkosong bertipe dictionari

identitas = {} # variable global



#membuat class resource
class ContohResource(Resource):
    def get(self):
      return identitas
    
    def post(self):
       nama = request.form["nama"]
       umur = request.form["umur"]
       identitas["nama"]= nama
       identitas["umur"] = umur

       response = {"msg" : "Data Berhasil dimasukan"}

       return response
    
api.add_resource(ContohResource, "/api", methods=["GET","POST"])

if __name__ == '__main__':
   app.run(debug=True, port=5005)
    