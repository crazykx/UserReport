from wtforms import Form, FloatField, IntegerField, DateField
from wtforms.validators import DataRequired, NumberRange


class OrderAddForm(Form):
    sales = FloatField(validators=[DataRequired(), NumberRange(min=0, )])
    seller_id = IntegerField()
    guest_id = IntegerField(validators=[DataRequired(), ])
    create_date = DateField(validators=[DataRequired(), ])


class OrderUpdateForm(Form):
    seller_id = IntegerField(validators=[DataRequired(), ])
    guest_id = IntegerField(validators=[DataRequired(), ])
    sales = FloatField(validators=[DataRequired(), NumberRange(min=0, )])
    create_date = DateField(validators=[DataRequired(), ])


class OrdersFromDate(Form):
    startdate = DateField(validators=[DataRequired(), ])
    enddate = DateField(validators=[DataRequired(), ])
