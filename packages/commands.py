import tkinter as tk
import logging
import webbrowser
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import os
import datetime
import shutil
from tkinter import *
from tkinter import filedialog

# ______________________________________________________________________________
# Constants
new = 1
url = "https://eoric.uenr.edu.gh/wp-content/uploads/2022/03/GEONETCAST-Data-Products-2022.pdf"

logger = logging.getLogger(__name__)


# ______________________________________________________________________________
# Functions
def doNothing():
    print("nothing to do")
    logger.log(logging.INFO, "Nothing to do")


def openweb():
    webbrowser.open(url, new=new)


def view_logs():
    View_Window = tk.Tk()
    View_Window.title('Log Messages')
    View_Window.geometry('1360x500')
    View_Window.iconbitmap(r"eoriclogo.ico")
    log = ScrolledText(View_Window, width=167, height=30)
    log.grid(column=0, row=0)


def about_info():
    tk.messagebox.showinfo('About', 'Version 1.0')


def tbox_select_all(tbox_list):
    for i in tbox_list:
        if not i.instate(['selected']):
            i.invoke()


def tbox_deselect_all(tbox_list):
    for i in tbox_list:
        if i.instate(['selected']):
            i.invoke()


def more_info(title, path):
    View_Window = tk.Tk()
    View_Window.title(title)
    View_Window.geometry('1360x850')
    View_Window.iconbitmap(r"eoriclogo.ico")
    log = ScrolledText(View_Window, width=169, height=50)
    log.grid(column=0, row=0)

    tf = open(path, 'r')  # or tf = open(tf, 'r')
    data = tf.read()
    log.insert(END, data)
    tf.close()


def epsg_info():
    head = 'A1C-EPS-G Channel Information'
    pth = 'info/epsg.txt'
    more_info(head, pth)


def geo3_info():
    head = 'A1C-GEO-3 Channel Information'
    pth = 'info/geo3.txt'
    more_info(head, pth)


def geo4_info():
    head = 'A1C-GEO-4 Channel Information'
    pth = 'info/geo4.txt'
    more_info(head, pth)


def rds1_info():
    head = 'A1C-RDS-1 Channel Information'
    pth = 'info/rds1.txt'
    more_info(head, pth)


def saf1_info():
    head = 'A1C-SAF-1 Channel Information'
    pth = 'info/saf1.txt'
    more_info(head, pth)


def saf2_info():
    head = 'A1C-SAF-2 Channel Information'
    pth = 'info/saf2.txt'
    more_info(head, pth)


def tpc1_info():
    head = 'A1C-TPC-1 Channel Information'
    pth = 'info/tpc1.txt'
    more_info(head, pth)


def tpc5_info():
    head = 'A1C-TPC-5 Channel Information'
    pth = 'info/tpc5.txt'
    more_info(head, pth)


def tpc6_info():
    head = 'A1C-TPC-6 Channel Information'
    pth = 'info/tpc6.txt'
    more_info(head, pth)


def tpg1_info():
    head = 'A1C-TPG-1 Channel Information'
    pth = 'info/tpg1.txt'
    more_info(head, pth)


