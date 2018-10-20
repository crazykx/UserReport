import json
import datetime
import calendar
from flask import current_app

from app.view_models.seller import get_seller_json
from app.models.models import Seller


def get_date_str(date):
    return datetime.date.strftime(date, '%Y-%m-%d')


def str_to_date(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d')


def day_to_date(day):
    start_date = current_app.config['START_DATE']
    start_date = str_to_date(start_date)
    end_date = start_date + datetime.timedelta(days=day)
    return end_date.date()


def get_start_end_date(month):
    year = current_app.config['DEFAULT_YEAR']
    startdate = datetime.date(year, month, 1)
    _, monthRange = calendar.monthrange(year, month)
    enddate = datetime.datetime(year, month, monthRange)
    return startdate, enddate


def get_order_json(order):
    order_dict = dict(id=order.id, sales=order.sales, create_date=get_date_str(order.create_date))
    order_dict['seller'] = {
        'seller_name': order.seller.realname,
        'seller_phone': order.seller.phone,
    }
    order_dict['guest'] = {
        'guest_name': order.guest.realname,
        'guest_phone': order.guest.phone,
        'guest_company': order.guest.company,
    }
    return json.dumps(order_dict)


def get_ranking_json(startdate, enddate, orders):
    ranking_list = []
    for i in range(len(orders)):
        seller_id, sale_sum = orders[i]
        seller = get_seller_json(Seller.query.filter_by(id=seller_id).first_or_404())
        ranking = {
            'ranking': i + 1,
            'sale_sum': sale_sum,
            'seller': seller,
        }
        ranking_list.append(ranking)
    return {get_date_str(startdate) + '至' + get_date_str(enddate): ranking_list}

