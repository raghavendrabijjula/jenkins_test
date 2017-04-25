#!/usr/bin/env python

import os
import argparse
from jira import JIRA
import zipfile

USER = os.environ['JIRA_USER']
PASSWD = os.environ['JIRA_PASS']

def main():
    parser = argparse.ArgumentParser(description='''Updates JIRA issue''',
                                     epilog="""Cloud Services,Qumu Corp""")
    parser.add_argument('--issue', dest='issue_id', help='Valid issue ID', required=True)
    parser.add_argument('--comment', dest='comment', help='comment', required=True)
    parser.add_argument('--log_path', dest='log', help='build log location')
    args = parser.parse_args()
    zf = zipfile.ZipFile('./build_log.zip', mode='w')
    zf.write(args.log, os.path.basename(args.log))
    zf.close()

    try:
        jac = JIRA('https://jira.atlassian.com', options={'verify': False}, basic_auth=(USER, PASSWD))
        issue = jac.issue(args.issue_id)
        issue.update(comment=str(args.comment))
        jac.add_attachment(args.issue_id,'./build_log.zip','build_log.zip') 
    except:
       raise  

if __name__ == '__main__':
    main()
