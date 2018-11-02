from flask import *
from flask_restful import *

app=Flask(__name__)
api=Api(app)


#POST
class Student(Resource):
    def get(self,name):
        return {'student':name}


api.add_resource(Student,'/student/<string:name>') #http://127.0.0.1/student/Gebb

app.run(port=5000)