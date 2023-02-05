from flask import Flask, request
from flask_restx import Resource, Namespace
from database.database import Database

user = Namespace('user')

@user.route('')
class UserManagement(Resource):
    def get(self):
        # 유저 데이터 조회
        id = request.args.get("id")
        pw = request.args.get("password")

        db = Database()
        sql = "SELECT * FROM user where id = %s"
        result = db.execute_one(sql, (id))

        db.commit()
        db.close()

        if (result == None):
            return { "message": "해당 유저가 존재하지 않음" }, 400
        elif (result['password'] != pw):
            return { "message": "아이디나 비밀번호 불일치" }, 400
        else:
            return { "nickname": result['nickname'] }, 200


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
        # 닉네임 변경
        id = request.get_json()["id"]
        pw = request.get_json()["password"]
        nn = request.get_json()["nickname"]

        db = Database()
        sql = "SELECT * FROM user where id = %s"
        result = db.execute_one(sql, (id))

        if (result == None or result['password'] != pw):
            db.commit()
            db.close()
            return { "is_success": False, "message": "아이디나 비밀번호 불일치" }, 400
        elif (result['nickname'] == nn):
            db.commit()
            db.close()
            return { "is_success": False, "message": "현재 닉네임과 같음" }, 400
        else:
            sql = "UPDATE user SET nickname=%s WHERE id = %s"
            db.execute(sql, (nn, id))
            db.commit()
            db.close()
            return { "is_success": True, "message": "유저 닉네임 변경 성공" }, 200
    

    def delete(self):
        # 유저 삭제
        id = request.get_json()["id"]
        pw = request.get_json()["password"]

        db = Database()
        sql = "SELECT * FROM user where id = %s"
        result = db.execute_one(sql, (id))

        if (result == None or result['password'] != pw):
            db.commit()
            db.close()
            return { "is_success": False, "message": "아이디나 비밀번호 불일치" }, 400
        else:
            sql = "DELETE FROM user WHERE id = %s"
            db.execute(sql, (id))
            db.commit()
            db.close()
            return { "is_success": True, "message": "유저 삭제 성공" }, 200