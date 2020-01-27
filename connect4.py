class Game:
    def __init__(self):
        self.length = 7
        self.hight = 6
        self.desk = None
        self.last_row = ''
        self.matrix = [[i for i in range(1, self.length + 1)]
                       for h in range(self.hight)]
        self.language = None
        self.intro = None
        self.desc_message = 'It is your desk'
        self.command = 'Type the number of column to put your figure: '
        self.error = 'Error. '
        self.full = 'This column has no more space. Choose another one:'
        self.first_player_step = 'First player turn, your figures are denoted as '
        self.second_player_step = 'Second player turn, your figures are denoted as '
        self.victory_first = 'First player wins!'
        self.victory_second = 'Second player wins!'
        self.no_winner = 'Dead heat.'

    def settings(self):
        language = input('Введите 1 для русского языка/ Type anything except 1 for English ')
        if language == '1':
            self.language = 'russian'
        else:
            self.language = 'english'
        if self.language == 'russian':
            self.desc_message = 'Это игровое поле'
            self.command = 'Введите номер, соответсвующий колонке, в которую хотите поместить вашу фигуру: '
            self.error = 'Ошибка. '
            self.full = 'Эта колонка уже полностью заполнена, надо выбрать другую:'
            self.first_player_step = 'Ход первого игрока, фигуры обозначены как '
            self.second_player_step = 'Ход второго игрока, фигуры обозначены как '
            self.victory_first = 'Победа первого игрока!'
            self.victory_second = 'Победа второго игрока!'
            self.no_winner = 'Ничья.'

    def desk_init(self):
        row = ''
        for h in range(self.hight):
            row += '. ' * self.length + '\n'
        for l in range(1, self.length + 1):
            self.last_row = self.last_row + str(l) + ' '
        self.desk = row
        print(self.desc_message)
        print(self.desk)
        print(self.last_row)

    def step(self, player: str):
        position = input(self.command)
        while position not in [str(i) for i in range(1, self.length + 1)]:
            position = input(self.error + self.command)
        while self.matrix[0][int(position) - 1] != int(position):
            position = input(self.full)
        position = int(position)
        for h in range(self.hight):
            if self.matrix[self.hight - h - 1][position - 1] == position:
                self.matrix[self.hight - h - 1][position - 1] = player
                break
        for h in self.matrix:
            h = ['. ' if str(element).isdigit() else element + ' ' for element in h]
            row = ''
            for elem in h:
                row = row + elem
            print(row)
        print(self.last_row)

    def game_over(self, player):
        if self.inline(player, self.matrix) == 'game over':
            return 'game over'
        new_matrix = self.transpose(self.matrix)
        if self.inline(player, new_matrix) == 'game over':
            return 'game over'
        diagonal_list = self.diagonals(self.matrix)
        if self.inline(player, diagonal_list) == 'game over':
            return 'game over'
        matrix_mirrowed = self.mirrow(self.matrix)
        diagonal_list_alternative = self.diagonals(matrix_mirrowed)
        if self.inline(player, diagonal_list_alternative) == 'game over':
            return 'game over'

    def dead_heat(self, player):
        # stop the game before all the positions are filled
        referee = 0
        filled_matrix = [[] for i in range(self.hight)]
        for h in range(self.hight):
            filled_matrix[h] = [player if str(element).isdigit()
                                else element for element in self.matrix[h]]
        if self.inline(player, filled_matrix) != 'game over':
            referee += 1
        new_matrix = self.transpose(filled_matrix)
        if self.inline(player, new_matrix) != 'game over':
            referee += 1
        diagonal_list = self.diagonals(filled_matrix)
        if self.inline(player, diagonal_list) != 'game over':
            referee += 1
        matrix_mirrowed = self.mirrow(filled_matrix)
        diagonal_list_alternative = self.diagonals(matrix_mirrowed)
        if self.inline(player, diagonal_list_alternative) != 'game over':
            referee += 1
        if referee == 4:
            return 'dead heat'

    def transpose(self, matrix):
        length = len(matrix[0])
        hight = len(matrix)
        new_matrix = [[] for i in range(length)]
        for l in range(length):
            for h in range(hight):
                new_matrix[l].append(matrix[h][l])
        return new_matrix

    def mirrow(self, matrix):
        length = len(matrix[0])
        hight = len(matrix)
        new_matrix = [[] for i in range(hight)]
        for h in range(hight):
            new_matrix[h] = [matrix[h][length - l - 1] for l in range(length)]
        return new_matrix

    def inline(self, player, matrix):
        for h in matrix:
            row = ''
            for l in h:
                if str(l).isdigit():
                    row = row + ' '
                elif str(l) != player:
                    row = row + ' '
                else:
                    row = row + str(l)
            row = row.split(' ')
            row = [r for r in row if r != '']
            for item in row:
                if len(item) >= 4:
                    return 'game over'

    def diagonals(self, matrix):
        se = []  # south-east :-)
        length = len(matrix[0])
        hight = len(matrix)
        for hi in range(hight):
            se.append([matrix[hi + l][l] for l in range(length) if hi + l < hight])
        for le in range(length):
            se.append([matrix[h][le + h] for h in range(hight) if h + le < length])
            # we have one duplicate
        return se

    def game(self):
        player1 = 'x'
        player2 = 'o'
        k = 0
        while True:
            if k % 2 == 0:
                print(self.first_player_step, player1)
                self.step(player1)
                k += 1
                if self.game_over(player1) == 'game over':
                    print(self.victory_first)
                    return self.victory_first
                if self.dead_heat(player1) == 'dead heat':
                    if self.dead_heat(player2) == 'dead heat':
                        print(self.no_winner)
                        return self.no_winner
            else:
                print(self.second_player_step, player2)
                self.step(player2)
                k += 1
                if self.game_over(player2) == 'game over':
                    print(self.victory_second)
                    return self.victory_second
                if self.dead_heat(player2) == 'dead heat':
                    if self.dead_heat(player1) == 'dead heat':
                        print(self.no_winner)
                        return self.no_winner


game = Game()
game.settings()
game.desk_init()
game.game()
