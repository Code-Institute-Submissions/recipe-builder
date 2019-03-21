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
        'category_name':request.form['category_name'],
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


"""View recipe"""    
@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    recipe = mongo.db.recipes
    recipe.find_one({'_id':ObjectId(recipe_id)})
    return render_template("viewrecipe.html", recipe=mongo.db.recipes.find_one({'_id':ObjectId(recipe_id)}))
                        


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            