from flask import Flask,render_template

app=Flask(__name__)
blog={
    "name":"My First Blog",
    "posts":{
        1:{
            "post_id":1,
            "title":"First Post",
            "content":"First Post Content"
        }
    }
}



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/post<int:post_id>")
def post(post_id):
    post=blog["posts"][post_id]
    return post["title"]

app.run(debug=True)    