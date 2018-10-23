from flask import request, jsonify
from werkzeug.security import check_password_hash

from . import web
from app import db
from app.models.models import Admin
from app.forms.base import RegisterForm, LoginForm


@web.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            nickname = form.nickname.data
            password = form.password.data
            admin = Admin.query.filter_by(nickname=nickname).first()
            if admin and check_password_hash(admin.password, password):
                return 'login success'
            else:
                return 'login failed'
        else:
            return jsonify(form.errors)
    else:
        return '', 404


@web.route('/admin/register/', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        form = RegisterForm(request.form)
        if form.validate():
            if Admin.query.filter_by(nickname=form.nickname.data).first():
                return 'admin success'
            else:
                admin = Admin()
                admin.set_attrs(form.data)
                db.session.add(admin)
                db.session.commit()
                return ''
        else:
            return jsonify(form.errors)
    else:
        return '', 404
