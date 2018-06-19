import requests
import datetime

branchKey = 'key_live_hkDytPACtipny3N9XmnbZlapBDdj4WIL'
branchSecret = 'secret_live_8CcBNYaLwvLM398sjTXOdptVf8EA57YP'
date = datetime.datetime.now()
endDate = date.strftime('%Y-%m-%d')
date -= datetime.timedelta(days = 6)
startDate = date.strftime('%Y-%m-%d')

requestBody = {
    'branch_key': branchKey,
    'branch_secret': branchSecret,
    'start_date': startDate,
    'end_date': endDate,
    'data_source': 'eo_install',
    'dimensions': [
        'user_data_os'
    ],
    'filters': {
        'last_attributed_touch_data_tilde_feature': [
          'paid advertising'
        ]
    },
    'granularity': 'day',
    'aggregation': 'total_count'
}
r = requests.post('http://api.branch.io/v1/query/analytics', data = requestBody)



print(r.json())
