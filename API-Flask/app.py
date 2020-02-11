#POST:We are receving Some Data
#GET:We Have To Send Some Data Back
#In Browser Perspective its opposite

from flask import Flask,jsonify,request,render_template
app=Flask(__name__)


stores=[
    {
        "name":"My Wonderful Store",
        "items":[
            {
            "name":"My Item",
            "price":15.99
            }
        ]
    
    }
]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/store",methods=["POST"])
def create_store():
    request_data=request.get_json()
    new_stores={"name":request_data["name"],
                "items":[]}
    stores.append(new_stores)
    return jsonify(new_stores)            

@app.route('/store/<string:name>')
def get_store(name):
    for i in stores:
        if i["name"]==name:
            return jsonify(i)
        else:
            return jsonify({"messgae":"Store Not Found"})

@app.route("/store")
def get_stores():
    return jsonify({"stores":stores})
    

@app.route("/store/<string:name>/item",methods=["POST"])
def create_item_in_store(name):
    request_data=request.get_json()
    for store in stores:
        if store["name"]==name:
            new_item={
                'name':request_data["name"],
                "price":request_data["price"]
            }
            store["items"].append(new_item)
            return jsonify(new_item)
        else:
            return jsonify({"message":"No Store With Given Name Available"})    


@app.route("/store/<string:name>/items")
def get_items_in_store(name):
    for store in stores:
        if store["name"]==name:
            return jsonify({"items":store["items"]})
        return jsonify({"message":"Store Not Found"})    


app.run()