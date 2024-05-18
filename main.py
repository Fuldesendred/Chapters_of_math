from tkinter import *
from tkinter import messagebox # для окна выхода
import time

def on_closing():
    global app_running # global - чтобы ф-я передала наружу своё значение
    if messagebox.askokcancel("Выход из игры", "Хотите выйти из игры?"): # окно выхода из игры
        app_running = False
        tk.destroy()

tk = Tk() # создание окна
app_running = True # чтоб узнать, работает ли приложение

size_canvas_x = 600
size_canvas_y = 600 # для создания окна 800 на 800 px



tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title("Морской бой")
tk.resizable(0,0) # запрет на изменение размера окна
tk.wm_attributes("-topmost", 1) # чтоб окно было поверх других окон
canvas = Canvas(tk, width=size_canvas_x, height=size_canvas_y, bd = 0, highlightthickness = 0) # создание окна
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill = "white") # создаём прямоугольную область внутри окна
canvas.pack() # паковка в окно
tk.update() # обновление окна

while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.05)