from flask import request, jsonify
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

from . import web
from app.forms.seller import SellerRegisterForm, SellerLoginForm
from app.models.models import Seller
from app.view_models.seller import get_seller_json
from webapi import admin_required
from app import db


@web.route('/seller/register/', methods=['GET', 'POST'])
@login_required
@admin_required
def seller_register():
    if request.method == 'POST':
        form = SellerRegisterForm(request.form)
        if form.validate():
            if Seller.query.filter_by(nickname=form.nickname.data).first():
                return 'seller has registered'
            else:
                seller = Seller()
                seller.set_attrs(form.data)
                db.session.add(seller)
                db.session.commit()
                return 'register success'
        else:
            return jsonify(form.errors)
    else:
        return '', 404


@web.route('/seller/login/', methods=['GET', 'POST'])
def seller_login():
    form = SellerLoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            nickname = form.nickname.data
            password = form.password.data
            seller = Seller.query.filter_by(nickname=nickname).first()
            if seller and check_password_hash(seller.password, password):
                login_user(seller, remember=False)
                return 'login success'
            else:
                return 'login failed'
        else:
            return jsonify(form.errors)
    else:
        return '', 404


@web.route('/seller/upd/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def seller_upd(id):
    if request.method == 'POST':
        form = SellerRegisterForm(request.form)
        if form.validate():
            seller = db.session.query.filter_by(id=id).first()
            if seller:
                seller.set_attrs(form.data)
                db.session.add(seller)
                db.session.commit()
                return 'seller update success'
        else:
            return jsonify(form.errors)
    else:
        return '', 404


@web.route('/seller/del/<int:id>')
@login_required
@admin_required
def seller_del(id):
    seller = db.session.query(Seller).filter_by(id=id).first()
    if seller:
        db.session.delete(seller)
        db.session.commit()
        return 'seller delete success'
    else:
        return '', 404


@web.route('/seller/show/<int:id>/')
@login_required
@admin_required
def seller_show(id):
    seller = db.session.query(Seller).filter_by(id=id).first()
    return jsonify(get_seller_json(seller))


@web.route('/seller/show/all/')
@login_required
@admin_required
def seller_show_all():
    sellers = db.session.query(Seller).all()
    seller_list = [get_seller_json(seller) for seller in sellers]
    return jsonify(seller_list)


@web.route('/seller/logout/')
@login_required
def seller_logout():
    logout_user()
    return 'logout success'
