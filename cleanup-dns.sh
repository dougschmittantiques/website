#!/bin/bash

FTP_PASSWORD=`cat /tmp/out1.txt`

DOMAIN_SERIAL=`curl --get https://server3.iqnecthosting.com:2083/execute/DNS/parse_zone?zone=dougschmittantiques.com -u "dsaadmin:$FTP_PASSWORD" | jq '.data[] | select(.record_type == "SOA") | .data_b64[2] | @base64d |tonumber'`
DOMAIN_INDEX=`curl --get https://server3.iqnecthosting.com:2083/execute/DNS/parse_zone?zone=dougschmittantiques.com -u "dsaadmin:$FTP_PASSWORD" | jq '.data[] | select(.dname_b64 == "X2FjbWUtY2hhbGxlbmdl") | .line_index'`

curl --get https://server3.iqnecthosting.com:2083/execute/DNS/mass_edit_zone -u "dsaadmin:$FTP_PASSWORD" --data "zone=dougschmittantiques.com" --data "serial=$DOMAIN_SERIAL" --data "remove=$DOMAIN_INDEX" 
