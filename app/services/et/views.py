from flask import render_template, flash, redirect, session, url_for, request, g, make_response, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app.models import  User, ROLE_USER, ROLE_ADMIN, ROLE_SUBMITTER
from struct import unpack, pack
from socket import inet_aton, inet_ntoa
from datetime import datetime, timedelta
from json import dumps, loads

from . import et
from .models import etModel, ip2int, int2ip


@et.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')    


@et.route('/getInfo', methods = ['GET', 'POST'])
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
        et = etModel.query.filter(ip >= etModel.start).filter(ip <= etModel.end).first() 
        if et != None:
            response = {"record": {"isKnown": True, "date":et.tdstamp}}
        

       
    return jsonify({"et":response})
        
    
