import json
import datetime
from flask import current_app


def get_date_str(date):
    return datetime.datetime.strftime(date, '%Y-%m-%d')


def str_to_date(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d')


def day_to_date(day):
    start_date = current_app.config['START_DATE']
    start_date = str_to_date(start_date)
    end_date = start_date + datetime.timedelta(days=day)
    return end_date.date()


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