#!\Python27\python
# This program was created by Luke Menzies for the Media Services
# Legacy PC Games collection.
#      Born-Digital Preservation lab
#      Wells Library, Room 501
#      Indiana University
#      1320 E 10th St.
#      Bloomington, IN 47405
#      lmenzies@indiana.edu
#
# This is a script for importing Users' saved games from the Desktop
# to the appropriate saved-games folders on the system. It also
# exports Users' saved games from the system to a SavedGames folder
# on the Desktop. Users must transfer this folder to Box.iu.edu or to
# a removable disk/drive in order to keep their saved games upon logout.
# Created 4/10/2017
# Last updated 5/10/2017 by LM
"""
* fix it so it can handle individual saved games, e.g. Doom
"""

import csv, os, shutil
from Tkinter import *
import tkMessageBox

# establishes the widget
class Checks(Frame):
    def __init__(self, parent=None, picks=[]):
        Frame.__init__(self, parent)
        self.vars = []
        numbs = 0
        rownum = 1
        cols = 0
        for pick in picks:
            if numbs >= 4:
                rownum = rownum + 1
                numbs = 0
                cols = 0
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var, fg='black', bg='gainsboro', relief=RAISED, bd=2, font=('Times', 18))
            chk.grid(column=cols, pady=10, padx=10, row=rownum, sticky=W)
            numbs = numbs + 1
            cols = cols + 1
            self.vars.append(var)

    def state(self):
        frmap = map((lambda var: var.get()), self.vars)
        return frmap

# figures out which game names to put in the widget based on GamePaths.csv
def frame_list(gamepaths):
    frame = []
    with open(gamepaths, 'r') as gpaths:
        reading = csv.reader(gpaths)
        for row in reading:
            gametuple = tuple(row)
            frame.append(gametuple[0])
    return frame

# This generates the Instructions window, using the file C:\PCGames\05IUGameSaver\Instructions.txt
def instruct():
    new = Tk()
    w = 850
    h = 450
    ws = new.winfo_screenwidth() # width of the screen
    hs = new.winfo_screenheight() # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    new.geometry('%dx%d+%d+%d' %(w, h, x, y))
    new.title('IU Game Saver')
    new.configure(bg='firebrick4', pady=30, padx=30)
    new.grid_propagate(False)
    new.grid_rowconfigure(0, weight=1)
    new.grid_columnconfigure(0, weight=1)
    txt = Text(new, relief=SUNKEN, bd=4, bg='AntiqueWhite1')
    txt.config(font=('Times', 14), wrap='word', padx=10, pady=10)
    txt.grid(row=0, column=0, sticky='nsew')
    scroller = Scrollbar(new, orient='vertical', command=txt.yview)
    scroller.grid(row=0, column=1, sticky='nsew')
    txt['yscrollcommand'] = scroller.set
    OK = Button(new, command=new.destroy, text='OK')
    OK.configure(font=('Arial', 15), bg='gainsboro', relief=RAISED, bd=4)
    OK.grid(row=1, column=0, sticky='nsew')
    instructions = '\\PCGames\\05IUGameSaver\\Instructions.txt'
    with open(instructions) as inst:
        quote = inst.read()
        txt.insert(END, quote)

# This deletes destination files and replaces them with source files.
def transfiles(src, dst):
    if not os.path.exists(src):
        tkMessageBox.showwarning(message = "The source directory %s does not exist!" %src)
        return
    if (os.listdir(src) == ['.DS_Store']) or (os.listdir(src) == []):
        tkMessageBox.showwarning(message = "The source directory %s is empty!" %src)
        return
    if not os.path.exists(dst):
        os.mkdir(dst)
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst, symlinks=False, ignore=None)

