from flask import Flask, render_template
import csv

app = Flask(__name__)

# Load products from CSV
def load_products():
    products = []
    with open('sample_products.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            products.append(row)
    return products

products = load_products()
current_index = 0

@app.route('/')
def show_product():
    global current_index
    product = products[current_index]
    return render_template('product.html', product=product)

@app.route('/next')
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
    app.run(debug=True)
