from flask import Blueprint
from flask_login import current_user
from flask import redirect, url_for

web = Blueprint('webapi', __name__)

from app.webapi import seller
from app.webapi import admin
from app.webapi import order
from app.webapi import guest


@web.errorhandler(404)
def page_not_found(error):
    return '', 404


def admin_required(f):
    seller = current_user

    def wrapper(*args, **kwargs):
        if seller.admin:
            return f(*args, **kwargs)
        else:
            return redirect('/admin/login/')
    return wrapper