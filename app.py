from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_recipe_secret_key' # Change this to a strong, random key

# In-memory list to store recipes. In a real app, this would be a database.
recipes = [
    {
        "id": 1,
        "title": "Classic Margherita Pizza",
        "category": "Italian",
        "ingredients": [
            "1 pre-made pizza dough", "1/2 cup tomato sauce", "1 cup mozzarella cheese",
            "Fresh basil leaves", "2 tbsp olive oil", "Salt and pepper to taste"
        ],
        "instructions": (
            "Preheat oven to 450°F (230°C). Roll out dough on a baking sheet. "
            "Spread tomato sauce, then sprinkle mozzarella. "
            "Bake for 10-15 minutes until crust is golden and cheese is bubbly. "
            "Garnish with fresh basil and a drizzle of olive oil. Season to taste."
        ),
        "image": "margherita_pizza.jpg", # Placeholder image
        "date_added": "2024-07-01"
    },
    {
        "id": 2,
        "title": "Vegetable Stir-Fry",
        "category": "Asian",
        "ingredients": [
            "2 cups mixed vegetables (broccoli, carrots, bell peppers)",
            "1 tbsp soy sauce", "1 tsp ginger (grated)", "1 clove garlic (minced)",
            "1 tbsp sesame oil", "Cooked rice for serving"
        ],
        "instructions": (
            "Heat sesame oil in a large skillet or wok over medium-high heat. "
            "Add garlic and ginger, stir-fry for 30 seconds. "
            "Add vegetables and stir-fry for 5-7 minutes until tender-crisp. "
            "Stir in soy sauce. Serve immediately with cooked rice."
        ),
        "image": "vegetable_stirfry.jpg", # Placeholder image
        "date_added": "2024-07-05"
    },
    {
        "id": 3,
        "title": "Spicy Chicken Tacos",
        "category": "Mexican",
        "ingredients": [
            "1 lb chicken breast (sliced)", "1 packet taco seasoning",
            "1/2 cup water", "8 small tortillas", "Toppings: lettuce, cheese, salsa"
        ],
        "instructions": (
            "Cook chicken in a skillet over medium heat until no longer pink. "
            "Drain fat. Stir in taco seasoning and water. Bring to a boil; reduce heat "
            "and simmer for 5 minutes, stirring occasionally. "
            "Warm tortillas. Serve chicken in tortillas with desired toppings."
        ),
        "image": "chicken_tacos.jpg", # Placeholder image
        "date_added": "2024-07-10"
    }
]

# Get unique categories for filtering
def get_categories():
    return sorted(list(set(r['category'] for r in recipes)))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recipes')
def recipe_list():
    category_filter = request.args.get('category')
    
    if category_filter and category_filter != 'All':
        filtered_recipes = [r for r in recipes if r['category'] == category_filter]
    else:
        filtered_recipes = recipes
        
    return render_template('recipe_list.html', 
                           recipes=filtered_recipes, 
                           categories=get_categories(),
                           selected_category=category_filter)

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = next((r for r in recipes if r['id'] == recipe_id), None)
    if recipe:
        return render_template('recipe_detail.html', recipe=recipe)
    flash('Recipe not found!', 'danger')
    return redirect(url_for('recipe_list'))

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        ingredients_raw = request.form['ingredients']
        instructions = request.form['instructions']
        image = request.form.get('image', None) # Optional image filename

        if not title or not category or not ingredients_raw or not instructions:
            flash('All fields (except image) are required!', 'danger')
            return render_template('add_recipe.html', categories=get_categories(),
                                   title=title, category=category, ingredients_raw=ingredients_raw,
                                   instructions=instructions, image=image)

        # Split ingredients by new line and clean up
        ingredients = [item.strip() for item in ingredients_raw.split('\n') if item.strip()]

        new_id = max([r['id'] for r in recipes]) + 1 if recipes else 1
        
        new_recipe = {
            "id": new_id,
            "title": title,
            "category": category,
            "ingredients": ingredients,
            "instructions": instructions,
            "image": image if image else None, # Use provided image or None
            "date_added": datetime.now().strftime("%Y-%m-%d")
        }
        recipes.append(new_recipe)
        flash('Recipe added successfully!', 'success')
        return redirect(url_for('recipe_detail', recipe_id=new_id))
    
    return render_template('add_recipe.html', categories=get_categories())

if __name__ == '__main__':
    app.run(debug=True, port=5006)