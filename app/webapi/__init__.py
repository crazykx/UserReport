from flask import Blueprint

web = Blueprint('webapi', __name__)

from app.webapi import seller
from app.webapi import admin
from app.webapi import order
from app.webapi import guest


@web.errorhandler(404)
def page_not_found(error):
    return '', 404