import database as db
import tkinter as tk
from tkinter import ttk

class GuiApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(HomePage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
    
    def seating_frame(self, frame_class, seat_bit):
        new_frame = frame_class(self, seat_bit)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class HomePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Welcome to Nutflix").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Showtimes and Booking", command = lambda: master.switch_frame(Showtimes)).pack()
        tk.Button(self, text="Pre-Book", command = lambda: master.switch_frame(PreBook)).pack()
        tk.Button(self, text="Staff", command = lambda: master.switch_frame(Staff)).pack()

class Showtimes(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Enter show's number to view seating").pack(side="top", fill="x", pady=10)
        self.def_date , self.def_movie, self.def_start, self.def_end = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()
        self.def_start.set('-')
        self.def_end.set('-')
        self.def_date.set('28.03.21')
        self.def_movie.set('-') 
        self.movie_opt = db.now_showing + ['-']
        self.menu = ShowMenu('28.03.21', '-', 0, 0)
        self.menu.display(db.now_showing, db.shows)
        self.selected = tk.Entry(self)
        self.selected.pack()
        tk.OptionMenu(self, self.def_date, '28.03.21', '29.03.21', '30.03.21', '31.03.21', '01.04.21', command = self.selected_date).pack()
        tk.OptionMenu(self, self.def_movie, *self.movie_opt, command = self.selected_movie).pack()
        tk.OptionMenu(self, self.def_start, *db.time_filter, command = self.selected_time).pack()
        tk.OptionMenu(self, self.def_end, *db.time_filter, command = self.selected_time).pack()
        tk.Button(self, text = "Reset Time", command = self.reset_time).pack()
        tk.Button(self, text = 'Preview Seating', command = lambda: master.seating_frame(Seating, self.selected_show(self.selected.get()))).pack()
        tk.Button(self, text="Back", command=lambda: master.switch_frame(HomePage)).pack()

    def selected_date(self, date):
        self.new_date = ''
        self.new_date = self.def_date.get()
        if self.new_date != self.def_date:
           self.menu.set_date(self.new_date)
           self.menu.display(db.now_showing, db.shows)

    def selected_movie(self, movie):
        self.new_movie = ''
        self.new_movie = self.def_movie.get()
        if self.new_movie != self.def_movie:
            self.menu.set_movie(self.new_movie)
            self.menu.display(db.now_showing, db.shows)
        else:
            self.menu.set_movie(self.new_movie)
            self.menu.display(db.now_showing, db.shows)

    def selected_time(self, time):
        self.new_start, self.new_end = '', ''
        self.new_start = self.def_start.get()
        self.new_end = self.def_end.get()
        if self.new_start != self.def_start and self.new_end != self.def_end:
            self.menu.set_time([self.new_start, self.new_end])
            self.menu.display(db.now_showing, db.shows)
    
    def reset_time(self):
        self.menu.set_time([0, 0])
        self.menu.display(db.now_showing, db.shows)
        self.def_start.set('-')
        self.def_end.set('-')
        
    def selected_show(self, input):
        res = ''
        res = input
        return self.menu.seating_search(res)

class Seating(tk.Frame):
    def __init__(self,  master, data):
        tk.Frame.__init__(self)
        self.seats = [[0 for x in range(5)] for y in range(3)]
        for row in data:
            count = -1
            for col in row:
                if col == '0':
                    count += 1
                    self.seats[data.index(row)][count] = tk.Button(self, bg = 'white')
                    self.seats[data.index(row)][count].grid(row = data.index(row), column = count)
                elif col == '1':
                    count += 1
                    self.seats[data.index(row)][count] = tk.Button(self, bg = 'gray')
                    self.seats[data.index(row)][count].grid(row = data.index(row), column = count)

class PreBook(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.movie, self.date = tk.StringVar(), tk.StringVar(),
        self.movie.set(db.now_showing[0])
        self.date.set('28.03.21')
        tk.OptionMenu(self, self.movie, *db.now_showing).pack()
        tk.OptionMenu(self, self.date, '28.03.21', '29.03.21', '30.03.21', '31.03.21', '01.04.21').pack()
        self.time = tk.Entry(self)
        self.time.pack()
        tk.Button(self, text="Submit", command = self.submit).pack()
        tk.Button(self, text="Back", command = lambda: master.switch_frame(HomePage)).pack()

    def submit(self):
        movie, date, time = '', '', ''
        movie = self.movie.get()
        date = self.date.get()
        time = self.time.get()
        res = '\n' + movie + ',' + date + ',' + time
        f = open('prebook.txt', 'a')
        f.write(res)
        f.close()
        self.time.destroy()
        self.time = tk.Entry(self)
        self.time.pack()

class Staff(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width = 10000, height = 5000)
        tk.Label(self, text="Staff").pack(side="top", fill="x", pady=10)
        self.username = tk.Entry(self)
        self.password = tk.Entry(self)
        self.username.pack()
        self.password.pack()
        self.select = tk.StringVar()
        self.select.set('Select a date')
        tk.Button(self, text="Login", command = self.auth).pack()
        tk.Button(self, text="Back", command = lambda: master.switch_frame(HomePage)).pack()

    def auth(self):
        for acc in db.staff:
            if self.username.get() == acc[0]:
                if self.password.get() == acc[1]:
                    self.username.destroy()
                    self.password.destroy()
                    tk.OptionMenu(self, self.select, '10.04.21', '11.04.21', '12.04.21', '13.04.21', '14.04.21', command = self.future_date).pack()
                else:
                    tk.Label(self, text = 'Invalid Password').pack()
                    return 0
        tk.Label(self, text ='Invalid Username').pack()

    def future_date(self, date):
        self.table = ttk.Treeview(self)
        self.table['columns'] = ('Movie', '00.00-02.00', '02.00-04.00', '04.00-06.00', '06.00-08.00', '08.00-10.00', '10.00-12.00', '12.00-14.00', '14.00-16.00', '16.00-18.00', '18.00-20.00', '20.00-22.00', '22.00-24.00')
        self.table.column('#0', width = 0, stretch='NO')
        for col in db.table_col:
            self.table.column(col, width = 80)
            self.table.heading(col, text = col)
        self.date, self.movie, self.res = '', [], [0 for i in range(12)]
        count = 0
        self.date = self.select.get()
        for entry in db.prebook:
            if entry[1] == self.date and entry[0] not in self.movie:
                self.movie.append(entry[0])
        for movie in self.movie:
            count += 1
            for entry in db.prebook:
                if entry[0] == movie and entry[1] == self.date:
                    self.res[int(float(entry[2])//2)] = entry[3]
            self.res = [movie] + self.res
            self.table.insert(parent = '', index = count, iid = count, values = self.res)
            self.res = [0 for i in range(12)]
        self.table.pack()

class ShowMenu:
    def __init__(self, date, movie, start, end):
        self.date = date
        self.movie = movie
        self.start = start
        self.end = end
        self.cart = []

    def display(self, now_showing, shows):
        print('\n\n\n')
        self.cart, self.count = [], 0
        if self.movie == '-':  
            for movie in now_showing: 
                print(movie)
                if self.start == self.end:
                    for show in shows:
                        if show[1] == movie and show[2] == self.date:
                            self.count += 1
                            self.cart.append(show + [self.count])
                            print(str(self.count) + '. ' + str(show[3]))
                else:
                    for show in shows:
                        if show[1] == movie and show[2] == self.date and self.start <= float(show[3]) <= self.end:
                            self.count += 1
                            self.cart.append(show + [self.count])
                            print(str(self.count) + '. ' + str(show[3]))
        else:
            print(self.movie)
            if self.start == self.end:
                for show in shows:
                    if show[1] == self.movie and show[2] == self.date:
                        self.count += 1
                        self.cart.append(show + [self.count])
                        print(str(self.count) + '. ' + str(show[3]))
            else:
                for show in shows:
                    if show[1] == self.movie and show[2] == self.date and self.start<= float(show[3]) <= self.end:
                        self.count += 1
                        self.cart.append(show + [self.count])
                        print(str(self.count) + '. ' + str(show[3]))

    def set_date(self, date):
        self.date = date
    
    def set_movie(self, title):
        self.movie = title

    def set_time(self, time):
        self.start = float(time[0])
        self.end = float(time[1])

    def seating_search(self, id):
        self.res, self.seat = '', []
        for show in self.cart:
            if int(id) == show[4]:
                self.res = show[0]
        for seating in db.seating:
            if self.res == seating[0]:
                self.seat += seating[1:]
        return self.seat

app = GuiApp()
app.mainloop()