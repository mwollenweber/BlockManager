from flask import render_template, flash, redirect, session, url_for, request, g, make_response, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app.models import  User, ROLE_USER, ROLE_ADMIN, ROLE_SUBMITTER
from struct import unpack, pack
from socket import inet_aton, inet_ntoa
from datetime import datetime, timedelta
from json import dumps, loads

from . import alexa
from .models import alexaModel, ip2int, int2ip


@alexa.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')    


@alexa.route('/getInfo', methods = ['GET', 'POST'])
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
        topIP = alexaModel.query.filter_by(ip=ip).first()
        isTop = (topIP != None)
    else:
        isTop = None
        
    if isTop: 
        response = {"record": {"found":True}}

    
    return jsonify({"alexa":response})
        
    
