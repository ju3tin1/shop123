import pymongo
import os
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Flask, render_template, url_for, flash, redirect, request, abort, session, jsonify, json
from flask_wtf import FlaskForm
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from forms import RegistrationForm, LoginForm
import bcrypt

MONGO_URI = os.getenv("MONGO_URI")
DBS_NAME = "books"
COLLECTION_NAME = "books"

"""
 This is to make a CSV file.
"""
try:
    f=open("csv.csv", "x")
except:
    print("already there")
    f=open("csv.csv", "w")

def mongo_connect(url):
    try:
        conn = pymongo.MongoClient("mongodb+srv://12345:dude123@cluster0.x5l6q.mongodb.net")
        print("Mongo is connected!")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e


conn = mongo_connect(MONGO_URI)

coll = conn[DBS_NAME][COLLECTION_NAME]

todos = conn[DBS_NAME][COLLECTION_NAME]

documents = coll.find()

for doc in documents:
	#print(doc)
	print(doc, file=f)
	
	


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    username = TextField('Userame:', validators=[validators.required()])
    surname = TextField('Surname:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])

    @app.route("/listings", methods=['GET', 'POST'])
    def listings():
	
        
    
        return render_template('listings.html')
    @app.route("/post/<int:bookID>")
    def post(bookID):
        post = conn[DBS_NAME][COLLECTION_NAME].query.get_or_404(bookID)
        return render_template('post.html', title=post.title, post=post)
	
    @app.route("/register", methods=['GET', 'POST'])
    def register():
        form = ReusableForm(request.form)
    
        print (form.errors)
        if request.method == 'POST':
            users = conn[DBS_NAME].users
            excisting_user = users.find_one({'email' : request.form['email']})
            name=request.form['name']
            surname=request.form['surname']
            username=request.form['username']
            password=request.form['password']
            email=request.form['email']
            print (name, " ", surname, " ", email, " ", password)

            if excisting_user is None:
                
                users.insert({'firstname' : name, 'surname' : surname,'email' : email, 'username' : username, 'password' : password})
                
                
    
        if form.validate():
        # Save the comment here.
            flash('Thanks for registration ' + name)
        else:
            flash('Error: All the form fields are required. ')
    
        return render_template('register.html', form=form)
	
	
    @app.route('/login')
    def login():
        return render_template('login.html')

        #return 'Invalid username/password combination'

        return render_template("login.html", form=form)
		
@app.route('/browseone', methods=['GET'])
def browseone():
    number = conn[DBS_NAME][COLLECTION_NAME]

    #offset = int(request.args['offset'])
    #limit = int(request.args['limit'])
    query = {}
    #query["authors"] = {u"$exists": True}
    query["authors"] = {u"$exists": True}
    query["average_rating"] = {u"$exists": True}
    query["isbn"] = {u"$exists": True}

    numbers = coll.find(query).sort('bookID', pymongo.DESCENDING)
    #numbers = coll.find({'bookID' : {'$lte' : last_id}}).sort('bookID', pymongo.DESCENDING).limit(limit)
    output =[]

   

    
    for i in numbers:
        #output.append({'title' : i['_id'] })
        output.append({'title': i['title'], 'author': i['authors'], 'bookID': i['bookID'], 'average_rating': i['average_rating'], 'isbn': i['isbn'], 'language_code': i['language_code'], 'publication_date': i['publication_date'], 'publisher': i['publisher']})
    
        #next_url = '/browseone?=limit' + str(limit) + '&offset=' + str(offset + limit)
       # prev_url = '/browseone?=limit' + str(limit) + '&offset=' + str(offset - limit)
    
    #return jsonify({'result' : output, 'prev_url' : 'prev_url', 'next_url' : 'next_url'})
    #return jsonify(output)
    your_json = '["foo", {"bar":["baz", null, 1.0, 2]}]'
    return render_template("listings.html", numbers=numbers)
		
@app.route('/book_club')
def book_club():
	return render_template('book_club.html')
    
    



def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/list")
def lists ():
	#Display the all Tasks
	todos_l = todos.find()
	a1="active"
	title="dude"
	heading="dude"
	return render_template('base1.html',a1=a1,todos=todos_l,t=title,h=heading)

@app.route("/")
def index ():
    todos_1 = todos.find('bookID')
    return render_template('index.html',todos='todos_l')

@app.route("/uncompleted")
def tasks ():
    title = 'index'
    heading = 'index'
    todos_l = todos.find({"done":"no"})
    a2="active"
    return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading)


@app.route("/completed")
def completed ():
	#Display the Completed Tasks
	todos_l = todos.find({"done":"yes"})
	a3="active"
	return render_template('index.html',a3=a3,todos=todos_l,t=title,h=heading)

@app.route("/done")
def done ():
	#Done-or-not ICON
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	if(task[0]["done"]=="yes"):
		todos.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
	else:
		todos.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
	redir=redirect_url()	

	return redirect(redir)

@app.route("/action", methods=['POST'])
def action ():
	#Adding a Task
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	todos.insert({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
	return redirect("/list")

@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	todos.remove({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Task with various references
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	id=request.values.get("_id")
	todos.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date, "pr":pr }})
	return redirect("/")

@app.route("/search", methods=['GET'])
def search():
	#Searching a Task with various references
	title="Search"
	heading="Search"
	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		todos_l = todos.find({refer:ObjectId(key)})
	else:
		todos_l = todos.find({refer:key})
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

@app.route("/listings1")
def listings1():
	#Searching a Task with various references
	title="Search"
	heading="Search"
	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		todos_2 = todos.find({refer:ObjectId(key)})
	else:
		todos_2 = todos.find({refer:key})
	return render_template('searchlist.html',todos=todos_2,t=title,h=heading)

@app.errorhandler(404)
def page_not_found(error):
	title="error"
	return render_template('404.html', error_code='404',t=title), 404

@app.errorhandler(500)
def special_exception_handler(error):
	title="error 505"
	return render_template('500.html', error_code='500', t=title), 500
    

if __name__ == "__main__":
    app.run()