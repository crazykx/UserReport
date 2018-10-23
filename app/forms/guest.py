from wtforms import Form, StringField
from wtforms.validators import Length, DataRequired


class GuestAddForm(Form):
    realname = StringField(validators=[DataRequired(), Length(min=2, max=20, message='realname length between 2-20'), ])
    company = StringField(validators=[DataRequired(), Length(min=2, max=128, message='please enter your company or name'), ])
    phone = StringField(validators=[DataRequired(), Length(min=3, max=20, message='phone number length between 3-20'), ])

class GuestSelectForm(Form):
    realname = StringField(validators=[Length(min=2, max=20, message='realname length between 2-20'), ])
    company = StringField(validators=[Length(min=2, max=128, message='please enter your company or name'), ])
    phone = StringField(validators=[Length(min=3, max=20, message='phone number length between 3-20'), ])
