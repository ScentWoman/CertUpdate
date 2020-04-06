#!/usr/bin/env python3
#coding=utf-8

import os
import sys
import idna
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
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

count = 0
for r in records:
    if r["Type"] == "TXT" and r["RR"] == "_acme-challenge":
        RecordId = r["RecordId"]
        count = count+1
        if count == len(sys.argv):
            continue

        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')
        request.set_RecordId(RecordId)
        request.set_RR("_acme-challenge")
        request.set_Type("TXT")
        request.set_Value(str(sys.argv[count]))
        response = client.do_action_with_exception(request) 
        print(str(response, encoding='utf-8'))
        print("Update TXT RecordId="+RecordId, "to", "\""+str(sys.argv[count])+"\"")
