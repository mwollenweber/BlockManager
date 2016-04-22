'''
models.py


Copyright Matthew Wollenweber 2015
mjw@cyberwart.com

'''


from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import request, url_for, current_app
from flask.ext.login import UserMixin, AnonymousUserMixin
from sqlalchemy.dialects.mysql import INTEGER, BLOB, DATETIME, TINYINT, TEXT
from sqlalchemy import ForeignKey, ForeignKeyConstraint,  or_
from sqlalchemy.orm import mapper, relationship, backref
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from struct import unpack, pack
from socket import inet_aton, inet_ntoa
import traceback
import sys

from app.database import Base, db_session
from app import db
from . import login_manager


ROLE_USER = 0
ROLE_SUBMITTER = 10
ROLE_APPROVER = 20
ROLE_ADMIN = 100
ROLE_GOD = 1000

db_session._model_changes = {}


def int2ip(addr):                                                               
    return inet_ntoa(pack("!I", addr))    


def ip2int(addr):                                                               
    return unpack("!I", inet_aton(addr))[0]  


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False
    
    def isAnonymous(self):
        return True
    
    def isAuthenticated(self):
        return False
    
    def isSubmitter(self):
        return False
    
    def isApprover(self):
        return False
    
    def isAdmin(self):
        return False
    
    def isDisabled(self):
        false

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class protectedRanges(Base):
    __tablename__ = 'protectedRanges'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(INTEGER(unsigned=True), index=True)
    end = db.Column(INTEGER(unsigned=True), index=True)
    tdSubmitted = db.Column(DATETIME, index=True, default=datetime.utcnow)
    notes = db.Column(BLOB)
    
    def isProtected(self, ip_str):
        target_ip = ip2int(ip_str)
        result = protectedRanges.query.filter(
            target_ip >= protectedRanges.start).filter(target_ip <= protectedRanges.end).first()

        if result:
            print "isProtected"
            return True
        
        print "notProtected"
        return False
    

class User(UserMixin, Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    password_hash = db.Column(db.String(128))
    fName = db.Column(db.String(32), index = True)
    lName = db.Column(db.String(32), index = True)
    accountCreated = db.Column(db.DateTime(), default=datetime.utcnow)
    lastLogin = db.Column(db.DateTime(), index = True, default=datetime.utcnow)
    confirmed = db.Column(db.SmallInteger, default = 0, index = True)
    disabled = db.Column(db.SmallInteger, default = 0, index = True)
    #fixme typo
    acountApproved =  db.Column(db.SmallInteger, default = 0, index = True)
    org = db.Column(db.String(32), index = True)        
    #blocks = db.relationship('blocks',  backref="ipBlock.submitter", lazy='dynamic')
    
    def makeSubmitter(self, user):
        if self.role >= ROLE_ADMIN:
            user.role = ROLE_SUBMITTER
            db.session.merge(user)
            return True
        
        return False
            
 
    def makeApprover(self, user):
        if self.role >= ROLE_ADMIN:
            user.role = ROLE_APPROVER
            db_session.merge(user)
            db_session.commit()
            
            return True
        
        return False    
    
    def makeAdmin(self, user):
        if self.role >= ROLE_ADMIN:
            user.role = ROLE_ADMIN
            db_session.merge(user)
            db_session.commit()
            
            return True
        
        return False
            
    def disable(self, user):
        if self.role >= ROLE_ADMIN:
            user.disabled = 1
            db_session.merge(user)
            db_session.commit()
            
            return True
        
        return False
    
    @property
    def password(self):
        raise AttributeError("ERROR: Cannot read password")
    
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, 
                                                   method='pbkdf2:sha1', 
                                                   salt_length=8)
        
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash,  password)
                              
    def is_authenticated(self):
        return True

    def is_active(self):
        return True
    
    def isDisabled(self):
        if self.disabled == 0:
            return False
        
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)    

    def __repr__(self):
        return '<User %r>' % (self.nickname)
    
    def get_last_login(self): 
        return self.lastLogin
    
    def isConfirmed(self):
        if self.confirmed == 1:
            return True
        
        return False
    
    def getRole(self):
        return self.role
    
    def isAdmin(self):
        return self.role >= ROLE_ADMIN
    
    def isApprover(self):
        return self.role >= ROLE_APPROVER
    
    def isSubmitter(self):
        return self.role >= ROLE_SUBMITTER
    
    def isAnonymous(self):
        return False
    
    def generate_confirmation_token(self, expiration=3600):
            s = Serializer(current_app.config['SECRET_KEY'], expiration)
            return s.dumps({'confirm': self.id})
    
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            print "Token data = %s"  % data
        
        except:
            traceback.print_tb(exc_traceback, limit=1, file=sys.stderr)
            return False

        if data.get('confirm') != self.id:
            print "ERROR: data.get confirm != self.id"
            return False
        
        self.confirmed = 1
        db_session.merge(self)
        db_session.commit()
        db_session.flush()
        return True
    
    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            
        except:
            traceback.print_tb(exc_traceback, limit=1, file=sys.stderr)
            return False
        
        if data.get('reset') != self.id:
            return False
        
        self.password = new_password
        db_session.add(self)
        db_session.flush()
        
        return True
    
    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        
        try:
            data = s.loads(token)
            
        except:
            traceback.print_tb(exc_traceback, limit=1, file=sys.stderr)
            return False
        
        if data.get('change_email') != self.id:
            return False
        
        new_email = data.get('new_email')
        
        if new_email is None:
            return False
        
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        
        self.email = new_email
        db_session.add(self)
        db_session.flush()
        
        return True    

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                           expires_in=expiration)
            
        return s.dumps({'id': self.id}).decode('ascii')
        
    @staticmethod
    def verify_auth_token(token):
        print "in verify auth"
        s = Serializer(current_app.config['SECRET_KEY'])
        
        try:
            data = s.loads(token)
            
        except:
            return None
        
        return User.query.get(data['id'])
    
    def __unicode__(self):
        return self.email    
    

