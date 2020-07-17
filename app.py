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
    title = TextField('tile:', validators=[validators.required()])
    author = TextField('author:', validators=[validators.required()])
    isbn = TextField('isbn:', validators=[validators.required()])
    read_time = TextField('read_time:', validators=[validators.required()])
    category = TextField('category:', validators=[validators.required()])
    rating = TextField('rating:', validators=[validators.required()])
    comment = TextField('comment:', validators=[validators.required()])
    url = TextField('url:', validators=[validators.required()])
    purchase = TextField('purchase:', validators=[validators.required()])
    
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
    
        return render_template('register1.html', form=form)
	
	
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = ReusableForm(request.form)
        print (form.errors)
        if request.method == 'POST':
            users = conn[DBS_NAME].users
            username=request.form['username']
            password=request.form['password']
            print (username, " ", password)
            login_user = users.find_one({'username' : username})
          #  login_user = users.find_one({'username' : request.form['username']})


            if login_user:
                if (password) == login_user['password']:
                    session['username'] = request.form['username']
                    session.permanent = True
                    user = request.form["username"]
                    session["user"] = user
                    return redirect(url_for('index'))
                    #return 'Invalid username/password combination'

        #return 'Invalid username/password combination'

        return render_template("login.html", form=form)
    
@app.route('/login1', methods = ['GET', 'POST'])
def login1():
    error = None
   
    if request.method == 'POST':
      if request.form['username'] != 'admin' or \
         request.form['password'] != 'admin':
         error = 'Invalid username or password. Please try again!'
      else:
         flash('You were successfully logged in')
         session['username'] = request.form['username']
         session.permanent = True
         user = request.form["username"]
         session["user"] = user
         return redirect(url_for('index'))
         
         #url = 'https://5000-a3185470-da53-4b4e-aaef-10153e2c0ffd.ws-eu01.gitpod.io/'
         #return request.base_url
         #return redirect(url, code=307)
			
    return render_template('login1.html', error = error)
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   todos_l = todos.find()
   session.pop('username', None)
   return redirect(url_for('index'))
		
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

@app.route('/additem')
def additem():
    return render_template('book_club2.html')


@app.route('/add_item', methods=['GET','POST'])
def additem1():
    form = ReusableForm(request.form)
    if request.method == 'POST':
        books = conn[DBS_NAME].books
        title=request.form['title']
        author=request.form['author']
        isbn=request.form['isbn']
        url=request.form['url']
        purchase=request.form['purchase']
        read_time=request.form['read_time']
        comment=request.form['comment']
        purchase=request.form['purchase']
        category=request.form['category']
        rating=request.form['rating']
        books.insert({'title' : title, 'author' : author, 'isbn' : isbn, 'url' : url, 'read_time' : read_time, 'rating' : rating, 'purchase' : purchase, 'comment' : comment, 'category' : category})
        return render_template('book_club3.html')
    else:
        return render_template('book_club3.html')

                       


@app.route('/list')
def lista():
    return render_template('book_club4.html')

@app.route('/browse')
def browse():
    return render_template('book_club5.html')
    
    



def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')
#check for issuses
@app.route("/index")
def index1():
    title = 'index'
    heading = 'index'
    todos_l = todos.find({"done":"no"})
    a2="active"
    return render_template('base1.html',a2=a2,todos=todos_l,t=title,h=heading)


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
    todos_l = todos.find()
    return render_template('base1.html',todos=todos_l)

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