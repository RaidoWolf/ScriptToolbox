echo "MAKE SURE YOU KNOW WHAT YOU'RE DOING! THIS SCRIPT DELETES FILES!"
if [ "$1" != "" ]; then
    dir="$1"
else
    echo "directory in which to delete old files:"
        read dir
fi
if [ "$2" != "" ]; then
    days="$2"
else
   	echo "delete files older than how many DAYS?"
        read days
fi
echo "is this correct: (y/n/t) (t means test)"
echo "Delete files in:"
echo "$dir"
echo "While your working directory is:"
echo "$pwd"
echo "That are older than:"
echo "$days days"
   	read correct
   	if [ "$correct" == "y" ]; then
       echo "Deleting files..."
       find $dir -mtime +$days -type f -delete
       echo "Complete!"
   	elif [ "$correct" == "n" ]; then
        echo "Exiting..."
        exit
   	elif [ "$correct" == "t" ]; then
        echo "##### THE FOLLOWING WOULD BE DELETED #####"
        find $dir -mtime +$days -type f
        echo "##### THE PRECEDING WOULD BE DELETED #####"
   	else
        echo "Invalid option (must be \"y\" (yes), \"n\" (no), or \"t\" (test)). Exiting."
        exit
   	fi
exit
