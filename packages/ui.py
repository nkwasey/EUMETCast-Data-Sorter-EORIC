from tkinter import *
from tkinter import ttk, filedialog
from packages.commands import *
import signal
import queue
from packages.commands import logger
from packages.data_formats import *
import threading
import time
from tqdm import tqdm


# ______________________________________________________________________________
class QueueHandler(logging.Handler):

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


# ______________________________________________________________________________
class DirectoriesUi:

    def __init__(self, frame):
        entry_width = 50
        pady = 10
        padx = 10

        self.frame = frame
        global SF_entry, DF_entry
        self.SourceFolder = StringVar(value="C:/EUMETCast/received/afr-1")
        self.des_Folder = StringVar(value="C:/EUMETCast/received/sorted")

        # Creating content for Directories frame
        self.SF_label = ttk.Label(self.frame, text='Source Folder')
        SF_entry = ttk.Entry(self.frame, width=entry_width, textvariable=self.SourceFolder)
        self.browse_sf_btn = ttk.Button(self.frame, text='Browse...', command=self.browse_file_SF)

        self.DF_label = ttk.Label(self.frame, text='Destination Folder')
        DF_entry = ttk.Entry(self.frame, width=entry_width, textvariable=self.des_Folder)
        self.browse_df_btn = ttk.Button(self.frame, text='Browse...', command=self.browse_file_DF)

        self.SF_label.grid(row=0, column=0, pady=pady)
        SF_entry.grid(row=0, column=1, pady=pady)
        self.browse_sf_btn.grid(row=0, column=2, padx=5, pady=pady)

        self.DF_label.grid(row=1, column=0, pady=pady)
        DF_entry.grid(row=1, column=1, pady=pady)
        self.browse_df_btn.grid(row=1, column=2, padx=padx, pady=pady)

    def browse_file_SF(self):
        SF_name = filedialog.askdirectory()
        if SF_name is not None:
            self.SourceFolder.set(str(SF_name))

    def browse_file_DF(self):
        DF_name = filedialog.askdirectory()
        if DF_name is not None:
            self.des_Folder.set(str(DF_name))


# ______________________________________________________________________________
class ActivityUi:

    def __init__(self, frame):
        pady = 10
        padx = 10
        self.frame = frame

        self.start_btn = ttk.Button(self.frame, text='Start', command=run)
        self.start_btn.grid(row=0, column=5, padx=padx, pady=pady)

        # global pgbar
        # pgbar = ttk.Progressbar(self.frame, length=200, orient=HORIZONTAL, maximum=100, mode='determinate')
        # pgbar.grid(row=0, column=0, columnspan=4, padx=padx, pady=pady)

        global var
        var = StringVar()
        var.set('Application idle ...')
        status_label = ttk.Label(self.frame, width=13, text="Latest Activity: ")
        status_text = ttk.Label(self.frame, width=40, textvariable=var)
        status_label.grid(row=0, column=0, padx=padx, pady=pady)
        status_text.grid(row=0, column=1, columnspan=4, padx=padx, pady=pady)


