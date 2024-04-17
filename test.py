import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.scrolled import ScrolledFrame

root = tk.Tk()

# Create a style object
style = Style(theme='flatly')

# Create a ScrolledFrame widget
scrolled_frame = ScrolledFrame(root, borderwidth=2, relief='sunken')
scrolled_frame.pack(expand=True, fill='both')

# Add some widgets to the inner frame
for i in range(50):
    label = tk.Label(scrolled_frame, text="Label " + str(i))
    label.pack()

root.mainloop()
