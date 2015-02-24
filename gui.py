

##########################################################################
# Copyright 2014 Samuel Gongora Garcia (s.gongoragarcia@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##########################################################################
# Author: s.gongoragarcia[at]gmail.com
##########################################################################


class GUI:

    def __init__(self):

        self.index = 0
        self.pyephem = 0
        self.predict = 0
        self.pyorbital = 0
        self.STK = 0
        self.orbitron = 0

        import get_elements
        object_elements = get_elements.Get_list_length()
        self.length = object_elements.length - 1

        self.widgets()

    def widgets(self):

        # Satellite name
        import get_elements
        self.object_name = get_elements.Get_name(self.index)

        import Tkinter as tk
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

        # Default
        available_predict = 'no'
        available_pyephem = 'no'
        available_pyorbital = 'no'
        available_orbitron = 'no'
        available_STK = 'no'

        import output_data
        from sys import argv
        actual_available = output_data.Check_data(
            self.index,
            self.object_name.name,
            argv[3],
            argv[4])
        available_predict = actual_available.predict
        available_pyephem = actual_available.pyephem
        available_pyorbital = actual_available.pyorbital
        available_orbitron = actual_available.orbitron
        available_STK = actual_available.STK

        # Plot
        self.f = Figure(figsize=(6, 7), dpi = 80)
        self.text = self.f.suptitle(self.object_name.name, fontsize=16)
