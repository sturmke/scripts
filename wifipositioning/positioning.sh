while true
do
var=0
l319=0
l320=0
gang=0
airmon=0
portal=0
i=0
for i in 1 2 3 4
do
        sudo iwlist wlan0 scan | egrep "Address:|ESSID:|Quality=" | cut -d: -f2- | tr -d ' ' > $1
        var=$(bash /home/pi/wifipositioning/script319 $1)
        l319=$(bc -l <<< "scale=2;($l319+$var)")
        var=$(bash /home/pi/wifipositioning/script320 $1)
        l320=$(bc -l <<< "scale=2;($l320+$var)")
        var=$(bash /home/pi/wifipositioning/scriptAirmon $1)
	airmon=$(bc -l <<< "scale=2;($airmon+$var)")
	var=$(bash /home/pi/wifipositioning/scriptPortal $1)
	portal=$(bc -l <<< "scale=2;($portal+$var)")
done
l319=$(bc -l <<< "scale=2;($l319/4)*13.5")
l320=$(bc -l <<< "scale=2;($l320/4)*13.5")
gang=$(bc -l <<< "scale=2;($gang/4)*13.5")
portal=$(bc -l <<< "scale=2;($portal/4)*13.5")
airmon=$(bc -l <<< "scale=2;($airmon/4)*13.5")
echo $portal","$airmon","$l319","$l320 > /usr/share/nginx/www/file.txt
rm $1
sleep 1
done
