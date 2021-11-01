import tkinter as tk
from tkinter.constants import LEFT, TOP
from tkinter import filedialog
from tkinter import StringVar
from tkinter import ttk
import os
import re

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
#



def make_input_text(frame_r, label_text, text_width, initial = None, side_=TOP, side_label = LEFT,fmt = None):
    """テキストの入力ボックスを作成

    Args:
        frame_r (tkinter.Frame): 配置するフレーム
        label_text (str): ラベル
        text_width (int): 入力欄の幅
        initial (str, optional): 初期値. Defaults to None.
        side_ (tk.constants, optional): テキストボックス群の配置. Defaults to TOP.
        side_label (tk.contains, optional): ラベルとテキストボックスの位置関係. Defaults to LEFT.
        fmt (str): 正規表現. Default to None.
    Returns:
        tkinter.entry: テキストボックス
    """
    frame = tk.Frame(frame_r)
    frame.pack(side=side_)
    label = tk.Label(frame, text = label_text)
    label.pack(side=LEFT)
    if not fmt == None:
        def validate_input_header(val):
            """正規表現チェック

            Args:
                val (str)): 入力値
                fmt (str):正規表現

            Returns:
                bool: 正規表現にマッチしているか
            """
            if val == "":
                return True
            if re.fullmatch(fmt, val):
                return True
            return False
        validate = frame_r.register(validate_input_header)
    else:
        validate = None
    text = tk.Entry(frame, width = text_width,validate="key",validatecommand=(validate, "%P"))
    if initial != None:
        text.insert(tk.END,initial)
    label.pack(side=side_label)
    text.pack(side=side_label)
    return text

def make_input_path(frame_r,  label_text, width_input, file_or_dir="file", initial = None,side_ = TOP):
    """ファイル（ディレクトリ）選択ボックスの配置

    Args:
        frame_r (tkinter.Frame): 配置するフレーム
        label_text (str): ラベル
        width_input (int): 入力欄の幅
        file_or_dir (str): "file" or "dir". Defaults to "file"
        initial (str, optional): 初期値. Defaults to None.
        side_ (tk.constants, optional): テキストボックス群の配置. Default to TOP.

    Returns:
        tkinter.Entry: パスの入力欄
    """
    frame = tk.Frame(frame_r)
    frame.pack(side=side_)
    label = tk.Label(frame, text = label_text)
    label.pack(side=LEFT)
    entry = StringVar()
    IFileEntry = ttk.Entry(frame, textvariable=entry, width=width_input)
    if initial != None:
        IFileEntry.insert(tk.END, initial)
    IFileEntry.pack(side=LEFT)
    if file_or_dir == "file":
        IFileButton = ttk.Button(frame, text="参照", command=lambda:filedialog_clicked(entry))
    elif file_or_dir == "dir":
        IFileButton = ttk.Button(frame, text="参照", command=lambda:dirdialog_clicked(entry))
    IFileButton.pack(side=LEFT)
    return entry
def make_label(frame_r, text,side="top"):
    """ラベルを配置

    Args:
        frame_r (tk.Frame): 配置するフレーム
        text (str): ラベル本文
        side (str, optional): 配置の仕方. Defaults to "top".
    """
    label = tk.Label(frame_r,text=text)
    label.pack(side=side)
    
def create_new_window(size, title="window", resize=None, icon_file = None, topLevel=False):
    """新規ウィンドウの作成

    Args:
        size (str): サイズ. "[width]x[height]"で入力
        title (str, optional): ウィンドウタイトル. Defaults to "window".
        resize (taple, optional): ウィンドウのサイズ変更の可否。タプル型でTrue or Falseで設定(width, height). Defaults to None.
        icon_file (str, optional): ウィンドウのアイコンファイルのパス. Defaults to None.
        topLevel (bool, optional): ウィンドウをメインウィンドウに連動させるか. Defaults to False.

    Returns:
        tkinter.Tk: ウィンドウ
    """
    if topLevel:
        win = tk.Toplevel()
    else:
        win = tk.Tk()
    win.geometry(size)
    win.title(title)
    if not resize == None:
        win.resizable(width = resize[0], height = resize[1])
    if not icon_file == None:
        if os.path.isfile(icon_file):
            win.iconphoto(False, tk.PhotoImage(file = icon_file))
    return win

