#POST:We are receving Some Data
#GET:We Have To Send Some Data Back
#In Browser Perspective its opposite

from flask import Flask

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


@app.route("/store",method=["POST"])
def create_store():
    pass

@app.route("/store/<string:name>")
def get_store():
    pass

@app.route("/store")
def get_stores():
    pass

@app.route("/store/<string:name>/item",method=["POST"])
def create_item_in_store():
    pass

@app.route("/store/<string:name>/item")
def get_items_in_store():
    pass


app.run()