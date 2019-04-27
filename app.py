from flask import Flask, render_template, redirect, request, url_for, session, flash
from forms import RegistrationForm, LoginForm, RecipeSearchForm
from flask_pymongo import PyMongo, DESCENDING
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from bson.objectid import ObjectId
import re
import os
import bcrypt


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'recipe_builder'
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.secret_key = os.getenv("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' #the login view of application

mongo = PyMongo(app)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)
    
class User(UserMixin):
    def __init__(self,id):
        self.id = id

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    recipes = mongo.db.recipes.find().sort([('views', DESCENDING)])
    
    if 'username' in session:
        return 'You are logged in as ' + session['username']
    
    return render_template('index.html', recipes=recipes)
    

"""User Login"""    
@app.route('/login', methods=['POST', 'GET'])
def login():
    users = mongo.db.users
    if request.method == 'POST':
        
        login_user = users.find_one({'name' : request.form['username']})

        if login_user:
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
                session['username'] = request.form['username']
                return redirect(url_for('index'))

        return 'Invalid username/password combination'
    else:
       return render_template('login.html')
    
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))

    
"""User Registration Form"""    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form =  RegistrationForm()
    
    if request.method == 'POST':
        users = mongo.db.users
        exsisting_user = users.find_one({'name' : request.form['username']})
        
        if exsisting_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return 'That username already exists!'
        
    return render_template('register.html', form = form)


"""Get all recipes"""
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", recipes=mongo.db.recipes.find())


"""Add recipe form"""  
@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html', 
                            categories=mongo.db.category.find(),
                            allergens=mongo.db.allergen.find(),
                            serves=mongo.db.serves.find(),
                            measurements=mongo.db.measurements.find(),
                            preparation=mongo.db.preparation.find())
                            
 
"""Submit recipe to database"""
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes=mongo.db.recipes
    recipes.insert_one({
        'recipe_name':request.form['recipe_name'],
        'brief_description':request.form['brief_description'],
        'category':request.form['category'],
        'allergen_name':request.form['allergen_name'],
        'prep_time':request.form['prep_time'],
        'cook_time':request.form['cook_time'],
        'amount_serves':request.form['amount_serves'],
        'image_file': request.form['image_file'],
        'ingredients':request.form['ingredients'],
        'method_description':request.form['method_description']
    })
    return redirect(url_for('get_recipes'))


"""Edit recipe form"""
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe=mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    all_categories = mongo.db.category.find()
    all_allergens = mongo.db.allergen.find()
    all_serves = mongo.db.serves.find()
    return render_template('editrecipe.html',
                            recipe=the_recipe,
                            categories=all_categories,
                            allergens=all_allergens,
                            serves=all_serves)
            

"""Submit edited recipe to database"""
@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipe = mongo.db.recipes
    recipe.update({'_id':ObjectId(recipe_id)},
    {
        'recipe_name':request.form.get('recipe_name'),
        'brief_description':request.form.get('brief_description'),
        'category_name':request.form.get('category_name'),
        'allergen_name':request.form.get('allergen_name'),
        'prep_time':request.form.get('prep_time'),
        'cook_time':request.form.get('cook_time'),
        'amount_serves':request.form.get('amount_serves'),
        'image_file': request.form.get('image_file'),
        'ingredients':request.form.get('ingredients'),
        'method_description':request.form.get('method_description')
    })
    return redirect(url_for('get_recipes'))
    

"""Delete recipe from database"""    
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id':ObjectId(recipe_id)})
    return redirect (url_for('get_recipes'))


"""View full recipe"""    
@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    recipe = mongo.db.recipes
    recipe.find_one_and_update(
        {'_id': ObjectId(recipe_id)},
        {'$inc': {'views': 1}}
    )
    recipe_db = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template("viewrecipe.html", recipe=recipe_db)


"""Search Database for Recipes"""
@app.route('/find_recipes')
def find_recipes():
    orig_query = request.args.get('query')
    query = {'$regex': re.compile('.*{}.*'.format(orig_query)), '$options': 'i'}
    recipes = mongo.db.recipes.find({
        '$or': [
            {'title': query},
            {'allergens': query},
            {'ingredients': query},
        ]
    })
    return render_template('search.html', enquiry=orig_query, results=recipes)
    

"""Search Database for Recipes Results"""
@app.route('/results')
def search_recipes():
    results = find_recipes()
    if results:
        for k,v in results.items():
            if k != "_id":
                return redirect(url_for('get_recipes'))
 


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

            