from flask import render_template, flash, redirect, session, url_for, request, g, make_response, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from ..models import User, ROLE_USER, ROLE_ADMIN, ROLE_SUBMITTER,  ipBlock, db, ip2int, int2ip, protectedRanges
from datetime import datetime, timedelta
from .forms import blockForm, uploadBlockListForm
from whoisxml import getWhoisDict
from ..email import send_email
from . import main



@main.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@main.route('/', methods=['GET', 'POST'])
def index():
    return viewBlocks()


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    data = "For Assistance please email root@dev.null"
    return render_template('index.html', message=data)

@main.route('/about', methods=['GET', 'POST'])
def about():
    data = []
    return render_template('index.html', table=data)


@main.route('/secret', methods=['GET', 'POST'])
@login_required
def secret():
    data = ["SECRET SAUCE"]
    return render_template('index.html', table=data)

@main.route('/viewBlocks', methods=['GET', 'POST'])
def viewBlocks():
    now = datetime.now()

    if current_user.isAnonymous() or request.args.get("format") == "csv":
        blocks = ipBlock.query.filter(ipBlock.tdSubmitted >= now - timedelta(days=90))\
            .filter(ipBlock.approved == 1)\
            .filter(ipBlock.deleted == 0)\
            .order_by(ipBlock.tdSubmitted.desc(), ipBlock.tdApproved.desc(), ipBlock.ip, ipBlock.submitter_id)\
            .group_by(ipBlock.ip, ipBlock.approved).all()

    else:
        #since = datetime.now() - timedelta(days=24)
        blocks = ipBlock.query.filter(ipBlock.tdSubmitted >= now - timedelta(days=90))\
            .order_by(ipBlock.tdSubmitted.desc(), ipBlock.ip, ipBlock.submitter_id).all()

    filteredBlocks = []
    for block in blocks:
        delta = now - timedelta(days=int(block.duration))
        if block.tdSubmitted >= delta:
            filteredBlocks.append(block)
            print "block = %s still valid" % block.getIP()

        else:
            print "block = %s SKIPPED for duration" % block.getIP()

    blocks = filteredBlocks
    if request.args.get("format") == "csv":
        blockList = ""
        for block in blocks:
            blockList += block.getIP() + "\n"
            
        response = make_response(blockList)
        response.headers["Content-Type"] = "text/plain"
        return response
    
    elif request.args.get("format") == "json":
        for block in blocks:
            {"action": block}

    else:   
        return render_template('viewTable.html',  ipBlocks=blocks)

@main.route('/addBlock', methods=['GET', 'POST'])
@login_required
def addBlock(address=None, note=None, duration=None):

    form = blockForm()
    if form.validate_on_submit():   
        if current_user.isSubmitter() and not current_user.isDisabled() and current_user.isConfirmed():
            address = form.address.data
            print "DEBUG: Trying to Block: %s, %s, %s" % (address, form.notes.data, form.duration.data)
            #fixme - should handle other data than just IP

            block = ipBlock()
            block.insert(current_user, address, form.notes.data, form.duration.data)
            flash("Block Successfully submitted for approval")
            return redirect(url_for('main.viewBlocks')) 
            
        else:
            flash("You don't have permission to do that!")
            return redirect(url_for('main.index'))
    else:
        print "DEBUG: Form validation failed or not a submit.. address = %s" % form.address.data
            
    return render_template('addForm.html', form=form)


@main.route('/approveBlock', methods=['GET', 'POST'])
@login_required
def approveBlocks():
    data = request.get_json()
    block_id = data["block_id"]

    if current_user.isApprover() and not current_user.isDisabled() and current_user.isConfirmed():   
        if block_id is None:
            print "No Block ID"
            return redirect(url_for('main.index'))         
        
        block = ipBlock.query.filter_by(id=block_id).first()
        
        if block is None:
            flash("Error: Unknown block_id")
            print "ERROR: Unknown block_id"
            return redirect(url_for('main.index')) 
        
        else:
            block.approve(current_user)
            flash("Block Approved")
        
        return viewBlocks()
    
    else:
        flash("You don't have permission to do that!")
        print "ERROR: You don't have permission to do that"
        return redirect(url_for('main.index'))      
    
    