# ______________________________________________________________________________
def sort(sourcePath, desPath, channels):
    global failed, success, desFilePath, channel
    logger.info('Sorting starting...')
    for index in channels:

        sourceOverwrite = True
        name, ext, folder, channel = channels[index].values()
        # print(path)

        for r, d, f in os.walk(sourcePath):
            failed = []
            success = 0
            for file in f:
                if name and ext in file:
                    # print(file, " | ", folder, " | ", channel, " | ", 'exists')
                    filePath = os.path.join(r, file)
                    desFolderPath = desPath + "/" + channel
                    if not os.path.exists(desFolderPath):
                        os.makedirs(desFolderPath)

                    folderPath = os.path.join(desFolderPath, folder)
                    # print(folderPath)
                    if not os.path.exists(folderPath):
                        # print("Creating " + folder + '...')
                        msg = "Creating " + folder + '...'
                        logger.log(logging.WARNING, msg)
                        os.makedirs(folderPath)
                    modTime = datetime.datetime.fromtimestamp(os.path.getmtime(filePath))

                    FolderName = str(modTime.year) + str(modTime.month).zfill(2)
                    FolderPath = os.path.join(folderPath, FolderName)
                    # print(FolderPath)
                    # msg = FolderPath
                    # logger.log(logging.INFO, msg)

                    # Check if folder exists, else make it
                    if not os.path.exists(FolderPath):
                        os.makedirs(FolderPath)
                    # print (file)

                    try:
                        desFilePath = os.path.join(FolderPath, file)
                        desFileSize = os.path.getsize(desFilePath)
                        srcFileSize = os.path.getsize(filePath)

                        if os.path.exists(desFilePath) and (desFileSize == srcFileSize):

                            # print('The file: \n' + file + '\n already exists in the destination')
                            # print('.\nDeleting duplicate at source...')
                            # msg = 'The file: \n' + file + '\n already exists in the destination' + '.\nDeleting duplicate at source...'
                            # logger.log(logging.INFO, msg)

                            os.remove(filePath)

                            # Check if file is gone
                            if not os.path.exists(filePath):
                                # print('Duplicate deleted.\n\n')
                                continue
                            else:
                                # print('Duplicate deletion failed for')
                                # print(file)
                                # print('/n/n')
                                msg = 'Duplicate deletion failed for \n' + file + '/n/n'
                                logger.log(logging.WARNING, msg)
                                failed.append(file)
                        # If duplicate files exist, use the sourceOvewrite to select precedence
                        elif os.path.exists(desFilePath) and (desFileSize != srcFileSize):

                            if sourceOverwrite:

                                # Use copy2 instead of copy or copyfile to preserve file metadata
                                # http://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
                                # print('Copying.. ' + str(file))
                                msg = 'Copying.. ' + str(file)
                                logger.log(logging.INFO, msg)
                                shutil.copy2(filePath, desFilePath)
                                success += 1
                                # print('Done.')
                                msg = 'Done'
                                logger.log(logging.INFO, msg)

                                # print('Deleting source file...')
                                # msg = 'Deleting source file...'
                                # logger.log(logging.INFO, msg)
                                os.remove(filePath)

                                # Check if file is gone
                                if not os.path.exists(filePath):
                                    # print('Source file deleted.\n\n')
                                    # msg = 'Source file deleted.\n\n'
                                    # logger.log(logging.INFO, msg)
                                    continue
                                else:
                                    # print('Source deletion failed for \n')
                                    # print(file)
                                    # print('/n/n')
                                    msg = 'Source deletion failed for \n' + file + '/n/n'
                                    logger.log(logging.WARNING, msg)
                                    failed.append(file)

                            else:
                                # Don't copy to destination
                                # print('Deleting source file...')
                                # msg = 'Deleting source file...'
                                # logger.log(logging.INFO, msg)
                                os.remove(filePath)

                                # Check if file is gone
                                if not os.path.exists(filePath):
                                    # print('Source file deleted.\n\n')
                                    # msg = 'Source file deleted.\n\n'
                                    # logger.log(logging.INFO, msg)
                                    continue
                                else:
                                    # print('Source deletion failed for \n')
                                    # print(file)
                                    # print('/n/n')
                                    msg = 'Source deletion failed for \n' + file + '/n/n'
                                    logger.log(logging.WARNING, msg)
                                    failed.append(file)

                    except:
                        # File does not already exist
                        # Use copy2 instead of copy or copyfile to preserve file metadata
                        # http://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
                        # print('Copying.. ' + str(file))
                        msg = 'Copying.. ' + str(file)
                        logger.log(logging.INFO, msg)
                        shutil.copy2(filePath, desFilePath)
                        success += 1
                        # print('Done.')
                        msg = 'Copying.. ' + str(file)
                        logger.log(logging.INFO, msg)
                        # print('Deleting source file...')
                        # msg = 'Deleting source file...'
                        # logger.log(logging.INFO, msg)
                        os.remove(filePath)

                        # Check if file is gone
                        if not os.path.exists(filePath):
                            # print('Source file deleted.\n\n')
                            # msg = 'Source file deleted.\n\n'
                            # logger.log(logging.INFO, msg)
                            continue
                        else:
                            # print('Source deletion failed for \n')
                            # print(file)
                            # print('/n/n')
                            msg = 'Source deletion failed for \n' + file + '/n/n'
                            logger.log(logging.WARNING, msg)
                            failed.append(file)

    if len(failed) == 0:
        # print("Sorting Complete!")
        # print(str(success) + " file(s) successfully sorted.")
        msg = "Sorting Complete for " + channel + ' Channel:' + str(success) + " file(s) successfully sorted."
        logger.log(logging.INFO, msg)
        # print('Completed in: {}'.format(endTime - startTime))

    else:
        # print("Sorting Complete!")
        # print(str(success) + " file(s) successfully sorted.")
        # print('Completed in: {}'.format(endTime - startTime))
        # print('\n')
        # print('The following files could not be deleted')
        msg = "Sorting Complete! \n" + str(
            success) + " file(s) successfully sorted.\n The following files could not be deleted"
        logger.log(logging.INFO, msg)
        for x in failed:
            # print(x)
            msg = x
            logger.log(logging.INFO, msg)


# ______________________________________________________________________________
