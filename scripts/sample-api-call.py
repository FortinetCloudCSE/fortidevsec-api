import argparse, requests, json, re

parser = argparse.ArgumentParser()
parser.add_argument("--demo", help="use demo app/credentials")
parser.parse_args()

base_url = "https://fortidevsec.forticloud.com/"

#API call urls
get_token_url = "api/v1/login/access-token"
demo_url = "api/v1/login/demo-user"
orgs_url = "api/v1/dashboard/get_orgs"
apps_url = "api/v1/dashboard/get_apps"
scans_url = "api/v1/dashboard/get_scans"

api_call=requests.post(base_url+demo_url)

token = json.loads(api_call.content)["access_token"]

headers = {}
headers["Authorization"] = "Bearer " + token

get_orgs_call=requests.get(base_url+orgs_url, headers=headers)
org_ids = re.findall("\"id\"\:(\d)", get_orgs_call.text)

"""
#Get apps with first org id
params = {'org_id': org_ids[0]}
get_apps_call=requests.get(base_url+apps_url, params=params, headers=headers) 
apps=json.loads(get_apps_call.text)['apps']

#Get list of apps sorted by number of new findings
app_tuples=[(x['name'],x['id'],x['new_findings']) for x in apps]
app_tuples_sorted=sorted(mytups, key=lambda x: x[2], reverse=True)

#Get scans of app with greatest number of new findings
app_id=app_tuples_sorted[0][1]
params = {'app_id': app_id}
get_scans_call=requests.get(base_url+scans_url, params=params, headers=headers)
scans=json.loads(get_scans_call.text)
scantups=[(x['created'],x['risk_score'],x['id']) for x in scans]

#Get findings of scan with greatest risk score
"""