# ______________________________________________________________________________
class ConsoleUi:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame):
        self.frame = frame
        # Create a ScrolledText widget

        self.scrolled_text = ScrolledText(frame, state='disabled', width=160, height=15)
        self.scrolled_text.grid(row=0, column=0)
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('WARNING', foreground='orange')

        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)

        # Start polling messages from the queue
        self.frame.after(1, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(1, self.poll_log_queue)


# ______________________________________________________________________________


class App:

    def __init__(self, root):
        pady = 10
        padx = 10
        width_all = 15

        self.root = root
        root.title("EORIC GEONETCast Data Sorter")
        root.geometry("1360x1080")
        root.iconbitmap(r"eoriclogo.ico")

        # Creating Menu bar
        Main_menu = Menu(self.root)
        self.root.config(menu=Main_menu)

        # Creating the sub menus for File
        FileMenu = Menu(Main_menu)
        Main_menu.add_cascade(label='File', menu=FileMenu)
        # FileMenu.add_command(label='Start', command=doNothing)
        # FileMenu.add_command(label='Stop', command=doNothing)
        FileMenu.add_command(label='Exit', command=self.root.destroy)

        # Creating the sub menu for Help
        HelpMenu = Menu(Main_menu)
        Main_menu.add_cascade(label='Help', menu=HelpMenu)
        HelpMenu.add_command(label='Documentation', command=openweb)
        HelpMenu.add_command(label='About', command=about_info)

        # Creating frames to be used
        heading = Label(self.root, text="GEONETCAST DATA SORTER", font="Calibri 30")
        folderFrame = ttk.LabelFrame(self.root, text="DIRECTORIES")
        activityFrame = ttk.LabelFrame(self.root, text="ACTIVITY")
        channelsFrame = ttk.LabelFrame(self.root, text="CHANNELS (afr-1)")
        logsFrame = ttk.LabelFrame(self.root, text="LOGS")

        epsgFrame = ttk.LabelFrame(channelsFrame, text="A1C-EPS-G")
        geo3Frame = ttk.LabelFrame(channelsFrame, text="A1C-GEO-3")
        geo4Frame = ttk.LabelFrame(channelsFrame, text="A1C-GEO-4")
        rds1Frame = ttk.LabelFrame(channelsFrame, text="A1C-RDS-1")
        saf1Frame = ttk.LabelFrame(channelsFrame, text="A1C-SAF-1")
        saf2Frame = ttk.LabelFrame(channelsFrame, text="A1C-SAF-2")
        tpc1Frame = ttk.LabelFrame(channelsFrame, text="A1C-TPC-1")
        tpc5Frame = ttk.LabelFrame(channelsFrame, text="A1C-TPC-5")
        tpc6Frame = ttk.LabelFrame(channelsFrame, text="A1C-TPC-6")
        tpg1Frame = ttk.LabelFrame(channelsFrame, text="A1C-TPG-1")

        heading.grid(row=0, column=1, columnspan=4)
        folderFrame.grid(row=1, column=1, columnspan=2, padx=50, pady=5)
        activityFrame.grid(row=1, column=3, columnspan=2, padx=30, pady=5)
        channelsFrame.grid(row=2, column=1, columnspan=4, padx=10, pady=5)
        logsFrame.grid(row=3, column=1, columnspan=4, padx=30, pady=10)

        epsgFrame.grid(row=1, column=0, padx=padx, pady=pady)
        geo3Frame.grid(row=1, column=1, padx=padx, pady=pady)
        geo4Frame.grid(row=1, column=2, padx=padx, pady=pady)
        rds1Frame.grid(row=1, column=3, padx=padx, pady=pady)
        saf1Frame.grid(row=1, column=4, padx=padx, pady=pady)
        saf2Frame.grid(row=2, column=0, padx=padx, pady=pady)
        tpc1Frame.grid(row=2, column=1, padx=padx, pady=pady)
        tpc5Frame.grid(row=2, column=2, padx=padx, pady=pady)
        tpc6Frame.grid(row=2, column=3, padx=padx, pady=pady)
        tpg1Frame.grid(row=2, column=4, padx=padx, pady=pady)

        global EPSG_cb, GEO3_cb, GEO4_cb, RDS1_cb, SAF1_cb, SAF2_cb, TPC1_cb, TPC5_cb, TPC6_cb, TPG1_cb

        # ______________________________________________________________________________
        # Inserting content into epsgFrame (EPS-G)
        EPSG_cb = StringVar()
        cb1 = ttk.Checkbutton(epsgFrame, text="Sort Channel", width=width_all, variable=EPSG_cb,
                              onvalue="on", offvalue="off", )
        epsg_btn = ttk.Button(epsgFrame, text='More Info', command=epsg_info)
        cb1.grid(row=0, column=0, padx=padx, pady=pady)
        epsg_btn.grid(row=0, column=1, padx=padx, pady=pady)
        epsgFrame.grid(row=1, column=0, padx=padx, pady=pady)

        # ______________________________________________________________________________
        # Inserting content into geo3Frame (GEO-3)
        GEO3_cb = StringVar()
        cb2 = ttk.Checkbutton(geo3Frame, text="Sort Channel", width=width_all, variable=GEO3_cb,
                              onvalue="on", offvalue="off", )
        geo3_btn = ttk.Button(geo3Frame, text='More Info', command=geo3_info)
        cb2.grid(row=0, column=0, padx=padx, pady=pady)
        geo3_btn.grid(row=0, column=1, padx=padx, pady=pady)
        geo3Frame.grid(row=1, column=1, padx=padx, pady=pady)

        # ______________________________________________________________________________
        # Inserting content into geo4Frame (GEO-4)
        GEO4_cb = StringVar(geo4Frame)
        cb3 = ttk.Checkbutton(geo4Frame, text="Sort Channel", width=width_all, variable=GEO4_cb,
                              onvalue="on", offvalue="off", )
        geo4_btn = ttk.Button(geo4Frame, text='More Info', command=geo4_info)
        cb3.grid(row=0, column=0, padx=padx, pady=pady)
        geo4_btn.grid(row=0, column=1, padx=padx, pady=pady)
        geo4Frame.grid(row=1, column=2, padx=padx, pady=pady)

        # ______________________________________________________________________________
        # Inserting content into rds1Frame (RDS-1)
        RDS1_cb = StringVar(rds1Frame)
        cb4 = ttk.Checkbutton(rds1Frame, text="Sort Channel", width=width_all, variable=RDS1_cb,
                              onvalue="on", offvalue="off", )
        rds1_btn = ttk.Button(rds1Frame, text='More Info', command=rds1_info)
        cb4.grid(row=0, column=0, padx=padx, pady=pady)
        rds1_btn.grid(row=0, column=1, padx=padx, pady=pady)
        rds1Frame.grid(row=1, column=3, padx=padx, pady=pady)

        # ______________________________________________________________________________
        # Inserting content into saf1Frame (SAF-1)
        SAF1_cb = StringVar(saf1Frame)
        cb5 = ttk.Checkbutton(saf1Frame, text="Sort Channel", width=width_all, variable=SAF1_cb,
                              onvalue="on", offvalue="off", )
        saf1_btn = ttk.Button(saf1Frame, text='More Info', command=saf1_info)
        cb5.grid(row=0, column=0, padx=padx, pady=pady)
        saf1_btn.grid(row=0, column=1, padx=padx, pady=pady)
        saf1Frame.grid(row=1, column=4, padx=padx, pady=pady)

        # ______________________________________________________________________________
        # Inserting content into saf2Frame (SAF-2)
        SAF2_cb = StringVar(saf2Frame)
        cb6 = ttk.Checkbutton(saf2Frame, text="Sort Channel", width=width_all, variable=SAF2_cb,
                              onvalue="on", offvalue="off", )
        saf2_btn = ttk.Button(saf2Frame, text='More Info', command=saf2_info)
        cb6.grid(row=0, column=0, padx=padx, pady=pady)
        saf2_btn.grid(row=0, column=1, padx=padx, pady=pady)
        saf2Frame.grid(row=2, column=0, padx=padx, pady=pady)

        # ______________________________________________________________________________
        # Inserting content into tpc1Frame (TPC-1)
        TPC1_cb = StringVar(tpc1Frame)
        cb7 = ttk.Checkbutton(tpc1Frame, text="Sort Channel", width=width_all, variable=TPC1_cb,
                              onvalue="on", offvalue="off", )
        tpc1_btn = ttk.Button(tpc1Frame, text='More Info', command=tpc1_info)
        cb7.grid(row=0, column=0, padx=padx, pady=pady)
        tpc1_btn.grid(row=0, column=1, padx=padx, pady=pady)
        tpc1Frame.grid(row=2, column=1, padx=padx, pady=pady)

        # ______________________________________________________________________________
        # Inserting content into tpc5Frame (TPC-5)
        TPC5_cb = StringVar(tpc5Frame)
        cb8 = ttk.Checkbutton(tpc5Frame, text="Sort Channel", width=width_all, variable=TPC5_cb,
                              onvalue="on", offvalue="off", )
        tpc5_btn = ttk.Button(tpc5Frame, text='More Info', command=tpc5_info)
        cb8.grid(row=0, column=0, padx=padx, pady=pady)
        tpc5_btn.grid(row=0, column=1, padx=padx, pady=pady)
        tpc5Frame.grid(row=2, column=2, padx=padx, pady=pady)

        # ______________________________________________________________________________
        # Inserting content into tpc5Frame (TPC-6)
        TPC6_cb = StringVar(tpc6Frame)
        cb9 = ttk.Checkbutton(tpc6Frame, text="Sort Channel", width=width_all, variable=TPC6_cb,
                              onvalue="on", offvalue="off", )
        tpc6_btn = ttk.Button(tpc6Frame, text='More Info', command=tpc6_info)
        cb9.grid(row=0, column=0, padx=padx, pady=pady)
        tpc6_btn.grid(row=0, column=1, padx=padx, pady=pady)
        tpc6Frame.grid(row=2, column=3, padx=padx, pady=pady)

        # ______________________________________________________________________________
        # Inserting content into tpg1Frame (TPG-1)
        TPG1_cb = StringVar(tpg1Frame)
        cb10 = ttk.Checkbutton(tpg1Frame, text="Sort Channel", width=width_all, variable=TPG1_cb,
                               onvalue="on", offvalue="off", )
        tpg1_btn = ttk.Button(tpg1Frame, text='More Info', command=tpg1_info)
        cb10.grid(row=0, column=0, padx=padx, pady=pady)
        tpg1_btn.grid(row=0, column=1, padx=padx, pady=pady)
        tpg1Frame.grid(row=2, column=4, padx=padx, pady=pady)

        # ______________________________________________________________________________
        tboxes_list = [cb1, cb2, cb3, cb4, cb5, cb6, cb7, cb8, cb9, cb10]
        # print(tboxes_list)
        for i in tboxes_list:
            i.invoke()
            i.invoke()

        # ______________________________________________________________________________
        # Inserting select all and deselect buttons

        deselect_all_tbox_button = ttk.Button(channelsFrame, text='Deselect all',
                                              command=lambda: tbox_deselect_all(tboxes_list))
        select_all_tbox_button = ttk.Button(channelsFrame, text='Select all',
                                            command=lambda: tbox_select_all(tboxes_list))

        select_all_tbox_button.grid(row=3, column=3, padx=padx, pady=pady, sticky=E)
        deselect_all_tbox_button.grid(row=3, column=4, padx=padx, pady=pady, sticky=W)

        stop_btn = ttk.Button(activityFrame, text='Quit', command=self.quit)
        stop_btn.grid(row=0, column=6, padx=padx, pady=pady)

        # Initialize all frames
        self.directories = DirectoriesUi(folderFrame)
        self.console = ConsoleUi(logsFrame)
        self.activity = ActivityUi(activityFrame)

        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.bind('<Control-q>', self.quit)
        signal.signal(signal.SIGINT, self.quit)
        self.root.update_idletasks()

    def quit(self, *args):
        self.root.destroy()


# ______________________________________________________________________________
def sort(sourcePath, desPath, channels):
    global failed, success, desFilePath, channel, var
    # logger.info('Sorting starting...')
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
def run():
    state_epsg = EPSG_cb.get()
    state_geo3 = GEO3_cb.get()
    state_geo4 = GEO4_cb.get()
    state_rds1 = RDS1_cb.get()
    state_saf1 = SAF1_cb.get()
    state_saf2 = SAF2_cb.get()
    state_tpc1 = TPC1_cb.get()
    state_tpc5 = TPC5_cb.get()
    state_tpc6 = TPC6_cb.get()
    state_tpg1 = TPG1_cb.get()
    s_name = SF_entry.get()
    d_name = DF_entry.get()

    worker = {"state_epsg": {"state": state_epsg, 'channel': 'A1C-EPS-G'},
              "state_geo3": {"state": state_geo3, 'channel': 'A1C-GEO-3'},
              "state_geo4": {"state": state_geo4, 'channel': 'A1C-GEO-4'},
              "state_rds1": {"state": state_rds1, 'channel': 'A1C-RDS-1'},
              "state_saf1": {"state": state_saf1, 'channel': 'A1C-SAF-1'},
              "state_saf2": {"state": state_saf2, 'channel': 'A1C-SAF-2'},
              "state_tpc1": {"state": state_tpc1, 'channel': 'A1C-TPC-1'},
              "state_tpc5": {"state": state_tpc5, 'channel': 'A1C-TPC-5'},
              "state_tpc6": {"state": state_tpc6, 'channel': 'A1C-TPC-6'},
              "state_tpg1": {"state": state_tpg1, 'channel': 'A1C-TPG-1'},
              }
    xx = 0.05
    xx_msg = ' Channel sorting completed ...'
    for state in worker:
        cb_state, channel_set = worker[state].values()

        if channel_set == 'A1C-EPS-G' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            time.sleep(xx)

            sort(sourcePath=s_name, desPath=d_name, channels=EPSG)

        if channel_set == 'A1C-GEO-3' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            sort(sourcePath=s_name, desPath=d_name, channels=GEO3)
            time.sleep(xx)

        if channel_set == 'A1C-GEO-4' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            sort(sourcePath=s_name, desPath=d_name, channels=GEO4)
            time.sleep(xx)

        if channel_set == 'A1C-RDS-1' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            sort(sourcePath=s_name, desPath=d_name, channels=RDS1)
            time.sleep(xx)

        if channel_set == 'A1C-SAF-1' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            sort(sourcePath=s_name, desPath=d_name, channels=SAF1)
            time.sleep(xx)

        if channel_set == 'A1C-SAF-2' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            sort(sourcePath=s_name, desPath=d_name, channels=SAF2)
            time.sleep(xx)

        if channel_set == 'A1C-TPC-1' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            sort(sourcePath=s_name, desPath=d_name, channels=TPC1)
            time.sleep(xx)

        if channel_set == 'A1C-TPC-5' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            sort(sourcePath=s_name, desPath=d_name, channels=TPC5)
            time.sleep(xx)

        if channel_set == 'A1C-TPC-6' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            sort(sourcePath=s_name, desPath=d_name, channels=TPC6)
            time.sleep(xx)

        if channel_set == 'A1C-TPG-1' and cb_state == 'on':
            var.set(channel_set + xx_msg)
            sort(sourcePath=s_name, desPath=d_name, channels=TPG1)
            time.sleep(xx)


# ______________________________________________________________________________
