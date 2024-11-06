# from . import tk 
from tkinter import *
import time

class ShowStatus:

    def __init__(self, master):
        self.status = {
            "Initilizing":{"background":"black","forground":"white"},
            "Listning":{"background":"red","forground":"black"},
            "Stoped":{"background":"white","forground":"black"},
            "Starting":{"background":"white","forground":"black"},
        }
        self.Show = master
        self.Show.title("ASSISTANT Status")
        self.change_status()
        # self.Show.mainloop() 

    def change_status(self, msg="Starting"):
        if msg in self.status:
            print(msg)
            self.label = Label(self.Show, text=msg, bg=self.status[msg]["background"], fg=self.status[msg]["forground"])
            self.label.pack(fill=BOTH, expand=True)  # Set label to fill the entire window
        else:
            self.label = Label(self.Show, text=msg, bg="Black", fg="white")
            self.label.pack(fill=BOTH, expand=True)  # Set label to fill the entire window

    def destroy_status(self):
        self.label.destroy()

    def __destroy__(self):
        self.Show.destroy()

