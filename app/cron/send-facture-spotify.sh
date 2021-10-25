TOMORROW=`date -v+1d +%d`

# See if tomorrow's day is less than today's
if [ $TOMORROW -eq 01 ]; then
	cd /Users/ndoan/PersoProj/automatically-send-facture-spotify/app/main
	/Users/ndoan/Library/Caches/pypoetry/virtualenvs/automatically-send-facture-spotify-6QxwvquE-py3.7/bin/python main.py
	exit
fi