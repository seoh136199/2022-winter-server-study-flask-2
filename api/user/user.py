from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database

user = Namespace('user')

@user.route('')
class UserManagement(Resource):
    def get(self):
        # GET method 구현 부분
        return {}

    def post(self):
        # 유저 생성
        id = request.get_json()["id"]
        pw = request.get_json()["password"]
        nn = request.get_json()["nickname"]

        db = Database()
        sql = "SELECT * FROM user where id = %s"
        result = db.execute_one(sql, (id))

        if (result == None):
            sql = "INSERT INTO user (id, password, nickname) VALUES (%s, %s, %s)"
            db.execute(sql, (id, pw, nn))
            db.commit()
            db.close()
            return { "is_success": True, "message": "유저 생성 성공" }, 200
        else:
            db.commit()
            db.close()
            return { "is_success": False, "message": "이미 있는 유저" }, 400


    def put(self):
        # PUT method 구현 부분
        return {}
    
    def delete(self):
        # DELETE method 구현 부분
        return {}