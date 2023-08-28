import tkinter as tk
from tkinter import ttk
import csv
import datetime

class Client:
    def __init__(self, dic):
        self.name = dic['name']
        self.ic = dic['ic']
        self.address = dic['address']
        self.phone = dic['phone']
        self.state = dic['state']
        self.age = dic['age']
        self.status = dic['status']
        self.curr_centre = dic['curr_centre']

class Centre:
    def __init__(self, dic):
        self.name = dic['name']
        self.address = dic['address']
        self.op_hour = dic['op_hour']
        self.phone = dic['phone']
        self.state = dic['state']
        self.vacc_brand = dic['vacc_brand']
        self.status = dic['status']


class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Launch)
        self.user = None

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class Launch(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = 'iSejahtera').pack()
        self.ic = tk.Entry(self)
        self.ic.pack()
        tk.Button(self, text = 'Login', command = self.login).pack()

    def login(self):
        ic = self.ic.get()
        client = dict()
        reader = csv.reader(open('client.csv', 'r'))
        found = False
        for row in reader:
            if ic == row[1]:
                client['name'], client['ic'], client['address'], client['phone'], client['state'], client['age'], client['status'], client['curr_centre'] = row
                found = True
        if found:
            main.user = Client(client)
            main.switch_frame(Home)
        else:
            tk.Label(self, text = 'Invalid IC').pack()


class Home(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = 'iSejahtera').pack()
        tk.Button(self, text = 'Check In/Check Out', command = lambda:main.switch_frame(CheckInOut)).pack()
        tk.Button(self, text = 'Find A Centre', command = lambda:main.switch_frame(FindCentre)).pack()
        tk.Button(self, text = 'View Profile', command = lambda: main.switch_frame(Profile)).pack()


