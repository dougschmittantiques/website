#!/bin/bash

echo $CERTBOT_VALIDATION > /tmp/$CERTBOT_TOKEN

FTP_PASSWORD=$(cat /tmp/out1.txt)

ftp -inv dougschmittantiques.com <<EOF
user
dsaadmin $FTP_PASSWORD
pasv
cd /public_html/wp/.well-known/acme-challenge/
lcd /tmp
mput $CERTBOT_TOKEN
bye
EOF
