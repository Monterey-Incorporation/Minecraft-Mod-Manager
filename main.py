from ttkbootstrap import ttk
import ttkbootstrap
import shutil
import tkinter as ltk
from threading import Thread
from PIL import Image, ImageTk
import PIL
from ttkbootstrap import Scrollbar
from tkinter import Tk
from tkinter import Tk, messagebox, filedialog, simpledialog, dialog
from requester import Modrinth, Search_Project
from ttkbootstrap.scrolled import ScrolledFrame
import json, os, sys, time, platform, zipfile, base64, icons_zip
from search_frame import Search_Frame
from ttkbootstrap.toast import ToastNotification
from traceback import format_exc, print_exc

debug = True

if os.name  == "nt":
    #! This is disabled on macos and linux because they are not Windows
    homedirectory = os.getcwd()
else:
    homedirectory = os.path.expanduser("~")
    if not os.path.exists(homedirectory + "/modmanager"):
        os.chdir(homedirectory)
        os.mkdir("modmanager")
        os.chdir("modmanager")
        homedirectory = os.getcwd()
        print("Decoding \"icons.zip\" and unarchiving")
        open("icons.zip","wb").write(base64.b64decode(icons_zip.DATA))
        zip = zipfile.ZipFile("icons.zip","r")
        zip.extractall()
        zip.close()
        os.remove("icons.zip")
    else:
        os.chdir(homedirectory)
        os.chdir("modmanager")
        homedirectory = os.getcwd()
print("Starting directory: " + homedirectory)

os.chdir(os.path.expanduser("~"))
print("Loading path...")
if not debug:
    if os.name == "nt":
        os.chdir("AppData")
        os.chdir("Roaming")
    else:
        os.chdir(os.path.expanduser("~"))
        os.chdir("Library")
        os.chdir("Application Support")

#? Loads Minecraft Client Path'
if not debug:
    try:
        if os.name == "nt":
            os.chdir(".minecraft")
        else:
            os.chdir("minecraft")
    except FileNotFoundError as e:
        messagebox.showerror(
            title="Minecraft Mods Folder not found",
            message=f"""Minecraft mods folder is not found!!

    Please check your minecraft installation
    Full error:

    {e}
    """,
        )
        sys.exit(1)
    except Exception as e:
        messagebox.showerror(
            title="Unable to access Minecraft Mods Folder",
            message=f"""Minecraft mods folder is unassable!!

    Please check your minecraft installation
    Full error:

    {e}
    """,
        )
        sys.exit(1)
    else:
        print("Minecraft Path loaded: "+os.getcwd())

#? Installs mod manager info
if not debug:
    if not os.path.exists("mod_manager"):
        messagebox.showinfo("Welcome!","""Welcome to Mod Manager for Minecraft Java Edition!

    Your minecraft client is not ready for Mod manager. 
    We are installing some important files for Mod Manager for it to run.
    """)
    else:
        print("Home Path is set to: " + os.getcwd())

    if os.path.exists("mods"):
        if len(os.listdir("mods")) != 0:
            mboxre = messagebox.askquestion("Extra Mods detected",f"""Extra Mods detected!

    The Mod manager requires the "./mods" folder in {os.getcwd()} to be empty

    Do you want to delete all of the mods or store them in an other folder?
    """,icon=messagebox.WARNING)
            if mboxre == "yes":
                if messagebox.askquestion("Confirmation","Are you sure? All mods will be deleted!",icon=messagebox.WARNING) == "yes":
                    shutil.rmtree(os.getcwd() + "/mods")
                    os.rmdir("mods")
                    os.mkdir("mods")
                else:
                    print("User input is No renaming folder...")
                    os.renames("mods","mods_old")
                    os.mkdir("mods")
                    print("done")
            elif mboxre == "no":
                os.renames("mods","mods_old")
                os.mkdir("mods")
            else:
                pass
    else:
        os.mkdir("mods")

