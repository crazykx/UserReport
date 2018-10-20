from wtforms import Form, StringField
from wtforms.validators import Length, DataRequired


class GuestAddForm(Form):
    realname = StringField(validators=[DataRequired(), Length(min=2, max=20, message='长度在2-20之间'), ])
    company = StringField(validators=[DataRequired(), Length(min=2, max=128, message='请填写正确的公司或个人'), ])
    phone = StringField(validators=[DataRequired(), Length(min=3, max=20, message='长度在3-20之间'), ])
