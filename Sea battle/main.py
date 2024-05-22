from tkinter import *
from tkinter import messagebox # для окна выхода
import time
import random

def on_closing():
    global app_running # global - чтобы ф-я передала наружу своё значение
    if messagebox.askokcancel("Выход из игры", "Хотите выйти из игры?"): # окно выхода из игры
        app_running = False
        tk.destroy()
# функция, которая создает поле
def draw_table(offset_x = 0): # offset_x - смещение по x
    for i in range(0, s_x + 1):
        canvas.create_line(offset_x + step_x * i, 0, offset_x + step_x * i, size_canvas_y)
    for i in range(0, s_y + 1):
        canvas.create_line(offset_x, step_y * i,offset_x + size_canvas_x, step_y * i)

def button_show_enemy_1(): # функция, которая показывает корабли противника
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships_1[j][i] > 0:
                color = 'red'
                if cleaked_positions_1[j][i] != -1:
                    color = 'green'
                _id = canvas.create_rectangle(step_x * i, step_y * j, step_x * i + step_x, step_y * j + step_y, fill = color)
                list_ids.append(_id)

def button_show_enemy_2(): # функция, которая показывает корабли противника
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships_2[j][i] > 0:
                color = 'red'
                if cleaked_positions_2[j][i] != -1:
                    color = 'green'
                _id = canvas.create_rectangle((size_canvas_x + menu_x) + step_x * i, step_y * j,(size_canvas_x + menu_x) + step_x * i + step_x, step_y * j + step_y, fill = color)
                list_ids.append(_id)

def button_restart(): # функция для кнопки Начать заново (очищает поле от кораблей)
    global list_ids
    global cleaked_positions_1, cleaked_positions_2
    global enemy_ships_1, enemy_ships_2
    for el in list_ids:
        canvas.delete(el)
    list_ids = []
    enemy_ships_1 = generate_enemy_ships()
    enemy_ships_2 = generate_enemy_ships()
    cleaked_positions_1 = [[-1 for i in range(s_x)] for i in range(s_y)]
    cleaked_positions_2 = [[-1 for i in range(s_x)] for i in range(s_y)]

