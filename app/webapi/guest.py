from flask import request, jsonify
from app import db

from . import web
from app.forms.guest import GuestAddForm
from app.models.models import Guest


@web.route('/guest/add/', methods=['GET', 'POST'])
def guest_add():
    if request.method == 'POST':
        form = GuestAddForm(request.form)
        if form.validate():
            if Guest.query.filter_by(realname=form.realname.data, phone=form.phone.data).first():
                return '已存在'
            else:
                guest = Guest()
                guest.set_attrs(form.data)
                db.session.add(guest)
                db.session.commit()
                return '添加客户成功'
        else:
            return jsonify(form.errors)
    else:
        return '', 404