from tkinter import *
from tkinter import messagebox # для окна выхода
import time

def on_closing():
    global app_running # global - чтобы ф-я передала наружу своё значение
    if messagebox.askokcancel("Выход из игры", "Хотите выйти из игры?"): # окно выхода из игры
        app_running = False
        tk.destroy()
def draw_table(): # функция, которая создает поле
    for i in range(0, s_x + 1):
        canvas.create_line(step_x * i, 0, step_x * i, size_canvas_y)
    for i in range(0, s_y + 1):
        canvas.create_line(0, step_y * i, size_canvas_x, step_y * i)

def button_show_enemy(): # функция, которая показывает корабли противника
    pass

def button_restart(): # функция, которая перезапускает игру
    pass

def add_to_all(event):
    _type = 0 # ЛКМ # переменная для хранения произведённого нажатия
    if event.num == 3:
        _type = 1 # ПКМ
    print(_type)
    # координаты игрового поля 
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx() 
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty() 
    print(mouse_x, mouse_y)
    # координаты ячейки
    cell_x = mouse_x // step_x
    cell_y = mouse_y // step_y
    print(cell_x, cell_y)



tk = Tk() # создание окна
app_running = True # чтоб узнать, работает ли приложение

size_canvas_x = 600
size_canvas_y = 600 # для создания окна с определённым разрешением px
s_x = s_y = 10 # размер игрового поля
# получаем размер шагов между ячейками
step_x = size_canvas_x // s_x # шаг по горизонтали
step_y = size_canvas_y // s_y # шаг по вертикали
# это для того, чтобы убрать остаток от деления из игровой области
size_canvas_x = step_x * s_x 
size_canvas_y = step_y * s_y

menu_x = 250

tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title("Морской бой")
tk.resizable(0,0) # запрет на изменение размера окна
tk.wm_attributes("-topmost", 1) # чтоб окно было поверх других окон
canvas = Canvas(tk, width=size_canvas_x + menu_x, height=size_canvas_y, bd = 0, highlightthickness = 0) # создание окна
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill = "white") # создаём прямоугольную область внутри окна
canvas.pack() # паковка в окно
tk.update() # обновление окна

draw_table()

b0 = Button(tk, text = "Показать корабли противника", command = button_show_enemy)
b0.place(x = size_canvas_x + 20, y = 30)
b1 = Button(tk, text = "Начать заново!", command = button_restart)
b1.place(x = size_canvas_x + 20, y = 80)

canvas.bind_all("<Button-1>", add_to_all) # ЛКМ
canvas.bind_all("<Button-3>", add_to_all) # ПКМ

while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.05)



