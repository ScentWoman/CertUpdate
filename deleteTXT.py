#!/usr/bin/env python3
#coding=utf-8

import os
import idna
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest

domain = idna.decode(os.getenv("DOMAIN"))
accessKeyID = os.getenv("ACCESSKEYID")
accessSecret = os.getenv("ACCESSSECRET")
apinode = "cn-shanghai"

client = AcsClient(accessKeyID, accessSecret, apinode)

request = DescribeDomainRecordsRequest()
request.set_accept_format('json')

request.set_DomainName(domain)

response = client.do_action_with_exception(request)
records = json.loads(str(response, encoding='utf-8'))
records = records["DomainRecords"]["Record"]

for r in records:
    if r["Type"] == "TXT" and r["RR"] == "_acme-challenge":
        RecordId = r["RecordId"]

        request = DeleteDomainRecordRequest()
        request.set_accept_format('json')

        request.set_RecordId(RecordId)

        response = client.do_action_with_exception(request)
        print(str(response, encoding='utf-8'))
