

from . import app_views
from app.controller.student import create as student_create
from app.controller.student import get_students
from flask import make_response, jsonify, request

@app_views.route('/')
def status():
    print('calling /')
    return make_response(jsonify({"status": "OK"}), 200)


@app_views.route('/students', methods=["POST"])
def create():
    print('calling post')
    resp = student_create({
        "first_name": "Student",
        "last_name": 'Test',
        "email": "teststudent2@gmail.com",
        "age": 23
    })

    return make_response(jsonify({"response": resp}), 201)


@app_views.route('/students', methods=['GET'])
def get():
    students = get_students()
    return make_response(jsonify({"students": students}), 200)