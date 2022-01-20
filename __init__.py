from flask import Flask, render_template, request, redirect, url_for, flash
from form import CreateItemForm, CreateLoanForm
import os
import shelve

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.datastructures import ImmutableMultiDict

import Item
import Loan
from Review import *
import shelve
from Chat import *

# Ensure WTForms is v2.3.3 (Otherwise it won't work)
try:
    os.system("pip install WTForms==2.3.3")
except:
    print("Error installing WTForms v2.3.3! Skipping.")

from form import CreateItemForm, CreateLoanForm

app = Flask(__name__)


# 404 error page

# @app.errorhandler(404)
# def error404(e):
#     return render_template('error404.html'),404

# main page
@app.route('/')
def listingpage():
    # retrieve items from database

    items_dict = {}
    db = shelve.open('items.db', 'c')

    try:
        items_dict = db['Items']

    except IndexError:
        print("Error in retrieving items")

    db.close()

    items_list = []
    for key in items_dict:
        item = items_dict.get(key)
        items_list.append(item)

    return render_template('listingpage.html', items_list=items_list)


# Done by Ng Rong Kai:

@app.route("/<string:USER>/<string:VENDOR>/<string:PRODUCT>/reviews", methods=["GET", "POST"])
def review(USER: str, VENDOR: str, PRODUCT: str):
    FEEDBACK: Feedback = Feedback(PRODUCT.strip(), VENDOR.strip())
    if request.method == "POST":
        f: ImmutableMultiDict[str, str] = request.form
        try:
            if not FEEDBACK.appendFeedbackReview(USER.strip(), str(f["text"]).strip(), int(f["stars"])):
                raise ValueError("Failed to FEEDBACK.appendFeedbackReview() ! (Missing or Invalid Parameter(s).)")
        except Exception as EE:
            return "Error handling review post:\n" + str(EE), 403
    r: list[Review] = FEEDBACK.getFeedback()
    for i in range(len(r)):
        r[i].index = i
    r.reverse()
    return render_template("review.html", me=USER.strip(), review=r)


# test
# view full specs of item
@app.route('/detailedview/<int:id>')
def detailed_view(id):
    # retrieve info from database

    db = shelve.open('items.db', 'r')
    items_dict = db["Items"]

    # get specific item
    item = items_dict.get(id)

    # close database
    db.close()

    return render_template('detailedview.html')


@app.route('/updateitem/<int:id>/', methods=["GET", "POST"])
def update_item(id):
    # request form to update item

    update_item_form = CreateItemForm(request.form)
    if request.method == 'POST' and update_item_form.validate():
        items_dict = {}
        db = shelve.open('items.db', 'w')
        items_dict = db["Items"]




        item = items_dict.get(id)
        item.set_image(update_item_form.image.data)
        request.files['image'].save(
            os.path.join('static/images', f"{item.get_id()}.png")
        )
        item.set_name(update_item_form.name.data)
        item.set_description(update_item_form.description.data)
        item.set_rate(update_item_form.rate.data)
        item.set_on_loan(update_item_form.on_loan.data)
        item.set_available(update_item_form.available.data)
        item.set_location(update_item_form.location.data)

        db['Items'] = items_dict
        db.close()

        return redirect(url_for('listingpage'))

    # display current information
    else:
        items_dict = {}
        # items_list = []
        db = shelve.open('items.db', 'r')
        items_dict = db['Items']
        item = items_dict.get(id)
        # items_list.append(item)
        update_item_form.image.data = item.get_image()
        print(update_item_form.image.data)
        # request.files['image'].save(
        #     os.path.join('static/images', f"{item.get_id()}.png")
        # )
        update_item_form.name.data = item.get_name()
        update_item_form.description.data = item.get_description()
        update_item_form.rate.data = item.get_rate()
        update_item_form.on_loan.data = item.get_on_loan()
        update_item_form.available.data = item.get_available()
        update_item_form.location.data = item.get_location()

    return render_template('updateitem.html', form=update_item_form)


# delete item
@app.route('/deleteitem/<int:id>/', methods=['POST'])
def delete_item(id):
    # retrieve item from database

    items_dict = {}
    db = shelve.open('items.db', 'w')
    try:
        items_dict = db['Items']

    except IndexError:
        print("Error in retreiving items")

    #delete image from static
    # delete image from static
    os.remove(f'static/images/{id}.png')

    # delete selected item

    items_dict.pop(id)

    # update database

    db['Items'] = items_dict
    db.close()

    return redirect(url_for('listingpage'))


# create new item

@app.route('/createitem', methods=['GET', 'POST'])
def create_item():
    # request for item creation form

    create_item_form = CreateItemForm(request.form)

    if request.method == 'POST' and create_item_form.validate():

        items_dict = {}
        db = shelve.open('items.db', 'c')

        # handle errors

        try:
            items_dict = db['Items']
        except:
            print("Error in retrieving items")

        # get information entered into form

        item = Item.Item(create_item_form.image.data,
                         create_item_form.name.data,
                         create_item_form.description.data,
                         create_item_form.rate.data,
                         create_item_form.on_loan.data,
                         create_item_form.available.data,
                         create_item_form.location.data)

        # update database

        items_dict[item.get_id()] = item
        db['Items'] = items_dict
        db.close()

        # save image to static
        request.files['image'].save(
            os.path.join('static/images', f"{item.get_id()}.png")
        )

        return redirect(url_for('listingpage'))
    return render_template('createItem.html', form=create_item_form)


