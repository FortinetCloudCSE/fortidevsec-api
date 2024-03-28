# fortidevsec-api

Some scripts for working with the FortiDevSec API(beta): [FNDN link](https://fndn.fortinet.net/index.php?/fortiapi/1476-fortidevsecbeta/)


### scripts/fortidevsec-api-call.py

Requires Python 3 (tested on 3.10.6).

The following steps detail working with the FortiDevSec demo application ![here](https://fortidevsec.forticloud.com/#/demo/). To work with your FortiDevSec account organization, omit the '--demo' flag and retrieve an API token as detailed ![here](https://docs.fortinet.com/document/fortidevsec/24.1.0/user-guide/2187/api-access).

<pre>
##### Get an authentication token to work with the demo FortiDevSec organization.
> python fortidevsec-api-call.py --demo
<i>access token: abcd1234efgh</i>

##### Get the demo organization id
> python fortidevsec-api-call.py --token abcd1234efgh --demo --get-orgs
<i>['2']</i>

##### Get info on apps with the greatest number of findings associated with that organization
> python fortidevsec-api-call.py --token abcd1234efgh --demo --get-apps 2
<i>
+-------------------+----+--------------+
|        name       | id | new_findings |
+-------------------+----+--------------+
|   ZulipPythonApp  | 6  |     1136     |
|    Timescaledb    | 7  |     253      |
| OWASPBenchmarkApp | 3  |     201      |
|    RailsGoatApp   | 4  |     129      |
|       Spdlog      | 9  |     103      |
+-------------------+----+--------------+
</i>

##### Get info on scans associated with a particular app, for example Timescaledb (id 7)
> python fortidevsec-api-call.py --token abcd1234efgh --demo --get-scans 7
<i>
+----------------------------+-------+------------+
|          created           |   id  | risk_score |
+----------------------------+-------+------------+
| 2023-06-02T07:22:29.363086 | 41915 |    8.0     |
+----------------------------+-------+------------+
</i>

##### Get info on findings with highest risk scores associated with this scan
> python fortidevsec-api-call.py --token abcd1234efgh --demo --get-findings 41915
<i>
+-----------------------------+----------+------------------+----------+
|       pretty_category       | severity | final_risk_score |    id    |
+-----------------------------+----------+------------------+----------+
| Format String Vulnerability |   high   |       8.0        | 22601556 |
|       Buffer Overflow       |  medium  |       4.0        | 22601555 |
|       Buffer Overflow       |  medium  |       4.0        | 22601554 |
|       Buffer Over-read      |  medium  |       3.0        | 22601552 |
|       Buffer Over-read      |  medium  |       3.0        | 22601551 |
+-----------------------------+----------+------------------+----------+
</i>

</pre>
