# Print the last two lines of each Kihi-02 csv file
# using ideas from https://stackoverflow.com/questions/890262/integer-ascii-value-to-character-in-bash-using-printf

python3 channelList.py

#for Chan in S T U V ; do echo $Chan ; tail -2 # #9e553100-4086-11ea-84bb-8f71124cfdfb_$Chan.csv ; echo ; done

for Chan in S T U V ; do
   Num=$( printf "%d" "'${Chan}" ) ;
   Num=`expr $Num - 64`
   echo $Chan, \($Num\) ; 
   tail -2 9e553100-4086-11ea-84bb-8f71124cfdfb_$Chan.csv ; 
   echo
   done

