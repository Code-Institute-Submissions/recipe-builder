import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'recipe_builder'
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", recipes=mongo.db.recipes.find())

    
@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html', 
                            categories=mongo.db.category.find(),
                            allergens=mongo.db.allergen.find(),
                            serves=mongo.db.serves.find())
                            
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes=mongo.db.recipes
    recipes.insert_one({
        'recipe_name':request.form['recipe_name'],
        'brief_description':request.form['brief_description'],
        'category':request.form['category_name'],
        'allergen':request.form['allergen_name'],
        'prep-time':request.form['prep_time'],
        'cook_time':request.form['cook_time'],
        'amount_serves':request.form['amount_serves'],
        'image_file': request.form['image_file']
    })
    return redirect(url_for('add_ingredient'))


                            
@app.route('/add_ingredient')
def add_ingredient():
    return render_template('addingredients.html',
                            measurements=mongo.db.measurements.find(),
                            preparation=mongo.db.preparation.find())
                            
@app.route('/insert_ingredient', methods=['POST'])
def insert_ingredient():
    ingredient=mongo.db.ingredients
    ingredient.insert_one({
        'ingredient_name':request.form['ingredient_name'],
        'amount':request.form['amount'],
        'measure_type':request.form['measure_type'],
        'prep_type':request.form['prep_type']
    })
    return redirect(url_for('thank_you'))
    
@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')
                            
@app.route('/add_method')
def add_method():
    return render_template('method.html')            

    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            