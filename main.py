from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
#render generates file from templates folder
#request get data from user
#redirect - to target location
#url_for gets url for function 
#flash - show temp message

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///corgIdeas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "key"
db = SQLAlchemy(app)


class Idea(db.Model):
  id = db.Column(db.Integer,primary_key = True)
  name = db.Column(db.String)
  content = db.Column(db.String)

  def __init__(self, content):
    self.content = content

db.drop_all() 
db.create_all() 

#main page
@app.route("/") 
def Index():
  return render_template("main.html")

#add ideas
@app.route("/insert", methods = ["POST"])
def insert():
  if request.method == "POST": #check sending data
    content = request.form["content"] #idea

    my_idea = Idea(content) #create idea object
    db.session.add(my_idea) #add idea object to database
    db.session.commit()
    flash("Successfully Added!")
    return redirect(url_for("Index")) #back to main

#Results page
@app.route("/result", methods = ["POST"])
def result():
  if request.method == "POST":
    ideas = Idea.query.all()
    return render_template("results.html", ideas=ideas)

if __name__ == "__main__":
  app.run(host="0.0.0.0") #remove debug when publish

