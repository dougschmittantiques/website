#!/bin/bash

echo "Certbot Validation: $CERTBOT_VALIDATION"
echo "Certbot Domain: $CERTBOT_DOMAIN"
echo "Certbot Token: $CERTBOT_TOKEN"
echo "Certbot Remaining Challenges: $CERTBOT_REMAINING_CHALLENGES"

FTP_PASSWORD=`cat /tmp/out1.txt`

DOMAIN_INDEXES=`curl --get https://server3.iqnecthosting.com:2083/execute/DNS/parse_zone?zone=dougschmittantiques.com -u "dsaadmin:$FTP_PASSWORD" | jq '.data[] | select(.dname_b64 == "X2FjbWUtY2hhbGxlbmdl") | .line_index'`

for DOMAIN_INDEX in $DOMAIN_INDEXES
do
    DOMAIN_SERIAL=`curl --get https://server3.iqnecthosting.com:2083/execute/DNS/parse_zone?zone=dougschmittantiques.com -u "dsaadmin:$FTP_PASSWORD" | jq '.data[] | select(.record_type == "SOA") | .data_b64[2] | @base64d |tonumber'`
    CURL_STATUS=`curl --get https://server3.iqnecthosting.com:2083/execute/DNS/mass_edit_zone -u "dsaadmin:$FTP_PASSWORD" --data "zone=dougschmittantiques.com" --data "serial=$DOMAIN_SERIAL" --data "remove=$DOMAIN_INDEX"`

    if [ "$CURL_STATUS" = "0" ]; then
        exit 1
    fi
done

exit 0