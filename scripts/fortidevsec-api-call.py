import argparse, requests, json, re, ast
from prettytable import PrettyTable

parser = argparse.ArgumentParser()
parser.add_argument('--token', dest='curr_token', required=False, help='optionally supply a valid access token')
parser.add_argument('--demo', dest='demo', action='store_true', required=False, help='work with demo application')
grp = parser.add_mutually_exclusive_group()
grp.add_argument('--get-orgs', dest='list_orgs', action='store_true', required=False, help='list organizations associated with user account')
grp.add_argument('--get-apps', dest='org_id_supplied', type=int, required=False, help='list apps for a given org id')
grp.add_argument('--get-scans', dest='app_id_supplied', type=int, required=False, help='list scans for a given app id')
grp.add_argument('--get-findings', dest='scan_id_supplied', type=int, required=False, help='list findings for a given scan id')
args = parser.parse_args()

#URLs
base_url = "https://fortidevsec.forticloud.com/"

get_token_url = "api/v1/login/access-token"
demo_url = "api/v1/login/demo-user"
orgs_url = "api/v1/dashboard/get_orgs"
apps_url = "api/v1/dashboard/get_apps"
scans_url = "api/v1/dashboard/get_scans"
findings_url = "api/v1/dashboard/get_findings"

def init_auth_demo():
    if args.curr_token == None:
        api_call = requests.post(base_url+demo_url)
        token = json.loads(api_call.content)["access_token"]
        print("access token: " + token)
    else:
        print("access token supplied...")
        token = args.curr_token
    return token

def list_organizations(curr_token):
    headers = {}
    headers["Authorization"] = "Bearer " + token
    get_orgs_call=requests.get(base_url+orgs_url, headers=headers)
    org_ids = re.findall("\"id\"\:(\d)", get_orgs_call.text)
    print(org_ids)
    return org_ids

def make_table(data, fields):
    mytuples=[([x[field] for field in fields]) for x in data]
    tuples_sorted=sorted(mytuples, key=lambda x: x[len(fields)-1], reverse=True)
    mytable = PrettyTable([field for field in fields])
    for x in range(min(len(tuples_sorted),5)):
        mytable.add_row([tuples_sorted[x][i] for i in range(len(fields))])
    print(mytable)

def list_apps_by_id(id, token):
    params = {'org_id': id}
    headers = {}
    headers["Authorization"] = "Bearer " + token
    get_apps_call=requests.get(base_url+apps_url, params=params, headers=headers) 
    apps=json.loads(get_apps_call.text)['apps']
    make_table(apps, ['name', 'id', 'new_findings'])
    return apps

def get_scans_by_app_id(app_id, token):
    params = {'app_id': app_id}
    headers = {}
    headers["Authorization"] = "Bearer " + token
    get_scans_call=requests.get(base_url+scans_url, params=params, headers=headers)
    scans=json.loads(get_scans_call.text)
    make_table(scans, ['created', 'id', 'risk_score']) 
    return scans

def get_findings_by_scan_id(scan_id, token):
    params = {'scan_id': scan_id}
    headers = {}
    headers["Authorization"] = "Bearer " + token
    get_findings_call=requests.get(base_url+findings_url, params=params, headers=headers)
    findings=json.loads(get_findings_call.text)
    make_table(findings, ['pretty_category', 'severity', 'final_risk_score', 'id'])
    return findings

if args.curr_token != None:
    token = args.curr_token
    arg_dict = ast.literal_eval(str(vars(args)))
    del arg_dict['curr_token']
    del arg_dict['demo']
    if not any(arg_dict.values()):
        print("")
        print("****Please supply one of the 'get' arguments below.****")
        print("")
        parser.print_help()
        exit(1)
else:
    token = None
    if args.demo == True:
        token=init_auth_demo()
    else:
        print("Demo creds/app only at the moment.")

if args.list_orgs:
    list_organizations(token)
if args.org_id_supplied:
    list_apps_by_id(args.org_id_supplied, token)
if args.app_id_supplied:
    get_scans_by_app_id(args.app_id_supplied, token)
if args.scan_id_supplied:
    get_findings_by_scan_id(args.scan_id_supplied, token)
