from tkinter import *
from tkinter import messagebox # для окна выхода
import time
import random

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
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships[j][i] > 0:
                _id = canvas.create_rectangle(step_x * i, step_y * j, step_x * i + step_x, step_y * j + step_y, fill='red')
                list_ids.append(_id)

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

def generate_enemy_ships(): # функция, которая генерирует корабли противника
    global enemy_ships
    ships_list = []
    # генерируем список случайных длин кораблей
    for i in range(0, ships):
        ships_list.append(random.choice([ship_len1, ship_len2, ship_len3]))
    print(ships_list)

    # подсчёт суммарной длины кораблей
    sum_1_all_ships = sum(ships_list)
    sum_1_enemy = 0
    # в цикле разбрасываем корабли, чтоб они не пересекалисье пе
    while sum_1_enemy != sum_1_all_ships:
        # обнуляем массив кораблей врага
        enemy_ships = [[0 for i in range(s_x + 1)] for i in range(s_y + 1)]  # +1 для доп. линии справа и снизу, для успешных проверок генерации противника

        for i in range(0, ships):
            len = ships_list[i] # длина корабля
            horizont_vertikal = random.randrange(1, 3)  # 1- горизонтальное 2 - вертикальное расположение корабля

            primerno_x = random.randrange(0, s_x) # координата расположения корабля по x
            if primerno_x + len > s_x:
                primerno_x -= len

            primerno_y = random.randrange(0, s_y) # координата расположения корабля по y
            if primerno_y + len > s_y:
                primerno_y -= len

            # print(horizont_vertikal, primerno_x,primerno_y)
            if horizont_vertikal == 1: # горизонтальное расположение
                if primerno_x + len <= s_x: # проверяем, не вышли ли за границы
                    for j in range(0, len): # цикл проверяет, нет ли по соседству корабля
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y][primerno_x - 1] + \
                                               enemy_ships[primerno_y][primerno_x + j] + \
                                               enemy_ships[primerno_y][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y][primerno_x + j] = i + 1  # записываем номер корабля
                        except Exception: # если возникнет исключение, то ничего не делаем
                            pass
            if horizont_vertikal == 2: # вертикальное расположение
                if primerno_y + len <= s_y:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y - 1][primerno_x] + \
                                               enemy_ships[primerno_y + j][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x - 1] + \
                                               enemy_ships[primerno_y + j][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j][primerno_x - 1]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y + j][primerno_x] = i + 1  # записываем номер корабля
                        except Exception:
                            pass

        # делаем подсчет 1ц
        sum_1_enemy = 0
        for i in range(0, s_x):
            for j in range(0, s_y):
                if enemy_ships[j][i] > 0:
                    sum_1_enemy = sum_1_enemy + 1

        # print(sum_1_enemy)
        # print(ships_list)
        print(enemy_ships)


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

ships = s_x // 2 # определяем max кол-во кораблей
ship_len1 = s_x // 5 # длина корабля 1 типа
ship_len2 = s_x // 3 # длина корабля 2 типа
ship_len3 = s_x // 2 # длина корабля 3 типа
enemy_ships = [[0 for i in range(s_y + 1)] for i in range(s_x + 1)]
#print(enemy_ships)
list_ids = [] # список объектов canvas 

generate_enemy_ships()

while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.05)



