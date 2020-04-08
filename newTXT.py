#!/usr/bin/env python3
#coding=utf-8

import os
import sys
import idna
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest

domain = idna.decode(os.getenv("DOMAIN"))
accessKeyID = os.getenv("ACCESSKEYID")
accessSecret = os.getenv("ACCESSSECRET")
apinode = "cn-shanghai"

client = AcsClient(accessKeyID, accessSecret, apinode)

for r in sys.argv[1:]:
    request = AddDomainRecordRequest()
    request.set_accept_format('json')

    request.set_DomainName(domain)
    request.set_RR("_acme-challenge")
    request.set_Type("TXT")
    request.set_Value(str(r))

    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))
