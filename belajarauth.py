# import librar flask dan lainnya

from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api

# import py jwt
import jwt
import datetime

# import libarary ntuk membuat decorator
from functools import wraps

# inisialisasi objek flask dkk

app = Flask(__name__)  # flask
api = Api(app)  # restfull

app.config['SECRET_KEY'] = 'inirahasianegara'

# decorator untuk kunci endpoint / authentikasi


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        # token akan diparsing melalui parameter di end point
        token = request.args.get('token')

        if not token:
            return make_response(jsonify({"msg": "token tidak ada"}), 404)

        # decode token yang diterima
        try:
            output = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return make_response(jsonify({"msg": "Token is invalid"}))
        return f(*args, **kwargs)
    return decorator

# membuat endpoint untuk login


class LoginUser(Resource):
    def post(self):
        # butuh multipart form untuk transmisi data
        username = request.form.get('username')
        password = request.form.get('password')

        # kondisi pengecekan password
        if username and password == 'admin':
            # hasil nomor token
            token = jwt.encode(
                {
                    "username": username,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
                }, app.config['SECRET_KEY'], algorithm="HS256"
            )

            return jsonify({
                "token": token,
                "msg": "anda berhasil login"
            })

        return jsonify({"msg": "silahkan login"})

# Halaman yang di-protected


class Dashboard(Resource):
    @token_required
    def get(self):
        return jsonify({"msg": "ini adalah halaman dashboard, butuh login untuk akses"})

# halaman yang tidak di protected


class HomePage(Resource):
    def get(self):
        return jsonify({"msg": "Ini adalah halaman umum / public"})


api.add_resource(LoginUser, "/api/login", methods=["POST"])
api.add_resource(Dashboard,"/api/dashboard", methods = ["GET"])
api.add_resource(HomePage,"/api/homepage", methods = ["GET"])

if __name__ == "__main__":
    app.run(debug=True, port=5005)
