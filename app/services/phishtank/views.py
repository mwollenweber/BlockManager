from flask import render_template, flash, redirect, session, url_for, request, g, make_response, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app.models import User, ROLE_USER, ROLE_ADMIN, ROLE_SUBMITTER
from struct import unpack, pack
from socket import inet_aton, inet_ntoa
from datetime import datetime, timedelta
from json import dumps, loads

from . import phishTank
from .models import phishTankModel, ip2int, int2ip


@phishTank.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@phishTank.route('/getInfo', methods=['GET', 'POST'])
def getInfo(ip_str=None):
    response = {"record": None}

    if ip_str is None:
        data = request.get_json()
        if data is not None:
            ip_str = data['ip']

        ip_str = ip_str or request.args.get("ip")

    if ip_str:
        ip = ip2int(ip_str)
        phishTank = phishTankModel.query.filter(ip == phishTankModel.ip).first()
        if not phishTank:
            response = {"record": {"id": phishTank.id, "url": phishTank.url, "verified": phishTank.verified,
                                   "ip": phishTank.ip}}

    return jsonify({"phishTank": response})
