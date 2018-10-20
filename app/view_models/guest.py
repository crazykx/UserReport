from app import db
from sqlalchemy import func
from app.models.models import Guest, Orders


def get_guest_json(guest):
    spend = db.session.query(func.sum(Orders.sales)).filter_by(guest_id=guest.id).first()
    return {
        'realname': guest.realname,
        'company': guest.company,
        'phone': guest.phone,
        'spend': spend[0] if spend[0] is not None else 0,
    }


def get_guests_by_form(form):
    realname = form.realname.data
    company = form.company.data
    phone = form.phone.data
    if realname == '' and company == '' and phone == '':
        guests = []
    elif realname != '' and company != '' and phone != '':
        guests = db.session.query(Guest).filter_by(realname=realname, company=company, phone=phone).all()
    elif realname != '' and company == '' and phone == '':
        guests = db.session.query(Guest).filter_by(realname=realname).all()
    elif realname == '' and company != '' and phone == '':
        guests = db.session.query(Guest).filter_by(company=company).all()
    elif realname == '' and company == '' and phone != '':
        guests = db.session.query(Guest).filter_by(phone=phone).all()
    elif realname != '' and company != '' and phone == '':
        guests = db.session.query(Guest).filter_by(realname=realname, company=company).all()
    elif realname != '' and company == '' and phone != '':
        guests = db.session.query(Guest).filter_by(realname=realname, phone=phone).all()
    else:
        guests = db.session.query(Guest).filter_by(company=company, phone=phone).all()
    return guests

