from flask import request, jsonify
from flask_login import login_required, current_user

from . import web
from app.forms.order import OrderAddForm, OrderUpdateForm
from app.models.models import Orders
from app import db
from app.view_models.order import get_order_json, day_to_date


@web.route('/order/add/', methods=['GET', 'POST'])
@login_required
def order_add():
    if request.method == 'POST':
        form = OrderAddForm(request.form)
        if form.validate():
            order = Orders()
            seller_id = form.seller_id.data
            if seller_id is None:
                seller_id = current_user.id
            order.set_attrs(form.data)
            order.seller_id = seller_id
            db.session.add(order)
            db.session.commit()
            return ''
        else:
            return jsonify(form.errors)
    else:
        return '', 404


@web.route('/order/upd/<int:order_id>/', methods=['GET', 'POST'])
@login_required
def order_upd(order_id):
    if request.method == 'POST':
        form = OrderUpdateForm(request.form)
        if form.validate():
            order = db.query(Orders).filter_by(id=order_id).first()
            order.set_attrs(form.data)
            print(order)
            db.session.commit()
            return '修改成功'
        else:
            return jsonify(form.errors)
    else:
        return '', 404


@web.route('/order/del/<int:order_id>/')
@login_required
def order_del(order_id):
    if request.method == 'GET':
        order = Orders.query.filter_by(id=order_id).first_or_404()
        db.session.delete(order)
        db.session.commit()
        # db.session.commit()
        return ''


@web.route('/order/select/<int:order_id>/')
@login_required
def order_select(order_id):
    order = Orders.query.filter_by(id=order_id).first_or_404()
    return get_order_json(order)


@web.route('/orders/week/<int:week>/', methods=['GET', 'POST'])
@login_required
def orders_week(week):
    end_date = day_to_date((week-1) * 7)
    print(end_date)
    return ''


@web.route('/orders/month/<int:month>/', methods=['GET', 'POST'])
@login_required
def orders_month(month):
    pass


@web.route('/orders/year/<int:year>/', methods=['GET', 'POST'])
@login_required
def orders_year(year):
    pass


@web.route('/orders/date/', methods=['GET', 'POST'])
@login_required
def orders_dates():
    if request.method == 'POST':
        pass
