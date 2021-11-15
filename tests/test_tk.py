import sys,os
from tkinter import mainloop
sys.path.append(os.getcwd())
import komepiTkinter.k_tkinter as tkm
import komepiTkinter.GraphPlt as gl
from komepiTkinter.k_tkinter import TreeView


if __name__ == "__main__":
    win = tkm.new_window("500x500")
    tree = TreeView(win,["test0","test1","test2"],[200,200,200],12,True,False)
    for i in range(20):
        iid = tree.insert_data(["data0","data1","data2"],is_open=True)
        tree.insert_data(["","data11","data12"],parent=iid)
    tree.plot("top")
    win.mainloop()