# imports saved games files for checked games from the SavedGames folder on the Desktop
def imp_games(gamepaths, homevar):
    cklist = list(lst.state())
    glist = ''
    with open(gamepaths, 'r') as gpaths:
        reading = csv.reader(gpaths)
        val = 0
        for row in reading:
            if cklist[val] == 1:
                dogame = tuple(row)
                glist = glist + '   *   ' + dogame[0] + '\n'
            val = val + 1
    savfolder = os.path.join(homevar, "Desktop\\SavedGames")
    if not os.path.exists(savfolder):
        tkMessageBox.showwarning(message = "You do not have any games to import.\nCould not find the Desktop\SavedGames folder.")
        return
    cont = tkMessageBox.askyesno(message = "This will import saved games from\nthe \"SavedGames\" folder on the Desktop\nfor the following games:\n\n%s\nAny old games already present will be overwritten.\n\nDo you wish to proceed?\n" %glist)
    if cont == False:
        return
    else:
        with open(gamepaths, 'r') as gpaths:
            reading = csv.reader(gpaths)
            val = 0
            for row in reading:
                if cklist[val] == 1:
                    dogame = tuple(row)
                    name = dogame[0]
                    path1 = dogame[2]
                    path2 = dogame[3]
                    if dogame[1] == "home":
                        dstfolder = os.path.join(homevar, path1)
                    else:
                        dstfolder = path1
                    srcfolder = os.path.join(homevar, path2)
                    transfiles(srcfolder, dstfolder)
                val = val + 1
    return

# exports only the saved games for the games checked in the widget
def exp_games(gamepaths, homevar):
    cklist = list(lst.state())
    glist = ''
    with open(gamepaths, 'r') as gpaths:
        reading = csv.reader(gpaths)
        val = 0
        for row in reading:
            if cklist[val] == 1:
                dogame = tuple(row)
                glist = glist + '   *   ' + dogame[0] + '\n'
            val = val + 1
    savfolder = os.path.join(homevar, "Desktop\\SavedGames")
    if not os.path.exists(savfolder):
        os.mkdir(savfolder)
    cont = tkMessageBox.askyesno(message = "This will transfer your saved games\nto the \"SavedGames\" folder on the\nDesktop for the following games:\n\n%s\nAny old games already there will be overwritten.\n\nDo you wish to proceed?\n" %glist)
    if cont == False:
        return
    else:
        with open(gamepaths, 'r') as gpaths:
            reading = csv.reader(gpaths)
            val = 0
            backup = False
            for row in reading:
                if cklist[val] == 1:
                    dogame = tuple(row)
                    name = dogame[0]
                    path1 = dogame[2]
                    path2 = dogame[3]
                    filetypes = dogame[4]
                    if dogame[1] == "sys":
                        srcfolder = path1
                        backup = True
                        backsrc = dogame[5]
                    else:
                        srcfolder = os.path.join(homevar, path1)
                    dstfolder = os.path.join(homevar, path2)
                    transfiles(srcfolder, dstfolder)
                    if backup == True:
                        transfiles(backsrc, srcfolder)
                        backup = False
                val = val + 1
    return

root = Tk()
# the following sets the dimensions of the root window and centers it on the screen
gamepaths = "\\PCGames\\05IUGameSaver\\GamePaths.csv"
# gamepaths = "/Users/lmenzies/Documents/1Docs2017/Python2017/IUGameSaver/GamePaths.csv"
homevar = os.environ['HOMEPATH']
# homevar = os.environ['HOME']
with open(gamepaths, 'r') as gpaths:
    reading = csv.reader(gpaths)
    howmanygames = 0
    for row in reading:
        howmanygames = howmanygames + 1
w = 860 # width for the Tk root
h = ((howmanygames * 20) + 120) # height for the Tk root
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' %(w, h, x, y))
root.title('IU Game Saver')
root.configure(bg='firebrick4', bd=4)
#
fr = frame_list(gamepaths)
lst = Checks(root, fr)
lst.pack(side=TOP,  fill=X)
lst.config(relief=RAISED, bd=6, bg='AntiqueWhite2')
# buttons on root window
wa = Button(root, text='Import (from Desktop to Games)', command= lambda: imp_games(gamepaths, homevar), font=('Arial', 15), bg='gainsboro', relief=RAISED, bd=4)
wa.pack(side=LEFT, expand=YES)
wd = Button(root, text='Help', command=instruct, font=('Arial', 15), bg='AntiqueWhite2', relief=SUNKEN, bd=2)
wd.pack(side=LEFT, expand=YES)
wc = Button(root, text='Export (from Games to Desktop)', command= lambda: exp_games(gamepaths, homevar), font=('Arial', 15), bg='gainsboro', relief=RAISED, bd=4)
wc.pack(side=RIGHT, expand=YES)
wb = Button(root, text='Quit', command=root.quit, font=('Arial', 15), bg='AntiqueWhite2', relief=SUNKEN, bd=2)
wb.pack(side=RIGHT)
root.mainloop()
