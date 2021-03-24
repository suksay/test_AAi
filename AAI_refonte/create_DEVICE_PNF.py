from aai_requests import *
import json
from jinja2 import Environment, FileSystemLoader
from parameters import *

from parameters import _MW_INVARIANT_ID_, _HUAWEI_MW_VERSION_ID_, _NEC_MW_VERSION_ID_
devices = {
    "0x346ac21d93b9": {
        "address": "172.20.183.162",
        "hostname": "950-1-REN",
        "vendor": "huawei"
    },
    "0x346ac25f1b5c": {
        "address": "172.20.183.163",
        "hostname": "950-2-REN",
        "vendor": "huawei"
    },
    "0x2c9d1e5d81a9": {
        "address": "172.20.183.164",
        "hostname": "380H-1-REN",
        "vendor": "huawei"
    },
    "0x2c9d1e5ada05": {
        "address": "172.20.183.165",
        "hostname": "380H-2-REN",
        "vendor": "huawei"
    },
    "0x8cdf9d4efe40": {
        "address": "172.20.183.179",
        "hostname": "iP-400",
        "vendor": "nec-ipa"
    },
    "0x8cdf9dbc1120": {
        "address": "172.20.183.185",
        "hostname": "vr4_rel2.8",
        "vendor": "nec-vr"
    }
}
env = Environment(loader=FileSystemLoader('./aai_templates/'))


### Save Host in AAI Database ###

devices_model = env.get_template('device.json') 
pnf_model = env.get_template('pnf.json') 


for id in devices:
    #-----  Device and  PNF associate ------#
    URL_DEVICE = URL_GET_DEVICES + '/device/{device_id}'.format(device_id = id )
    URL_PNF = URL_GET_PNFS + '/pnf/{pnf_name}'.format(pnf_name = id )

    #Data normalize
    device_data = json.loads(devices_model.render(device_id=id, device_name=devices[id]['hostname'], vendor=devices[id]['vendor'], ipv4=devices[id]['address'], description="We use model-customization-id for NE ID ", model_invariant_id=_MW_INVARIANT_ID_, model_version_id=_NEC_MW_VERSION_ID_))
    pnf_data = json.loads(pnf_model.render(device_id=id, device_name=devices[id]['hostname'], selflink=URL_DEVICE, equip_type="microwave", vendor=devices[id]['vendor'], model_invariant_id=_MW_INVARIANT_ID_, model_version_id=_NEC_MW_VERSION_ID_))

    #print(device_data)
    #print(pnf_data)
    #input("Wait")
    #Requests
    req_device = put_request(URL_DEVICE, device_data)
    req_pnf = put_request(URL_PNF, pnf_data)
