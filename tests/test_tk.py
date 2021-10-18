import sys,os
from tkinter import mainloop
sys.path.append(os.getcwd())
import komepiLib.k_tkinter as tkm
import komepiLib.GraphPlt as gl
import numpy as np

if __name__ == "__main__":
    win = tkm.create_new_window("100x100")
    x = [i for i in range(100)]
    y = [i*2 for i in range(100)]
    y2=[i*3 for i in range(100)]
    gg = gl.GraphPlt()
    
    gg.make_graph(x,y,"line",color="gray",label="test")
    gg.twin_axes()
    gg.twin_add_graph(x,y2,"bar",color="red",label="test2")
    #gg.ax.set_xticks(np.arange(0,len(x),5))
    gg.set_span_xlim(y[-1],5,0)
    gg.plt(is_twin=True,rotate_xlim=-10)
    mainloop()