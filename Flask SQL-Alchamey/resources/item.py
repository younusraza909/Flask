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
                item.insert()
            except:
                return{"message":"Something Went Wrong While Execution"},500    
           
            return item.json() ,201 #hhtp code for created

      

        def delete(self,name):
            connection=sqlite3.connect("data.db")
            cursor=connection.cursor()
            query="DELETE FROM items WHERE name=?"

            cursor.execute(query,(name,))
            connection.commit()
            connection.close()
            return {"message":"item Deleted"}

        def put(self,name):
            data=Item.parser.parse_args()

            item=ItemModel.find_by_name(name)
            update_item=ItemModel(name,data["price"])

            if item is None:
                try:
                   update_item.insert()
                except:
                    return {"message":"unexpected error in runnnig the request"},500
                 
            else:
                try:
                    update_item.update()
                except:
                     return {"message":"unexpected error in runnnig the request"},500

            return update_item      



class ItemList(Resource):
    def get(self):
        connection=sqlite3.connect("data.db")
        cursor=connection.cursor()
        query="SELECT * FROM items"
        result=cursor.execute(query)
        items=[]
        for i in result:
            items.append({"name":i[0],"price":i[1]})
        
        connection.close()  
        return{"items":items}
