from tkinter import *
import random

root = Tk()  # Создаем окно
root.title("Змейка")  # Устанавливаем название окна

WIDTH = 800  # ширина экрана
HEIGHT = 600  # высота экрана
SEG_SIZE = 20  # Размер сегмента змейки
IN_GAME = True  # Переменная отвечающая за состояние игры


def create_food():  # Создает еду в случайной позиции на карте
    global FOOD
    posx = SEG_SIZE * random.randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * random.randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE)

    FOOD = c.create_oval(posx, posy,  # еда это кружочек красного цвета
                         posx + SEG_SIZE,
                         posy + SEG_SIZE,
                         fill="red")


def main():
    global IN_GAME

    if IN_GAME:
        s.move()  # Двигаем змейку

        head_coords = c.coords(s.body_elements[-1].instance)  # Определяем координаты головы
        x1, y1, x2, y2 = head_coords

        if x1 < 0 or x2 > WIDTH or y1 < 0 or y2 > HEIGHT:  # Столкновение с границами экрана
            IN_GAME = False

        elif head_coords == c.coords(FOOD):  # Поедание еды
            s.add_segment()
            c.delete(FOOD)
            create_food()

        # Если врезаться в тело
        else:
            for index in range(len(s.body_elements) - 1):  # Проходим по всем сегментам змеи
                if c.coords(s.body_elements[index].instance) == head_coords:
                    IN_GAME = False
        root.after(100, main)
    # Если не в игре выводим сообщение о проигрыше
    else:
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')


class body_elements(object):  # Класс элементов тела
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y, x + SEG_SIZE, y + SEG_SIZE, fill="green")


class Snake(object):  # Создаем класс змеи
    def __init__(self, body_elements):
        self.body_elements = body_elements
        self.mapping = {"Down": (0, 1), "Up": (0, -1), "Left": (-1, 0),
                        "Right": (1, 0)}  # список доступных направлений движения змейки
        self.vector = self.mapping["Right"]  # изначально змейка двигается вправо

    def move(self):  # Двигает змейку в заданном направлении

        for index in range(len(self.body_elements) - 1):  # перебираем все сегменты кроме первого
            segment = self.body_elements[index].instance
            x1, y1, x2, y2 = c.coords(self.body_elements[index + 1].instance)
            c.coords(segment, x1, y1, x2, y2)  # задаем каждому сегменту позицию сегмента стоящего после него

        x1, y1, x2, y2 = c.coords(self.body_elements[-2].instance)  # получаем координаты сегмента перед "головой"

        c.coords(self.body_elements[-1].instance,  # помещаем "голову" в направлении указанном в векторе движения
                 x1 + self.vector[0] * SEG_SIZE,
                 y1 + self.vector[1] * SEG_SIZE,
                 x2 + self.vector[0] * SEG_SIZE,
                 y2 + self.vector[1] * SEG_SIZE)

    def change_direction(self, event):  # Изменяет направление движения змейки
        # event передаст нам символ нажатой клавиши
        # и если эта клавиша в доступных направлениях
        # изменяем направление
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def add_segment(self):  # Добавляет сегмент змейке

        last_seg = c.coords(self.body_elements[0].instance)  # определяем последний сегмент

        x = last_seg[2] - SEG_SIZE  # определяем координаты куда поставить следующий сегмент
        y = last_seg[3] - SEG_SIZE

        self.body_elements.insert(0, body_elements(x, y))  # добавляем змейке еще один сегмент в заданных координатах

    def reset_snake(self):  # перезапускаем змейку
        for segment in self.body_elements:
            c.delete(segment.instance)


def set_state(item, state):  # Выводим сообщения
    c.itemconfigure(item, state=state)


def clicked(event):  # Обработка клика
    global IN_GAME
    s.reset_snake()
    IN_GAME = True
    c.delete(FOOD)
    c.itemconfigure(restart_text, state='hidden')
    c.itemconfigure(game_over_text, state='hidden')
    start_game()


def start_game():  # Запускаем игру
    global s
    create_food()
    s = create_snake()
    c.bind("<KeyPress>", s.change_direction)  # Реакция на нажатия клавиш
    main()


def create_snake():  # Создание змейки
    body = [body_elements(SEG_SIZE, SEG_SIZE),
            body_elements(SEG_SIZE * 2, SEG_SIZE),
            body_elements(SEG_SIZE * 3, SEG_SIZE)]
    return Snake(body)


c = Canvas(root, width=WIDTH, height=HEIGHT, bg="black")  # создаем экземпляр класса Canvas
                                                            # (его мы еще будем использовать)
                                                            # и заливаем все зеленым цветом
c.grid()
c.focus_set()  # Наводим фокус на Canvas, чтобы мы могли ловить нажатия клавиш

game_over_text = c.create_text(WIDTH / 2, HEIGHT / 2, text="Поражение!", fill='red', state='hidden', font='Calibri 30')
restart_text = c.create_text(WIDTH / 2, HEIGHT - HEIGHT / 3, fill='white', text="Новая игра", state='hidden',
                             font='Calibri 50')

c.tag_bind(restart_text, "<Button-1>", clicked)

start_game()

root.mainloop()  # Запускаем окно
