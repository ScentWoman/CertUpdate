#!/usr/bin/env python3
#coding=utf-8

import os
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcdn.request.v20180510.SetDomainServerCertificateRequest import SetDomainServerCertificateRequest

domain = os.getenv("DOMAIN")
accessKeyID = os.getenv("ACCESSKEYID")
accessSecret = os.getenv("ACCESSSECRET")
apinode = "cn-shanghai"
client = AcsClient(accessKeyID, accessSecret, apinode)

with open(os.path.expanduser("~") + "/.acme.sh/" + domain + "_ecc/fullchain.cer") as f:
    certificate = f.read()
privateKey = os.getenv("PRIVATEKEY")

request = SetDomainServerCertificateRequest()
request.set_accept_format('json')

request.set_DomainName("." + domain)
request.set_ServerCertificateStatus("on")
request.set_CertName("wxs-wildcard")
request.set_CertType("upload")
request.set_ServerCertificate(certificate)
request.set_PrivateKey(privateKey)
request.set_ForceSet("1")

response = client.do_action_with_exception(request)
print(str(response, encoding='utf-8'))
