import peeweedbevolve
from flask import Flask, render_template, request, url_for, redirect, flash
from models import db, Store, Warehouse
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


@app.cli.command()
def migrate():
    db.evolve(ignore_tables={'base_model'})


@app.route("/", methods=['GET'])
def index():
    stores = Store.select().order_by(Store.id)
    warehouses = Warehouse.get()
    return render_template('index.html', stores=stores, warehouses=warehouses)


@app.route("/store", methods=['GET'])
def store():
    return render_template('store.html')


@app.route("/store", methods=['POST'])
def create_store():
    s = Store(
        name=request.form.get('store_name')
    )
    if s.save():
        flash("successfully save")
        return redirect(url_for('create_store'))
    else:
        return render_template('store.html',  name=request.form.get('store_name'))


@app.route("/stores/<username>", methods=['GET'])
def stores():
    stores = Store.select().order_by(Store.id)
    warehouses = Warehouse.get()
    return render_template('stores.html', stores=stores, warehouses=warehouses)


@app.route("/warehouse", methods=['GET'])
def warehouse():
    stores = Store.select()

    return render_template('warehouse.html', stores=stores)


@app.route("/warehouse", methods=['POST'])
def create_warehouse():
    store = request.form['store_id']
    w = Warehouse(location=request.form['warehouse_location'], store=store)
    if w.save():
        flash("successfully save")
        return redirect(url_for('warehouse'))
    else:
        return render_template('warehouse.html',  name=request.form.get('store_location'))


if __name__ == '__main__':
    app.run()
