from random import randint
import time
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    pass

class Unit():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __repr__(self):
        return f"({self.x},{self.y})"
class Ship:
    def __init__(self,coords,size,orientation):
        self.size = size
        self.HP = size
        self.coords = coords
        self.orientation = orientation

    @property
    def ship_units(self):
        ship_units = []
        for i in range(self.size):
            cur_x = self.coords.x
            cur_y = self.coords.y

            if self.orientation == 0:
                cur_x += i
            elif self.orientation == 1:
                cur_y += i
            ship_units.append(Unit(cur_x,cur_y))
        return  ship_units
    def shooten(self,shot):
        return shot in self.ship_units
class Battlefield:
    def __init__(self,size = 6,hiden = False):
        self.size = size
        self.hid = hiden
        self.busy = []
        self.ships = []
        self.field = [["0"] * size for i in range(size)]
        self.count = 0

    def __str__(self):
        result = "  |"
        for i in range(self.size):
            result += f" {i+1} |"
        for i, row in enumerate(self.field):
            result += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            result = result.replace("■","0")
        return result

    def out(self, d):
        return not((0<= d.x < self.size) and (0<= d.y < self.size))

    def contour(self,ship,verb = False):
        close_zone = [(-1,-1),(-1,0),(-1,1),
                      (0,-1),(0,0),(0,1),
                      (1,-1),(1,0),(1,1)]
        for d in ship.ship_units:
            for dx, dy in close_zone:
                cur = Unit(d.x + dx,d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.ship_units:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()

        for d in ship.ship_units:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self,d):
        if self.out(d):
            raise BoardOutException()
        if d in self.busy:
            raise BoardUsedException()
        self.busy.append(d)

        for ship in self.ships:
            if ship.shooten(d):
                ship.HP -= 1
                self.field[d.x][d.y] = "F"
                if ship.HP == 0:
                    self.count += 1
                    self.contour(ship,verb = True)
                    print("Корабль уничтожен")
                    return "Убил"
                else:
                    print("Корабль ранен")
                    return "Попал"
        self.field[d.x][d.y] = "."
        print("Мимо")
        return "Мимо"
    def begin(self):
        self.busy = []
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self, hit = None):
        while True:
            try:
                target = self.ask(hit)
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self, last_hit = None):
        b = Battlefield()
        time.sleep(1.5)
        while True:
            if not last_hit is None:
                d = Unit(randint(last_hit.x - 1, last_hit.x + 1), randint(last_hit.y - 1, last_hit.y + 1))
            else:
                d = Unit(randint(0, b.size), randint(0, b.size))
            if not d in b.busy and not b.out(d):
                break
        print(f"Ход компьютера: {d.x+1} {d.y+1}")
        self.hit = d
        return d

class User(Player):
    def ask(self, last_hit = None):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Unit(x - 1, y - 1)

class Game:
    def __init__(self, size=6, choise = "Нет"):
        self.size = size
        self.choise = choise
        if choise == "Нет" or choise == "Ytn":
            pl = self.random_board()
        elif choise == "Да" or choise == "Lf":
            pl = self.creat_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Battlefield(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Unit(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def creat_board(self):
        lens = [3, 2, 2, 1, 1, 1]
        board = Battlefield(size=self.size)
        for l in lens:
            while True:
                print(board)
                cords = input(f"Введите координаты корабля размером {l}: ").split()

                if len(cords) != 2:
                    print(" Введите 2 координаты! ")
                    continue

                x, y = cords

                if not (x.isdigit()) or not (y.isdigit()):
                    print(" Введите числа! ")
                    continue

                x, y = int(x), int(y)
                if l != 1:
                    o = input("Выберите ориентацию(верт/гор): ")
                    if o == "верт" or o == "dthn":
                        o = 0
                    elif o == "гор" or o == "ujh":
                        o = 1
                    ship = Ship(Unit(x - 1, y - 1), l, int(o))
                elif l == 1:
                    ship = Ship(Unit(x - 1, y - 1), l, 1)
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    print("Неправильное расположение корабля")
                    continue
        board.begin()
        return board

    def loop(self):
        num = 0
        last_hit = None
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move(last_hit)

            if num % 2 != 0:
                if repeat == "Попал":
                    last_hit = self.ai.hit
                if repeat == "Убил":
                    last_hit = None
                if repeat == "Мимо":
                    last_hit = None

            if repeat == "Убил" or repeat == "Попал":
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.loop()

def greet():
    print("-------------------")
    print("  Приветсвуем вас  ")
    print("      в игре       ")
    print("    морской бой    ")
    print("-------------------")
    print(" формат ввода: x y ")
    print(" x - номер строки  ")
    print(" y - номер столбца ")
    print("-------------------")
    print("Если вы хотите быстрый Старт")
    print("    Введите Да     ")
    print("Если вы хотите настроить бой")
    print("    Введите Нет    ")

def start_game():
    greet()
    while True:
        fast = input("Быстрый бой? ")
        if fast == "Ytn" or fast =="Нет" or fast == "нет" or fast == "ytn":
            s = input("Выберите размер поля: ")
            if s.isdigit():
                b = input("Желаете расставить корабли самостоятельно?(Да/Нет): ")
                if b == "Lf" or b =="Ytn" or b =="Да" or b =="Нет":
                    g = Game(int(s),str(b))
                    g.start()
                    break
                else:
                    print("Напишите Да или Нет")
                    continue
            else:
                print("Введите число")
                continue
        elif fast == "Lf" or fast == "Да" or fast == "да" or fast == "lf":
            g = Game()
            g.start()
            break
        else:
            print("Напишите Да или Нет")
start_game()