import requests
import datetime
from io import BytesIO
import gzip
import pandas

branchKey = 'key_live_hkDytPACtipny3N9XmnbZlapBDdj4WIL'
branchSecret = 'secret_live_8CcBNYaLwvLM398sjTXOdptVf8EA57YP'
date = datetime.datetime.now() - datetime.timedelta(days = 1)
exportDate = date.strftime('%Y-%m-%d')

requestBody = {
    'branch_key': branchKey,
    'branch_secret': branchSecret,
    'export_date': exportDate,
}
r = requests.post('http://api.branch.io/v3/export', data = requestBody)

def loadDataForEventType(eventType, initialResponse, exportDate):
    installFileUrls = initialResponse.json()['eo_' + eventType]
    dataFrames = []

    for url in installFileUrls:
        response = requests.get(url)
        installsFile = BytesIO(response.content)

        newInstallsFile = gzip.open(installsFile, mode = 'rt')
        df = pandas.read_csv(newInstallsFile)
        dataFrames.append(df)

    combinedData = pandas.concat(dataFrames)

    finalFrame = combinedData.filter(['id', 'timestamp', 'last_attributed_touch_data_tilde_feature', 'last_attributed_touch_type','last_attributed_touch_timestamp', 'last_attributed_touch_data_tilde_campaign_id', 'last_attributed_touch_data_tilde_creative_id', 'last_attributed_touch_data_tilde_ad_set_id', 'last_attributed_touch_data_tilde_keyword_id', 'event_data_transaction_id', 'event_data_revenue', 'event_data_currency', 'custom_data'], axis = 1)
    finalFrame.to_csv('branch-' + eventType + 's-' + exportDate + '.csv')

loadDataForEventType('install', r, exportDate)
loadDataForEventType('commerce_event', r, exportDate)