class ipBlock(Base):
    __tablename__ = 'blocks'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(INTEGER(unsigned=True), index=True)
    tdApproved = db.Column(DATETIME, index=True, default=None)
    tdSubmitted = db.Column(DATETIME, index=True, default=datetime.utcnow)
    approved = db.Column(TINYINT, default=0, index=True)
    deleted = db.Column(TINYINT, default=0, index=True)
    approver_id = db.Column(db.Integer, ForeignKey("users.id"), index=True)
    submitter_id = db.Column(db.Integer, ForeignKey("users.id"), index=True)
    duration = db.Column(INTEGER(unsigned=True))
    notes = db.Column(BLOB)
    
    submitter = relationship('User', foreign_keys='ipBlock.submitter_id')
    approver = relationship('User', foreign_keys='ipBlock.approver_id')

    def __init__(self):
        print "initializing the ipblock object"
        db_session.flush()
    
    def isApproved(self):
        if self.approved == 1:
            return True
        else:
            return False
    
    def isDisabled(self):
        if self.deleted == 1:
            return True
        return False
    
    def isDeleted(self):
        if self.deleted != 0:
            return True
        return False
    
    def isActive(self):
        if self.approved == 1 and self.deleted == 0:
            return True
        else:
            return False

    def getIP(self):
        return int2ip(int(self.ip))
    
    def getSubmitter(self):
        return self.submitter.email
    
    def getApprover(self):
        if self.isApproved():
            return self.approver.email
        else:
            return None

    def approve(self, user):
        if user.isApprover():
            approver_id = user.id
            now = datetime.utcnow()
            
            self.approver_id = approver_id
            self.tdApproved = now
            self.approved = 1
            
            db_session.flush()
            db_session.merge(self)
            db_session.commit()
           
            return True
        
        else:
            return False
    
    def delete(self, user):
        if user.isApprover():
            self.deleted = 1
            
            db_session.flush()
            db_session.merge(self)
            db_session.commit()
           
            return True
        
        else:
            return False
    
    def undelete(self, user):
        if user.isApprover():
            self.deleted = 0
            
            db_session.flush()
            db_session.merge(self)
            db_session.commit()
           
            return True
        
        else:
            return False

    def insert(self, current_user, address, notes, duration):
        if address is None:
            db_session.flush()
            return False

        submitterID = current_user.id

        #fix me: should handle additional address types (cidr, range, name)
        ipString = address.strip()
        ipAddress = unpack('!L', inet_aton(ipString))[0]

        self.ip = ipAddress
        self.notes = notes
        self.duration = int(duration)
        self.submitter_id = submitterID
        #self.tdSubmitted = datetime.utcnow()
        #self.approver_id = submitterID


        try:
            print "Blocking %s for %s days" % (ipString, self.duration)
            print int2ip(ipAddress)

            #db_session.flush()
            db_session.merge(self)
            #db_session.add(self)
            db_session.commit()

        except AttributeError:
            traceback.print_exc(file=sys.stderr)


    def flush(self):
        db_session.flush()

    def commit(self):
        db_session.commit()


