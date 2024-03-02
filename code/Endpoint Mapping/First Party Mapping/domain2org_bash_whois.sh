INPUT=temp.csv
OUTPUT=domain2org.csv
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
touch $OUTPUT
while read domain
do
	#echo -n "$domain, "  >> OUTPUT
	#whois $domain | grep 'Registrant Organization' | awk '{print substr($0, 26)}' >> OUTPUT
	org=$(whois $domain | grep 'Registrant Organization' | awk '{print substr($0, 26)}')
	echo "$domain, $org" >> $OUTPUT
	sleep 1
done < $INPUT
IFS=$OLDIFS