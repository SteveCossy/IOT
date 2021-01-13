 #!/bin/bash

if [ "$#" -eq  "0" ]
   then
     echo Syntax: one of
     echo source $0 r
     echo source $0 s
   else
     if [ "$1" == "r" ]
     then
	echo rebooting!
	action="sudo reboot"
     else
       if [ "$1" == "s" ]
       then
          echo shutting down!
	  action="sudo poweroff"
       else
          echo Invalid letter
       fi
     fi
     sleep 5 && $action &
     echo Exiting
     exit
   fi

