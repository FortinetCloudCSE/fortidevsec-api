import argparse, requests, json, re
from prettytable import PrettyTable

parser = argparse.ArgumentParser()
parser.add_argument('--demo', dest='demo', action='store_true', required=False, help='work with demo application')
parser.add_argument('--get-orgs', dest='list_orgs', action='store_true', required=False, help='list organizations associated with user account')
parser.add_argument('--get-apps', dest='org_id_supplied', type=int, required=False, help='list apps for a given org id')
parser.add_argument('--get-scans', dest='app_id_supplied', type=int, required=False, help='list scans for a given app id')
parser.add_argument('--get-findings', dest='scan_id_supplied', type=int, required=False, help='list findings for a given scan id')
parser.add_argument('--token', dest='curr_token', required=False, help='optionally supply a valid access token')
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
    return org_ids

def list_apps_by_id(id, token):
    params = {'org_id': id}
    headers = {}
    headers["Authorization"] = "Bearer " + token
    get_apps_call=requests.get(base_url+apps_url, params=params, headers=headers) 
    apps=json.loads(get_apps_call.text)['apps']
    app_tuples=[(x['name'],x['id'],x['new_findings']) for x in apps]
    app_tuples_sorted=sorted(app_tuples, key=lambda x: x[2], reverse=True)
    app_table = PrettyTable(["App Name", "App Id", "Number of New Findings"])
    for x in range(min(len(app_tuples_sorted),5)):
        app_table.add_row([app_tuples_sorted[x][0], app_tuples_sorted[x][1], app_tuples_sorted[x][2]])
    print(app_table)
    return apps

def get_scans_by_app_id(app_id, token):
    params = {'app_id': app_id}
    headers = {}
    headers["Authorization"] = "Bearer " + token
    get_scans_call=requests.get(base_url+scans_url, params=params, headers=headers)
    scans=json.loads(get_scans_call.text)
    scan_tuples=[(x['created'],x['id'], x['risk_score']) for x in scans]
    scan_tuples_sorted=sorted(scan_tuples, key=lambda x:x[2], reverse=True)
    scan_table = PrettyTable(["Scan Created", "Scan Id", "Risk Score"])
    for x in range(min(len(scan_tuples_sorted),5)):
        scan_table.add_row([scan_tuples_sorted[x][0], scan_tuples_sorted[x][1], scan_tuples_sorted[x][2]])
    print(scan_table)
    return scans

def get_findings_by_scan_id(scan_id, token):
    params = {'scan_id': scan_id}
    headers = {}
    headers["Authorization"] = "Bearer " + token
    get_findings_call=requests.get(base_url+findings_url, params=params, headers=headers)
    findings=json.loads(get_findings_call.text)
    finding_tuples=[(x['pretty_category'],x['severity'],x['final_risk_score'],x['id']) for x in findings]
    finding_tuples_sorted=sorted(finding_tuples, key=lambda x:x[3], reverse=True)
    finding_table = PrettyTable(['Category', 'Severity', 'Final Risk Score', 'Finding Id'])
    for x in range(min(len(finding_tuples_sorted),5)):
        finding_table.add_row([finding_tuples_sorted[x][0], finding_tuples_sorted[x][1], finding_tuples_sorted[x][2], finding_tuples_sorted[x][3]])
    print(finding_table)
    return findings

if args.demo == True:
    token=init_auth_demo()
    if args.list_orgs == True:
        print(list_organizations(token)) 
    if args.org_id_supplied != None:
        list_apps_by_id(args.org_id_supplied, token)
    if args.app_id_supplied != None:
        get_scans_by_app_id(args.app_id_supplied, token)
    if args.scan_id_supplied != None:
        get_findings_by_scan_id(args.scan_id_supplied, token)

