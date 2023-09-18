from tkinter import Tk, Label
 
# メインウィンドウ生成
root = Tk()
 
# メインウィンドウの設定
root.title("サンプル1")
 
# Labelウィジェットをメインウィンドウに生成&配置
label = Label(root, text="Hello world")
label.pack()
 
# イベントループの開始
root.mainloop()