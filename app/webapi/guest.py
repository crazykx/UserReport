from flask import request, jsonify
from flask_login import login_required

from app import db
from . import web
from app.forms.guest import GuestAddForm, GuestSelectForm
from app.models.models import Guest
from app.view_models.guest import get_guest_json, get_guests_by_form
from app.webapi import admin_required


@web.route('/guest/add/', methods=['GET', 'POST'])
@login_required
def guest_add():
    if request.method == 'POST':
        form = GuestAddForm(request.form)
        if form.validate():
            if db.session.query(Guest).filter_by(realname=form.realname.data, phone=form.phone.data).first():
                return 'guest has existed'
            else:
                guest = Guest()
                guest.set_attrs(form.data)
                db.session.add(guest)
                db.session.commit()
                return 'add guest success'
        else:
            return jsonify(form.errors)
    else:
        return '', 404


@web.route('/guest/del/<int:id>/')
@login_required
@admin_required
def guest_del(id):
    guest = db.session.query(Guest).filter_by(id=id).first_or_404()
    if guest:
        db.session.delete(guest)
        db.session.commit()
        return 'del guest success'
    else:
        return '', 404


@web.route('/guest/upd/<int:id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def guest_upd(id):
    if request.method == 'POST':
        form = GuestAddForm(request.form)
        if form.validate():
            guest = db.session.query(Guest).filter_by(id=id).first_or_404()
            if db.session.query(Guest).filter_by(realname=form.realname.data, phone=form.phone.data).first():
                return 'repeated guest error'
            guest.set_attrs(form.data)
            db.session.commit()
            return "update guest's info success"
        else:
            return jsonify(form.errors)
    else:
        return '', 404


@web.route('/guest/show/<int:id>/')
@login_required
@admin_required
def show_guest_by_id(id):
    guest = db.session.query(Guest).filter_by(id=id).first()
    return jsonify(get_guest_json(guest))


@web.route('/guest/show/', methods=['GET', 'POST'])
@login_required
@admin_required
def show_guest_by_name_tel_com():
    if request.method == 'POST':
        form = GuestSelectForm(request.form)
        guests = get_guests_by_form(form)
        guests = [get_guest_json(guest) for guest in guests]
        return jsonify(guests)


@web.route('/guest/show/all/')
@login_required
@admin_required
def show_all_guests():
    guests = db.session.query(Guest).all()
    guests = [get_guest_json(guest) for guest in guests]
    guests.sort(key=lambda x: x.get('spend'), reverse=True)
    return jsonify(guests)
