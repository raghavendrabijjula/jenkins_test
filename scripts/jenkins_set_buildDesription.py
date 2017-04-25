#!/usr/bin/env python

__author__='raghav'

import os, sys
import argparse
import requests
from requests.auth import HTTPBasicAuth

def set_description(url,auth,desc):
    head_resp = requests.head(url)
    header = {'content-type':'application/x-www-form-urlencoded'}
    payload = 'description=' + desc
    if head_resp.status_code == 302 :
        response = requests.post(url,data=payload,headers=header)
    elif head_resp.status_code == 403 :
        response = requests.post(url,data=payload,headers=header,auth=auth)
    else :
          print ("REST api request returned response code - [%s]. Check the URL" % (head_resp.status_code))
    if response.status_code != 200 :
        print("Failed to set description! Response code - [%s]" % (response.status_code))
        print("Plese set the description [%s] manually!" % (desc))

def main():
    parser = argparse.ArgumentParser(description='''Toggles Keep Build Forever''',
                                     epilog="""Cloud Services,Qumu Corp""")
    parser.add_argument('-url|u', dest='url', help='Build URL', required=True)
    parser.add_argument('-desc', dest='desc', help='Description to set')
    
    args = parser.parse_args()
    auth = None
    if os.environ.has_key('JENKINS_USER') and os.environ.has_key('JENKINS_PASS') :
        auth=HTTPBasicAuth(str(os.environ['JENKINS_USER']), str(os.environ['JENKINS_PASS']))
    set_description(args.url,auth,args.desc)

if __name__ == '__main__':
   main()
