sleep 15

outputFile=/tmp/userList.out

userList=`users`
echo ${#userList} > $outputFile

if [ ${#userList} != "0" ]  # More than zero users logged in
then
        sudo echo `date +%y%m%d%H%M` Logged in user - aborting script  >> $outputFile
else
        sudo echo `date +%y%m%d%H%M` Shutting down >> $outputFile
#        sudo poweroff
fi