#Closes window and stops main thread
def close():
    global keep_alive_thread, processthread, mainframe
    keep_alive_thread = False
    mainframe.quit()
    try:
        window.destroy()
    except:
        pass

#Main window
mod = Modrinth()
window = Tk()
window.title("Mod Manager")
window.geometry("1000x600")
if os.name == "nt":
    window.wm_iconbitmap(homedirectory + "/icons/icon.ico")
keep_alive_status = False
keep_alive_thread = True
mainframe = ttk.Frame(window)
processthread = None
style = ttkbootstrap.Style(theme="yeti")
maxsearch = ltk.IntVar(value=25)
connectionbarvalue = ltk.IntVar()
cart = []
cartids = []
connectionbar = ttk.Progressbar(
    window, variable=connectionbarvalue, maximum=100, bootstyle="striped"
)

toast = ToastNotification(
    title="Your download's are completed",
    message="Your download's are completed please restart minecraft java",
    duration=3000,
    alert=True,
)

iconsize = (17, 17)

searchicon = ltk.PhotoImage(
    file=homedirectory + "/icons/search.png", width=iconsize[0], height=iconsize[1]
)
settingicon = ltk.PhotoImage(
    file=homedirectory + "/icons/settings.png", width=iconsize[0], height=iconsize[1]
)
reloadicon = ltk.PhotoImage(
    file=homedirectory + "/icons/reload.png", width=iconsize[0], height=iconsize[1]
)
carticon = ltk.PhotoImage(
    file=homedirectory + "/icons/cart.png", width=iconsize[0], height=iconsize[1]
)
downloadicon = ltk.PhotoImage(
    file=homedirectory + "/icons/download.png", width=iconsize[0], height=iconsize[1]
)
view_modsicon = ltk.PhotoImage(
    file=homedirectory + "/icons/view_mods.png", width=iconsize[0], height=iconsize[1]
)
erroricon = ltk.PhotoImage(file=homedirectory + "/icons/error.png")

searchstring = ltk.StringVar(window)
globalwidgets = {}
processthread = None
globalsearchs = {}
gloablvariable = {}
searchquery = ""


def showfullmod(id=None,reload=False):
    global mainframe, connectionbarvalue, globalwidgets
    connectionbarvalue.set(0)
    window.update()
    if reload:
        globalwidgets["searchentry"].config(state="disabled")
        globalwidgets["reload"].config(state="disabled")
    else:
        globalwidgets["searchentry"].config(state="disabled")
        globalwidgets["reload"].config(command=lambda: run_thread(showfullmod, reload=True))
        globalwidgets["reload"].config(state="disabled")
        gloablvariable["project_id"] = id
    print("Loading Project with the id: {}".format(gloablvariable["project_id"]))
    mainframe.destroy()
    connectionbarvalue.set(20)
    window.update()
    project = mod.get_project(gloablvariable["project_id"])
    connectionbarvalue.set(30)
    window.update()
    mainframe = ttk.Frame(window)
    connectionbarvalue.set(50)
    window.update()
    
    #TODO This area is reserved for the actual function
    
    connectionbarvalue.set(100)
    window.update()
    globalwidgets["searchentry"].config(state="normal")
    globalwidgets["reload"].config(state="normal")
    mainframe.pack(fill="both", expand=True)
    window.title(f"Mod Manager - {project.title}")
    connectionbarvalue.set(0)
    window.update()

def add_to_cart(title,project_id,slug,button):
    button.config(state="disabled")
    cartids.append(slug)
    cart.append({"title":title,"id":project_id,"slug":slug})
    print({"title":title,"id":project_id,"slug":slug})
    print(cart)

def download_now():
    pass

def freeze_window():
    global blocker_window
    blocker_window = ltk.Toplevel(window)
    blocker_window.grab_set()
    blocker_window.withdraw()
    unfreeze_button = ltk.Button(blocker_window, text="Unfreeze", command=unfreeze_window)
    unfreeze_button.pack()

def unfreeze_window():
    blocker_window.destroy()

