import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('iPhone Style Calculator')
        self.setFixedSize(300, 400)
        self.init_ui()
        self.current_expression = ''

    def init_ui(self):
        main_layout = QVBoxLayout()

        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(50)
        self.display.setStyleSheet('font-size: 24px;')
        main_layout.addWidget(self.display)

        grid_layout = QGridLayout()

        buttons = [
            ['AC', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        for row, row_buttons in enumerate(buttons):
            col_offset = 0
            for col, btn_text in enumerate(row_buttons):
                if btn_text == '0':
                    btn = QPushButton(btn_text)
                    btn.setFixedHeight(60)
                    btn.setFixedWidth(135)
                    grid_layout.addWidget(btn, row + 1, col, 1, 2)
                    btn.clicked.connect(self.on_button_click)
                    col_offset = 1
                elif btn_text == '=':
                    btn = QPushButton(btn_text)
                    btn.setFixedSize(60, 60)
                    grid_layout.addWidget(btn, row + 1, col + col_offset)
                    btn.clicked.connect(self.on_button_click)
                else:
                    btn = QPushButton(btn_text)
                    btn.setFixedSize(60, 60)
                    grid_layout.addWidget(btn, row + 1, col + col_offset)
                    btn.clicked.connect(self.on_button_click)

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def on_button_click(self):
        sender = self.sender()
        new_text = sender.text()

        if new_text == 'AC':
            self.current_expression = ''
        elif new_text == '=':
            try:
                result = str(eval(self.current_expression))
                self.current_expression = result
            except Exception:
                self.current_expression = 'Error'
        elif new_text == '+/-':
            try:
                if self.current_expression:
                    if self.current_expression.startswith('-'):
                        self.current_expression = self.current_expression[1:]
                    else:
                        self.current_expression = '-' + self.current_expression
            except Exception:
                self.current_expression = 'Error'
        elif new_text == '%':
            try:
                self.current_expression = str(float(self.current_expression) / 100)
            except Exception:
                self.current_expression = 'Error'
        else:
            self.current_expression += new_text

        self.display.setText(self.current_expression)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())
