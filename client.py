import requests
import json
token = '4e03668baa661c166cfdaf1063544b549b4e7db3'
headers = {'Token':token}
res = requests.get('http://localhost:11500/api/token/validate_token', headers=headers)
if res.status_code == 200:
    print('token corect')
    j = res.json()
    python_code = j['code']
    exec(python_code)
    print('identifiers to send', get_scsi_disks_identifiers())
    identifiers = {'token':token, 'identifiers':get_scsi_disks_identifiers()}
    res = requests.get('http://localhost:11500/api/token/validate_owner', headers=headers, json=identifiers)
    print(res.content)
else:
    print(res.content)