def edit_search_settings():
    global mainframe
    mainframe.destroy()
    mainframe = ttk.Frame(window)
    mainframe.pack(fill="both", expand=True)

def run_thread(function, reload=False):
    global processthread
    if processthread == None:
        processthread = Thread(target=function, kwargs={"reload": reload})
        processthread.start()
    elif not processthread.is_alive():
        processthread = Thread(target=function, kwargs={"reload": reload})
        processthread.start()
    else:
        pass

def search(reload=False):
    print(reload)
    global globalwidgets, searchstring, searchquery, mainframe
    if reload:
        globalwidgets["searchentry"].config(state="disabled")
        globalwidgets["reload"].config(state="disabled")
    else:
        globalwidgets["searchentry"].config(state="disabled")
        globalwidgets["reload"].config(command=lambda: run_thread(search, reload=True))
        searchquery = searchstring.get()
        globalwidgets["reload"].config(state="disabled")

    print('Searching for the query "' + searchquery + '"')
    connectionbarvalue.set(20)
    window.update()
    mainframe.destroy()
    mainframe = ttk.Frame(window)
    connectionbarvalue.set(30)
    window.update()
    try:
        mods = mod.search_projects(searchquery)
        connectionbarvalue.set(50)
        window.update()
        if searchquery != "":
            l5 = ttk.Label(mainframe, text=f"Results for the query {searchquery}")
            l5.pack(padx=40)
        globalwidgets["searchframe"] = ScrolledFrame(mainframe)
        for i in mods:
            Search_Frame(globalwidgets["searchframe"],globalsearchs,i,showfullmod)
        connectionbarvalue.set(100)
        window.update()
        globalwidgets["searchframe"].pack(fill="both", expand=True, side="left")
    except Exception:
        print("An error occured")
        lf1 = ttk.Frame(mainframe)

        l1 = ttk.Label(lf1, image=erroricon)
        l1.pack()
        l2 = ttk.Label(
            lf1, text="An Error Occured While connectng to the servers", font=("", 28)
        )
        l2.pack()
        l3 = ttk.Label(
            lf1,
            text="The connection to the server has been terminated due to of an error",
        )
        l3.pack()
        l4 = ttk.Label(
            lf1,
            text="If this issue still occurs please tell the developer with the information:",
        )
        l4.pack()
        print_exc()
        fullerror = ttkbootstrap.ScrolledText(lf1)
        fullerror.insert("end", "Python " + sys.version + " " + platform.platform())
        fullerror.insert("end", "\n\nFull Traceback:\n")
        fullerror.insert("end", format_exc())
        fullerror.pack(fill="x", expand=True)
        lf1.pack(side="top")

    connectionbarvalue.set(0)
    window.title("Mod Manager - Mod Store")
    window.update()
    globalwidgets["searchentry"].config(state="normal")
    globalwidgets["reload"].config(state="normal")
    mainframe.pack(fill="both", expand=True)


topframe = ttk.Frame(window)
globalwidgets["reload"] = ttk.Button(topframe, image=reloadicon, command=None)
globalwidgets["searchentry"] = ttk.Entry(topframe, textvariable=searchstring)
globalwidgets["search"] = ttk.Button(
    topframe, image=searchicon, command=lambda: run_thread(search)
)
globalwidgets["reload"].pack(side="left")
globalwidgets["searchentry"].pack(side="left", fill="x", expand=True)
globalwidgets["search"].pack(side="left")
globalwidgets["settings"] = ttk.Button(topframe,image=settingicon,command=edit_search_settings)
globalwidgets["settings"].pack(side="left")
b1 = ttk.Button(topframe, image=carticon, text="0")
b1.pack(side="left")
topframe.pack(side="top", fill="x")
connectionbar.pack(fill="x")
mainframe.pack(fill="both", expand=True)

sp1 = ttk.Separator(window)
sp1.pack(fill="x")

run_thread(search)

window.protocol("WM_DELETE_WINDOW", close)
window.mainloop()
