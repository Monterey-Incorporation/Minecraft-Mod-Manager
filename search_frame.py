from ttkbootstrap import ttk

class Search_Frame:
    def __init__(self,window,globalsearchs,i,function):
        self.info = i
        self.function = function
        globalsearchs[i.slug] = {"frame":ttk.Frame(window),"info":i}
        projectf = ttk.Frame(globalsearchs[i.slug]["frame"])
        l1 = ttk.Label(projectf, text=i.title, font=("", 15))
        l1.pack(side="left")
        projectf.pack()
        projectf2 = ttk.Frame(globalsearchs[i.slug]["frame"])
        l2 = ttk.Label(projectf2, text=i.desc)
        l2.pack()
        projectf2.pack()
        projectf3 = ttk.Frame(globalsearchs[i.slug]["frame"])
        b10 = ttk.Button(projectf3, text="Download Now", bootstyle="warning",command=None)
        b10.pack(side="left", padx=10)
        b11 = ttk.Button(projectf3, text="View Project",command=self.load)
        b11.pack(side="left")
        projectf3.pack()
        globalsearchs[i.slug]["frame"].pack()
        sp1 = ttk.Separator(window)
        sp1.pack(fill="x", padx=20)
    
    def load(self):
        self.function(id=self.info.slug)