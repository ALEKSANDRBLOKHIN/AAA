import random


# Класс исключения для выхода за пределы поля
class BoardOutException(Exception):
    pass


# Класс точки на поле
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# Класс корабля
class Ship:
    def __init__(self, length, bow, direction):
        self.length = length
        self.bow = bow
        self.direction = direction
        self.lives = length

    def dots(self):
        ship_dots = []
        x, y = self.bow.x, self.bow.y
        for i in range(self.length):
            x += self.direction.x
            y += self.direction.y
            ship_dots.append(Dot(x, y))
        return ship_dots


# Класс игровой доски
class Board:
    def __init__(self, hidden=False):
        self.field = [[' '] * 6 for _ in range(6)]
        self.ships = []
        self.hidden = hidden
        self.live_ships = 0

    def add_ship(self, ship):

        for dot in ship.dots():
            if self.out(dot):
                raise BoardOutException("Cannot place a ship here")
            if self.field[dot.x][dot.y] in ['■', '.']:
                raise BoardOutException("Cannot place a ship here")

        for dot in ship.dots():
            self.field[dot.x][dot.y] = '■'
        self.ships.append(ship)
        self.live_ships += 1
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dot in ship.dots():
            for dx, dy in near:
                x, y = dot.x + dx, dot.y + dy
                if not (self.out(Dot(x, y))) and self.field[x][y] in [' ', '.']:
                    if verb:
                        self.field[x][y] = '•'
                    else:
                        self.field[x][y] = '.'

    def out(self, dot):
        return not ((0 <= dot.x < 6) and (0 <= dot.y < 6))

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException("Out of the board")
        if self.field[dot.x][dot.y] in ['•', 'X']:
            raise BoardOutException("Cannot shot there")
        for ship in self.ships:
            if dot in ship.dots():
                ship.lives -= 1
                self.field[dot.x][dot.y] = 'X'
                if ship.lives == 0:
                    self.live_ships -= 1
                    self.contour(ship, verb=True)
                    print("You destroyed a ship!")
                    return True
                else:
                    print("You hit a ship!")
                    return True
        self.field[dot.x][dot.y] = '•'
        print("You missed!")
        return False

    def get_board(self):
        board = '  | 1 2 3 4 5 6'
        for i, row in enumerate(self.field):
            row_str = ' '.join(row)
            board += f'\n{i + 1} | {row_str}'
        return board

    def __str__(self):
        if self.hidden:
            return self.get_board().replace("■", ' ').replace(".", ' ')

        return self.get_board()


# Класс игрока
class Player:
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                if not repeat:
                    return
            except BoardOutException as e:
                print(e)
            except Exception as e:
                print(e)


# Класс игрока-пользователя
class User(Player):
    def ask(self):
        while True:
            try:
                coords = list(map(int, input("Enter coordinates for your shot ( x,y e.g. 2,3): ").strip().split(",")))
                if len(coords) != 2:
                    raise ValueError("Enter 3 characters: x,y")
                x = coords[0] - 1
                y = coords[1] - 1
                return Dot(x, y)
            except ValueError as e:
                print(e)

    def move(self):
        global game

        while True:
            try:
                game.showBoard()
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                if not repeat:
                    return
            except BoardOutException as e:
                print(e)
            except Exception as e:
                print(e)


# Класс игрока-компьютера
class AI(Player):
    def ask(self):
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        return Dot(x, y)


# Класс игры
class Game:
    def __init__(self):
        self.user_board = Board()
        self.ai_board = Board(True)

        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)

    def random_board(self, board):
        directions = [Dot(-1, 0), Dot(1, 0), Dot(0, -1), Dot(0, 1)]
        ships = [3, 2, 2, 1, 1, 1, 1]
        for ship_len in ships:
            count = 0
            while True:
                count += 1
                if count > 1000:
                    print("Не получилось")
                    break
                ship = Ship(ship_len, Dot(random.randint(0, 5), random.randint(0, 5)), directions[random.randint(0, 3)])
                try:
                    board.add_ship(ship)
                    break
                except BoardOutException:
                    pass

    def greet(self):
        print("Welcome to Battleship!")
        # self.showBoard()

    def showBoard(self):
        print("Your board:")
        print(self.user_board)
        print("Enemy board:")
        print(self.ai_board)

    def loop(self):
        while True:
            if self.user_board.live_ships == 0:
                print("AI wins! You lose!")
                break
            if self.ai_board.live_ships == 0:
                print("You win! AI loses!")
                break
            print("Your turn:")
            self.user.move()
            print("Enemy's turn:")
            self.ai.move()

    def start(self):
        self.random_board(self.user_board)
        self.random_board(self.ai_board)
        self.greet()
        self.loop()


game = Game()
game.start()