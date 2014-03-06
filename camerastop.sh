sudo kill $(ps aux | awk '/raspistill/{print $2}')
