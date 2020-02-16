from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
        parser=reqparse.RequestParser()
        parser.add_argument("price",type=float,help="This Field Cannot Be Blank",required=True) 


        @jwt_required()
        def get(self,name):
            item=self.find_by_name(name)
            if item:
                return item
            return {"message":"Item Not Found"},404

        @classmethod
        def find_by_name(cls,name):
            connection=sqlite3.connect("data.db")
            cursor=connection.cursor()

            query="SELECT * FROM items WHERE name=?"
            result=cursor.execute(query,(name,))
            row=result.fetchone()
            connection.close()

            if row:
                return{"item":{"name":row[0],"price":row[1]}}
                        


        def post(self,name):
            if self.find_by_name(name):
                return {"message":"An item With {} already exist.".format(name)},400

            data=Item.parser.parse_args()
            item={"name":name,"price":data["price"]}
            try:
                self.insert(item)
            except:
                return{"message":"Something Went Wrong While Execution"},500    
           
            return item ,201 #hhtp code for created

        @classmethod
        def insert(cls,item):
            connection=sqlite3.connect("data.db")
            cursor=connection.cursor()
            query="INSERT INTO items VALUES(?,?)"

            cursor.execute(query,(item["name"],item["price"]))
            connection.commit()
            connection.close()   

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

            item=self.find_by_name(name)
            update_item={"name":name,"price":data["price"]}

            if item is None:
                try:
                    self.insert(update_item)
                except:
                    return {"message":"unexpected error in runnnig the request"},500
                 
            else:
                try:
                    self.update(update_item)
                except:
                     return {"message":"unexpected error in runnnig the request"},500

            return update_item      
        @classmethod
        def update(cls,item):
            connection=sqlite3.connect("data.db")
            cursor=connection.cursor()
            query="UPDATE items SET price=? WHERE name=?"
            cursor.execute(query,(item["price"],item["name"]))
            connection.commit()
            connection.close()
            


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
