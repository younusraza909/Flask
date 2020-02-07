from flask import Flask,render_template,request,redirect,url_for

app=Flask(__name__)
blog={
    "name":"My First Blog",
    "posts":{}
}



@app.route("/")
def home():
    return render_template("home.html",blog=blog)

@app.route("/post<int:post_id>")
def post(post_id):
    post=blog["posts"].get(post_id)
    if not post:
        return render_template("404NotFound.html",message=f"The post having Id {post_id} Was Not found")
    return render_template("post.html",post=post)

@app.route("/post/create",methods=["GET","POST"])
def create():
    if request.method=="POST":
        title=request.form.get("title")
        content=request.form.get("content")
        post_id=len(blog["posts"])
        blog["posts"][post_id]={"post_id":post_id,"title":title,"content":content}
        return redirect(url_for("post",post_id=post_id))
    return render_template("create.html")
app.run()    