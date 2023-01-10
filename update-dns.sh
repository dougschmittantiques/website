#!/bin/bash

FTP_PASSWORD=`cat /tmp/out1.txt`

DOMAIN_SERIAL=`curl --get https://server3.iqnecthosting.com:2083/execute/DNS/parse_zone?zone=dougschmittantiques.com -u "dsaadmin:$FTP_PASSWORD" | jq '.data[] | select(.record_type == "SOA") | .data_b64[2] | @base64d |tonumber'`

curl --get https://server3.iqnecthosting.com:2083/execute/DNS/mass_edit_zone -u "dsaadmin:$FTP_PASSWORD" --data "zone=dougschmittantiques.com" --data "serial=$DOMAIN_SERIAL" --data "add={\"dname\":\"_acme-challenge\",\"ttl\":3600,\"record_type\":\"TXT\",\"data\":[\"$CERTBOT_VALIDATION\"]}" 
