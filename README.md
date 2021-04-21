# Uebungsblatt2

% Interaction Techniques and Technologies 
  Assignment 2: PyQt
% Summer semester 2021
% **Submission due: Wednesday, 28. April 2021, 23:55**

**no group work**

Your task is to implement a simple calculator UI and get familiar with the Qt toolkit.

2.1: Implement a simple calculator
==================================

Implement a simple graphical calculator using PyQt. The calculator should support the following 18 inputs:

* digits from 0 to 9 and the decimal point
* operators: +, -, \*, /
* =, clear, delete last digit on screen

The UI should be implemented using a .ui-File. 
Use signals and slots for communication.
Pressing a key on the keyboard should do the same as clicking the corresponding button.

**Hint:** check out Python's `eval` function. 

Furthermore, instrument the calculator's code so that all relevant input events (such as keypresses, clicks on buttons) are logged to `stdout`. 
Use decorators for logging each function call.

Hand in the following files:

* **calculator.py**: the source code of the calculator
* **calculator.ui**: the Qt UI description of the calculator

Points
------------

* **1** The script is well-structured and follows the Python style guide (PEP 8)
* **2** The calculator correctly calculates the results
* **2** Input dispatching is handled via Qt signals
* **2** Logging works and is handled via decorators

2.2: Peer review solutions to Assignment 1
==========================================

Review the assigned submissions that are assigned to you in GRIPS and give feedback.
Please read the separate task description in GRIPS for details on the review process.

* **3** Your grading is plausible (i.e. follows the reviewing guidelines)
* **2** You have given relevant (1 point) or helpful (2 points) feedback.

**Note:** the points for Assignment 2.2 will be assigned to Assignment 1 in GRIPS due to technical reasons.

Submission 
=========================================
Submit via GRIPS until the deadline

All files should use UTF-8 encoding and Unix line breaks.
Python files should use spaces instead of tabs.
If you need to submit further supporting files, please add a comment describing their use.

                                                               Have Fun!
