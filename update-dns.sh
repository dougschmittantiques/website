#!/bin/bash

echo "Certbot Validation: $CERTBOT_VALIDATION"
echo "Certbot Domain: $CERTBOT_DOMAIN"
echo "Certbot Token: $CERTBOT_TOKEN"
echo "Certbot Remaining Challenges: $CERTBOT_REMAINING_CHALLENGES"

FTP_PASSWORD=`cat /tmp/out1.txt`

DOMAIN_SERIAL=`curl --get https://server3.iqnecthosting.com:2083/execute/DNS/parse_zone?zone=dougschmittantiques.com -u "dsaadmin:$FTP_PASSWORD" | jq '.data[] | select(.record_type == "SOA") | .data_b64[2] | @base64d |tonumber'`

RESULT=`curl --get https://server3.iqnecthosting.com:2083/execute/DNS/mass_edit_zone -u "dsaadmin:$FTP_PASSWORD" --data "zone=dougschmittantiques.com" --data "serial=$DOMAIN_SERIAL" --data "add={\"dname\":\"_acme-challenge\",\"ttl\":3600,\"record_type\":\"TXT\",\"data\":[\"$CERTBOT_VALIDATION\"]}"`

echo $RESULT

VALUE_GOTTEN=`dig -t txt _acme-challenge.dougschmittantiques.com +short`

echo "DNS Value: $VALUE_GOTTEN"

CURL_STATUS=`echo $RESULT | jq .status`

echo "CURL_STATUS: $CURL_STATUS"

if [ "$CURL_STATUS" = "1" ]; then
    exit 0
else
    exit 1
fi

