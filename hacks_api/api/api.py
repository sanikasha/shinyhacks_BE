from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse
from .. import db
from ..model.model import Student

student_bp = Blueprint("students", __name__)
student_api = Api(student_bp)

def get_name_list():
    names_list = [[name._name] for name in Student.query.all()]
    return names_list

def find_by_name(name):
    names = Student.query.filter_by(_name=name).all()
    return names[0]


class StudentAPI(Resource):
    def get(self):
        name = request.get_json().get("name")
        print(name, "name")
        name = find_by_name(name)
        if name:
            return name.to_dict()
        return {"message": name}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, type=str)
        parser.add_argument("GPA", required=True, type=int)
        parser.add_argument("grade", required=True, type=int)
        args = parser.parse_args()

        student = Student(args["name"], args["GPA"],
                                  args["grade"])
        try:
            db.session.add(student)
            db.session.commit()
            return student.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def put(self):
        name = request.get_json().get("name")
        print(name, "name")

        try:
            name = find_by_name(name)
            if name:
                name.GPA = int(request.get_json().get("GPA"))
                name.grade = int(request.get_json().get("grade"))
                db.session.commit()
                return name.to_dict(), 201
            else:
                return {"message": "student not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def delete(self):
        name = request.get_json().get("name")
        print(name, "name")

        try:
            name = find_by_name(name)
            if name:
                db.session.delete(name)
                db.session.commit()
                return name.to_dict()
            else:
                return {"message": "studnet not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500


class StudentListAPI(Resource):
    def get(self):
        try:
            students = db.session.query(Student).all()
            return [student.to_dict() for student in students]
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def delete(self):
        try:
            db.session.query(Student).delete()
            db.session.commit()
            return []
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500
        


student_api.add_resource(StudentAPI, "/student")
student_api.add_resource(StudentListAPI, "/studentList")

