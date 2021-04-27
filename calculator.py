#!/usr/bin/env python3
# coding: utf-8
import functools
import math
import sys
from typing import Any
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QPushButton


def log_keys(on_keyboard: bool):
    def func_decorator(func):
        @functools.wraps(func)
        def wrapper(class_instance, event):
            if on_keyboard:
                print(f"The button \"{event.text()}\" was clicked on the keyboard.")
            else:
                print(f"The button \"{event.text()}\" was clicked in the pyqt gui.")

            func(class_instance, event)

        return wrapper

    return func_decorator


def log_other_interaction(func):
    @functools.wraps(func)
    def wrapper(class_instance, event, on_keyboard: bool):
        if on_keyboard:
            print(f"The button \"{event.text()}\" was clicked on the keyboard.")
        else:
            print(f"The button \"{event.text()}\" was clicked in the pyqt gui.")

        func(class_instance)

    return wrapper


# This method was taken from https://realpython.com/python-eval-function/
# and slightly updated with a try-except block to handle wrong input.
def evaluate(expression: str) -> Any:
    """Evaluate a math expression."""
    # Compile the expression
    try:
        code = compile(expression, "<string>", "eval")
    except SyntaxError as e:
        print(f"The given function is not syntactically correct! Error:\n{e}")
        return "ERROR"

    # Validate allowed names
    for name in code.co_names:
        if name not in Calculator.ALLOWED_NAMES:
            raise NameError(f"The use of '{name}' is not allowed")

    return eval(code, {"__builtins__": {}}, Calculator.ALLOWED_NAMES)


class Calculator(QtWidgets.QWidget):
    # restrict eval() - function to prevent security issues,
    # see https://realpython.com/python-eval-function/
    ALLOWED_NAMES = {
        k: v for k, v in math.__dict__.items() if not k.startswith("__")
    }

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("calculator.ui", self)

        self.__current_input = []
        self._setup_keys()

    def _setup_keys(self) -> None:
        self.__DIGIT_KEY_NAMES = [self.ui.btn_0, self.ui.btn_1,
                                  self.ui.btn_2, self.ui.btn_3,
                                  self.ui.btn_4, self.ui.btn_5,
                                  self.ui.btn_6, self.ui.btn_7,
                                  self.ui.btn_8, self.ui.btn_9]

        self.__OPERATOR_KEY_NAMES = [self.ui.btn_mult, self.ui.btn_div,
                                     self.ui.btn_add, self.ui.btn_sub,
                                     self.ui.btn_point]

        self.__KEYBOARD_KEYS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "+", "-", "*", "/"]

        # don't let user edit input field directly for now
        self.ui.input_field.setReadOnly(True)
        self._setup_listeners()

    def _setup_listeners(self) -> None:
        for key_identifier in self.__DIGIT_KEY_NAMES + self.__OPERATOR_KEY_NAMES:
            # lambda taken from
            # https://stackoverflow.com/questions/18836291/lambda-function-returning-false#comment45916219_18862798
            key_identifier.clicked.connect(
                lambda ignore, x=key_identifier: self._handle_button_press(x)
            )

        self.ui.btn_calculate.clicked.connect(lambda: self._calculate_result(self.ui.btn_calculate, False))
        self.ui.btn_clear.clicked.connect(lambda: self._clear_input(self.ui.btn_clear, False))
        self.ui.btn_delete_last.clicked.connect(lambda: self._remove_last_digit(self.ui.btn_delete_last, False))

    # override the keyPressEvent of the QWidget; does NOT work if inheriting from QMainWindow
    @log_keys(True)
    def keyPressEvent(self, event):
        if event.text() == '=':
            self._calculate_result(self.ui.btn_calculate, True)
        elif event.text() == 'c':  # TODO c for clear??
            self._clear_input(self.ui.btn_clear, True)
        elif event.key() == QtCore.Qt.Key_Backspace:
            self._remove_last_digit(self.ui.btn_delete_last, True)
        elif event.text() in self.__KEYBOARD_KEYS:
            self._update_input_field(event.text())
        else:
            pass

    @log_keys(False)
    def _handle_button_press(self, pressed_button: QPushButton) -> None:
        # clicked_button = self.sender()  # get the signal that fired the event
        pressed_key = pressed_button.text()
        # update the input field with the value of the pressed button
        self._update_input_field(pressed_key)

    def _update_input_field(self, new_input: str) -> None:
        self.__current_input.append(new_input)
        self.ui.input_field.setText(
            ''.join([str(el) for el in self.__current_input])
        )

    @log_other_interaction
    def _calculate_result(self) -> None:
        calc_input = self.ui.input_field.text()
        if not calc_input:
            # empty strings are false in python, so return if no input is given
            print("Please provide an input!")
            return

        result = evaluate(calc_input)
        self.ui.result_field.display(result)

    @log_other_interaction
    def _clear_input(self) -> None:
        self.__current_input = []
        self.ui.input_field.clear()
        self.ui.result_field.display(0)

    @log_other_interaction
    def _remove_last_digit(self) -> None:
        try:
            # traverse the list from the end and find the last digit in the current input
            for element in reversed(self.__current_input):
                if element.isdigit():
                    index_last_digit = self.__current_input.index(element)

                    # update the current input by removing the last digit and everything after it
                    self.__current_input = self.__current_input[:index_last_digit]
                    self.ui.input_field.setText(
                        ''.join([str(el) for el in self.__current_input])
                    )
                    break
        except ValueError:
            print(f"The last digit could not be removed from the current input :(")


def main():
    app = QtWidgets.QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
