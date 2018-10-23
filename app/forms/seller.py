from wtforms import Form, StringField
from wtforms.validators import Length, DataRequired


class SellerRegisterForm(Form):
    realname = StringField(validators=[DataRequired(), Length(min=2, max=20, message='realname length between 2-20'), ])
    nickname = StringField(validators=[DataRequired(), Length(min=2, max=20, message='nickname length between 2-20'), ])
    password = StringField(validators=[DataRequired(), Length(min=6, max=128, message='pwd length between 6-128'), ])
    phone = StringField(validators=[DataRequired(), Length(min=3, max=20, message='phone number length between 3-20'), ])


class SellerLoginForm(Form):
    nickname = StringField(validators=[DataRequired(),Length(min=2, max=20, message='nickname length between 2-20'), ])
    password = StringField(validators=[Length(min=6, max=20, message='pwd length between 6-128'), ])