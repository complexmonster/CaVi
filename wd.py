import os, sys, time, pickle
from tkinter import Tk, filedialog, Button, Label, StringVar
from category import Category
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#Canem Vigilate by Phil Gullberg (woldandvoid.com) (c) 2019
window = Tk()
folder = StringVar()
folder_to_watch = ""

filetypes =   { Category("Documents", ["doc", "docx", "txt", "pdf"]),
                Category("Images", ["jpg", "jpeg", "gif", "png", "tiff"]),
                Category("Applications", ["dmg", "exe", "app"]),
                Category("Compressed Files", ["zip", "tar.gz", "rar"]), }



def run():
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=True)
    observer.start()
    check_folders_exist()
    print("Started CaVi")

def stop():
    save()
    try:
        if observer.is_alive():
            observer.stop()
    except NameError:
        pass
    sys.exit()

def setup_gui():
    window.title("CaVi")
    window.geometry('250x150')

    dir_location = Label(window, textvariable=folder).pack()
    btn_folder = Button(window, text="Choose Folder to Watch", command=open_directory).pack()
    bt_run = Button(window, text="Start", bg="green", command=run).pack()
    bt_stop = Button(window, text="Stop/Close", command=stop).pack()
    bt_save = Button(window, text="Save", command=save).pack()

    window.mainloop()

def open_directory():
    active_folder = filedialog.askdirectory()
    folder_to_watch=active_folder
    folder.set(folder_to_watch)
    save(active_folder)
    
def new_category(_name):
    filetypes.add(Category(_name, []))

def save(_dir=folder_to_watch): 
    pickle.dump(_dir, open('cavi.pkl', 'wb'))
    print("Pickle Saved, " + folder_to_watch)

def load():
    try:
        folder_to_watch = pickle.load(open('cavi.pkl', 'rb'))
        folder.set(folder_to_watch)
        print("Pickle Loaded, Captain!")
        print("Loaded pickle: " + folder_to_watch)

    except (OSError, IOError) as e:
        print("Couldn't load save file!")

def check_folders_exist():
    for category in filetypes:
        f = folder_to_watch + "/" + category.name
        if not os.path.exists(f):
            create_folder(f)

def create_folder(_folder_name):
        os.mkdir(_folder_name)
        print("Creating folder: " + _folder_name)

class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for filename in os.listdir(folder_to_watch):
            src = folder_to_watch + "/" + filename

            t = get_file_type(filename)

            if not get_folder(t) == "No match":
                new_destination = folder_to_watch + "/" + get_folder(t) + "/" + filename
                os.rename(src, new_destination)

def get_file_type(_file):
    ext = os.path.splitext(_file)[1]
    return ext[1:].lower()

def get_folder(_filetype):
    for category in filetypes:
        for ff in category.filetypes:
            if _filetype == ff:
                return category.name
    return "No match"

load()
setup_gui()