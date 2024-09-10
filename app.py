from flask import Flask, render_template, jsonify
import json
from livereload import Server
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
            products.append(row)
    return products

products = load_products()
current_index = 0

@app.route('/')
def show_product():
    global current_index
    product = products[current_index]
    return render_template('product.html', product=product)

@app.route('/like', methods=['POST'])
def like_product():
    global current_index
    product = products[current_index]
    try:
        with open('liked_products.json', 'r+', encoding='utf-8') as file:
            liked_products = json.load(file)
            liked_products.append(product)
            file.seek(0)
            json.dump(liked_products, file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        with open('liked_products.json', 'w', encoding='utf-8') as file:
            json.dump([product], file, ensure_ascii=False, indent=4)
    return jsonify(success=True)
def next_product():
    global current_index
    current_index = (current_index + 1) % len(products)
    return show_product()

@app.route('/previous')
def previous_product():
    global current_index
    current_index = (current_index - 1) % len(products)
    return show_product()


if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.serve(port=5000, debug=True)
