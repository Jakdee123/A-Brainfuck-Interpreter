from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PyQt5.QtWidgets import *
import sys

class backend:
    ascii_table = [chr(i) for i in range(256)]  # Including character for index 255
    mem_array = [0] * 33000
    mem_index = 0  # Starting at 0 for Python's zero-based indexing
    arg = ""
    arg_index = 0
    arg_curr = arg[arg_index] if arg else None  # Check if arg is not empty
    first_arg_read = True
    code = ""  # Brainfuck code should be placed here
    code_index = 0
    output_result = ""  # Renamed to avoid conflict with the output function
    arg_err = False
    need_arg = False
    invalid_char_found = False
    command = 0

    @staticmethod
    def add():
        if backend.mem_array[backend.mem_index] == 255:
            backend.mem_array[backend.mem_index] = 0
        else:
            backend.mem_array[backend.mem_index] += 1

    @staticmethod
    def sub():
        if backend.mem_array[backend.mem_index] == 0:
            backend.mem_array[backend.mem_index] = 255
        else:
            backend.mem_array[backend.mem_index] -= 1

    @staticmethod
    def right():
        backend.mem_index += 1
        if backend.mem_index >= 33000:
            backend.mem_index = 0

    @staticmethod
    def left():
        backend.mem_index -= 1
        if backend.mem_index <= 0:
            backend.mem_index = 33000

    @staticmethod
    def output_char():
        backend.output_result += backend.ascii_table[backend.mem_array[backend.mem_index]]


    @staticmethod
    def arg():
        if backend.first_arg_read:
            backend.first_arg_read = False
        else:
            backend.arg_index += 1
        if backend.arg_index < len(backend.arg):
            backend.arg_curr = backend.arg[backend.arg_index]
        else:
            backend.arg_index = 1
        backend.mem_array[backend.mem_index] = backend.ascii_table.find(backend.arg_curr)

    func_map = {
        '>': right,
        '<': left,
        '+': add,
        '-': sub,
        '.': output_char,
        ',': arg,
    }

    loop_stack = []

    @staticmethod
    def run():
        backend.arg_curr = backend.arg[0] if backend.arg else None

        while backend.code_index < len(backend.code):
            try:
                command = backend.code[backend.code_index]

                if command in backend.func_map:
                    backend.func_map[command]()
                elif command == "[":
                    if backend.mem_array[backend.mem_index] == 0:
                        loop_start = backend.code_index
                        depth = 1
                        while depth > 0:
                            backend.code_index += 1
                            if backend.code[backend.code_index] == "[":
                                depth += 1
                            elif backend.code[backend.code_index] == "]":
                                depth -= 1
                    else:
                        backend.loop_stack.append(backend.code_index)
                elif command == "]":
                    if backend.mem_array[backend.mem_index] != 0:
                        backend.code_index = backend.loop_stack[-1]
                    else:
                        backend.loop_stack.pop()
                else:
                    pass
                backend.code_index += 1

            except Exception as error:
                print(error)
                break


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.save = QPushButton(self.centralwidget)
        self.save.setObjectName(u"save")
        self.save.setGeometry(QRect(0, 0, 320, 75))
        font = QFont()
        font.setPointSize(35)
        self.save.setFont(font)
        icon = QIcon()
        icon.addFile(u"./assets/icons/save.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.save.setIcon(icon)
        self.save.setIconSize(QSize(70, 70))
        self.help = QPushButton(self.centralwidget)
        self.help.setObjectName(u"help")
        self.help.setGeometry(QRect(960, 0, 320, 75))
        self.help.setFont(font)
        icon1 = QIcon()
        icon1.addFile(u"./assets/icons/help.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.help.setIcon(icon1)
        self.help.setIconSize(QSize(70, 70))
        self.open = QPushButton(self.centralwidget)
        self.open.setObjectName(u"open")
        self.open.setGeometry(QRect(320, 0, 320, 75))
        self.open.setFont(font)
        icon2 = QIcon()
        icon2.addFile(u"./assets/icons/open.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.open.setIcon(icon2)
        self.open.setIconSize(QSize(70, 70))
        self.run = QPushButton(self.centralwidget)
        self.run.setObjectName(u"run")
        self.run.setGeometry(QRect(640, 0, 320, 75))
        self.run.setFont(font)
        icon3 = QIcon()
        icon3.addFile(u"./assets/icons/run.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.run.setIcon(icon3)
        self.run.setIconSize(QSize(70, 70))
        self.codeinput = QTextEdit(self.centralwidget)
        self.codeinput.setObjectName(u"codeinput")
        self.codeinput.setGeometry(QRect(3, 81, 635, 636))
        self.arginput = QTextEdit(self.centralwidget)
        self.arginput.setObjectName(u"arginput")
        self.arginput.setGeometry(QRect(640, 81, 637, 92))
        self.outputbox = QTextEdit(self.centralwidget)
        self.outputbox.setObjectName(u"outputbox")
        self.outputbox.setGeometry(QRect(640, 179, 638, 538))
        self.outputbox.setInputMethodHints(Qt.ImhMultiLine)
        self.outputbox.setReadOnly(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.codeinput.raise_()
        self.save.raise_()
        self.help.raise_()
        self.open.raise_()
        self.run.raise_()
        self.arginput.raise_()
        self.outputbox.raise_()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.save.setText(QCoreApplication.translate("MainWindow", u"Save As", None))
        self.help.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.open.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.run.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.codeinput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Code", None))
        self.arginput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Argument", None))
        self.outputbox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Output", None))

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.save.clicked.connect(self.save_file)
        self.help.clicked.connect(self.show_help)
        self.open.clicked.connect(self.open_file)
        self.run.clicked.connect(self.run_code)

    def save_variable(self, code):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Brainfuck Files (*.bf)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(code)

    def save_file(self):
        code_text = self.codeinput.toPlainText()  # Retrieve text from codeinput
        self.save_variable(code_text)

    def show_help(self):
        msg = QMessageBox()
        msg.setWindowTitle("Why")
        msg.setText("You don't need this")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Brainfuck Files (*.bf)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                bf_code = file.read()
                self.codeinput.setText(bf_code)

    def run_code(self):
        self.code_text = self.codeinput.toPlainText()  # Retrieve text from codeinput
        self.arg_text = self.arginput.toPlainText()
        self.need_arg = False
        self.invalid_arg_char = False
        self.err_code = None
        self.finde = 0

        backend.code = self.code_text
        backend.arg = self.arg_text


        self.finde = backend.code.find(",")
        if self.finde != -1:
            self.need_arg = True
        else:
            self.need_arg = False


        if self.need_arg and not self.arg_text:
            self.outputbox.setText("Argument Error 1: The program requires an argument but has not been given one")
            self.err_code = 1

        # Check if the argument contains invalid characters
        if self.need_arg:
            for char in backend.arg:
                if char not in backend.ascii_table:
                    self.outputbox.setText("Argument Error 2: A character in the argument is not a valid character in Brainfuck")
                    self.err_code = 2
        else:
            pass



        if self.err_code == 1:
            print("ERR 1")
        elif self.err_code == 2:
            print("ERR 2")
        else:
            self.outputbox.setText("")
            backend.run()
            self.outputbox.setText(backend.output_result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()  # Use show() on the MainWindow instance
    sys.exit(app.exec_())
