import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class GraphPlt():
    def __init__(self):
        """インスタンス化。Figureの作成
        """
        self.fig = Figure(figsize=(6,6))

    def plt(self, title="plot graph",topLevel=True,kind_grid=None, is_legend = False,is_twin=False, rotate_xlim=0,show_bar=20):
        """作成したグラフのプロット

        Args:
            title (str, optional): ウィンドウのタイトル. Defaults to "plot graph".
            topLevel (bool, optional): ウィンドウをトップレベルにするか. Defaults to True.
            kind_grid (str, optional): グリッドの有無と方向. Defaults to None.
            is_legend (bool, optional): 凡例の有無. Defaults to False.
            is_twin (bool, optional): 2軸グラフか否か. Defaults to False.
            rotate_xlim (int, optional): x軸ラベルの角度. Defaults to 0.
            show_bar (int, optional): スクロールのスケール. Defaults to 20.
        """
        if topLevel:
            frame = tk.Toplevel()
        else:
            frame = tk.Tk()
        frame.title(title)
        canvasFrame = tk.Frame(frame)
        canvasFrame.pack(side=tk.TOP)
        
        controlFrame = tk.Frame(frame)
        controlFrame.pack(side=tk.BOTTOM)

        canvas = FigureCanvasTkAgg(self.fig, canvasFrame)

        tmp = canvas.get_tk_widget()
        tmp.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        showbars = show_bar
        if not kind_grid == None:
            self.ax.grid(axis = kind_grid,linestyle="--")
        if is_legend:
            self.ax.legend()
        if is_twin:
            self.ax.legend(self.twin_label_handle[0][0]+self.twin_label_handle[1][0],self.twin_label_handle[0][1]+self.twin_label_handle[1][1],loc=2,borderaxespad=0.)
        self.fig.autofmt_xdate(rotation=rotate_xlim)
        def draw_plot(pos):
            pos_ = float(pos)
            self.ax.set_xlim(pos_-1, pos_+showbars+1)
            canvas.draw()
        
        y_scale = ttk.Scale(controlFrame, from_=0.0, to=self.data_len-showbars, length=480, orient=tk.HORIZONTAL, command=draw_plot)
        y_scale.pack(fill=tk.X)
        btn = tk.Button(controlFrame, text="閉じる", command = frame.destroy)
        btn.pack()
        draw_plot(0)
    

    
    def make_graph(self, x, y, graph_type,color = None,marker = None,label=None):
        """最初のグラフの作成

        Args:
            x (list)): x軸のデータ
            y (list): y軸のデータ
            graph_type (str)): グラフの種類
            color (str, optional): グラフの色. Defaults to None.
            label (str, optional): グラフのラベル. Defaults to None.
        """
        self.axes_set()
        self.handler, self.label = self.graph_set(self.ax,x, y, graph_type,color,marker,label)
    

    def add_graph(self, x, y, graph_type,color = None,marker=None,label=None):
        """グラフの追加

        Args:
            x (list): x軸のデータ
            y (list): y軸のデータ
            graph_type (str)): グラフの種類
            color (str, optional): グラフの色. Defaults to None.
            label (str, optional): グラフのラベル. Defaults to None.
        """
        self.graph_set(self.ax,x, y, graph_type,color,marker,label)

    def twin_axes(self):
        """2軸グラフにする
        """
        self.ax_t = self.ax.twinx()
        self.twin_label_handle=list()
        self.twin_label_handle.append((self.handler,self.label))

    def twin_add_graph(self,x,y,graph_type,color=None, marker = None,label=None):
        """2軸グラフに新たなデータの追加

        Args:
            x (list): x軸のデータ
            y (list)): y軸のデータ
            graph_type (str): グラフの種類
            color (str, optional): グラフの色. Defaults to None.
            label (str, optional): グラフのラベル. Defaults to None.
        """
        handler, labels=self.graph_set(self.ax_t,x,y,graph_type,color,marker,label)
        self.twin_label_handle.append((handler,labels))

    def axes_set(self):
        """新たなグラフの追加
        """
        self.ax = self.fig.add_subplot(111)

    def graph_set(self,ax,x,y,graph_type,color,marker,label):
        """グラフのセット

        Args:
            ax (plt.axes): 追加先のグラフ
            x (list): x軸のデータ
            y (list): y軸のデータ
            graph_type (str): グラフの種類
            color (str): グラフの色
            label (str): グラフのラベル

        Returns:
            [type]: [description]
        """
        g = self._graph_select(ax,graph_type)
        if graph_type=="line":
            g(x,y,color=color,label=label,marker=marker)
        else:
            g(x,y,color=color,label=label)
        self.data_len = len(x)
        handler, label = ax.get_legend_handles_labels()
        return handler, label

    
    def set_span_xlim(self,span,last=0,first=0,delta = None):
        """x軸の設定

        Args:
            span (int): 間隔
            last (int, optional): 最後の数値. Defaults to 0.
            first (int, optional): 最初のデータ. Defaults to 0.
            delta (int, optional): last-firstの値. Defaults to None.
        """
        if delta == None:
            xtick = [first]
            xtick.extend([i * span for i in range(1, (( last-first -1)//span) + 1)])
        else:
            xtick = [1]
            xtick.extend([i * span for i in range(1, ((delta-1)//span) + 1)])
        self.ax.set_xticks(xtick)

    def _graph_select(self,ax,graph_type):
        """graph_typeから適するグラフメソッドを返す

        Args:
            ax (plt.axes): 対象のグラフ
            graph_type (str): グラフタイプ.line:折れ線, bar:棒

        Returns:
            plt.axes.method: 適切なグラフメソッド
        """
        if graph_type == "bar":
            return ax.bar
        elif graph_type == "line":
            return ax.plot