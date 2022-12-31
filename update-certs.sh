#!/bin/bash

echo $CERTBOT_VALIDATION > /tmp/$CERTBOT_TOKEN

ftp -inv dougschmittantiques.com <<EOF
user
dsaadmin $FTP_PASSWORD
pasv
cd /public_html/.well-known/acme-challenge/
lcd /tmp
mput $CERTBOT_TOKEN
bye
EOF