#		self.f.suptitle(self.object_name.name, fontsize=16)

        # Subplots altitude & azimuth
        self.a = self.f.add_subplot(211)
        self.b = self.f.add_subplot(212)

        # Check if data is available and print it

        if available_pyephem == 'yes':
            figure_pyephem = output_data.Read_pyephem_data(self.pyephem)
            pyephem_time = figure_pyephem.pyephem_simulation_time
            pyephem_alt = figure_pyephem.pyephem_alt_satellite
            self.plot_pyephem_alt, = self.a.plot(
                pyephem_time, pyephem_alt, 'b', label="PyEphem")

            pyephem_az = figure_pyephem.pyephem_az_satellite
            self.plot_pyephem_az, = self.b.plot(
                pyephem_time, pyephem_az, 'b', label="PyEphem")

        if available_predict == 'yes':
            figure_predict = output_data.Read_predict_data(self.predict)
            predict_time = figure_predict.predict_simulation_time
            predict_alt = figure_predict.predict_alt_satellite
            self.plot_predict_alt, = self.a.plot(
                predict_time, predict_alt, 'r', label="predict")

            predict_az = figure_predict.predict_az_satellite
            self.plot_predict_az, = self.b.plot(
                predict_time, predict_az, 'r', label="predict")

        if available_pyorbital == 'yes':
            figure_pyorbital = output_data.Read_pyorbital_data(self.pyorbital)
            pyorbital_time = figure_pyorbital.pyorbital_simulation_time
            pyorbital_alt = figure_pyorbital.pyorbital_alt_satellite
            self.plot_pyorbital_alt, = self.a.plot(
                pyorbital_time, pyorbital_alt, 'y', label="pyorbital")

            pyorbital_az = figure_pyorbital.pyorbital_az_satellite
            self.plot_pyorbital_az, = self.b.plot(
                pyorbital_time, pyorbital_az, 'y', label="pyorbital")

        if available_orbitron == 'yes':
            from sys import argv
            print(argv[4])
            figure_orbitron = output_data.Read_orbitron_data(
                self.orbitron,
                self.object_name.name,
                argv[4])
            orbitron_alt = figure_orbitron.orbitron_alt_satellite
            orbitron_time = figure_orbitron.orbitron_time
            self.plot_orbitron_alt, = self.a.plot(
                orbitron_time, orbitron_alt, 'm', label="orbitron")

            orbitron_az = figure_orbitron.orbitron_az_satellite
            self.plot_orbitron_az, = self.b.plot(
                orbitron_time, orbitron_az, 'm', label="orbitron")

        if available_STK == 'yes':
            figure_STK = output_data.Read_STK_data(self.STK, argv[3])
            STK_alt = figure_STK.STK_alt_satellite
            STK_time = figure_STK.STK_simulation_time
            self.plot_STK_alt, = self.a.plot(
                STK_time, STK_alt, 'g', label="STK")

            STK_az = figure_STK.STK_az_satellite
            self.plot_STK_az, = self.b.plot(STK_time, STK_az, 'g', label="STK")

        self.a.legend(loc=2, borderaxespad=0., prop={'size': 12})
        self.a.set_ylabel("Degrees")
        # Grid is on
        self.a.grid(True)

        self.b.legend(loc=2, borderaxespad=0., prop={'size': 12})
        self.b.set_ylabel("Degrees")

        # Grid is on
        self.b.grid(True)

        import Tkinter as tk
        left_frame = tk.Frame(root, height=800, width=500, padx=5, pady=5)
        left_frame.grid(column=0, row=0, columnspan=1, rowspan=3)

        # Figure controls
        self.canvas = FigureCanvasTkAgg(self.f, master=left_frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)

        toolbar = NavigationToolbar2TkAgg(self.canvas, left_frame)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=0)

        # Plot g
        self.g = Figure(figsize=(6, 4), dpi = 80)
        self.g.suptitle("Comparation", fontsize=16)

        # Subplot c
        self.c = self.g.add_subplot(111)

        right_frame = tk.Frame(root, height=330, width=500, bd=0)
        right_frame.grid(
            column=1,
            row=0,
            columnspan=1,
            rowspan=1,
            padx=5,
            pady=5)
        right_frame.grid_propagate(0)

        self.canvas2 = FigureCanvasTkAgg(self.g, master=right_frame)
        self.canvas2.show()
        self.canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)

        data_frame = tk.LabelFrame(
            root,
            text="Data",
            height=215,
            width=500,
            padx=5,
            pady=5)
        data_frame.grid(column=1, row=1, columnspan=1, rowspan=1)
        data_frame.columnconfigure(0, minsize=110)
        data_frame.columnconfigure(1, minsize=65)
        data_frame.columnconfigure(2, minsize=110)
        data_frame.columnconfigure(3, minsize=110)
        data_frame.rowconfigure(0, minsize=25)
        data_frame.rowconfigure(1, minsize=25)
        data_frame.rowconfigure(2, minsize=20)
        data_frame.rowconfigure(3, minsize=20)
        data_frame.rowconfigure(4, minsize=20)
        data_frame.rowconfigure(5, minsize=20)
        data_frame.rowconfigure(6, minsize=20)
        data_frame.rowconfigure(7, minsize=20)

        data_frame.grid_propagate(0)

        # Name
        label_name = tk.Label(data_frame, text="Name")
        label_name.grid(column=0, row=0, columnspan=1, rowspan=1, sticky=tk.W)

        self.text_name = tk.StringVar()
        import get_elements
        object_name = get_elements.Get_name(self.index)
        self.text_name.set(object_name.name)

        name = tk.Label(data_frame, textvariable=self.text_name)
        name.grid(column=1, row=0, columnspan=1, rowspan=1, sticky=tk.E)

        # Inclination
        from sys import argv
        elements = get_elements.Get_elements(argv[1], self.index)
        label_incl = tk.Label(data_frame, text="Inclination")
        label_incl.grid(column=2, row=0, columnspan=1, rowspan=1, sticky=tk.W)

        self.text_incl = tk.DoubleVar()
        self.text_incl.set(elements.inclination)

        incl = tk.Label(data_frame, textvariable=self.text_incl)
        incl.grid(column=3, row=0, columnspan=1, rowspan=1, sticky=tk.E)

        # File
        file_name = tk.Label(data_frame, text="File")
        file_name.grid(column=0, row=1, columnspan=1, rowspan=1, sticky=tk.W)

        self.file_name = tk.StringVar()
        self.file_name.set(argv[1])

        file_ = tk.Label(data_frame, textvariable=self.file_name)
        file_.grid(column=1, row=1, columnspan=1, rowspan=1, sticky=tk.E)

        # Mean motion
        label_motion = tk.Label(data_frame, text="Mean motion")
        label_motion.grid(
            column=2,
            row=1,
            columnspan=1,
            rowspan=1,
            sticky=tk.W)

        self.text_motion = tk.DoubleVar()
        self.text_motion.set(elements.mean_motion)

        motion = tk.Label(data_frame, textvariable=self.text_motion)
        motion.grid(column=3, row=1, columnspan=1, rowspan=1, sticky=tk.E)

        label_sims = tk.Label(data_frame, text="Simulations availables")
        label_sims.grid(column=0, row=2, columnspan=2, rowspan=1, sticky=tk.W)

        # Generate data
        import scrolledlist
        sims_availables = scrolledlist.ScrolledList(
            data_frame,
            width=16,
            height=3,
            callback=self.pick_simulation)
        sims_availables.grid(
            column=0,
            row=3,
            columnspan=1,
            rowspan=3,
            sticky=tk.W)

        # Generate list of simulations
        self.sims_availables(
            available_predict,
            available_pyephem,
            available_pyorbital,
            available_orbitron,
            available_STK)

        for i in range(len(self.list_of_simulations)):
            sims_availables.append(self.list_of_simulations[i])

        # STD
        label_std = tk.Label(data_frame, text="Standard desviation")
        label_std.grid(column=2, row=2, columnspan=1, rowspan=1, sticky=tk.W)

        std_button = tk.Button(
            data_frame,
            text="Get data",
            command=self.std_simulations)
        std_button.grid(column=3, row=2, columnspan=1, rowspan=1, sticky=tk.E)

        label_std_alt = tk.Label(data_frame, text="Altitude")
        label_std_alt.grid(
            column=2,
            row=3,
            columnspan=1,
            rowspan=1,
            sticky=tk.E)

        label_std_az = tk.Label(data_frame, text="Azimuth")
        label_std_az.grid(
            column=3,
            row=3,
            columnspan=1,
            rowspan=1,
            sticky=tk.E)

        # PyEphem STD
        text_std_pyephem = tk.Label(data_frame, text="PyEphem")
        text_std_pyephem.grid(
            column=1,
            row=4,
            columnspan=1,
            rowspan=1,
            sticky=tk.E)

        self.text_std_pyephem_alt = tk.DoubleVar()
        self.text_std_pyephem_alt.set("PyEphem alt.")

        std_pyephem_alt = tk.Label(
            data_frame,
            textvariable=self.text_std_pyephem_alt)
        std_pyephem_alt.grid(
            column=2,
            row=4,
            columnspan=1,
            rowspan=1,
            sticky=tk.E)

        self.text_std_pyephem_az = tk.DoubleVar()
        self.text_std_pyephem_az.set("PyePhem az.")

        std_pyephem_az = tk.Label(
            data_frame,
            textvariable=self.text_std_pyephem_az)
        std_pyephem_az.grid(
            column=3,
            row=4,
            columnspan=1,
            rowspan=1,
            sticky=tk.E)

        # predict STD
        text_std_predict = tk.Label(data_frame, text="predict")
        text_std_predict.grid(
            column=1,
            row=5,
            columnspan=1,
            rowspan=1,
            sticky=tk.E)

        self.text_std_predict_alt = tk.DoubleVar()
        self.text_std_predict_alt.set("predict alt.")

        std_predict_alt = tk.Label(
            data_frame,
            textvariable=self.text_std_predict_alt)
        std_predict_alt.grid(
            column=2,
            row=5,
            columnspan=1,
            rowspan=1,
            sticky=tk.E)

        self.text_std_predict_az = tk.DoubleVar()
        self.text_std_predict_az.set("predict az.")

        std_predict_az = tk.Label(
            data_frame,
            textvariable=self.text_std_predict_az)
        std_predict_az.grid(
            column=3,
            row=5,
            columnspan=1,
            rowspan=1,
            sticky=tk.E)

        # Boton para realizar de nuevo las simulaciones
        save = tk.Button(
            data_frame,
            text="Save sims",
            command=self.save_routine)
        save.grid(column=0, row=6, columnspan=1, rowspan=2, sticky=tk.W)

        # PyOrbital STD
        text_std_pyorbital = tk.Label(data_frame, text="PyOrbital")
        text_std_pyorbital.grid(
            column=1,
            row=6,
            columnspan=1,
            rowspan=1,
            sticky=tk.E)

        self.text_std_pyorbital_alt = tk.DoubleVar()
        self.text_std_pyorbital_alt.set("PyOrbital alt.")

        std_pyorbital_alt = tk.Label(
            data_frame,
            textvariable=self.text_std_pyorbital_alt)
        std_pyorbital_alt.grid(
            column=2,
            row=6,
            columnspan=1,
            rowspan=1,
            sticky=tk.E)

        self.text_std_pyorbital_az = tk.DoubleVar()
        self.text_std_pyorbital_az.set("PyOrbital az.")

        std_pyorbital_az = tk.Label(
            data_frame,
            textvariable=self.text_std_pyorbital_az)
        std_pyorbital_az.grid(
            column=3,
            row=6,
            columnspan=1,
            rowspan=1,
            sticky=tk.E)

        # Orbitron STD
        text_std_orbitron = tk.Label(data_frame, text="Orbitron")
        text_std_orbitron.grid(
            column=1,
            row=7,
            columnspan=1,
            rowspan=1,
            sticky=tk.E)

        self.text_std_orbitron_alt = tk.DoubleVar()
        self.text_std_orbitron_alt.set("Orbitron alt.")

        std_orbitron_alt = tk.Label(
            data_frame,
            textvariable=self.text_std_orbitron_alt)
        std_orbitron_alt.grid(
            column=2,
            row=7,
            columnspan=1,
            rowspan=1,
            sticky=tk.E)

        self.text_std_orbitron_az = tk.DoubleVar()
        self.text_std_orbitron_az.set("Orbitron az.")

        std_orbitron_az = tk.Label(
            data_frame,
            textvariable=self.text_std_orbitron_az)
        std_orbitron_az.grid(
            column=3,
            row=7,
            columnspan=1,
            rowspan=1,
            sticky=tk.E)

        # Control frame
        control_frame = tk.LabelFrame(
            root,
            text="Controls",
            height=55,
            width=500,
            padx=5,
            pady=5)
        control_frame.grid(column=1, row=2, columnspan=1, rowspan=1)
        control_frame.grid_propagate(0)

        control_frame.columnconfigure(0, minsize=40)
        control_frame.columnconfigure(1, minsize=40)
        control_frame.columnconfigure(2, minsize=350)

        self.next = tk.Button(
            master=control_frame,
            text='Next',
            command=self.next)
        self.next.grid(column=0, row=0, columnspan=1, rowspan=1)

        self.forward = tk.Button(
            master=control_frame,
            text='Forward',
            command=self.forward)
        self.forward.grid(column=1, row=0, columnspan=1, rowspan=1)

        button = tk.Button(
            master=control_frame,
            text='Quit',
            command=self._quit)
        button.grid(column=2, row=0, columnspan=1, rowspan=1, sticky=tk.E)

        # Check buttons state
        if self.index == 0:
            self.forward.configure(state=tk.DISABLED)
            self.next.configure(state=tk.NORMAL)
        elif self.index == self.length:
            self.forward.configure(state=tk.NORMAL)
            self.next.configure(state=tk.DISABLED)
        else:
            self.forward.configure(state=tk.NORMAL)
            self.next.configure(state=tk.NORMAL)

    def next(self):

        self.index = self.index + 1

        import get_elements
        self.object_name = get_elements.Get_name(self.index)

        import output_data
        from sys import argv
        available = output_data.Check_data(
            self.index,
            self.object_name.name,
            argv[3],
            argv[4])

        available_predict = available.predict
        if available_predict == 'yes':
            self.predict = self.predict + 1
        available_pyephem = available.pyephem
        if available_pyephem == 'yes':
            self.pyephem = self.pyephem + 1
        available_pyorbital = available.pyorbital
        if available_pyorbital == 'yes':
            self.pyorbital = self.pyorbital + 1
        available_orbitron = available.orbitron
        if available_orbitron == 'yes':
            self.orbitron = self.orbitron + 1
        available_STK = available.STK
        if available_STK == 'yes':
            self.STK = self.STK + 1

        figure = output_data.Read_data(self.pyephem, self.predict, self.pyorbital,
                                       self.orbitron, self.object_name.name, self.STK, argv[3], argv[4])

        # Available
        actual_available = output_data.Check_data(
            self.index,
            self.object_name.name,
            argv[3],
            argv[4])
        available_predict = actual_available.predict
        available_pyephem = actual_available.pyephem
        available_pyorbital = actual_available.pyorbital
        available_orbitron = actual_available.orbitron
        available_STK = actual_available.STK

        import get_elements
        object_name = get_elements.Get_name(self.index)

        self.text.set_text(object_name.name)

        # Check if data is available and print it

        if available_pyephem == 'yes':
            figure_pyephem = output_data.Read_pyephem_data(self.pyephem)
            pyephem_time = figure_pyephem.pyephem_simulation_time

            pyephem_alt = figure_pyephem.pyephem_alt_satellite
            self.plot_pyephem_alt.set_ydata(pyephem_alt)
            self.plot_pyephem_alt.set_xdata(pyephem_time)

            pyephem_az = figure_pyephem.pyephem_az_satellite
            self.plot_pyephem_az.set_ydata(pyephem_az)
            self.plot_pyephem_az.set_xdata(pyephem_time)

        if available_predict == 'yes':
            figure_predict = output_data.Read_predict_data(self.predict)
            predict_time = figure_predict.predict_simulation_time

            predict_alt = figure_predict.predict_alt_satellite
            self.plot_predict_alt.set_ydata(predict_alt)
            self.plot_predict_alt.set_xdata(predict_time)

            predict_az = figure_predict.predict_az_satellite
            self.plot_predict_az.set_ydata(predict_az)
            self.plot_predict_az.set_xdata(predict_time)

        if available_pyorbital == 'yes':
            figure_pyorbital = output_data.Read_pyorbital_data(self.pyorbital)
            pyorbital_time = figure_pyorbital.pyorbital_simulation_time

            pyorbital_alt = figure_pyorbital.pyorbital_alt_satellite
            self.plot_pyorbital_alt.set_ydata(pyorbital_alt)
            self.plot_pyorbital_alt.set_xdata(pyorbital_time)

            pyorbital_az = figure_pyorbital.pyorbital_az_satellite
            self.plot_pyorbital_az.set_ydata(pyorbital_az)
            self.plot_pyorbital_az.set_xdata(pyorbital_time)

        if available_orbitron == 'yes':
            from sys import argv
            figure_orbitron = output_data.Read_orbitron_data(self.orbitron,
                                                             self.object_name.name, argv[4])

            orbitron_time = figure_orbitron.orbitron_time
            orbitron_alt = figure_orbitron.orbitron_alt_satellite
            self.plot_orbitron_alt.set_ydata(orbitron_alt)
            self.plot_orbitron_alt.set_xdata(orbitron_time)

            orbitron_az = figure_orbitron.orbitron_az_satellite
            self.plot_orbitron_az.set_ydata(orbitron_az)
            self.plot_orbitron_az.set_xdata(orbitron_time)

        if available_STK == 'yes':
            figure_STK = output_data.Read_STK_data(self.STK, argv[3])

            STK_alt = figure_STK.STK_alt_satellite
            STK_time = figure_STK.STK_simulation_time
            self.plot_STK_alt.set_ydata(STK_alt)
            self.plot_STK_alt.set_xdata(STK_time)

            STK_az = figure_STK.STK_az_satellite
            self.plot_STK_az.set_ydata(STK_az)
            self.plot_STK_az.set_xdata(STK_time)

        self.f.canvas.draw()

        # Subplot c
        self.c.clear()

        # Check buttons state
        if self.index == 0:
            self.forward.configure(state=tk.DISABLED)
            self.next.configure(state=tk.NORMAL)
        elif self.index == self.length:
            self.forward.configure(state=tk.NORMAL)
            self.next.configure(state=tk.DISABLED)
        else:
            self.forward.configure(state=tk.NORMAL)
            self.next.configure(state=tk.NORMAL)

    def forward(self):

        self.index = self.index - 1

        import get_elements
        self.object_name = get_elements.Get_name(self.index)

        import output_data
        from sys import argv
        available = output_data.Check_data(
            self.index,
            self.object_name.name,
            argv[3],
            argv[4])

        available_predict = available.predict
        if available_predict == 'yes':
            self.predict = self.predict - 1
        available_pyephem = available.pyephem
        if available_pyephem == 'yes':
            self.pyephem = self.pyephem - 1
        available_pyorbital = available.pyorbital
        if available_pyorbital == 'yes':
            self.pyorbital = self.pyorbital - 1
        available_orbitron = available.orbitron
        if available_orbitron == 'yes':
            self.orbitron = self.orbitron - 1
        available_STK = available.STK
        if available_STK == 'yes':
            self.STK = self.STK - 1

        import output_data
        figure = output_data.Read_data(self.pyephem, self.predict, self.pyorbital,
                                       self.orbitron, self.object_name.name, self.STK, argv[3], argv[4])

        # Available
        actual_available = output_data.Check_data(
            self.index,
            self.object_name.name,
            argv[3],
            argv[4])
        available_predict = actual_available.predict
        available_pyephem = actual_available.pyephem
        available_pyorbital = actual_available.pyorbital
        available_orbitron = actual_available.orbitron
        available_STK = actual_available.STK

        import get_elements
        object_name = get_elements.Get_name(self.index)

        self.text.set_text(object_name.name)

        if available_pyephem == 'yes':
            figure_pyephem = output_data.Read_pyephem_data(self.pyephem)
            pyephem_time = figure_pyephem.pyephem_simulation_time

            pyephem_alt = figure_pyephem.pyephem_alt_satellite
            self.plot_pyephem_alt.set_ydata(pyephem_alt)
            self.plot_pyephem_alt.set_xdata(pyephem_time)

            pyephem_az = figure_pyephem.pyephem_az_satellite
            self.plot_pyephem_az.set_ydata(pyephem_az)
            self.plot_pyephem_az.set_xdata(pyephem_time)

        if available_predict == 'yes':
            figure_predict = output_data.Read_predict_data(self.predict)
            predict_time = figure_predict.predict_simulation_time

            predict_alt = figure_predict.predict_alt_satellite
            self.plot_predict_alt.set_ydata(predict_alt)
            self.plot_predict_alt.set_xdata(predict_time)

            predict_az = figure_predict.predict_az_satellite
            self.plot_predict_az.set_ydata(predict_az)
            self.plot_predict_az.set_xdata(predict_time)

        if available_pyorbital == 'yes':
            figure_pyorbital = output_data.Read_pyorbital_data(self.pyorbital)
            pyorbital_time = figure_pyorbital.pyorbital_simulation_time

            pyorbital_alt = figure_pyorbital.pyorbital_alt_satellite
            self.plot_pyorbital_alt.set_ydata(pyorbital_alt)
            self.plot_pyorbital_alt.set_xdata(pyorbital_time)

            pyorbital_az = figure_pyorbital.pyorbital_az_satellite
            self.plot_pyorbital_az.set_ydata(pyorbital_az)
            self.plot_pyorbital_az.set_xdata(pyorbital_time)

        if available_orbitron == 'yes':
            from sys import argv
            figure_orbitron = output_data.Read_orbitron_data(self.orbitron,
                                                             self.object_name.name, argv[4])

            orbitron_time = figure_orbitron.orbitron_time
            orbitron_alt = figure_orbitron.orbitron_alt_satellite
            self.plot_orbitron_alt.set_ydata(orbitron_alt)
            self.plot_orbitron_alt.set_xdata(orbitron_time)

            orbitron_az = figure_orbitron.orbitron_az_satellite
            self.plot_orbitron_az.set_ydata(orbitron_az)
            self.plot_orbitron_az.set_xdata(orbitron_time)

        if available_STK == 'yes':
            figure_STK = output_data.Read_STK_data(self.STK, argv[3])

            STK_alt = figure_STK.STK_alt_satellite
            STK_time = figure_STK.STK_simulation_time
            self.plot_STK_alt.set_ydata(STK_alt)
            self.plot_STK_alt.set_xdata(STK_time)

            STK_az = figure_STK.STK_az_satellite
            self.plot_STK_az.set_ydata(STK_az)
            self.plot_STK_az.set_xdata(STK_time)

        self.f.canvas.draw()

        # Subplot c
        self.c.clear()

        # Check buttons state
        if self.index == 0:
            self.forward.configure(state=tk.DISABLED)
            self.next.configure(state=tk.NORMAL)
        elif self.index == self.length:
            self.forward.configure(state=tk.NORMAL)
            self.next.configure(state=tk.DISABLED)
        else:
            self.forward.configure(state=tk.NORMAL)
            self.next.configure(state=tk.NORMAL)

    def sims_availables(self, available_predict, available_pyephem,
                        available_pyorbital, available_orbitron, available_STK):

        list_of_simulations = []
        if available_STK == 'yes':
            if available_predict == 'yes':
                list_of_simulations.append("STK vs. predict Alt.")
                list_of_simulations.append("STK vs. predict Azi.")
            if available_pyephem == 'yes':
                list_of_simulations.append("STK vs. PyEphem Alt.")
                list_of_simulations.append("STK vs. PyEphem Azi.")
            if available_pyorbital == 'yes':
                list_of_simulations.append("STK vs. PyOrbital Alt.")
                list_of_simulations.append("STK vs. PyOrbital Azi.")
            if available_orbitron == 'yes':
                list_of_simulations.append("STK vs. Orbitron Alt.")
                list_of_simulations.append("STK vs. Orbitron Azi.")
        else:
            list_of_simulations.append("STK not available")

        self.list_of_simulations = list_of_simulations

    def pick_simulation(self, index):

        from output_data import Read_data
        from sys import argv
        comparation = Read_data(self.pyephem, self.predict, self.pyorbital,
                                self.orbitron, self.object_name.name, self.STK, argv[3], argv[4])

        if self.list_of_simulations[index][8:12] == "pred" and\
                self.list_of_simulations[index][16:19] == 'Alt':
            (time, list_alt, list_az) = comparation.STK_vs_predict_comp()

            self.c.clear()

            self.c.plot(time, list_alt, 'ys', label="Difference")
            self.c.legend(loc=2, borderaxespad=0., prop={'size': 12})
            self.c.set_ylabel("Altitude - Degrees")
            self.c.grid(True)

            self.g.canvas.draw()

        elif self.list_of_simulations[index][8:12] == "pred" and\
                self.list_of_simulations[index][16:19] == 'Azi':
            (time, list_alt, list_az) = comparation.STK_vs_predict_comp()

            self.c.clear()

            self.c.plot(time, list_az, 'ys', label="Difference")
            self.c.legend(loc=2, borderaxespad=0., prop={'size': 12})
            self.c.set_ylabel("Azimuth - Degrees")
            self.c.grid(True)

            self.g.canvas.draw()

        elif self.list_of_simulations[index][8:12] == "PyEp" and\
                self.list_of_simulations[index][16:19] == 'Alt':
            (time, list_alt, list_az) = comparation.STK_vs_PyEphem_comp()

            self.c.clear()

            self.c.plot(time, list_alt, 'rs', label="Difference")
            self.c.legend(loc=2, borderaxespad=0., prop={'size': 12})
            self.c.set_ylabel("Altitude - Degrees")
            self.c.grid(True)

            self.g.canvas.draw()

        elif self.list_of_simulations[index][8:12] == "PyEp" and\
                self.list_of_simulations[index][16:19] == 'Azi':
            (time, list_alt, list_az) = comparation.STK_vs_PyEphem_comp()

            self.c.clear()

            self.c.plot(time, list_az, 'rs', label="Difference")
            self.c.legend(loc=2, borderaxespad=0., prop={'size': 12})
            self.c.set_ylabel("Azimuth - Degrees")
            self.c.grid(True)

            self.g.canvas.draw()

        elif self.list_of_simulations[index][8:12] == "PyOr" and\
                self.list_of_simulations[index][18:21] == 'Alt':
            (time, list_alt, list_az) = comparation.STK_vs_PyOrbital_comp()

            self.c.clear()

            self.c.plot(time, list_az, 'bs', label="Difference")
            self.c.legend(loc=2, borderaxespad=0., prop={'size': 12})
            self.c.set_ylabel("Altitude - Degrees")
            self.c.grid(True)

            self.g.canvas.draw()

        elif self.list_of_simulations[index][8:12] == "PyOr" and\
                self.list_of_simulations[index][18:21] == 'Azi':
            (time, list_alt, list_az) = comparation.STK_vs_PyOrbital_comp()

            self.c.clear()

            self.c.plot(time, list_az, 'bs', label="Difference")
            self.c.legend(loc=2, borderaxespad=0., prop={'size': 12})
            self.c.set_ylabel("Azimuth - Degrees")
            self.c.grid(True)

            self.g.canvas.draw()

        elif self.list_of_simulations[index][8:12] == "Orbi" and\
                self.list_of_simulations[index][17:20] == 'Alt':
            (time, list_alt, list_az) = comparation.STK_vs_Orbitron_comp()

            self.c.clear()

            self.c.plot(time, list_alt, 'gs', label="Difference")
            self.c.legend(loc=2, borderaxespad=0., prop={'size': 12})
            self.c.set_ylabel("Altitude - Degrees")
            self.c.grid(True)

            self.g.canvas.draw()

        elif self.list_of_simulations[index][8:12] == "Orbi" and\
                self.list_of_simulations[index][17:20] == 'Azi':
            (time, list_alt, list_az) = comparation.STK_vs_Orbitron_comp()

            self.c.clear()

            self.c.plot(time, list_az, 'gs', label="Difference")
            self.c.legend(loc=2, borderaxespad=0., prop={'size': 12})
            self.c.set_ylabel("Azimuth - Degrees")
            self.c.grid(True)

            self.g.canvas.draw()

    def save_routine(self):

        from tkFileDialog import asksaveasfile
        f = asksaveasfile(mode='w', defaultextension=".txt")
        # asksaveasfile return `None` if dialog closed with "cancel".
        if f is None:
            return

        text = self.save_data()

        f.writelines(("%s\n" % line for line in text))
        f.close()

    def save_data(self):

        import tkMessageBox
        tkMessageBox.showinfo(
            "Wait until simulations end.",
            "This could take a while.")

        index = 0
        i = 0

        text = []
        text.append("==================================")
        from sys import argv
        text.append(" Family %s" % (argv[1]))
        text.append("==================================")

        for i in range(self.length):

            import get_elements
            object_name = get_elements.Get_name(i)

            text.append(" Satellite: %s" % (object_name.name))

            from sys import argv
            from output_data import Check_data
            actual_available = Check_data(
                index,
                object_name.name,
                argv[3],
                argv[4])
            available_STK = actual_available.STK

            if available_STK == 'yes':

                available_predict = actual_available.predict
                available_pyephem = actual_available.pyephem
                available_pyorbital = actual_available.pyorbital
                available_orbitron = actual_available.orbitron

                from output_data import Read_data
                from sys import argv
                data = Read_data(index, index, index,
                                 index, self.object_name.name, index, argv[3], argv[4])

                if available_predict == 'yes':

                    (std_predict_alt, std_predict_az) = data.STK_vs_predict()

                    std_predict_alt = round(float(std_predict_alt), 7)
                    std_predict_az = round(float(std_predict_az), 7)

                    text.append(" predict data")
                    text.append(
                        " Alt: %s Az: %s" %
                        (std_predict_alt, std_predict_az))

                if available_pyephem == 'yes':

                    (std_pyephem_alt, std_pyephem_az) = data.STK_vs_PyEphem()

                    std_pyephem_alt = round(float(std_pyephem_alt), 7)
                    std_pyephem_az = round(float(std_pyephem_az), 7)

                    text.append(" PyEphem data")
                    text.append(
                        " Alt: %s Az: %s" %
                        (std_pyephem_alt, std_pyephem_az))

                if available_pyorbital == 'yes':

                    (std_pyorbital_alt,
                     std_pyorbital_az) = data.STK_vs_PyOrbital()

                    std_pyorbital_alt = round(float(std_pyorbital_alt), 7)
                    round(float(std_pyorbital_az), 7)

                    text.append(" PyOrbital data")
                    text.append(
                        " Alt: %s Az: %s" %
                        (std_pyorbital_alt, std_pyorbital_az))

                if available_orbitron == 'yes':

                    (std_orbitron_alt,
                     std_orbitron_az) = data.STK_vs_Orbitron()

                    std_orbitron_alt = round(float(std_orbitron_alt), 7)
                    std_orbitron_az = round(float(std_orbitron_az), 7)

                    text.append(" Orbitron data")
                    text.append(
                        " Alt: %s Az: %s" %
                        (std_orbitron_alt, std_orbitron_az))

            elif available_STK == 'no':

                print("Data don't available %s" % (i))

            else:

                pass
                # pass

            i = i + 1
            index = index + 1
            text.append("")

        return text

        # save in pdf file

    def std_simulations(self):

        from output_data import Read_data
        from sys import argv

        # predict
        data = Read_data(self.pyephem, self.predict, self.pyorbital,
                         self.orbitron, self.object_name.name, self.STK, argv[3], argv[4])
        (std_predict_alt, std_predict_az) = data.STK_vs_predict()

        self.text_std_predict_alt.set(round(float(std_predict_alt), 7))
        self.text_std_predict_az.set(round(float(std_predict_az), 7))

        # pyephem
        (std_pyephem_alt, std_pyephem_az) = data.STK_vs_PyEphem()

        self.text_std_pyephem_alt.set(round(float(std_pyephem_alt), 7))
        self.text_std_pyephem_az.set(round(float(std_pyephem_az), 7))

        # pyorbital
        (std_pyorbital_alt, std_pyorbital_az) = data.STK_vs_PyOrbital()

        self.text_std_pyorbital_alt.set(round(float(std_pyorbital_alt), 7))
        self.text_std_pyorbital_az.set(round(float(std_pyorbital_az), 7))

        # orbitron
        (std_orbitron_alt, std_orbitron_az) = data.STK_vs_Orbitron()

        self.text_std_orbitron_alt.set(round(float(std_orbitron_alt), 7))
        self.text_std_orbitron_az.set(round(float(std_orbitron_az), 7))

    def _quit(self):
        root.quit()     # stops mainloop


if __name__ == '__main__':
    import Tkinter as tk
    root = tk.Tk()
    interfaz = GUI()
    root.title("Simulaciones")
    root.geometry("1010x620")
    root.resizable(0, 0)
    root.mainloop()
