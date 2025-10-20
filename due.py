from AesEverywhere import aes256
import base64
import requests
import json


def infosimples(keynfe, senha):
    url = 'https://api.infosimples.com/api/v2/consultas/receita-federal/nfe'

    pkcs12_cert = aes256.encrypt(base64.b64encode(open("/ssh/AgroCrestani.pfx", "rb").read()).decode(),
                                      "QIpKCTOWkvYKMReYoi9c08DS8AUG1flXsPBsof-x")
    pkcs12_pass = aes256.encrypt(f"{senha}", "QIpKCTOWkvYKMReYoi9c08DS8AUG1flXsPBsof-x")

    args = {
        "pkcs12_cert": pkcs12_cert,
        "pkcs12_pass": pkcs12_pass,
        "token": "SEiDpm7AXh5rlGGf1w6r17lb5KCa8M51DQQzj6sy",
        "nfe": f"{keynfe}"
    }

    response = requests.post(url, args)
    response = response.text
    return response

if __name__ == '__main__':
    nfe = infosimples('51241103262185000109550010000304361871907181', 'Crestani123')
    nfe = json.loads(nfe)
    status_code = nfe['code']
    mensagem = nfe['code_message']