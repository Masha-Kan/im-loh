import hmac
import os
from flask import Flask, make_response, jsonify, request
import hashlib
from settings import DevelopmentConfig
app = Flask(__name__)

@app.errorhandler(405)
def handler_405(error):
    return make_response(jsonify({'error': 'method not allowed for requested url'}), 405)


@app.errorhandler(404)
def handler_404(error):
    return make_response(jsonify({'error': 'requested url not found'}), 404)


def token_gen(tokens):
    h = hmac.new(secret, tokens.to_bytes(8, 'big'), hashlib.sha1)
    while True:
        tokens += 1
        h.update(tokens.to_bytes(8, 'big'))
        yield h.hexdigest()


@app.route('/secured')
def secured_page():
    return 'Did\'t you know this server is fully secured?'


@app.route('/api/token/validate_token')
def validate_token():
    if "Token" in request.headers:
        token = request.headers['Token']
        if token in tokens:
            return make_response(jsonify({'code':hardware_identificators_code}),200)
        else:
            return make_response(jsonify({'error':'token not found'}), 400)
    else:
        return make_response(jsonify({'error':' no "Token" header found'}), 400)


@app.route('/api/token/validate_owner')
def validate_token_owner():
    user_json = request.get_json()
    if 'token' in user_json and 'identifiers' in user_json: 
        if user_json['token'] in tokens:
            if not tokens[user_json['token']]:
                tokens[user_json['token']] = user_json['identifiers']
            if tokens[user_json['token']] == user_json['identifiers']:
                print(user_json['token'], user_json['identifiers'])
                return jsonify({'code':wallfuck_code})
            else:
                return make_response(jsonify({'error':'incorrect identifiers for the token'}))
        else:
            return make_response(jsonify({'error':'token not found'}), 400)
    else:
        return make_response(jsonify({'error':'token or identifers not found'}), 400)


hardware_identificators_code = '''
import winreg
import os
def get_scsi_disks_identifiers():
    arch_keys = winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY
    key_path = r'HARDWARE\DEVICEMAP\Scsi'
    aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    scsi_ports = []
    scsi_identifiers = []
    for arch_key in arch_keys:
        aKey = winreg.OpenKey(aReg, key_path, 0, winreg.KEY_READ | arch_key)
        for i in range(1024):
            try:
                scsi_port = winreg.EnumKey(aKey,i)
                scsi_ports.append(scsi_port)
            except EnvironmentError:
                break
        for scsi_port in scsi_ports:
            port_key_path = os.path.join(key_path, scsi_port, r'Scsi Bus 0\Target Id 0\Logical Unit Id 0')
            try:
                key=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, port_key_path)
                identifier = winreg.QueryValueEx(key,'Identifier')[0]
                scsi_identifiers.append(identifier)
            except FileNotFoundError:
                pass
    return scsi_identifiers
'''

wallfuck_code = '''
import pymem
import re

pm = pymem.Pymem('csgo.exe')
client = pymem.process.module_from_name(pm.process_handle,
                                        'client.dll')

clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
address = client.lpBaseOfDll + re.search(rb'\x83\xF8.\x8B\x45\x08\x0F',
                                         clientModule).start() + 2

pm.write_uchar(address, 2 if pm.read_uchar(address) == 1 else 1)
pm.close_process()
'''
app.config.from_object(DevelopmentConfig)
secret = app.config['SECRET_KEY']
tokens_amount = 0
tokens_g = token_gen(tokens_amount)
tokens = {}
my_token = next(tokens_g)
tokens[my_token] = []
print(my_token)


if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))

# tokens
# token_id primary key auto-increment, token not null, exp_date ISO-data not null, host_id auto-increment can be null

# hosts_data
# host_id foreign key tokens(host_id), identifier not null, serial_number not null