def draw_point(x, y): # функция для отрисовки точки или крестика
    # print(enemy_ships[y][x])
    if enemy_ships_1[y][x] == 0: # отрисовка круга при промахе
        color = 'black'
        id1 = canvas.create_oval(step_x * x, step_y * y, step_x * x + step_x, step_y * y + step_y, fill=color)
        id2 = canvas.create_oval(step_x * x + (step_x // 4), step_y * y + (step_y // 4), step_x * x + step_x - (step_x // 4), step_y * y + step_y - (step_y // 4), fill= "gray")  
        list_ids.append(id1) # добавляем круги в список
        list_ids.append(id2) # чтоб они очищались
    if enemy_ships_1[y][x] > 0: # отрисовка крестика при попадании
        color = "blue"
        id1 = canvas.create_rectangle(step_x * x, step_y * y + (step_y // 2 - step_y // 10), step_x * x + step_x, step_y * y + (step_y // 2 + step_y // 10), fill= color)
        id2 = canvas.create_rectangle(step_x * x + (step_x // 2 - step_x // 10), step_y * y, step_x * x + (step_x // 2 + step_x // 10), step_y * y + step_y, fill= color)
        list_ids.append(id1)
        list_ids.append(id2)

def check_winner(): # функция для проверки победы
    win = True
    for i in range(0,s_x):
        for j in range(0, s_y):
            if enemy_ships_1[j][i] > 0: # если для всех эл-в, где нах-ся вражеский корабль 
                if cleaked_positions_1[j][i] == -1: # мы прокликали, то мы победили
                    win = False
    return win
def add_to_all(event): # ф-я для определения координат клика мышки
    global cleaked_positions_1
    _type = 0 # ЛКМ # переменная для хранения произведённого нажатия
    if event.num == 3:
        _type = 1 # ПКМ
    # print(_type)
    # координаты игрового поля 
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx() 
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty() 
    # print(mouse_x, mouse_y)
    # координаты ячейки
    cell_x = mouse_x // step_x
    cell_y = mouse_y // step_y
    # print(cell_x, cell_y, "type: ", _type)
    # проверка на выход за границы поля
    if cell_x < s_x and cell_y < s_y:
        if cleaked_positions_1[cell_y][cell_x] == -1:
            cleaked_positions_1[cell_y][cell_x] = _type
            draw_point(cell_x, cell_y) # вызываем ф-ю для отображения точки или крестика
            # Проверка победы
            if check_winner():
                print("Вы выиграли!")
                cleaked_positions_1 = [[10 for i in range(s_x)] for i in range(s_y)]
        # print(len(list_ids))


def generate_enemy_ships(): # функция, которая генерирует корабли противника
    enemy_ships = []  
    ships_list = []
    # генерируем список случайных длин кораблей
    for i in range(0, ships):
        ships_list.append(random.choice([ship_len1, ship_len2, ship_len3]))
    # print(ships_list)

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
        # print(enemy_ships)
        return enemy_ships

tk = Tk() # создание окна
app_running = True # чтоб узнать, работает ли приложение

size_canvas_x = 500
size_canvas_y = 500 # для создания окна с определённым разрешением px
s_x = s_y = 10 # размер игрового поля
# получаем размер шагов между ячейками
step_x = size_canvas_x // s_x # шаг по горизонтали
step_y = size_canvas_y // s_y # шаг по вертикали
# это для того, чтобы убрать остаток от деления из игровой области
size_canvas_x = step_x * s_x 
size_canvas_y = step_y * s_y

menu_x = step_x * 5 #250
menu_y = 40

tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title("Морской бой")
tk.resizable(0,0) # запрет на изменение размера окна
tk.wm_attributes("-topmost", 1) # чтоб окно было поверх других окон
canvas = Canvas(tk, width = size_canvas_x + menu_x + size_canvas_x, height = size_canvas_y + menu_y, bd = 0, highlightthickness = 0) # создание окна
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill = "white") # создаём прямоугольную область внутри окна
canvas.create_rectangle(size_canvas_x + menu_x, 0, size_canvas_x + menu_x + size_canvas_x, size_canvas_y, fill = "lightyellow") #  для 2 игрока
canvas.pack() # паковка в окно
tk.update() # обновление окна

draw_table() # расчерчиваем линии для 1 игрока
draw_table(size_canvas_x + menu_x) # расчерчиваем линии для 1 игрока

# Надписи Игрок 1 и Игрок 2 делаем
t0 = Label(tk, text = "Игрок 1", font = ("Times New Roman", 16), fg = "black")
t0.place(x = size_canvas_x // 2 - (t0.winfo_reqwidth() // 2), y = size_canvas_y + 3)
t1 = Label(tk, text = "Игрок 2", font = ("Times New Roman", 16), fg = "black")
t1.place(x = size_canvas_x + menu_x + size_canvas_x // 2 - (t1.winfo_reqwidth() // 2), y = size_canvas_y + 3)

# Для определения: кто сейчас ходит
t0.configure(bg = 'red')
t0.configure(bg = '#f0f0f0')

b0 = Button(tk, text = "Показать корабли Игрока 1", command = button_show_enemy_1)
b0.place(x = size_canvas_x + 20, y = 30)

b1 = Button(tk, text = "Показать корабли Игрока 2", command = button_show_enemy_2)
b1.place(x = size_canvas_x + 20, y = 80)

b2 = Button(tk, text = "Начать заново!", command = button_restart)
b2.place(x = size_canvas_x + 20, y = 120)

# привязка событий к нажатию кнопок
canvas.bind_all("<Button-1>", add_to_all) # ЛКМ
canvas.bind_all("<Button-3>", add_to_all) # ПКМ

ships = s_x // 2 # определяем max кол-во кораблей
ship_len1 = s_x // 5 # длина корабля 1 типа
ship_len2 = s_x // 3 # длина корабля 2 типа
ship_len3 = s_x // 2 # длина корабля 3 типа
enemy_ships_1 = [[0 for i in range(s_y + 1)] for i in range(s_x + 1)] # корабли 1 игрока
enemy_ships_2 = [[0 for i in range(s_y + 1)] for i in range(s_x + 1)] # корабли 2 игрока
#print(enemy_ships)
list_ids = [] # список объектов canvas (области)
# cleaked_positions - список, куда кликнули мышкой
cleaked_positions_1 = [[-1 for i in range(s_x)] for i in range(s_y)]
cleaked_positions_2 = [[-1 for i in range(s_x)] for i in range(s_y)]

enemy_ships_1 = generate_enemy_ships()
enemy_ships_2 = generate_enemy_ships()
# print(10*"*")
# print(enemy_ships_1)
# print(10*"*")
# print(enemy_ships_2)
# print(10*"*")

while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.05)



