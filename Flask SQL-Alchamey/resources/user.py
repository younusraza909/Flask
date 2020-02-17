import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel

class userRegister(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument("username",type=str,required=True,help="This Field Cannot be Set Empty")
    parser.add_argument("password",type=str,required=True,help="This Field Cannot be Set Empty")

    def post(self):
        data=userRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]) :
            return{"message":"User With This Username Already Exist"}
        else:    
            connection=sqlite3.connect("data.db")
            cursor=connection.cursor()

            query="INSERT INTO users VALUES(NULL,?,?)"
            cursor.execute(query,(data["username"],data["password"]))
            connection.commit()
            connection.close()

            return {"message":"User Has Been Created"},201
