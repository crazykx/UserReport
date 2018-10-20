from flask import request, jsonify
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

from . import web
from app.forms.seller import SellerRegisterForm, SellerLoginForm
from app.models.models import Seller
from app import db


# 销售注册
@web.route('/seller/register/', methods=['GET', 'POST'])
def seller_register():
    if request.method == 'POST':
        form = SellerRegisterForm(request.form)
        if form.validate():
            if Seller.query.filter_by(nickname=form.nickname.data).first():
                return '已存在'
            else:
                seller = Seller()
                seller.set_attrs(form.data)
                db.session.add(seller)
                db.session.commit()
                return '注册成功'
        else:
            return jsonify(form.errors)
    else:
        return '', 404


# 销售登录处理
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
                return '登陆成功'
            else:
                return '登录失败'
        else:
            return jsonify(form.errors)
    else:
        return '', 404


@web.route('/seller/logout/')
@login_required
def seller_logout():
    logout_user()
    return '已退出登录'