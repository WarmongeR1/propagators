#!/bin/bash
# Script para realizar las simulaciones.
# Contiene las llamadas necesarias para calcular los valores y mostrarlos
# a continuacion por pantalla.

clear
# Check last TLE's update
cd TLEs/

# Check if amateur.txt exist
if [ ! -f amateur.txt ]
then
	echo "Updating orbital elements database..."
	
	cd ..

	chmod +x update_tles.sh
	./update_tles.sh
    
fi

# Check file's date
file_month=`ls -Ald amateur.txt | awk '{print $6}'`
system_month=`date +"%m"`

file_day=`ls -Ald amateur.txt | awk '{print $7}'`
system_day=`date +"%d"`

cd ..

if [ "$file_month" = "jan" ]; then
	declare month=1
elif [ "$file_month" = "feb" ]; then
	declare month=2 
elif [ "$file_month" = "mar" ]; then
	declare month=3
elif [ "$file_month" = "apr" ]; then
        declare month=4
elif [ "$file_month" = "may" ]; then
        declare month=5
elif [ "$file_month" = "jun" ]; then
        declare month=6
elif [ "$file_month" = "jul" ]; then
        declare month=7
elif [ "$file_month" = "aug" ]; then
        declare month=8
elif [ "$file_month" = "ago" ]; then
		declare month=8
elif [ "$file_month" = "sep" ]; then
        declare month=9
elif [ "$file_month" = "oct" ]; then
        declare month=10
elif [ "$file_month" = "nov" ]; then
        declare month=11
elif [ "$file_month" = "dec" ]; then
        declare month=12
else
	echo "Invalid Month"
fi


if [ $month -lt $system_month ]; then

	echo "Updating orbital elements database..."

	chmod +x update_tles.sh
	./update_tles.sh

	echo "Database updated."
else
	if [ $file_day -lt $system_day ]; then

		echo "Updating orbital elements database..."

		chmod +x update_tles.sh
		./update_tles.sh

		echo "Database updated."
	else
		echo "Database updated."
	fi
fi

LOCATION=`awk 'NR==1' ~/.predict/predict.qth`
LATITUDE=`awk 'NR==2' ~/.predict/predict.qth`
LONGITUDE=`awk 'NR==3' ~/.predict/predict.qth`
ELEVATION=`awk 'NR==4' ~/.predict/predict.qth`

echo "In first place you must specify your location."
echo "Current location is: $LOCATION"
echo "Latitude: $LATITUDE"
echo "Longitude:  $LONGITUDE"
echo -e "Elevation: $ELEVATION\n" 

echo -e "Want to change it?"
CHANGES="No Yes"
select change in $CHANGES; do
	if [ "$change" = "Yes" ]; then
		# Absolut path because program need it.
		rm ~/.predict/predict.qth
		echo -e "New location: \c"
		read -e NEW_LOCATION
		echo "New location...: $NEW_LOCATION"
		echo $NEW_LOCATION > ~/.predict/predict.qth
		echo -e "Latitude: \c"
		read -e NEW_LATITUDE
		echo $NEW_LATITUDE >> ~/.predict/predict.qth
		echo -e "Longitude: \c"
		read -e NEW_LONGITUDE
		echo $NEW_LONGITUDE >> ~/.predict/predict.qth
		echo -e "Elevation: \c"
		read -e ELEVATION
		echo $ELEVATION >> ~/.predict/predict.qth
		break

	elif [ "$change" = "No" ]; then
		echo -e "Location $LOCATION approved!"
		break

	else
		echo "Invalid Selection."

	fi
done

echo "Specify simulation start time."
echo "================================================="

OPTIONSTIME="Now Another"
select opt_time in $OPTIONSTIME; do
        if [ "$opt_time" = "Now" ]; then
                echo -e "Simulation will start right now!\n"
		# Unix time
		DATE=`date +%s`
                break

        elif [ "$opt_time" = "Another" ]; then                
		echo -e "The starting date and time should be entered now."

		# Date
		echo -e "Day: \c"
		read -e DAY
		echo -e "Month: \c"
		read -e MONTH
		echo -e "Year: \c"
		read -e YEAR

		# Time
		echo -e "Hours (Two digits. 24 hours format.): \c"
		read -e HOURS
		echo -e "Minutes (Two digits): \c"
		read -e MINUTES
		echo -e "Seconds (Two digits): \c"
		read -e SECONDS
     
		echo -e "Time is: ...\n"           
		break
        else
                echo "Wrong chosen"
        fi
done

echo "Set the simulation's interval."
echo "================================================="


OPTIONSINTERVAL="1hour 1day user_defined"
select opt_interval in $OPTIONSINTERVAL; do
	if [ "$opt_interval" = "1hour" ]; then
		echo -e "1 hour time.\n"
		END_TIME=`expr $DATE + 3600`
		break

	elif [ "$opt_interval" = "1day" ]; then
		echo -e "1 day time.\n"
		END_TIME=`expr $DATE + 86400`
		break

	elif [ "$opt_interval" = "user_defined" ]; then
		echo -e "Set the simulation's range in seconds: \c"
		read -e USER_INTERVAL
		END_TIME=`expr $DATE + $USER_INTERVAL`
		break
	else
		echo ">>> Invalid Selection"
	fi
done
echo " "



echo "Choose a family!"
echo "================================================="
cd TLEs/

select d in *; do 
	FAMILY=$d
	break 
done

cp $FAMILY COPY$FAMILY

cd ..

# Extract satellite names
python get_names.py $FAMILY

# Predict data
echo " "
echo "predict data"	
chmod +x do_list2.sh
./do_list2.sh ~/TLEs/$FAMILY $FAMILY $DATE $END_TIME

# PyEphem data
python do_list.py ~/TLEs/$FAMILY $DATE $END_TIME

# pyorbital data
python do_list2.py ~/TLEs/$FAMILY $DATE $END_TIME

# Orbitron data
echo "Perfom Orbitron simulations"
#	wine "C:\\Program Files\Orbitron\Orbitron.exe"

# Request for STK data
echo "Perfom STK simulations"

echo " "
echo "$FAMILY family simulations done!"

python gui.py $FAMILY COPY$FAMILY

# Remove garbage
cd TLEs/

rm $FAMILY
rm xa*

mv COPY$FAMILY $FAMILY

cd ../predict
rm *

cd ../PyEphem
rm *

cd ../pyorbital
rm *

cd ..
