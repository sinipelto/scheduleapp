# coding=utf-8

"""
Autocomplete widget module.
Contains a widget that helps filtering
search results between a list of options and given input.
"""

from tkinter import *


class AutocompleteEntry(Entry):
    """
    Autocomplete widget for main window.
    Takes string input in entry field and automatically
    filters answers in a listbox by input. Helps to quickly
    find a specific selection from large amount of options.
    """

    def __init__(self, lista, *args, **kwargs):
        """
        Widget initializer. Sets up attributes and needed methods.
        :param lista: list of options to filter from
        :param args: optional positional arguments
        :param kwargs: dictionary arguments
        """
        Entry.__init__(self, *args, **kwargs)
        self.lista = lista
        self.var = self["textvariable"]
        self.lb = None

        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Return>", self.selection)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

        self.lb_up = False

    def changed(self, name, index, mode):
        """
        Handles changes in input.
        :param name:
        :param index: 
        :param mode: 
        :return: none
        """
        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = Listbox()
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.lb_up = True

                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END, w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def selection(self, event):
        """
        Sets the current selection by choosing active
        entry from the listbox
        :param event: event parameter
        :return: none
        """
        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):
        """
        Handles press of up-button. 
        Changes selection to one above.
        :param event: event parameter
        :return: none
        """
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):
        """
        Handles moving down in listbox by pressing down-button.
        Changes selection to one below.
        :param event: event parameter
        :return: none
        """
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        """
        Does a regex comparison between current input
        and available options and furthens filtering by its result
        :return: matching pattern
        """
        pattern = re.compile('.*' + self.var.get().capitalize() + '.*')
        return [w for w in self.lista if re.match(pattern, w)]

    def get_target(self):
        """
        Used to get the current active selection in listbox.
        Needed in main window.
        :return: current selection in listbox as string
        """
        return self.var.get()
