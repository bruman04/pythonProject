from flask import Blueprint, render_template
import shelve

bookings = Blueprint("bookings", __name__)

@bookings.route("/<int:id>", methods=["GET"])
def index(id):

    items_dict = {}
    db = shelve.open('items.db', 'c')

    # handle errors

    try:
        items_dict = db['Items']
    except:
        print("Error in retrieving items")

    item = items_dict[id]

    return render_template("book_item.html", item=item)

@bookings.route("/<int:id>/date", methods=["GET"])
def date(id):

    items_dict = {}
    db = shelve.open('items.db', 'c')

    # handle errors

    try:
        items_dict = db['Items']
    except:
        print("Error in retrieving items")

    item = items_dict[id]

    return render_template("book_item_date.html", item=item)