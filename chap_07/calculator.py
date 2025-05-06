from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
import sys


class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current = '0'
        self.operator = None
        self.operand = None
        self.result_shown = False

    def input_number(self, number):
        if self.result_shown:
            self.current = number
            self.result_shown = False
        elif self.current == '0':
            self.current = number
        else:
            self.current += number
        return self.current

    def input_decimal(self):
        if '.' not in self.current:
            self.current += '.'
        return self.current

    def set_operator(self, operator):
        if self.operator and not self.result_shown:
            self.equal()
        self.operand = float(self.current)
        self.operator = operator
        self.result_shown = False
        self.current = '0'

    def equal(self):
        if self.operator is None:
            return self.current

        try:
            second = float(self.current)
            if self.operator == '+':
                result = self.operand + second
            elif self.operator == '-':
                result = self.operand - second
            elif self.operator == '*':
                result = self.operand * second
            elif self.operator == '/':
                if second == 0:
                    raise ZeroDivisionError
                result = self.operand / second
            else:
                return self.current

            if abs(result) > 1e100:
                raise OverflowError

            self.current = str(round(result, 6))
            if self.current.endswith('.0'):
                self.current = self.current[:-2]
            self.result_shown = True
            self.operator = None
            return self.current

        except ZeroDivisionError:
            self.reset()
            return 'Error (div by 0)'
        except OverflowError:
            self.reset()
            return 'Error (overflow)'

    def toggle_sign(self):
        if self.current.startswith('-'):
            self.current = self.current[1:]
        else:
            if self.current != '0':
                self.current = '-' + self.current
        return self.current

    def percent(self):
        try:
            value = float(self.current) / 100
            self.current = str(round(value, 6))
            if self.current.endswith('.0'):
                self.current = self.current[:-2]
        except ValueError:
            self.current = '0'
        return self.current


class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.calc = Calculator()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Calculator')
        self.setGeometry(100, 100, 300, 400)

        vbox = QVBoxLayout()
        self.display = QLineEdit('0')
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet('font-size: 28px; height: 50px;')

        grid = QGridLayout()
        buttons = [
            ('C', self.clear), ('+/-', self.toggle_sign), ('%', self.percent), ('/', self.operator),
            ('7', self.digit), ('8', self.digit), ('9', self.digit), ('*', self.operator),
            ('4', self.digit), ('5', self.digit), ('6', self.digit), ('-', self.operator),
            ('1', self.digit), ('2', self.digit), ('3', self.digit), ('+', self.operator),
            ('0', self.digit), ('.', self.decimal), ('=', self.equal)
        ]

        positions = [(i, j) for i in range(5) for j in range(4)]
        for position, (text, handler) in zip(positions, buttons):
            btn = QPushButton(text)
            if text == '=':
                btn.clicked.connect(lambda _, h=handler: h())
                grid.addWidget(btn, 4, 3)
            elif text == '0':
                btn.clicked.connect(lambda _, t=text, h=handler: h(t))
                grid.addWidget(btn, 4, 0, 1, 2)
            elif text == '.':
                btn.clicked.connect(lambda _, t=text, h=handler: h(t))
                grid.addWidget(btn, 4, 2)
            else:
                btn.clicked.connect(lambda _, t=text, h=handler: h(t))
                grid.addWidget(btn, *position)


        vbox.addWidget(self.display)
        vbox.addLayout(grid)
        self.setLayout(vbox)

    def update_display(self, value):
        font_size = max(18, 28 - len(value) // 2)
        self.display.setStyleSheet(f'font-size: {font_size}px; height: 50px;')
        self.display.setText(value)

    def digit(self, value):
        self.update_display(self.calc.input_number(value))

    def decimal(self, value):
        self.update_display(self.calc.input_decimal())

    def operator(self, op):
        self.calc.set_operator(op)

    def equal(self):
        self.update_display(self.calc.equal())

    def clear(self, value):
        self.calc.reset()
        self.update_display('0')

    def toggle_sign(self, value):
        self.update_display(self.calc.toggle_sign())

    def percent(self, value):
        self.update_display(self.calc.percent())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc_ui = CalculatorUI()
    calc_ui.show()
    sys.exit(app.exec_())