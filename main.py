# coding=utf-8

"""
This program inits a tkinter window widget to
show train schedule using VR API and to display API data
inside the widget, properly formatted.
Generally used language inside widgets is finnish.
UTF-8 coding is necessary.

Main module. Main is defined here.
Creates ui frame and main window and
starts event loop.
"""

from tkinter import Tk  # UI main frame
from mainwindow import MainWindow  # Main Window class


def main():
    """Main function. Creates tkinter application
    and launches schedule window.
    :return 0: exit code zero
    """
    # Init ui application
    root = Tk()

    # Create main widget
    app = MainWindow(root)
    app.mainloop()

    # Exit
    return 0


if __name__ == '__main__':
    main()
