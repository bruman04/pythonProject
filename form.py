from wtforms import Form, StringField, TextAreaField, validators, FileField, DateField, DecimalField, IntegerField
class CreateItemForm(Form):
    image = FileField(u'Image File')
    name = StringField('Item Name', [validators.Length(min = 1, max = 150), validators.DataRequired()], render_kw={"placeholder": "Enter Item name"})
    description = TextAreaField('Description', [validators.DataRequired()] ,render_kw={"rows": 10, "cols": 11})
    rate = DecimalField('Daily Rate', [validators.number_range(min=0),validators.InputRequired()])
    on_loan = IntegerField('On Loan', [validators.number_range(min=0),validators.InputRequired()])
    available = IntegerField('Inventory stock', [validators.number_range(min=1),validators.InputRequired()])
    location = StringField('Pickup/Dropoff location', [validators.Length(min = 1, max = 1000), validators.DataRequired()])

class CreateLoanForm(Form):
    item_pic = FileField(u'Image File')
    item_name = StringField('Item Name', [validators.Length(min = 1, max = 150), validators.DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d')
    end_date = DateField('End Date', format='%Y-%m-%d')
    customer_name = StringField('Customer Name', [validators.Length(min = 1, max = 150), validators.DataRequired()])
