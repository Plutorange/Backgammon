import random
import sqlite3
import sys

from PIL import Image, ImageDraw
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication

from main import Ui_Dialog


class Example(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.wsum = 0
        self.bsum = 0
        self.sequence = 1
        self.bblot = 0
        self.wblot = 0
        self.setupUi(self)
        self.buttonList = []
        self.n = []
        self.nom = []
        self.m = 0
        self.show_pic = False
        self.white_out = 0
        self.black_out = 0
        self.first = None
        self.second = None
        self.buttonCheck = [['w', 2], ['-', 0], ['-', 0], ['-', 0], ['-', 0], ['b', 5],
                            ['-', 0], ['b', 3], ['-', 0], ['-', 0], ['-', 0], ['w', 5],
                            ['b', 5], ['-', 0], ['-', 0], ['-', 0], ['w', 3], ['-', 0],
                            ['w', 5], ['-', 0], ['-', 0], ['-', 0], ['-', 0], ['b', 2]]
        self.buttonList = [self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4,
                           self.pushButton_5, self.pushButton_6, self.pushButton_7,
                           self.pushButton_8, self.pushButton_9, self.pushButton_10,
                           self.pushButton_11, self.pushButton_12, self.pushButton_13,
                           self.pushButton_14, self.pushButton_15, self.pushButton_16,
                           self.pushButton_17, self.pushButton_18, self.pushButton_19,
                           self.pushButton_20, self.pushButton_21, self.pushButton_22,
                           self.pushButton_23, self.pushButton_24]
        self.num_edit = [self.spinBox, self.spinBox_2, self.spinBox_3, self.spinBox_4,
                         self.spinBox_5, self.spinBox_6, self.spinBox_7, self.spinBox_8,
                         self.spinBox_9, self.spinBox_10, self.spinBox_11, self.spinBox_12,
                         self.spinBox_13, self.spinBox_14, self.spinBox_15, self.spinBox_16,
                         self.spinBox_17, self.spinBox_18, self.spinBox_19, self.spinBox_20,
                         self.spinBox_21, self.spinBox_22, self.spinBox_23, self.spinBox_24]
        self.col_edit = [self.comboBox, self.comboBox_2, self.comboBox_3, self.comboBox_4,
                         self.comboBox_5, self.comboBox_6, self.comboBox_7, self.comboBox_8,
                         self.comboBox_9, self.comboBox_10, self.comboBox_11, self.comboBox_12,
                         self.comboBox_13, self.comboBox_14, self.comboBox_15, self.comboBox_16,
                         self.comboBox_17, self.comboBox_18, self.comboBox_19, self.comboBox_20,
                         self.comboBox_21, self.comboBox_22, self.comboBox_23, self.comboBox_24]
        self.t = ' '.join(open('texts/rules.txt').read())
        self.order.setText('ХОД БЕЛЫХ')
        self.replayButton.setHidden(True)
        for i in range(len(self.col_edit)):
            self.col_edit[i].addItems(['-', 'w', 'b'])
        for i in self.col_edit:
            i.setHidden(True)
        for i in self.num_edit:
            i.setHidden(True)
        self.confirmButton.setHidden(True)
        self.edit_maker()
        self.board_maker()
        self.score_maker()
        self.movements_maker()
        self.blot_maker()
        self.initUI()
        self.buttonDice.clicked.connect(self.dice_maker)
        for i in self.buttonList:
            i.clicked.connect(self.make_move)
        self.whiteHouse.clicked.connect(self.make_move)
        self.blackHouse.clicked.connect(self.make_move)
        self.buttonBlot.clicked.connect(self.make_move)
        self.buttonRules.clicked.connect(self.set_rules)
        self.optionButton.clicked.connect(self.make_edit)
        self.confirmButton.clicked.connect(self.make_edit)
        self.replayButton.clicked.connect(self.replay)

    def initUI(self):
        self.label.setPixmap(QPixmap('board.png'))
        self.buttonDice.setIcon(QIcon('dices.png'))
        self.buttonDice.setIconSize(QSize(96, 48))
        self.whiteHouse.setIconSize(QSize(24, 360))
        self.blackHouse.setIconSize(QSize(24, 360))
        self.buttonBlot.setIcon(QIcon('blot.png'))
        self.buttonBlot.setIconSize(QSize(48, 96))

    def set_rules(self):
        if self.textRule.text() == '':
            self.textRule.setText(self.t)
        else:
            self.textRule.setText('')

    def edit_maker(self):
        self.edit = Image.new('RGB', (600, 600), (80, 80, 80))
        self.draw = ImageDraw.Draw(self.edit)
        self.draw.rectangle(((40, 40), (560, 560)), (130, 130, 130))
        self.draw.rectangle(((280, 40), (320, 560)), (80, 80, 80))
        for j in range(2):
            for i in range(6):
                if i < 3:
                    self.draw.polygon(
                        ((abs(600 * j - (40 + 80 * i)), abs(600 * j - 40)),
                         (abs(600 * j - (60 + 80 * i)), abs(600 * j - 280)),
                         (abs(600 * j - (80 + 80 * i)), abs(600 * j - 40))), (0, 180, 180))
                    self.draw.polygon(
                        ((abs(600 * j - (80 + 80 * i)), abs(600 * j - 40)),
                         (abs(600 * j - (100 + 80 * i)), abs(600 * j - 280)),
                         (abs(600 * j - (120 + 80 * i)), abs(600 * j - 40))), (180, 180, 180))
                else:
                    self.draw.polygon(
                        ((abs(600 * j - (80 + 80 * i)), abs(600 * j - 40)),
                         (abs(600 * j - (100 + 80 * i)), abs(600 * j - 280)),
                         (abs(600 * j - (120 + 80 * i)), abs(600 * j - 40))), (0, 180, 180))
                    self.draw.polygon(
                        ((abs(600 * j - (120 + 80 * i)), abs(600 * j - 40)),
                         (abs(600 * j - (140 + 80 * i)), abs(600 * j - 280)),
                         (abs(600 * j - (160 + 80 * i)), abs(600 * j - 40))), (180, 180, 180))
        self.edit.save('edit.png', 'PNG')

    def board_maker(self):
        self.board = Image.new("RGB", (720, 720), (80, 80, 80))
        self.draw = ImageDraw.Draw(self.board)
        self.draw.rectangle(((48, 48), (672, 672)), (130, 130, 130))
        self.draw.rectangle(((336, 48), (384, 672)), (80, 80, 80))
        self.board.save('board.png', 'PNG')
        self.label.setPixmap(QPixmap('board.png'))

    def score_maker(self):
        self.score = Image.new("RGB", (24, 360), (50, 50, 50))
        self.draw = ImageDraw.Draw(self.score)
        for i in range(self.white_out):
            self.draw.rectangle(((2, 338 - 24 * i), (21, 357 - 24 * i)), (255, 255, 0))
        self.score.save('score.png', 'PNG')
        self.whiteHouse.setIcon(QIcon('score.png'))
        self.score = Image.new("RGB", (24, 360), (50, 50, 50))
        self.draw = ImageDraw.Draw(self.score)
        for i in range(self.black_out):
            self.draw.rectangle(((2, 2 + 24 * i), (21, 21 + 24 * i)), (255, 255, 0))
        self.score.save('score.png', 'PNG')
        self.blackHouse.setIcon(QIcon('score.png'))

    def blot_maker(self):
        self.blotp = Image.new("RGB", (48, 96), (128, 0, 255))
        self.draw = ImageDraw.Draw(self.blotp)
        if self.wblot:
            self.draw.ellipse(((2, 2), (45, 45)), (255, 255, 255))
        if self.bblot:
            self.draw.ellipse(((2, 50), (45, 93)), (0, 0, 0))
        self.blotp.save('blot.png', 'PNG')
        self.buttonBlot.setIcon(QIcon('blot.png'))

    def movements_maker(self):
        for i in self.buttonList:
            if self.buttonList.index(i) < 12:
                if self.buttonList.index(i) % 2 == 0:
                    self.triangle2 = Image.new("RGB", (48, 288), (130, 130, 130))
                    self.draw = ImageDraw.Draw(self.triangle2)
                    self.draw.polygon(((0, 0), (24, 288), (47, 0)), (180, 180, 180))
                    for j in range(self.buttonCheck[self.buttonList.index(i)][1]):
                        if self.buttonCheck[self.buttonList.index(i)][0] == 'w':
                            self.draw.ellipse(((1, 1 + 48 * j), (46, 46 + 48 * j)), (255, 255, 255))
                        else:
                            self.draw.ellipse(((1, 1 + 48 * j), (46, 46 + 48 * j)), (0, 0, 0))
                    self.triangle2.save('triangle1.png', 'PNG')
                    i.setIcon(QIcon('triangle1.png'))
                    i.setIconSize(QSize(48, 288))
                else:
                    self.triangle1 = Image.new("RGB", (48, 288), (130, 130, 130))
                    self.draw = ImageDraw.Draw(self.triangle1)
                    self.draw.polygon(((0, 0), (24, 288), (47, 0)), (0, 180, 180))
                    for j in range(self.buttonCheck[self.buttonList.index(i)][1]):
                        if self.buttonCheck[self.buttonList.index(i)][0] == 'w':
                            self.draw.ellipse(((1, 1 + 48 * j), (46, 46 + 48 * j)), (255, 255, 255))
                        else:
                            self.draw.ellipse(((1, 1 + 48 * j), (46, 46 + 48 * j)), (0, 0, 0))
                    self.triangle1.save('triangle1.png', 'PNG')
                    i.setIcon(QIcon('triangle1.png'))
                    i.setIconSize(QSize(48, 288))
            else:
                if self.buttonList.index(i) % 2 != 0:
                    self.triangle4 = Image.new("RGB", (48, 288), (130, 130, 130))
                    self.draw = ImageDraw.Draw(self.triangle4)
                    self.draw.polygon(((0, 288), (24, 0), (47, 288)), (180, 180, 180))
                    for j in range(self.buttonCheck[self.buttonList.index(i)][1]):
                        if self.buttonCheck[self.buttonList.index(i)][0] == 'w':
                            self.draw.ellipse(((1, 288 - (46 + 48 * j)), (46, 288 - (1 + 48 * j))),
                                              (255, 255, 255))
                        else:
                            self.draw.ellipse(((1, 288 - (46 + 48 * j)), (46, 288 - (1 + 48 * j))),
                                              (0, 0, 0))
                    self.triangle4.save('triangle1.png', 'PNG')
                    i.setIcon(QIcon('triangle1.png'))
                    i.setIconSize(QSize(48, 288))
                else:
                    self.triangle3 = Image.new("RGB", (48, 288), (130, 130, 130))
                    self.draw = ImageDraw.Draw(self.triangle3)
                    self.draw.polygon(((0, 288), (24, 0), (47, 288)), (0, 180, 180))
                    for j in range(self.buttonCheck[self.buttonList.index(i)][1]):
                        if self.buttonCheck[self.buttonList.index(i)][0] == 'w':
                            self.draw.ellipse(((1, 288 - (46 + 48 * j)), (46, 288 - (1 + 48 * j))),
                                              (255, 255, 255))
                        else:
                            self.draw.ellipse(((1, 288 - (46 + 48 * j)), (46, 288 - (1 + 48 * j))),
                                              (0, 0, 0))
                    self.triangle3.save('triangle1.png', 'PNG')
                    i.setIcon(QIcon('triangle1.png'))
                    i.setIconSize(QSize(48, 288))

    def dice_maker(self):
        if not self.nom:
            self.n = [random.randrange(1, 7), random.randrange(1, 7)]
            self.n.sort()
            if self.n[0] == self.n[1]:
                self.nom = [self.n[0], self.n[0], self.n[0], self.n[0]]
            else:
                self.nom = [self.n[0], self.n[1]]
            self.dice = Image.new('RGB', (96, 48), (255, 255, 255))
            self.draw = ImageDraw.Draw(self.dice)
            for i in range(2):
                if self.n[i] % 2 == 1:
                    self.draw.ellipse(((20 + 48 * i, 20), (27 + 48 * i, 27)), (0, 0, 0))
                    if self.n[i] >= 3:
                        self.draw.ellipse(((6 + 48 * i, 34), (13 + 48 * i, 41)), (0, 0, 0))
                        self.draw.ellipse(((34 + 48 * i, 6), (41 + 48 * i, 13)), (0, 0, 0))
                        if self.n[i] == 5:
                            self.draw.ellipse(((6 + 48 * i, 6), (13 + 48 * i, 13)), (0, 0, 0))
                            self.draw.ellipse(((34 + 48 * i, 34), (41 + 48 * i, 41)), (0, 0, 0))
                else:
                    self.draw.ellipse(((6 + 48 * i, 34), (13 + 48 * i, 41)), (0, 0, 0))
                    self.draw.ellipse(((34 + 48 * i, 6), (41 + 48 * i, 13)), (0, 0, 0))
                    if self.n[i] >= 4:
                        self.draw.ellipse(((6 + 48 * i, 6), (13 + 48 * i, 13)), (0, 0, 0))
                        self.draw.ellipse(((34 + 48 * i, 34), (41 + 48 * i, 41)), (0, 0, 0))
                        if self.n[i] == 6:
                            self.draw.ellipse(((6 + 48 * i, 20), (13 + 48 * i, 27)), (0, 0, 0))
                            self.draw.ellipse(((34 + 48 * i, 20), (41 + 48 * i, 27)), (0, 0, 0))
            self.dice.save('dices.png', 'PNG')
            self.buttonDice.setIcon(QIcon('dices.png'))
        for i in self.nom:
            if (self.sequence % 2 == 1 and self.wblot) or \
                    (self.sequence % 2 == 0 and self.bblot):
                allow = False
                for j in self.n:
                    if not ((self.buttonCheck[j - 1][0] == 'w' or self.buttonCheck[j - 1][0]
                             == 'b') and self.buttonCheck[j - 1][1] > 1):
                        allow = True
                if not allow:
                    self.nom = []
                    self.cor()

    def make_edit(self):
        lis = list(map(lambda x: self.col_edit.index(x),
                       filter(lambda x: x.currentText() == 'b', self.col_edit)))
        self.black_summ = sum(map(lambda x: x.value(),
                                  filter(lambda x: self.num_edit.index(x) in lis, self.num_edit)))
        lis = list(map(lambda x: self.col_edit.index(x),
                       filter(lambda x: x.currentText() == 'w', self.col_edit)))
        self.white_summ = sum(map(lambda x: x.value(),
                                  filter(lambda x: self.num_edit.index(x) in lis, self.num_edit)))
        if not self.show_pic:
            self.textRule.setPixmap(QPixmap('edit.png'))
            self.show_pic = True
            for i in self.col_edit:
                i.setHidden(False)
            for i in self.num_edit:
                i.setHidden(False)
            self.confirmButton.setHidden(False)
        else:
            self.textRule.setText(' ')
            self.textRule.setText('')
            self.show_pic = False
            for i in self.col_edit:
                i.setHidden(True)
            for i in self.num_edit:
                i.setHidden(True)
            self.confirmButton.setHidden(True)
        if self.sender() == self.confirmButton:
            if self.white_summ == 15 and self.black_summ == 15:
                for i in range(len(self.buttonCheck)):
                    self.buttonCheck[i] = [self.col_edit[i].currentText(), self.num_edit[i].value()]
                for i in range(len(self.buttonCheck)):
                    if self.buttonCheck[i][1] == 0:
                        self.buttonCheck[i][0] = '-'
                    elif self.buttonCheck[i][0] == '-':
                        self.buttonCheck[i][1] = 0
            self.movements_maker()

    def make_move(self):
        self.wsum = sum(map(lambda x: self.buttonCheck[self.buttonList.index(x)][1],
                            filter(lambda x: self.buttonCheck[self.buttonList.index(x)][0] == 'w',
                                   self.buttonList[18:])))
        self.bsum = sum(map(lambda x: self.buttonCheck[self.buttonList.index(x)][1],
                            filter(lambda x: self.buttonCheck[self.buttonList.index(x)][0] == 'b',
                                   self.buttonList[:6])))
        if not self.first and self.nom:
            self.first = self.sender()
        elif not self.second and self.nom:
            self.second = self.sender()
            if self.second == self.whiteHouse:
                if self.buttonCheck[self.buttonList.index(self.first)][0] == 'w' and \
                        self.sequence % 2 == 1 and self.wsum == 15 and \
                        (len(self.buttonList) - self.buttonList.index(self.first)) <= max(self.n):
                    self.buttonCheck[self.buttonList.index(self.first)][1] -= 1
                    self.white_out += 1
                    self.score_maker()
                    self.m = len(self.buttonList) - self.buttonList.index(self.first)
                    for i in self.n:
                        if i >= self.m:
                            self.m = i
                            break
                    self.cor()
            elif self.second == self.blackHouse:
                if self.buttonCheck[self.buttonList.index(self.first)][0] == 'b' and \
                        self.sequence % 2 == 0 and self.bsum == 15 and \
                        self.buttonList.index(self.first) <= max(self.n):
                    self.buttonCheck[self.buttonList.index(self.first)][1] -= 1
                    self.black_out += 1
                    self.score_maker()
                    self.m = self.buttonList.index(self.first) + 1
                    for i in self.n:
                        if i >= self.m:
                            self.m = i
                            break
                    self.cor()
            elif self.first == self.buttonBlot:
                if self.sequence % 2 == 1 and self.wblot and \
                        self.buttonList.index(self.second) + 1 in self.n:
                    self.m = self.buttonList.index(self.second) + 1
                    if self.buttonCheck[self.buttonList.index(self.second)][0] == 'w' or \
                            self.buttonCheck[self.buttonList.index(self.second)][0] == '-':
                        self.wblot -= 1
                        self.buttonCheck[self.buttonList.index(self.second)][1] += 1
                        self.buttonCheck[self.buttonList.index(self.second)][0] = 'w'
                        self.blot_maker()
                        self.cor()
                    elif self.buttonCheck[self.buttonList.index(self.second)][1] == 1:
                        self.wblot -= 1
                        self.blot()
                        self.buttonCheck[self.buttonList.index(self.second)][0] = 'w'
                        self.cor()
                elif self.sequence % 2 == 0 and self.bblot and \
                        len(self.buttonList) - self.buttonList.index(self.second) in self.n:
                    self.m = len(self.buttonList) - 1 - self.buttonList.index(self.second)
                    if self.buttonCheck[self.buttonList.index(self.second)][0] == 'b' or \
                            self.buttonCheck[self.buttonList.index(self.second)][0] == '-':
                        self.bblot -= 1
                        self.buttonCheck[self.buttonList.index(self.second)][1] += 1
                        self.buttonCheck[self.buttonList.index(self.second)][0] = 'b'
                        self.blot_maker()
                        self.cor()
                    elif self.buttonCheck[self.buttonList.index(self.second)][1] == 1:
                        self.bblot -= 1
                        self.blot()
                        self.buttonCheck[self.buttonList.index(self.second)][0] = 'b'
                        self.cor()
            elif abs(self.buttonList.index(self.first) - self.buttonList.index(
                    self.second)) in self.nom and \
                    (self.buttonCheck[self.buttonList.index(self.first)][0] ==
                     'w' or self.buttonCheck[self.buttonList.index(self.first)][0] == 'b'):
                self.m = abs(self.buttonList.index(self.first) - self.buttonList.index(self.second))
                if self.buttonCheck[self.buttonList.index(self.first)][0] == 'w' and \
                        self.sequence % 2 == 1 and self.wblot == 0 and \
                        self.buttonList.index(self.first) < self.buttonList.index(self.second):
                    if self.buttonCheck[self.buttonList.index(self.first)][0] == \
                            self.buttonCheck[self.buttonList.index(self.second)][0] or \
                            self.buttonCheck[self.buttonList.index(self.second)][0] == '-':
                        self.buttonCheck[self.buttonList.index(self.first)][1] -= 1
                        self.buttonCheck[self.buttonList.index(self.second)][1] += 1
                        self.buttonCheck[self.buttonList.index(self.second)][0] = \
                            self.buttonCheck[self.buttonList.index(self.first)][0]
                        self.cor()
                    elif self.buttonCheck[self.buttonList.index(self.second)][1] == 1:
                        self.blot()
                        self.buttonCheck[self.buttonList.index(self.first)][1] -= 1
                        self.buttonCheck[self.buttonList.index(self.second)][0] = \
                            self.buttonCheck[self.buttonList.index(self.first)][0]
                        self.cor()
                elif self.buttonCheck[self.buttonList.index(self.first)][0] == 'b' and \
                        self.sequence % 2 == 0 and self.bblot == 0 and \
                        self.buttonList.index(self.first) > self.buttonList.index(self.second):
                    if self.buttonCheck[self.buttonList.index(self.first)][0] == \
                            self.buttonCheck[self.buttonList.index(self.second)][0] or \
                            self.buttonCheck[self.buttonList.index(self.second)][0] == '-':
                        self.buttonCheck[self.buttonList.index(self.first)][1] -= 1
                        self.buttonCheck[self.buttonList.index(self.second)][1] += 1
                        self.buttonCheck[self.buttonList.index(self.second)][0] = \
                            self.buttonCheck[self.buttonList.index(self.first)][0]
                        self.cor()
                    elif self.buttonCheck[self.buttonList.index(self.second)][1] == 1:
                        self.blot()
                        self.buttonCheck[self.buttonList.index(self.first)][1] -= 1
                        self.buttonCheck[self.buttonList.index(self.second)][0] = \
                            self.buttonCheck[self.buttonList.index(self.first)][0]
                        self.cor()
            if self.first in self.buttonList:
                if self.buttonCheck[self.buttonList.index(self.first)][1] == 0:
                    self.buttonCheck[self.buttonList.index(self.first)][0] = '-'
            self.first, self.second = None, None
            self.movements_maker()

    def cor(self):
        for i in range(len(self.nom)):
            if self.nom[i] == self.m:
                self.nom.pop(i)
                break
        if not self.nom:
            self.sequence += 1
        if self.sequence % 2 == 1:
            self.order.setText('ХОД БЕЛЫХ')
        else:
            self.order.setText('ХОД ЧЁРНЫХ')
        if self.white_out == 15:
            self.order.setText('ПОБЕДИЛИ БЕЛЫЕ')
            self.sqlka = sqlite3.connect('win_statistics.sqlite')
            self.cur = self.sqlka.cursor()
            self.cur.execute(f'''INSERT INTO turn_of_wins(white_wins,black_wins)
VALUES(True,False)''')
            self.parameter_1 = self.cur.execute('''SELECT white_wins FROM turn_of_wins''')
            self.s1 = sum(map(lambda x: x[0], self.parameter_1))
            self.parameter_2 = self.cur.execute('''SELECT black_wins FROM turn_of_wins''')
            self.s2 = sum(map(lambda x: x[0], self.parameter_2))
            self.label_2.setText(f'Белые {self.s1} : {self.s2} Чёрные')
            self.sqlka.commit()
            self.replayButton.setHidden(False)
        if self.black_out == 15:
            self.order.setText('ПОБЕДИЛИ ЧЁРНЫЕ')
            self.sqlka = sqlite3.connect('win_statistics.sqlite')
            self.cur = self.sqlka.cursor()
            self.cur.execute(f'''INSERT INTO turn_of_wins(white_wins,black_wins)
VALUES(False,True)''')
            self.parameter_1 = self.cur.execute('''SELECT white_wins FROM turn_of_wins''')
            self.s1 = sum(map(lambda x: x[0], self.parameter_1))
            self.parameter_2 = self.cur.execute('''SELECT black_wins FROM turn_of_wins''')
            self.s2 = sum(map(lambda x: x[0], self.parameter_2))
            self.label_2.setText(f'Белые {self.s1} : {self.s2} Чёрные')
            self.sqlka.commit()
            self.replayButton.setHidden(False)
        if self.sequence > 1:
            self.optionButton.setHidden(True)

    def blot(self):
        if self.buttonCheck[self.buttonList.index(self.second)][0] == 'w':
            self.wblot += 1
        else:
            self.bblot += 1
        self.blot_maker()

    def replay(self):
        self.replayButton.setHidden(True)
        self.order.setText('ХОД БЕЛЫХ')
        self.label_2.setText('')
        self.wsum = 0
        self.bsum = 0
        self.sequence = 1
        self.bblot = 0
        self.wblot = 0
        self.n = []
        self.nom = []
        self.m = 0
        self.show_pic = False
        self.white_out = 0
        self.black_out = 0
        self.first = None
        self.second = None
        self.buttonCheck = [['w', 2], ['-', 0], ['-', 0], ['-', 0], ['-', 0], ['b', 5],
                            ['-', 0], ['b', 3], ['-', 0], ['-', 0], ['-', 0], ['w', 5],
                            ['b', 5], ['-', 0], ['-', 0], ['-', 0], ['w', 3], ['-', 0],
                            ['w', 5], ['-', 0], ['-', 0], ['-', 0], ['-', 0], ['b', 2]]
        self.edit_maker()
        self.board_maker()
        self.score_maker()
        self.movements_maker()
        self.blot_maker()
        self.initUI()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec()
