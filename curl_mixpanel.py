""" mixpanel data retriever """

import base64
import requests
import urllib3

b64 = base64.b64encode(b'f2ffad341887b1430b4d2aff1fb64282:')

headers = {
    'Authorization': 'Basic {}'.format(b64.decode("utf-8")),
}

params = (
    ('from_date', '2019-03-10'),
    ('to_date', '2019-03-10'),
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#response = requests.get('https://data.mixpanel.com/api/2.0/export/', headers=headers, params=params, verify=False)
response = requests.get('https://google.com')

try:
    raise(TypeError)
    file = open("C:/files/practice/response_content.txt", "w")
    file.write(response.content.decode("utf-8"))
    file.close()
except Exception:
    print("Exception happens:" + Exception.__traceback__)
else:
    print("Success!")

