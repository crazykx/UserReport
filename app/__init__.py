from flask import Flask
from app.models.models import login_manager

from models.models import db
from app.webapi.seller import web


app = Flask(__name__)
app.config.from_pyfile('secure.cfg')
app.config.from_pyfile('setting.cfg')

app.register_blueprint(web, url_prefix='/v{}/'.format(app.config['VERSION']))

db.init_app(app=app)

db_session = db.session

login_manager.init_app(app=app)
login_manager.login_view = '/v1/seller/login/'
login_manager.login_message = '请登录以访问此页面'

if __name__ == '__main__':
    # db.drop_all(app=app)
    # db.create_all(app=app)
    # print('/v{}'.format(app.config['VERSION']))
    pass