def make_scroll(frame_r, widget, vector = "Y", is_canvas = False,region = None):
    """スクロールの作成

    Args:
        frame_r (tk.Frame): 配置フレーム
        widget (widget): 対象ウィジェット
        vector (int, optional): スクロール方向.y方向:"Y", x方向:"X". Defaults to "Y".
        is_canvas (bool, optional): canvasに配置するかどうか. Defaults to False.
        region (list), optional): canvasに配置する場合、スクロールサイズ. Defaults to None.
    """
    if vector == "X":
        scroll = tk.Scrollbar(frame_r,orient=tk.HORIZONTAL,command = widget.xview)
        widget.config(xscrollcommand = scroll.set)
    elif vector == "Y":
        scroll = tk.Scrollbar(frame_r,orient=tk.VERTICAL,command = widget.yview)
        widget.config(yscrollcommand = scroll.set)
    if is_canvas:
        widget.config(scrollregion=region)
    return scroll

def make_progress_bar(value, max_ = 100):
    """プログレスバーの配置

    Args:
        value (method): 返り値が値のメソッド
        max_ (int, optional): 最大値. Defaults to 100.
    """
    win = create_new_window("300x100", "しばらくお待ちください")
    pb = ttk.Progressbar(win, maximum= max_, mode = "determinate", variable = value)
    pb.pack()

def change_frame(frame):
    """画面遷移

    Args:
        frame (tk.Frame): 表示するフレーム
    """
    frame.tkraise()

def make_listbox(frame_r, lists, text_ = None, side_ = TOP, width_ = 30, height_ = 6):
    """リストボックスを作成
    listbox.curselection()で現在選択しているインデックスを取得
    listbox.get(xx)でそのテキストを取得
    Args:
        frame_r (tk.Frame): 配置したフレーム
        lists (list): 項目
        text_ (str, optional): 何のリストか示すテキスト. Defaults to None.
        side_ (tk.contains, optional): どこに配置するか. Defaults to TOP.
        width_ (int, optional): 幅. Defaults to 30.
        height_ (int, optional): 表示する項目数. Defaults to 6.

    Returns:
        tk.Listbox: 作成したリストボックス
    """
    var = tk.StringVar(value = lists)
    frame = tk.Frame(frame_r)
    frame.pack(side = side_)
    if not text_ == None:
        label = tk.Label(frame, text = text_)
        label.pack()
    listbox = tk.Listbox(frame, listvariable=var,width = width_,height = height_)
    listbox.pack(side="left")
    if len(lists) > height_:
        scrollbar = ttk.Scrollbar(frame, orient = "vertical", command=listbox.yview)
        listbox["yscrollcommand"] = scrollbar.set
        scrollbar.pack(side="right",fill="both")

    return listbox

def make_table(frame_r, header, lists, widths, side_=TOP, is_scroll = False):
    """テーブルを作成する

    Args:
        frame_r (tk.Frame): 配置したいフレーム
        header (list): 項目名のリスト
        lists (list): 挿入するデータのリスト。項目数が複数の場合、listsのそれぞれの要素はlistもしくはtupleとなる.

        widths (list): それぞれの項目の幅
        side_ (tk.contains, optional): どこに配置するか. Defaults to TOP.
        is_scroll (bool, optional): スクロールは必要か. Defaults to False.

    Returns:
        tk.Treeview: テーブル
    """
    tree_frame = tk.Frame(frame_r)
    tree_frame.pack(side=side_)
    tree = ttk.Treeview(tree_frame)
    tree["column"] = tuple([i for i in range(1, len(header)+1)])
    tree["show"] = "headings"

    for i in tree["column"]:
        tree.column(int(i), width = widths[int(i)-1])
    for i in range(1, len(header) + 1):
        tree.heading(i, text=header[i-1])
    
    for l in lists:
        tree.insert("", "end", values=tuple(l))
    
    if is_scroll:
        vbar = make_scroll(tree_frame, tree)
        tree.pack(side="left")
        vbar.pack(side="left",fill=tk.Y)
    else:
        tree.pack()
    
    return tree

