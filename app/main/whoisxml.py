import urllib2
import json
import traceback
import sys
import xml.etree.ElementTree as etree
from json import dumps
from socket import gethostbyaddr
from flask import jsonify

########################
# Fill in your details #
########################
username = "username"
password = "password"

def getHostnames(target):
    results = []
    try:
        hostnames = gethostbyaddr(target)
        
        for host in hostnames:
            if type(host) == str:
                results.append(host)
                
            if type(host) == list:
                for h in host:
                    results.append(h)
        
    except:
        results = []
    
    return results


def getWhoisDict(target):
    try:
        hostnames = getHostnames(target)
        data = lookupWhois(target)
        registrant = data["WhoisRecord"]["registrant"]["organization"]
        regObj = data["WhoisRecord"]["registrant"]
        
        if regObj.has_key("city"):
            city = data["WhoisRecord"]["registrant"]["city"]
        else:
            city = "Unknown"
            
        country = regObj["country"]
        
        if regObj.has_key("contactEmail"):
            email = regObj["contactEmail"]
            
        else:
            email = "unknown"
        
        
        response = {"registrant": registrant, "email":email, "city":city, "country":country, "hostnames":hostnames}
        
    except KeyError:
        traceback.print_exc(file=sys.stderr)
        
    except:
        traceback.print_exc(file=sys.stderr)    
    
    return response

# A function to recursively print out multi-level dicts with indentation
def RecursivePrettyPrint(obj, indent):
    for x in list(obj):
        if isinstance(obj[x], dict):
            print (' '*indent + str(x)[0:50] + ": ")
            RecursivePrettyPrint(obj[x], indent + 5)
        elif isinstance(obj[x], list):
            print(' '*indent + str(x)[0:50] + ": " + str(list(obj[x])))
        else:
            print (' '*indent + str(x)[0:50] + ": " + str(obj[x])[0:50].replace("\n",""))
            
            
            

def lookupWhois(target):
    format = "JSON"
    url = 'http://www.whoisxmlapi.com/whoisserver/WhoisService?domainName=' + target+ '&username=' + username + '&password=' + password + '&outputFormat=' + format
    try:
            
        # Get and build the JSON object
        result = json.loads(urllib2.urlopen(url).read())
        print json.dumps(result, indent=4, sort_keys=True)
        
        # Handle some odd JS cases for audit, whose properties are named '$' and '@class'.  Dispose of '@class' and just make '$' the value for each property
        if 'audit' in result:
            if 'createdDate' in result['audit']:
                if '$' in result['audit']['createdDate']:
                    result['audit']['createdDate'] = js['audit']['createdDate']['$']
                    
        if 'updatedDate' in result['audit']:
            if '$' in result['audit']['updatedDate']:
                result['audit']['updatedDate'] = js['audit']['updatedDate']['$']
        
        # Get a few data members.
        if ('WhoisRecord' in result):
            registrantName = result['WhoisRecord']['registrant']['name']
            domainName = result['WhoisRecord']['domainName']
            createdDate = result['WhoisRecord']['createdDate']
    except KeyError:
        print "Nothing to see here"
    
    except:
        print "Nothing to see here"
    
    # Print out a nice informative string
    RecursivePrettyPrint(result, 0)
    return result
