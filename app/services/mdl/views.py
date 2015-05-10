from flask import render_template, flash, redirect, session, url_for, request, g, make_response, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app.models import  User, ROLE_USER, ROLE_ADMIN, ROLE_SUBMITTER
from struct import unpack, pack
from socket import inet_aton, inet_ntoa
from datetime import datetime, timedelta
from json import dumps, loads

from . import mdl
from .models import mdlModel, ip2int, int2ip


@mdl.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')    


@mdl.route('/getInfo', methods = ['GET', 'POST'])
def getInfo(ip_str = None):
    response = {"record": None}
    
    if ip_str == None:
        data = request.get_json()
        if data != None:
            ip_str = data['ip']
            
        if ip_str == None:
            ip_str = request.args.get("ip")
        
    if ip_str != None:
        ip = ip2int(ip_str)
        mdl = mdlModel.query.filter_by(ip=ip).order_by(mdlModel.date).first()
        if mdl != None:
            response = {"record": {"date":mdl.date, "url": mdl.url, "domain":mdl.domain, "ip":int2ip(mdl.ip), "reverseLookup":mdl.reverseLookup, "description":mdl.description, "registrant":mdl.registrant}}
        

       
    return jsonify({"mdl":response})
        
    