@main.route('/deleteBlock', methods = ['GET', 'POST'])
@login_required
def deleteBlock():
    data = request.get_json()
    block_id = data["block_id"]

    if current_user.isApprover() and not current_user.isDisabled() and current_user.isConfirmed():   
        if block_id is None:
            print "No Block ID"
            return redirect(url_for('main.index'))         
        
        block = ipBlock.query.filter_by(id=block_id).first()
        
        if block is None:
            flash("Error: Unknown block_id")
            print "ERROR: Unknown block_id"
            return redirect(url_for('main.index')) 
        
        else:
            block.delete(current_user)
            flash("Block Deleted")
        
        return viewBlocks()
    
    else:
        flash("You don't have permission to do that!")
        print "ERROR: You don't have permission to do that"
        return redirect(url_for('main.index'))        

    
@main.route('/undeleteBlock', methods = ['GET', 'POST'])
@login_required
def undeleteBlock():
    data = request.get_json()
    block_id = data["block_id"]

    if current_user.isApprover() and not current_user.isDisabled() and current_user.isConfirmed():   
        if block_id is None:
            print "No Block ID"
            return redirect(url_for('main.index'))         
        
        block = ipBlock.query.filter_by(id=block_id).first()
        
        if block is None:
            flash("Error: Unknown block_id")
            print "ERROR: Unknown block_id"
            return redirect(url_for('main.index')) 
        
        else:
            block.undelete(current_user)
            flash("Block Undeleted")
        
        return viewBlocks()
    
    else:
        flash("You don't have permission to do that!")
        print "ERROR: You don't have permission to do that"
        return redirect(url_for('main.index'))        
    

@main.route('/editBlocks', methods=['GET', 'POST'])
@login_required
def editBlocks():
    flash("Edit Blocks")
    data = None    
    return render_template('index.html')

@main.route('/uploadBlockList', methods=['GET', 'POST'])
@login_required
def uploadBlockList():
    if not current_user.isApprover() or current_user.isDisabled() or not current_user.isConfirmed():
        return redirect(url_for('main.index'))

    form = uploadBlockListForm()
    if form.validate_on_submit():
        if current_user.isSubmitter() and not current_user.isDisabled() and current_user.isConfirmed():
            cidr = form.cidr.data
            #fixme actually treat it as a cidr


            #db.session.add(block)
            #db.session.flush()
            #db.session.commit()

            flash("Block List Successfully Added")
            return redirect(url_for('main.viewBlocks'))

        else:
            flash("You don't have permission to do that!")
            return redirect(url_for('main.viewBlocks'))

    return render_template('uploadForm.html', form=form)

@main.route('/getWhois', methods=['GET', 'POST'])
@login_required
def getWhois(ip = None):
    ip_str = None
    info = {}
    data = request.get_json()
    if data is not None:
        ip_str = data['ip']
        
    if ip_str is None:
        ip_str = request.args.get("ip")
     
    if ip_str is not None:
        info = getWhoisDict(ip_str)
        
    response = {"record": info} 
    return jsonify({"whois": response})

@main.route("/internal/getInfo", methods = ['GET', 'POST'])
@login_required
def getInternalInfo(ip_str=None):
    response = {"record": None}
    data = request.get_json()
    if data is not None:
        ip_str = data['ip']
        
    if ip_str is None:
        ip_str = request.args.get("ip")
     
    if ip_str is not None:
        protected = protectedRanges()
        if protected.isProtected(ip_str):
            info = {"isProtected": True}
            response = {"record": info} 
            
    return jsonify({"internal": response})    
    
    
    
@main.route('/pesterApprovers', methods = ['GET', 'POST'])
@login_required
def pesterApprovers(user):
    print "Pester Approvers"
    




