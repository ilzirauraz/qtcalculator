import sys
# from interface import *
from PyQt5 import QtCore, QtGui, QtWidgets
from interface import Ui_MainWindow

READY = 0
INPUT = 1

class MyWin(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MyWin, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.memory = 0
        self.reset()

        
        #Событие нажатия на кнопку
        #self.ui.pushButton_0.clicked.connect(self.func)

        # #Привязываем все кнопки с цифрами к одному обработчику события
        for n in range(0, 10):
            getattr(self, 'pushButton_' + str(n)).pressed.connect(lambda v=n: self.input_number(v))

        #обработчики для математических операций
        self.pushButton_add.pressed.connect(lambda:self.operation(add))
        self.pushButton_sub.pressed.connect(lambda:self.operation(subtract))
        self.pushButton_div.pressed.connect(lambda:self.operation(divide))s
        self.pushButton_mul.pressed.connect(lambda:self.operation(multiply))
        self.pushButton_per.pressed.connect(self.operation_pc)
        self.pushButton_m.pressed.connect(self.memory_store)
        self.pushButton_mr.pressed.connect(self.memory_recall)

        self.pushButton_equal.pressed.connect(self.equals)

        #кнопка сброса
        self.pushButton_17.pressed.connect(self.reset)



    def func(self):
        pass

    def display(self):
        """Отображение цифр при нажатии"""        
        self.lcdNumber.display(self.stack[-1])

    def reset(self):
        """сброс"""        
        self.state = READY
        self.stack = [0]
        self.last_operation = None
        self.current_op = None
        self.display()
    
    def input_number(self, v):
        """Это стек. Каждое числовое нажатие умножает текущее конечное значение стека на 10 и добавляет нажатое значение.
        Например, если мы нажали попоряду 2,4,5 то в стеке будет лежать число 235"""
        if self.state == READY:
            self.state = INPUT
            self.stack[-1] = v
        else:
            self.stack[-1] = self.stack[-1] * 10 + v

        self.display()
    
    def operation(self, op):
        """храним выбранную операцию"""    

        if self.current_op:  # Если до этого содержалась какая-то операция, то вычисляем ее значение с помощью функции equals
            self.equals()

        self.stack.append(0)
        self.state = INPUT
        self.current_op = op

    def equals(self):
        """Равно"""        
        # Support to allow '=' to repeat previous operation
        # if no further input has been added.
        if self.state == READY and self.last_operation:
            s, self.current_op = self.last_operation
            self.stack.append(s)

        if self.current_op:
            self.last_operation = self.stack[-1], self.current_op

            try:
                #в стек зносится только что полученный результат
                self.stack = [self.current_op(*self.stack)]
            except Exception:
                self.lcdNumber.display('Err')
                self.stack = [0]
            else:
                self.current_op = None
                self.state = READY
                self.display()

    def operation_pc(self):
        """Подсчет процента"""        
        self.state = INPUT
        self.stack[-1] *= 0.01 #берется введенное число
        self.display()

    #Работа с памятью
    def memory_store(self):
        """Сохранить в памяти значение, которое сейчас на экране"""        
        self.memory = self.lcdNumber.value()

    def memory_recall(self):
        """Вывести значение, которое сохранено в памяти"""        
        self.state = INPUT
        self.stack[-1] = self.memory
        self.display()
    



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
