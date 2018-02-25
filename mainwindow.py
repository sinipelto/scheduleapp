# coding=utf-8

"""
Main Window class.
Everything needed in UI window is defined here.
Needs functions and autocomplete modules to function properly.
"""

import tkinter as tk
from autocomplete import AutocompleteEntry
from functions import *


class MainWindow(tk.Frame):
    """
    The Main Window class. Shows schedule data about trains
    departing and arriving a specific train station. Uses couple of
    non-included functions and is dependent of them.
    """

    def __init__(self, master):
        """
        Main initializer. Initializes all needed attributes
        and subwidgets under master widget.
        :param master: master widget for all subwidgets
        """
        # Basic initials
        super().__init__(master)
        self.__directions = ["Lähtevät", "Saapuvat"]  # Departures and arrivals
        self.__stations_dict = get_station_names()  # Destinations and abbreviations
        self.__list_options = []  # List of destinations
        self.__schedule_list = []  # List of scheduled trains

        self.__direction = None
        self.__target = None

        # Add station names to selection list
        for key in self.__stations_dict:
            self.__list_options.append(key)

        # Window settings
        self.master.minsize(200, 200)  # Literal minimum size for window, may be changed if needed
        self.master.resizable(False, False)  # User cant break sizing mechanism
        self.master.title("Aseman junatiedot")  # Window title

        # Buttons
        self.__get_button = tk.Button(self.master, text="Hae junia", command=self.get_entries)
        self.__exit_button = tk.Button(self.master, text="Sulje Sovellus", command=self.close)

        # Selection objects
        self.__searchbox = AutocompleteEntry(self.__list_options)
        self.__direction_switch = self.init_switch()

        # Labels
        self.__station_label = tk.Label(text="Hae aseman nimellä:")
        self.__info_label = tk.Label()

        self.__title_name = tk.Label(text="Juna:\t")
        self.__title_from = tk.Label(text="Lähtöasema:\t")
        self.__title_to = tk.Label(text="Pääteasema:\t")
        self.__title_time = tk.Label(text="Aika:\t")
        self.__title_late = tk.Label(text="Myöhässä (min):\t")

        # Initialize widget graphics
        self.init_window()

        self.__searchbox.focus()

    def init_window(self):
        """
        Initializes window graphics, sets layout manager
        to window and adjusts subwidgets.
        """
        # Set layout manager
        self.grid()

        # Configure element positions
        self.__station_label.grid(row=0, column=0)
        self.__searchbox.grid(row=1, column=0)
        self.__direction_switch.grid(row=1, column=1)
        self.__get_button.grid(row=2, column=0)
        self.__exit_button.grid(row=2, column=1)
        self.__info_label.grid(row=2, column=2)

        self.__title_name.grid(row=3, column=0)
        self.__title_from.grid(row=3, column=1)
        self.__title_to.grid(row=3, column=2)
        self.__title_time.grid(row=3, column=3)
        self.__title_late.grid(row=3, column=4)

    def init_switch(self):
        """
        Initializes direction switch to have options for
        both departing and arriving trains.
        :return OptionMenu with set parameters:
        """
        default = self.__directions[0]
        var = tk.StringVar(self.master)
        self.__direction = default
        var.set(default)
        return tk.OptionMenu(self.master, var, *self.__directions, command=self.set_direction)

    def set_direction(self, *args):
        """
        Sets the direction by the current
        state of direction switch.
        Has 2 options: arrivals and departures.
        :param args: parameter to carry set signal from option menu.
        """
        self.__direction = args[0]

    def set_target(self, *args):
        """
        Sets the current target by the entry label value.
        The target set may be invalid and will be checked later.
        :param args: parameter to carry data signal from entry widget
        """
        self.__target = args[0]

    def get_entries(self):
        """
        This function is called after pressing get button.
        Begins processing selected target and direction data.
        Makes validity checks on target and calls displaying function if valid.
        First clears old entries, then shows new entries. Finally
        clears current target to maintain validity.
        :return: Returns and does nothing if target was invalid
        """
        # Configure
        self.__info_label.config(text="")
        station = self.__searchbox.get_target()

        try:
            self.__target = self.__stations_dict[station]
        except KeyError:
            self.__target = None

        if self.__target is None:
            self.__info_label.config(text="Asemaa ei löydy.")
            print("ERROR, INVALID STATION")
            return

        self.clear_list()  # Remove trains of old target

        # TARGET: STATION ABBR; DIRECTION: DEP / ARR
        print("STATION:", self.__target, "-- DIRECTION:", self.__direction)

        self.show_trains()
        self.clear_target()  # Finally, clear destination

    def show_trains(self):
        """
        This function generates information lines about data
        using the given target station and direction. Processes data
        as a row of labels below corresponding titles. Also keeps label references
        in a list to keep access to them.
        """
        if self.__direction == self.__directions[0]:  # If departures
            self.__title_time.config(text="Lähtee:\t")
            data = get_station_data(self.__target, True)
            mode = 0
        else:  # If arrivals
            self.__title_time.config(text="Saapuu:\t")
            data = get_station_data(self.__target, False)
            mode = 1

        if len(data) <= 0:
            self.__info_label.config(text="Junia asemalle ei valitettavasti löytynyt.")
            print("NO TRAINS FOUND")

        keys = ["trainType", "trainNumber", "timeTableRows", "commuterLineID"]

        r = 10
        x = 0
        for i in range(0, len(data)):
            # TODO: SORT DATA BY TIME HERE
            if i >= 40:  # No space for any more trains
                break
            fail = False
            if data[i]["cancelled"] == "true":
                cancelled = True
            else:
                cancelled = False

            self.__schedule_list.append([])

            origin = data[i][keys[2]][0]["stationShortCode"].upper()
            origin = self.station_long_name(origin)

            size = len(data[i][keys[2]])
            dest = data[i][keys[2]][size - 1]["stationShortCode"].upper()
            dest = self.station_long_name(dest)

            timerow = None
            if mode == 0:  # Get departure
                for row in data[i][keys[2]]:
                    if row["stationShortCode"] == self.__target and row["type"] == "DEPARTURE":
                        timerow = row
                        break
            else:  # Get arrival
                for row in data[i][keys[2]]:
                    if row["stationShortCode"] == self.__target and row["type"] == "ARRIVAL":
                        timerow = row
                        break

            for j in range(0, 5):
                text = None
                late = False

                if j == 0:
                    # Train name settings
                    if data[i][keys[3]] != "":
                        text = str("Commuter line " + str(data[i][keys[3]]))
                    else:
                        text = str(str(data[i][keys[0]]) + " " + str(data[i][keys[1]]))

                elif j == 1:
                    # Train origin station settings
                    if origin is None:
                        print("ORIGIN FAIL")
                        fail = True
                    text = str(origin)

                elif j == 2:
                    # Train destination station settings
                    if dest is None:
                        print("DEST FAIL")
                        fail = True
                    text = str(dest)

                elif j == 3:
                    # Train time schedule settings
                    if timerow is None:
                        print("TIMEROW FAIL")
                        fail = True
                    else:
                        # Get train scheduled time
                        schedtime = convert_date_format(timerow["scheduledTime"])
                        schedtime = schedtime[1][0] + ":" + schedtime[1][1]
                        text = schedtime
                        try:
                            # Tries to use live estimate time if available
                            actime = convert_date_format(timerow["liveEstimateTime"])
                            if actime is None:
                                # In other case use actual time
                                actime = convert_date_format(timerow["actualTime"])
                            actime = actime[1][0] + ":" + actime[1][1]
                            if actime != schedtime:
                                text = actime + " (" + schedtime + ")"
                                late = True
                        except KeyError:
                            pass

                else:  # j == 4
                    # Train time difference settings, late in mins or cancelled
                    if cancelled:
                        text = "Peruttu"
                    else:
                        diff = 0
                        try:
                            diff = timerow["differenceInMinutes"]
                            if diff > 0:
                                late = True
                        except KeyError:
                            pass
                        text = str(diff)

                if fail:
                    # If any settings above failed
                    for widget in self.__schedule_list[x]:
                        widget.destroy()
                    self.__schedule_list.remove(self.__schedule_list[x])
                    r -= 1
                    x -= 1
                    break

                label = tk.Label(text=text)
                self.__schedule_list[x].append(label)
                label.grid(row=r, column=j)

                if cancelled or late:
                    if j == 3 or j == 4:
                        label.config(fg="red")
            r += 1
            x += 1

    def clear_list(self):
        """
        Clears current list of lable widgets from
        screen. No-throw function, performs no checks and
        fails if list has data in incorrect form.
        """
        for i in range(0, len(self.__schedule_list)):
            for j in range(0, len(self.__schedule_list[i])):
                self.__schedule_list[i][j].destroy()

    def station_long_name(self, short):
        """
        Gets station shortname and converts
        it to long version. Doesnt do any implicit
        modifications, uses and retuns only raw input.
        :param short: station shortname (2-3 letters)
        :return: station long name from station name dict
        """
        for key in self.__stations_dict:
            if self.__stations_dict[key] == short:
                return key

    def clear_target(self):
        """
        Clears the current target station.
        """
        self.__target = None

    def close(self):
        """
        Closes the main window by destroying
        its master. Whole application should end
        after this is called.
        """
        self.master.destroy()