class CheckInOut(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        if main.user.curr_centre == '0':
            tk.Label(self, text = 'iSejahtera').pack()
            reader = csv.reader(open('centre.csv', 'r'))
            centre_list = []
            for row in reader:
                centre_list.append(row[0])
            self.check_in_location = ttk.Combobox(self, values = centre_list, width = 50)
            self.check_in_location.pack()
            tk.Button(self, text = 'Check In', command = self.check_in).pack()
            tk.Button(self, text = 'Back', command = lambda: main.switch_frame(Home)).pack()
        else:
            tk.Label(self, text = 'iSejahtera').pack()
            tk.Label(self, text = 'Vaccination In Progress').pack()
            tk.Button(self, text = 'Check Out', command = self.check_out).pack()
            tk.Button(self, text = 'Back', command = lambda: main.switch_frame(Home)).pack()
    
    def check_in(self):
        centre = self.check_in_location.get()
        centre_dic = dict()
        reader = csv.reader(open('centre.csv', 'r'))
        for row in reader:
            if centre == row[0]:
                centre_dic['name'], centre_dic['address'], centre_dic['op_hour'], centre_dic['vacc_brand'], centre_dic['phone'], centre_dic['state'], centre_dic['status'] = row
        main.centre_visited = Centre(centre_dic)
        main.user.curr_centre = centre
        reader = csv.reader(open('centre.csv', 'r'))
        new_data = []
        for row in reader:
            if centre == row[0]:
                new_data.append(row[0:-1] + [int(row[-1]) + 1])
            else:
                new_data.append(row)
        writer = csv.writer(open('centre.csv', 'w', newline = ''))
        writer.writerows(new_data)
        reader = csv.reader(open('client.csv', 'r'))
        new_data = []
        for row in reader:
            if main.user.name == row[0]:
                new_data.append(row[0:-1] + [centre])
            else:
                new_data.append(row)
        writer = csv.writer(open('client.csv', 'w', newline = ''))
        writer.writerows(new_data)
        main.switch_frame(Home)
    
    def check_out(self):
        date = datetime.date.today().strftime('%d/%m/%Y')
        row = [main.user.name] + [main.user.ic] + [main.user.curr_centre] + [date] + [main.user.phone] + [main.user.state]
        writer = csv.writer(open('record.csv', 'a', newline = ''))
        writer.writerow(row)
        reader = csv.reader(open('client.csv', 'r'))
        new_data = []
        user = main.user.name
        for row in reader:
            if user == row[0]:
                new_data.append(row[0:-2] + ['Vaccinated'] + ['0'])
            else:
                new_data.append(row)
        writer = csv.writer(open('client.csv', 'w', newline = ''))
        writer.writerows(new_data)
        reader = csv.reader(open('centre.csv', 'r'))
        new_data = []
        centre = main.user.curr_centre
        for row in reader:
            if centre == row[0]:
                new_data.append(row[0:-1] + [int(row[-1]) - 1])
            else:
                new_data.append(row)
        writer = csv.writer(open('centre.csv', 'w', newline = ''))
        writer.writerows(new_data)
        main.user.curr_centre = '0'
        main.switch_frame(Home)


class FindCentre(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = 'iSejahtera').pack()
        self.district = tk.StringVar()
        self.district.set('Select Your District')
        tk.OptionMenu(self, self.district, 'Barat Daya', 'Seberang Perai Selatan', 'Seberang Perai Tengah', 'Seberang Perai Utara', 'Timur Laut', command = self.get_centre).pack()
        tk.Button(self, text = 'Back', command = lambda: main.switch_frame(Home)).pack()
        self.centre_found = []
        self.new_search = True

    def get_centre(self, district):
        if not self.new_search:
            self.table.destroy()
            self.scale.destroy()
        for button in self.centre_found:
            button.destroy()
        self.centre_found.clear()
        district = self.district.get()
        reader = csv.reader(open('district.csv', 'r'))
        btn = 0
        for row in reader:
            if district == row[0]:
                centre_list = row[1:]
        for centre in centre_list:
            self.centre_found.append(tk.Button(self, text = centre, command = lambda button = btn: self.centre_info(button)))
            btn += 1
        for button in self.centre_found:
            button.pack()

    def centre_info(self, btn):
        if not self.new_search:
            self.table.destroy()
            self.scale.destroy()
        centre = self.centre_found[btn].cget("text")
        reader = csv.reader(open('centre.csv', 'r'))
        for row in reader:
            if centre == row[0]:
                self.info_table(row)
                self.people_count(row[-1])
        self.new_search = False

    def info_table(self, info):
        self.table = ttk.Treeview(self, columns = (1, 2))
        count = 0
        self.table.column('#0', width = 0, stretch = 'NO')
        self.table.column(1, width = 100)
        self.table.column(2, width = 650)
        rows = ['Name', 'Address', 'Operation Hour', 'Vaccine Brand', 'Phone', 'State', 'Status']
        for i in range(len(rows)):
            values = [rows[i]] + [info[i]]
            self.table.insert(parent = '', index = count, iid = count, values = values)
            count += 1
        self.table.pack()

    def people_count(self, status):
        self.scale = tk.Scale(self, from_ = 0, to = 10, orient = tk.HORIZONTAL)
        self.scale.set(status)
        self.scale.pack()


class Profile(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text = 'iSejahtera').pack()
        user_info = []
        reader = csv.reader(open('client.csv', 'r'))
        for row in reader:
            if main.user.name == row[0]:
                user_info = row
        self.profile = ttk.Treeview(self, columns = (1, 2))
        count = 0
        self.profile.column('#0', width = 0, stretch='NO')
        self.profile.column(1, width = 100)
        self.profile.column(2, width = 300)
        rows = ['Name', 'IC', 'Address', 'Phone', 'State', 'Age', 'Status']
        for i in range(len(rows)):
            values = [rows[i]] + [user_info[i]]
            self.profile.insert(parent = '', index = count, iid = count, values = values)
            count += 1
        self.profile.pack()
        tk.Button(self, text = 'Back', command = lambda: main.switch_frame(Home)).pack()


if __name__ == "__main__":
    main = Main()
    main.mainloop()