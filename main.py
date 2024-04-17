from ttkbootstrap import ttk
import ttkbootstrap
import tkinter as ltk
from threading import Thread
from PIL import Image, ImageTk
import PIL
from ttkbootstrap import Scrollbar
from tkinter import Tk
from tkinter import Tk, messagebox, filedialog, simpledialog, dialog
from requester import Modrinth, Search_Project
from ttkbootstrap.scrolled import ScrolledFrame
import json, os, sys, time, platform
from ttkbootstrap.toast import ToastNotification
from traceback import format_exc, print_exc

homedirectory = os.getcwd()
print("Starting directory: " + homedirectory)

os.chdir(os.path.expanduser("~"))
print("Loading path...")
os.chdir("AppData")
os.chdir("Roaming")

#? Loads Minecraft Client Path
try:
    os.chdir(".minecraft")
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
if not os.path.exists("mod_manager"):
    messagebox.showinfo("Welcome!","""Welcome to Mod Manager for Mminecraft Java Edition!

Your minecraft client is not ready for Mod manager. 
We are installing some important files for Mod Manager for it to run.
""")
    if len(os.listdir()) != 0:
        pass
else:
    print("Home Path is set to: " + os.getcwd())

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
window.title("Mod Manager - Mod Store")
window.geometry("1000x600")
window.wm_iconbitmap(homedirectory + "/icons/icon.ico")
keep_alive_status = False
keep_alive_thread = True
mainframe = ttk.Frame(window)
processthread = None
style = ttkbootstrap.Style(theme="superhero")
connectionbarvalue = ltk.IntVar()
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
erroricon = ltk.PhotoImage(file=homedirectory + "/icons/error.png")

searchstring = ltk.StringVar(window)
globalwidgets = {}
searchquery = ""


def showfullmod():
    pass


def run_thread(command, reload=False):
    processthread = Thread(target=command, kwargs={"reload": reload})
    processthread.start()


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
            projectf = ttk.Frame(globalwidgets["searchframe"])
            l1 = ttk.Label(projectf, text=i.title, font=("", 15))
            l1.pack(side="left")
            projectf.pack()
            projectf2 = ttk.Frame(globalwidgets["searchframe"])
            l2 = ttk.Label(projectf2, text=i.desc)
            l2.pack()
            projectf2.pack()
            projectf3 = ttk.Frame(globalwidgets["searchframe"])
            b10 = ttk.Button(projectf3, text="Download Now", bootstyle="warning")
            b10.pack(side="left", padx=5)
            b11 = ttk.Button(projectf3, text="View Project")
            b11.pack(side="left", padx=5)
            b12 = ttk.Button(projectf3, text="Add to cart", bootstyle="success")
            b12.pack(side="left", padx=5)
            projectf3.pack()
            sp1 = ttk.Separator(globalwidgets["searchframe"])
            sp1.pack(fill="x", padx=20)

        connectionbarvalue.set(100)
        window.update()
        globalwidgets["searchframe"].pack(fill="both", expand=True, side="left")
    except Exception as e:
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
        fullerror = ttkbootstrap.Text(lf1)
        fullerror.insert("end", "Python " + sys.version + " " + platform.platform())
        fullerror.insert("end", "\n\nFull Traceback:\n")
        fullerror.insert("end", format_exc())
        fullerror.pack(fill="x", expand=True)
        lf1.pack(side="top")

    connectionbarvalue.set(0)
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
