# @file: nano_hmi.py
#
# @brief: Create a simple HMI GUI using tkinter.
#

# imports
import sys
from tkinter import *
from tkinter import ttk

def main(argv):
  """ Main Program """
  
  root = Tk()
  frm = ttk.Frame(root, padding=10)
  frm.grid()
  ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
  ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
  root.mainloop()

if __name__ == "__main__":
  main(sys.argv)
  