@app.route('/createloan', methods=['GET', 'POST'])
def create_loan():
    create_loan_form = CreateLoanForm(request.form)
    if request.method == 'POST' and create_loan_form.validate():
        previous_loans_dict = {}
        db = shelve.open('previousloans.db', 'c')

        # handle errors

        try:
            future_loans_dict = db['PreviousLoans']
        except IndexError:
            print("Error in retrieving items")

        # get information entered into form

        loan = Loan.Loan(create_loan_form.item_pic.data,
                         create_loan_form.item_name.data,
                         create_loan_form.start_date.data,
                         create_loan_form.end_date.data,
                         create_loan_form.customer_name.data)
        # update database

        previous_loans_dict[loan.get_id()] = loan
        db['PreviousLoans'] = previous_loans_dict

        db.close()

        return redirect(url_for('listingpage'))
    return render_template('createloan.html', form=create_loan_form)


@app.route('/futureloans')
def future_loans():
    # retrieve future loans
    future_loans_dict = {}
    db = shelve.open('futureloans.db', 'r')
    future_loans_dict = db['FutureLoans']
    db.close()

    future_loans_list = []
    for key in future_loans_dict:
        loan = future_loans_dict.get(key)
        future_loans_list.append(loan)

    return render_template('futureloans.html', future_loans_list=future_loans_list)


@app.route('/currentloans')
def current_loans():
    # retrieve future loans
    current_loans_dict = {}
    db = shelve.open('currentloans.db', 'r')
    current_loans_dict = db['CurrentLoans']
    db.close()

    current_loans_list = []
    for key in current_loans_dict:
        loan = current_loans_dict.get(key)
        current_loans_list.append(loan)

    return render_template('currentloans.html', current_loans_list=current_loans_list)


@app.route('/previousloans')
def previous_loans():
    # retrieve previous loans
    previous_loans_dict = {}
    db = shelve.open('previousloans.db', 'r')
    previous_loans_dict = db['PreviousLoans']
    db.close()

    previous_loans_list = []
    for key in previous_loans_dict:
        loan = previous_loans_dict.get(key)
        previous_loans_list.append(loan)

    return render_template('pastloans.html', previous_loans_list=previous_loans_list)


@app.route('/movetocurrent/<int:id>', methods=['POST'])
def move_to_current(id):
    future_loans_dict = {}
    current_loans_dict = {}

    # retrieve items from future loans database

    db = shelve.open('futureloans.db', 'c')
    future_loans_dict = db['FutureLoans']

    # retrieve items from current loans database

    db_current = shelve.open('currentloans.db', 'c')
    current_loans_dict = db_current['CurrentLoans']

    loan = future_loans_dict(id)
    current_loans_dict[loan.get_id()] = loan

    # save to current loans database
    db_current['CurrentLoans'] = current_loans_dict

    # delete item from future loans dictionary
    future_loans_dict.pop(id)
    db['FutureLoans'] = future_loans_dict

    # close database
    db.close()
    db_current.close()

    return render_template('futureloans.html')


# Done by Ng Rong Kai:

@app.route("/<string:TYPE>/chats/<string:ID>", methods=["GET"])
def chats(TYPE: str, ID: str):
    TYPE: bool = TYPE.strip().lower().startswith('v')
    _chats: set[str] = Chat().getChatsByID(ID)
    __chats: list = []
    for chat_ in _chats:
        c: Chat = Chat(chat_ if TYPE else ID, ID if TYPE else chat_)
        __chats.append((chat_, c.getLastMessageObject(), c.getUnreadMessagesCount(asVendor=TYPE)))
    return render_template("chats.html", count=len(__chats), chats_list=__chats, asVendor=TYPE, me=ID)


# Done by Ng Rong Kai:

@app.route("/<string:TYPE>/chats/<string:MY_ID>/<string:YOUR_ID>", methods=["GET", "POST"])
def chat(TYPE: str, MY_ID: str, YOUR_ID: str):
    TYPE: bool = TYPE.strip().lower().startswith('v')
    CHAT: Chat = Chat(YOUR_ID if TYPE else MY_ID, MY_ID if TYPE else YOUR_ID)
    if request.method == "POST":
        CHAT.appendChatMessage(TYPE, request.form.get("text", '', str))
    c: list[Message] = CHAT.getChat()
    for i in range(len(c)):
        c[i].index = i
    c.reverse()
    return render_template("chat.html", asVendor=TYPE, me=MY_ID, you=YOUR_ID, chat=c)


# Done by Ng Rong Kai:

@app.route("/<string:TYPE>/chats/<string:MY_ID>/<string:YOUR_ID>/edit", methods=["POST"])
def edit_chat(TYPE: str, MY_ID: str, YOUR_ID: str):
    TYPE: bool = TYPE.strip().lower().startswith('v')
    CHAT: Chat = Chat(YOUR_ID if TYPE else MY_ID, MY_ID if TYPE else YOUR_ID)
    try:
        index: int = int(request.json.get('i', -1))
        newMsg: str = str(request.json.get("msg", ''))
        if MY_ID == CHAT.getChat()[index].id() and CHAT.editChatMessage(index, newMsg):
            return '', 200
    except:
        pass
    return '', 403


# Done by Ng Rong Kai:

@app.route("/<string:TYPE>/deleteChat/<string:MY_ID>/<string:YOUR_ID>", methods=["POST"])
def delete_chat(TYPE: str, MY_ID: str, YOUR_ID: str):
    TYPE: bool = TYPE.strip().lower().startswith('v')
    if Chat(YOUR_ID if TYPE else MY_ID, MY_ID if TYPE else YOUR_ID).delChat():
        return redirect(url_for("chats", TYPE=("vendor" if TYPE else "customer"), ID=MY_ID))
    return '', 403


# Done by Ng Rong Kai:

if __name__ == r"__main__":
    app.run(debug=True)
