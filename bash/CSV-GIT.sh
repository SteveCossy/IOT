# Send the current files to GitHub
for DIR in /home/cosste/CSVfiles /home/cosste/CayMQTT
do
   cd $DIR
   git pull
   git add .
   git commit -m "`date +%F_%T`"
   git push
done