def make_button(frame_r, text_, command_,width_ = 20,side_ = TOP):
    """ボタンを配置

    Args:
        frame_r (tk.Frame): 配置したいフレーム
        text_ (str): ボタンに表記するテキスト
        command_ (command): 押されたときに呼び出される関数
        width_ (int, optional): 幅. Defaults to 20.
        side_ (tk.contains, optional): 配置される位置. Defaults to TOP.
    """
    frame = tk.Frame(frame_r)
    frame.pack(side=side_)
    button = tk.Button(frame, text=text_,width = width_,command=command_)
    button.pack()

#def graph_plt(data, graph_type="bar",title_ = "plot graph", twin_data = None, graph_type2 = "bar", kind_grid = None, range5 = None, rotate_xlim = None, showbar_=60, topLevel = False):
#    """データをプロットしたウィンドウを表示する。グラフ、スクロールバー、ボタンが配置され、スクロールバーを動かしてグラフのプロット範囲を変更する。ボタンを押下するとウィンドウが閉じる。
#
#    Args:
#        data (dict): キーにx軸、値にy軸の値を持つ辞書型
#        graph_type (str, optional): グラフのタイプ。bar:棒グラフ, line:折れ線グラフ. Defaults to "bar".
#        title_ (str, optional): ウィンドウのタイトル. Default to "plot graph".
#        twin_data(dict) :複数のグラフを重ねる場合、dataと同じ形式で二つ目のデータを入力. Default to None.
#        graph_type2(str): 複数のグラフを重ねる場合、twin_dataをプロットするグラフの種類. Default to "bar".
#        kind_grid (bool, optional): 表示するグリッドの種類("x" or "y"). Defaults to False.
#        range5(int) :x軸を5刻みにするとき、表示する範囲. Default to None.
#        rotate_xlim (int, optional): x軸ラベルの角度. Defaults to None.
#        showbar_ (int, optional): グラフの拡大率. Defaults to 60.
#        topLevel (bool, optional): ウィンドウを連動させるか. Defaults to False.
#    """
#    fig = Figure(figsize=(6,6))
#    ax1 = fig.add_subplot(111)
#    if topLevel:
#        frame = tk.Toplevel()
#    else:
#        frame = tk.Tk()
#    frame.title(title_)
#    canvasFrame = tk.Frame(frame)
#    canvasFrame.pack(side=tk.TOP)
#
#    controlFrame = tk.Frame(frame)
#    controlFrame.pack(side=tk.BOTTOM)
#
#    canvas = FigureCanvasTkAgg(fig, canvasFrame)
#
#    tmp = canvas.get_tk_widget()
#    tmp.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
#    showbars=showbar_
#    if graph_type == "bar":
#        ax1.bar(list(data.keys()), list(data.values()))
#    elif graph_type == "line":
#        ax1.plot(list(data.keys()), list(data.values()))
#    if not kind_grid == None:
#        ax1.grid(axis = kind_grid, linestyle="--")
#    if not range5 == None:
#        xtick = [1]
#        xtick.extend([i * 5 for i in range(1, ((range5 - 1)//5) + 1)])
#        ax1.set_xticks(xtick)
#    if not rotate_xlim == None:
#        fig.autofmt_xdate(rotation = rotate_xlim)
#
#    def draw_plot(pos):
#        pos_ = float(pos)
#        ax1.set_xlim(pos_-1, pos_+showbars+1)
#        canvas.draw()
#    
#    y_scale = ttk.Scale(controlFrame, from_=0.0, to=len(data)-showbars, length=480, orient=tk.HORIZONTAL, command=draw_plot)
#    y_scale.pack(fill=tk.X)
#    btn = tk.Button(controlFrame, text="閉じる", command = frame.destroy)
#    btn.pack()
#    draw_plot(0)


# ファイル指定の関数
def filedialog_clicked(entry):
    fTyp = [("", "*")]
    iFile = os.path.abspath(os.path.dirname(__file__))
    iFilePath = filedialog.askopenfilename(filetype = fTyp, initialdir = iFile)
    entry.set(iFilePath)

# フォルダ指定の関数
def dirdialog_clicked(entry):
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir = iDir)
    entry.set(iDirPath)
