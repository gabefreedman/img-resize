# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 15:49:25 2019

@author: Gabe Freedman
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from image_tools import resize_all

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

class ImageApp():

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Image Resizing Application')
        
        self.folderLabel = tk.Label(self.root, text='Choose folder with images to resize:')
        self.folderLabel.grid(column=0, row=0, sticky='EW', padx=4, pady=4)
        self.folderVar = tk.StringVar(None)
        self.folderName = tk.Entry(self.root, textvariable=self.folderVar)
        self.folderName.grid(column=1,row=0,sticky='EW', padx=4, pady=4)
        self.folderName.update()
        self.folderName.focus_set()
        
        self.heightLabel = tk.Label(self.root, text='Enter desired image height in inches:')
        self.heightLabel.grid(column=0,row=1,sticky='EW', padx=4, pady=4)
        self.heightVar = tk.StringVar(None)
        self.heightEntry = tk.Entry(self.root, bd=1, textvariable=self.heightVar)
        self.heightEntry.grid(column=1,row=1,sticky='EW', padx=4, pady=4)
    
        self.button = tk.Button(self.root, text='Browse', command=self.browse)
        self.button.grid(column=2,row=0,sticky='EW', padx=4, pady=4)
        
        self.identLabel = tk.Label(self.root, text='Identifier to add to new folder name:')
        self.identLabel.grid(column=0, row=2, sticky='EW', padx=4, pady=4)
        self.identEntry = EntryWithPlaceholder(self.root, '(Optional)')
        self.identEntry.grid(column=1, row=2, sticky='EW', padx=4, pady=4)
        
        self.borderVar = tk.IntVar(None)
        self.borderCheck = tk.Checkbutton(self.root, text='Add border? (1px)', variable = self.borderVar)
        self.borderCheck.grid(column=1, row=3, sticky='EW', padx=4, pady=4)        
        
        self.bigButton = tk.Button(self.root, text='Resize', command=self.gather_resize_params)
        self.bigButton.grid(column=1,row=4,sticky='EW', padx=4, pady=4)
        
        self.root.mainloop()
    
    def browse(self):
        self.filename = filedialog.askdirectory(parent=self.root,title='Choose a file')
        self.folderVar.set(self.filename)
    
    def clear_box(self):
        self.identVar.delete(0, tk.END)
        return
    def handle_event(self, event):
      print('Handling an event')
    
    def gather_resize_params(self):
        folder = self.folderVar.get()
        if folder == '':
            messagebox.showerror('error', 'try again')
            return
        
        height = self.heightEntry.get()
        try:
            height = float(height)
        except ValueError:
            messagebox.showerror('error', 'try again')
            return
        
        ident = self.identEntry.get()
        if ident in ['', '(Optional)']:
            ident = str(height) + 'inch'
        
        border = self.borderVar.get()
        
        resize_all(folder, height, ident, border)

if __name__ == '__main__':
    ImageApp()