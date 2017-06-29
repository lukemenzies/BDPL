#!/usr/bin/python
# ====================================================
# BDPL Inventory Script
# Written by Luke Menzies for the Born Digital Preservation Lab
# Indiana University
# Herman B. Wells Library  W501
# 1320 E 10th St
# Bloomington, IN 47405
# Last Updated 10/10/16 by Luke Menzies
# ====================================================

import os, time, hashlib, magic, Tkinter, math
from Tkinter import *
import tkMessageBox
from tkFileDialog import askdirectory, asksaveasfilename

# function to get folder path
def ask_folder(question):
    while True:
        Tk().withdraw()
        entry = ""
        entry = askdirectory(title = "%s" %question)
        if entry == "":
            quit = tkMessageBox.askyesno(message = "Quit?")
            if quit == True:
                exit()
            else:
                choice = False
        else:
            choice = tkMessageBox.askyesno(message = "You have chosen:\n%s\nIs this correct (y/n)?  " %entry)
        if choice == True:
            return entry

def ask_file():
    while True:
        ansfile = ""
        ansfile = asksaveasfilename(initialdir = destfolder, title = "Enter the name of the CSV file.", defaultextension = ".csv")
        if ansfile == "":
            quit = tkMessageBox.askyesno(message = "Quit?")
            if quit == True:
                exit()
            else:
                looksok = False
        else:
            looksok = tkMessageBox.askyesno(message="You have chosen:\n%s\nIs this correct (y/n)?  " %ansfile)
        if looksok == True:
            return ansfile

# function to generate md5
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# function to convert file sizes from bytes to larger denominations
def convertSize(size):
    if (size == 0):
        return '0B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size,1024)))
    p = math.pow(1024,i)
    s = round(size/p,2)
    return '%s %s' % (s,size_name[i])

# Main Part of the Program
quit = False
# asks for object folder, destination folder, and csv file
objectfolder = ask_folder("What folder would you like to analyze?")
destfolder = ask_folder("In what folder will the results be placed?")
destfile = ask_file()

# sets up the csv file and comparison file
csvfile = open(destfile, "w")
csvfile.write("#,file_name,size,file_type,c_datetime,last_modified,last_accessed,md5,md5_datetime,file_path,")
csvfile.write("additional =>,mode,ino,device,nlink,uid,gid\n")
compfile = open(os.path.join(destfolder, "Compare%s.txt" %time.strftime("%m%d_%H%M%S")), "w")

# walks each file in the object folder and writes info to the csv file and comparison file
counter = 0
for root, dirs, files in os.walk(objectfolder):
    for name in files:
        counter = counter + 1
        rownum = str(counter)
        filepathname = os.path.join(root, name)
        statinfo = os.stat(filepathname)
        filesize = statinfo[6]
        convsize = convertSize(filesize)
        filemime = magic.from_file(filepathname, mime=True)
        filectime = time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(statinfo.st_ctime))
#       note: on a Windows system, ctime is "date created" but on Unix it is
#       "change time", i.e. the last time the metadata was changed.
        modifdate = time.strftime("%Y.%m.%d %H:%M:%S",time.localtime(statinfo.st_mtime))
        accessdate = time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(statinfo.st_atime))
        md5hash = md5(filepathname)
        runtime = time.strftime("%Y.%m.%d %H:%M:%S")
        filemode = str(statinfo.st_mode)
        fileino = str(statinfo.st_ino)
        filedevice = str(statinfo.st_dev)
        filenlink = str(statinfo.st_nlink)
        fileuser = str(statinfo.st_uid)
        filegroup = str(statinfo.st_gid)
        compfile.write("%s, " %name + "%s\n" %md5hash)
        csvfile.write("%s," %rownum + "\"%s\"," %name + "%s," %convsize + "\"%s\"," %filemime + "%s," %filectime + "%s," %modifdate + "%s," %accessdate + "%s," %md5hash + "%s," %runtime + "\"%s\"," %filepathname)
        csvfile.write(" ,%s," %filemode + "%s," %fileino + "%s," %filedevice + "%s," %filenlink + "%s," %fileuser + "%s\n" %filegroup)
compfile.close()
csvfile.close()
done = tkMessageBox.askokcancel(message = "All Done!")
if done == True:
    exit()
else:
    exit()
