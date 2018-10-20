from wtforms import Form, StringField
from wtforms.validators import Length, DataRequired


class RegisterForm(Form):
    realname = StringField(validators=[DataRequired(), Length(min=2, max=20, message='长度在2-20之间'), ])
    nickname = StringField(validators=[DataRequired(), Length(min=2, max=20, message='长度在2-20之间'), ])
    password = StringField(validators=[DataRequired(), Length(min=6, max=128, message='请合理设置密码长度'), ])
    phone = StringField(validators=[DataRequired(), Length(min=3, max=20, message='长度在3-20之间'), ])


class LoginForm(Form):
    nickname = StringField(validators=[DataRequired(),Length(min=1, max=20, message='长度在1-20之间'), ])
    password = StringField(validators=[Length(min=6, max=20, message='长度在6-20之间'), ])