#!/bin/bash
# =========================================
# Script for Imaging Large Disks Remotely
# Born Digital Preservation Lab at Indiana University
# Heidi Dowding, Brian Wheeler, Luke Menzies
# 06-07-2016
# last updated 06-14-2016 by Luke Menzies
# =========================================
# User is prompted to enter:
# 	devname - the device to be imaged (ex. dev/sdb1)
# 	servername - the username and server on which to create the image (ex. user@server.com)
#	bdplname - BDPL Accession Number (ex. UAC0520160200) 
#	remotedir - the directory on the server where the image will be placed
# User is then asked whether to use ~/Documents/1received or another directory on the BDPL computer
#	localdir - Local Path to Md5's (ex. ~/Documents/1received)
# Script then creates subdirectories for the image and the checksums, based on the BDPL accession number.
# Finally, it asks to make a comparison between the locally stored checksum and a checksum of the remotely stored image. 
#
echo "Please enter the device to be imaged (ex. sdb1):"
echo "(Do not use a final slash /)"
read devname
echo "What is the remote server (ex. user@server.com)?"
read servername
echo "Please enter the BDPL accession number (ex. UAC0520160200):"
read bdplname
echo "Enter the directory on the remote server where the new item will go (ex. ~/BDPL/Images):"
echo "Note: This script will create the subdirectory, $bdplname, in this location."
echo "(Do not use a final slash /)"
read remotans
remotedir=`ssh $servername "echo $remotans"`
# Confirms location of BDPL local images, checksums, etc.
echo "Would you like the checksums placed in ~/Documents/1received (enter y or n)?"
while true
do
  read ans
  case $ans in
    [yY]* ) localdir=/home/bcadmin/Documents/1received
	break;;
    [nN]* ) echo "Please enter the path to your local directory (ex. ~/Documents/1received):"
	echo "Note: This script will create the subdirectory, $bdplname, in this location."	
	echo "(Do not use a final slash /)"
	read diranswer
	localdir=`sh -c "echo $diranswer"`
	break;;
    * ) echo "Please enter y or n.";;
  esac
done
# Makes a directory on the local BDPL computer
mkdir -p $localdir/$bdplname
# Makes a directory on the remote server
ssh $servername "mkdir -p $remotedir/$bdplname"
# Main command
dd if=/dev/$devname | \
		tee >(md5sum > $localdir/$bdplname/$bdplname.uncomprssd.md5
		) > >(gzip | \
				tee >(ssh $servername "cat > $remotedir/$bdplname/$bdplname.dd.gz"
				) > >(md5sum > $localdir/$bdplname/$bdplname.comprssd.md5))
# Asks to compare checksums
echo "Would you like to compare the local checksum with the checksum of the remote compressed image (timeout after 5 tries or 10min.)?"
n=1
while (( $n<=5 ))
do
  read -t 10 ans2
  case $ans2 in
    [yY]* ) diff -u $localdir/$bdplname/$bdplname.comprssd.md5 <(ssh $servername "md5sum $remotedir/$bdplname/$bdplname.dd.gz")
	break;;
    [nN]* ) echo "Ok, goodbye."
	exit;;
    * ) echo "Please enter y or n.";;
  esac
  n=$(( n+1 ))
done
if (( $n>=6 )) 
  then
	echo "Timing out. Goodbye."
fi
exit
