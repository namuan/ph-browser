from flask import Flask, render_template, jsonify, redirect, url_for, abort
import json
import ast
import csv

app = Flask(__name__)

# Load products from CSV
def load_products():
    products = []
    with open('sample_products.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Parse the comments field from the CSV
            row['comments'] = eval(row['comments'])
            # Convert the websites field to a Python list
            row['websites'] = ast.literal_eval(row['websites'])
            products.append(row)
    return products

products = load_products()
current_index = 0

def get_product_by_id(product_id):
    try:
        product_id = int(product_id)
        if 1 <= product_id <= len(products):
            return products[product_id - 1], product_id - 1
    except ValueError:
        pass
    return None, None

@app.route('/')
def show_product():
    global current_index
    product = products[current_index]
    # Format the release date to remove the timestamp
    product['release_date'] = product['release_date'].split(' ')[0]
    # Add the product ID to the context
    product['id'] = current_index + 1
    return render_template('product.html', product=product)

@app.route('/product/<product_id>')
def show_product_by_id(product_id):
    global current_index
    product, index = get_product_by_id(product_id)
    if product:
        current_index = index
        product['release_date'] = product['release_date'].split(' ')[0]
        product['id'] = index + 1
        return render_template('product.html', product=product)
    else:
        abort(404)

@app.route('/like', methods=['POST'])
def like_product():
    global current_index
    product = products[current_index]
    try:
        with open('liked_products.json', 'r+', encoding='utf-8') as file:
            liked_products = json.load(file)
            if product not in liked_products:
                liked_products.append(product)
                file.seek(0)
                json.dump(liked_products, file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        with open('liked_products.json', 'w', encoding='utf-8') as file:
            json.dump([product], file, ensure_ascii=False, indent=4)
    return jsonify(success=True, redirect=url_for('next_product'))

@app.route('/next')
def next_product():
    global current_index
    current_index = (current_index + 1) % len(products)
    return redirect(url_for('show_product_by_id', product_id=current_index + 1))

@app.route('/previous')
def previous_product():
    global current_index
    current_index = (current_index - 1) % len(products)
    return redirect(url_for('show_product_by_id', product_id=current_index + 1))

if __name__ == '__main__':
    app.run(port=5011, debug=True)