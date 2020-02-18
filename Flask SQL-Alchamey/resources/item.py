from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
import sqlite3
from  models.item import ItemModel

class Item(Resource):
        parser=reqparse.RequestParser()
        parser.add_argument("price",type=float,help="This Field Cannot Be Blank",required=True) 


        @jwt_required()
        def get(self,name):
            item=ItemModel.find_by_name(name)
            if item:
                return item.json()
            return {"message":"Item Not Found"},404

       
        def post(self,name):
            if ItemModel.find_by_name(name):
                return {"message":"An item With {} already exist.".format(name)},400

            data=Item.parser.parse_args()
            item=ItemModel(name,data["price"])
            try:
                item.save_to_db()
            except:
                return{"message":"Something Went Wrong While Execution"},500    
           
            return item.json() ,201 #hhtp code for created

      

        def delete(self,name):
            item=ItemModel.find_by_name(name)
            if item:
                item.delete_from_db()
            return {"message":"Item Was Successfully Deleted"}    

        def put(self,name):
            data=Item.parser.parse_args()

            item=ItemModel.find_by_name(name)
            
            if item is None:
                item=ItemModel(name,data["price"])

            else:
                item.price=data["price"]

            item.save_to_db()    

            return item.json()      



class ItemList(Resource):
    def get(self):
        connection=sqlite3.connect("data.db")
        cursor=connection.cursor()
        query="SELECT * FROM items"
        result=cursor.execute(query)
        items=[]
        for i in result:
            items.append({"name":i[1],"price":i[2]})
        
        connection.close()  
        return{"items":items}
