INPUT=temp.csv
OUTPUT=domain2org.csv
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
touch $OUTPUT
while read domain
do
	$(openssl s_client -connect $domain:443 -showcerts  </dev/null | openssl x509 -outform pem > cert.pem)
	org=$(openssl x509 -in cert.pem -noout -subject -nameopt sep_multiline | grep 'O=' | awk '{print substr($0, 7)}')
	echo "$domain, $org" >> $OUTPUT
done < $INPUT
IFS=$OLDIFS