# Love Food Recipe Builder

## What is it about?

I have developed this project using the skills learnt to build a Flask Website, using MongoDB. The application includes a database of recipes that can be searched and viewed by any user. When a user has registered and logged in to the application the user is able to create, update and delete their own recipes. This project can be viewed at https://love-food-recipe-builder.herokuapp.com

## UX

The project needs to be a web applicaition where users can log into a recipe builder where they can create, store, edit and delete their own recipes. They will have access to other users' recipes stored on the database. The user must be able to search by cuisine, allergens, ingredient or author of the recipe.

## Features

The applicaition is fully responsive. Any user can search and view (read) all of the recipes. The user can register an account which enables them to create, edit (update) and delete their own recipes once they are logged in. The user can log out at the end of their session. 

### Existing Features

On the home page a list of 6 most popular recipes are displayed in descending order by amount of views of each recipe. A list of all of the recipes can also be viewed in another page. 

Each recipe can be clicked on to view the full recipe as a single recipe. If the user submitted this recipe they are able to edit or delete it if they wish. 

### Features Left to Implement

As the database grows the "All Recipes" page could be paginated to create a better user experience. To load thousands of recipes at one time would take too long, therefore if they were paginated with say 12 recipes to a page the loading time would be quicker and be much better for the end user. 

## Technologies Used

Throughout this project I have used

* HTML5
* CSS / Materialise / Fontawesome
* Python
* PyMongo
* Flask
* JavaScript / JQuery
* WTForms

## Testing

I tested the applicaition manually as follows:

1. Home page 
    1. Ensure loads correctly 
    2. recipe cards load as required


2. Recipes page 
    1. Ensure that each recipe card load fully and are all following the same form.

3. Register
    1. Enter a username that already exsists 
    2. Verify an error flashes up and they are asked to choose an alternative username. 
    3. Register an account successfully verify that the username and password is saved in MongoDB. The user's password is encoded.
    4. I did not enter a username and password but the user was still created. Therefore I added a "minlength" and "required" to the input field to fix this. 

4. Login page
    1. Enter a correct username and an incorrect password combination and verify an error message appears. 
    2. Once the user is logged in I verify that they are able to create, edit and delete their own recipes. 
    3. If the user views another user's recipe I verify that the user will not see the edit and delete buttons. 

5. Create Recipe page 
    1. Click on create recipe
    2. Add a test recipe and ensure that this recipe and submit.
    3. I verified that the recipe can be viewed from the Home page, All Recipes page, searched for and the full recipe is loaded. 
    4. I also verified that the test recipe was saved in MongoDB.

6. Search 
    1. Enter any word from any part of a recipe, eg. Title, ingredient, allergen, category, username, eg. Cheesecake 
    2. Verify that the recipe and any other recipe which includes that word is displayed.
    3. I also entered a random string of characters. 

7. Update Recipe page
    1. Log in
    2. Click on view ensuring that it was orginally submitted by that user.
    3. Change some data and resubmitting it.
    4. This then redirects the user to the home page.
    5. I then checked that the updated information was seen in that recipe.
    6. I realised that once a recipe was updated the username was not copied to the database. Therefore I fixed the problem by adding user session to app.py.

8. Delete Recipe page 
    1. Log in
    2. Click on view ensuring that it was orginally submitted by that user.
    3. Click on Delete
    4. This then redirects the user to the Home page. 
    5. I then verified that the deleted recipe does not appear on the list.
    6. I also searched for this recipe to check it had been deleted.

When performing the tests I came across a problem that my search was not returning any results. After seeking advise from Slack and Tutors it was pointed out that I was not pushing and getting the form input therefore it was not connecting with MongoDB. 

9. As the application is fully responsive I checked it works fully for mobiles, ipads, laptops and desktop. I checked on:
* iPhones 5 to X
* iPads, mini to pro
* MacBook Pro
* iMac, 27 inch.

10. I verfied that the application works over different web browsers. I checked on:
* Safari
* Edge
* iOS
* Chrome - I have come across a problem that the time picker does not open unless you right click. It does work over the other web browsers.

11. I verfied my JavaScript on https://jshint.com and amended my code accordingly. I had just missed off a couple of ;

## Deployment

The application was coded on Cloud9. I then committed the code GITHUB at https://github.com/sarahg177/recipe-builder

The application was deployed from GITHUB to Heroku at https://love-food-recipe-builder.herokuapp.com/

My database is stored on MongoDB and is setup within Heroku.

## Credits

For my Login and Registeration functionalities I watched a YouTube video from "Pretty Printed" where I took my code from. 

For the recipes I have loaded onto the database are copied from https://goodfood.uktv.co.uk and https://www.bbcgoodfood.com/recipes