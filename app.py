from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
import os


# Inisiasi object

app = Flask(__name__)
api = Api(app)
CORS(app)


db = SQLAlchemy(app)

# konfig db

basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database

# mebuat database model


class ModelDatabase(db.Model):
    #    membuat field /colom
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    umur = db.Column(db.Integer)
    alamat = db.Column(db.TEXT)  # fiel tambahan

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False


db.create_all()

# inisiasi variabelkosong bertipe dictionari

identitas = {}  # variable global


# membuat class resource
class ContohResource(Resource):
    def get(self):
        # meanampilkan data dari database sqlite
        query = ModelDatabase.query.all()

        # iterasi pada model modelDatabase teknik listComprehensive
        output = [
            {
             "id" : data.id,
             "nama": data.nama, 
             "umur": data.umur,
             "alamat": data.alamat
            } 
            for data in query
        ]

        response = {
            "code" : 200,
            "msg" : "Query data sukses",
            "data" : output
        }
        return response

    def post(self):
        dataNama = request.form["nama"]
        dataUmur = request.form["umur"]
        dataAlamat = request.form["alamat"]
        db.session.commit()

        model = ModelDatabase(nama=dataNama, umur=dataUmur, alamat=dataAlamat)

        model.save()

        response = {
            "msg": "Data Berhasil dimasukan",
            "code": 200
        }
        
        return response
    
    def delete(self):
        query = ModelDatabase.query.all()
        # looping
        for data in query:
            db.session.delete(data)
            db.session.commit()

        response = {
            "msg" : "Semua data berhasil di hapus",
            "code" : 200
        }

        return response    


# membuat class baru untuk mengedit / menghapus data

class UpdateResource(Resource):
    # update by id
    def put(self, id):
        # konsums id itu untuk query di odel databasenya
        query = ModelDatabase.query.get(id)

        # form data edit 
        editNama = request.form["nama"]
        editUmur = request.form["umur"]
        editAlamat = request.form["alamat"]

        # set / replace data pada setiap field column
        query.nama = editNama
        query.umur = editUmur
        query.alamat = editAlamat
        db.session.commit()

        response = {
            "msg" : "edit data berhasil",
            "code" : 200
        }

        return response
    # delete by id
    def delete(self, id):
        # konsums id itu untuk query di odel databasenya
        query = ModelDatabase.query.get(id)

        # panggil method untuk delete data by id

        db.session.delete(query)
        db.session.commit()

        response = {
            "msg" : "data berhasil dihapus",
            "code" : 200
        }

        return response


api.add_resource(ContohResource, "/api", methods=["GET", "POST", "DELETE"])
api.add_resource(UpdateResource, "/api/<id>", methods=["PUT", "DELETE"])

if __name__ == '__main__':
    app.run(debug=True, port=5005)
