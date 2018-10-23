import datetime

from flask import request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func, desc, extract

from . import web
from app.forms.order import OrderAddForm, OrderUpdateForm, OrdersFromDate
from app.models.models import Orders
from app.webapi import admin_required
from app import db
from app.view_models.order import get_order_json, day_to_date, get_ranking_json, get_start_end_date


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
            return 'add success'
        else:
            return jsonify(form.errors)
    else:
        return '', 404


@web.route('/order/upd/<int:order_id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def order_upd(order_id):
    if request.method == 'POST':
        form = OrderUpdateForm(request.form)
        if form.validate():
            order = db.session.query(Orders).filter_by(id=order_id).first()
            order.set_attrs(form.data)
            db.session.commit()
            return 'update success'
        else:
            return jsonify(form.errors)
    else:
        return '', 404


@web.route('/order/del/<int:order_id>/')
@login_required
@admin_required
def order_del(order_id):
    if request.method == 'GET':
        db.session.query(Orders).filter(Orders.id==order_id).delete()
        # db.session.delete(order)
        db.session.commit()
        return 'remove success'


@web.route('/order/show/<int:order_id>/')
@login_required
@admin_required
def order_select(order_id):
    order = Orders.query.filter_by(id=order_id).first_or_404()
    return get_order_json(order)


@web.route('/orders/ranking/week/<int:week>/')
@login_required
@admin_required
def orders_week(week):
    if week > 0:
        # startdate = str_to_date(current_app.config['START_DATE'])
        startdate = day_to_date((week-1)*7)
        enddate = day_to_date(week * 7 - 1)
        orders = db.session.query(Orders.seller_id, func.sum(Orders.sales).label('sale_sum')).filter(
            Orders.create_date.between(startdate, enddate)).group_by(Orders.seller_id).order_by(desc('sale_sum')).all()
        ranking_json_str = get_ranking_json(startdate, enddate, orders)
        return jsonify(ranking_json_str)
    else:
        return '', 404


@web.route('/orders/ranking/month/<int:month>/')
@login_required
@admin_required
def orders_month(month):
    if 0 < month <= 12:
        # startdate = str_to_date(current_app.config['START_DATE'])
        orders = db.session.query(Orders.seller_id, func.sum(Orders.sales).label('sale_sum')).filter(extract('month', Orders.create_date)==month).group_by(Orders.seller_id).order_by(desc('sale_sum')).all()
        startdate, enddate = get_start_end_date(month)
        ranking_json_str = get_ranking_json(startdate, enddate, orders)
        return jsonify(ranking_json_str)
    else:
        return '', 404


@web.route('/orders/ranking/year/<int:year>/')
@login_required
@admin_required
def orders_year(year):
    if year > 0:
        # startdate = str_to_date(current_app.config['START_DATE'])
        orders = db.session.query(Orders.seller_id, func.sum(Orders.sales).label('sale_sum')).filter(extract('year', Orders.create_date)==year).group_by(Orders.seller_id).order_by(desc('sale_sum')).all()
        startdate = datetime.date(year, 1, 1)
        enddate = datetime.date(year, 12, 31)
        ranking_json_str = get_ranking_json(startdate, enddate, orders)
        return jsonify(ranking_json_str)
    else:
        return '', 404


@web.route('/orders/ranking/', methods=['GET', 'POST'])
@login_required
@admin_required
def orders_dates():
    if request.method == 'POST':
        form = OrdersFromDate(request.form)
        if form.validate():
            startdate = form.startdate.data
            enddate = form.enddate.data
            orders = db.session.query(Orders.seller_id, func.sum(Orders.sales).label('sale_sum')).filter(Orders.create_date.between(startdate, enddate)).group_by(Orders.seller_id).order_by(desc('sale_sum')).all()
            # orders = Orders.query.filter_by(create_date=date).order_by(Orders.sales).all()
            # print(orders, type(orders))
            # ranking_list = []
            # for i in range(len(orders)):
            #     seller_id, sale_sum = orders[i]
            #     seller = get_seller_json(Seller.query.filter_by(id=seller_id).first_or_404())
            #     ranking = {
            #         'ranking': i + 1,
            #         'sale_sum': sale_sum,
            #         'seller': seller,
            #     }
            #     ranking_list.append(ranking)
            # return jsonify({get_date_str(startdate)+'至'+get_date_str(enddate): ranking_list})

            # orders = [get_order_json(order) for order in orders]
            # return jsonify({get_date_str(date): orders})
            ranking_json_str = get_ranking_json(startdate, enddate, orders)
            return jsonify(ranking_json_str)
        else:
            return jsonify(form.errors)
    else:
        return '', 404
