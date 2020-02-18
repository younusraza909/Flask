from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
import sqlite3
from  models.item import ItemModel

class Item(Resource):
        parser=reqparse.RequestParser()
        parser.add_argument("price",type=float,help="This Field Cannot Be Blank",required=True) 
        parser.add_argument("store_id",type=int,help="Every item needs a store id",required=True) 




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
            item=ItemModel(name,**data)
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
                item=ItemModel(name,**data)

            else:
                item.price=data["price"]

            item.save_to_db()    

            return item.json()      



class ItemList(Resource):
    def get(self):
        return {"items":[item.json for item in ItemModel.query.all()]}
        #return {"items":list(map(lambda x:x.json(),ItemModel.quesry.all()))}
