import tkinter as tk
from tkinter import ttk
from nsepy import *
import nsepy
import numpy as np
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt1
import mysql.connector
import threading
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.dates as mdates
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense , Dropout , LSTM
import datetime as dt

#  connector for databse
my_connect = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="5615",
    database="stock"
)
my_cursor = my_connect.cursor()
times_enter = 0

LARGE_FONT = ("Verdana", 22)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)
counter1 = 0

file1 = pd.read_excel("mcap.xlsx")

l_company = file1["Company Name"]
l_symbol = file1['Symbol']
final_list = list(map(lambda x, y: x + "::" + y, l_company, l_symbol))

test_list = final_list
test_list1 = final_list


class Stock:

    def PageOneGui(self):

        my_cursor.execute("""create table IF NOT EXISTS stock_table (stocks_id int auto_increment primary key,
                                                    user_id int(10), company_name varchar(30),
                                                    buy_at float(3),units int,
                                                    total_amount float(30)

                                                    );
                                    """)
        my_cursor.execute("""create table IF NOT EXISTS user (user_id int auto_increment primary key,
                                                            user_name varchar(20));
                                   """)
        my_cursor.execute(
            """alter table stock_table add FOREIGN KEY (user_id) REFERENCES user(user_id) on delete cascade;""")

        self.tickerSymbol = tk.StringVar()
        self.tickerSymbol.trace('w', self.on_change)
        self.tickerSymbol1 = tk.StringVar()
        self.tickerSymbol1.trace('w', self.on_change1)
        self.units_no = tk.IntVar()
        self.v = tk.IntVar()
        # BackGround image
        load = Image.open(
            "euro-447214_1920.jpg")
        banner = ImageTk.PhotoImage(load)
        w = tk.Label(Home_t)
        w.image = banner
        w.configure(background="#D2D7CE")
        w.place(x=0, y=0, relwidth=1, relheight=1)

        load1 = Image.open(
            "euro-447214_1920.jpg")
        banner1 = ImageTk.PhotoImage(load)
        w1 = tk.Label(Trading)
        w1.image = banner
        w1.configure(background="#D2D7CE")
        w1.place(x=0, y=0, relwidth=1, relheight=1)

        # Title and fvicon
        root.title("Stock Forecasting")
        root.minsize(width=1540, height=810)

        fvicon = tk.PhotoImage(file="stock-earnings.png")
        root.iconphoto(False, fvicon)
        # Labels for Tabs
        tk.Label(Home_t, text="ANALYZER", font=LARGE_FONT, fg="#639A36", bg="#D2D7CE").pack(padx=100)
        tk.Label(Trading, text=" TRADE ", font=LARGE_FONT, fg="#639A36", bg="#D2D7CE").pack(padx=10, pady=10)
        self.v = tk.IntVar()
        self.v.set(1)

        # Label and Searchbox for entering tickers
        tk.Label(Home_t, text="ENTER COMPANY : ", bg="#D2D7CE", font=("Verdana", 11)).place(relx=0.331, rely=0.1,
                                                                                            anchor="center")
        self.searchbox = tk.Entry(Home_t, textvariable=self.tickerSymbol, background="#E9EFE5", fg="#639A36",
                                  font=("Verdana", 12),
                                  borderwidth=0)
        self.searchbox.place(relx=0.5, rely=0.1, relwidth=0.2, anchor="center")

        # Radio Buttons
        tk.Label(Home_t, text="   Predict For  ", font=("Verdana", 15), bg="#D2D7CE").place(relx=0.5, rely=0.15,
                                                                                            anchor="center")

        self.d3 = tk.Radiobutton(Home_t, text="10 days", font=("Verdana", 10), variable=self.v, command=self.ShowChoice,
                                 value=10, bg="#D2D7CE").place(relx=0.475, rely=0.2, anchor="center")
        self.d4 = tk.Radiobutton(Home_t, text="15 days", font=("Verdana", 10), variable=self.v, command=self.ShowChoice,
                                 value=15, bg="#D2D7CE").place(relx=0.525, rely=0.2, anchor="center")

        # Search button
        self.searchbutton = tk.Button(Home_t, text="Predict", bg='#878786', fg="white", height=2, width=20,
                                      font=("Verdana", 10), command=self.GetTickers).place(
            relx=0.5, rely=0.255, anchor="center")

        self.listbox = tk.Listbox(Home_t, background="#E9EFE5", fg="#639A36",
                                  font=("Verdana", 12),
                                  borderwidth=0)
        vsb = ttk.Scrollbar(self.listbox, orient="horizontal", command=self.listbox.xview)
        vsb.place(relx=0, rely=0.9, relwidth=1)
        self.listbox.configure(xscrollcommand=vsb.set, height=10)
        self.listbox.place(relwidth=0.2, relx=0.5, rely=0.25, anchor="center")
        # listbox.bind('<Double-Button-1>', on_select)
        
        self.listbox.place_forget()
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.listbox_update(test_list)

        # all of Trading page
        # company name and entry box

        tk.Label(Trading, text="ENTER Company : ", font=("Verdana", 11), bg="#D2D7CE").place(relx=0.331, rely=0.1,
                                                                                             anchor="center")

        self.tickerbox = tk.Entry(Trading, textvariable=self.tickerSymbol1, background="#E9EFE5",
                                  fg="#639A36", font=("Verdana", 12),
                                  borderwidth=0)
        self.tickerbox.place(relx=0.5, rely=0.1, relwidth=0.2, anchor="center")
        # no of units entry and label
        tk.Label(Trading, text="ENTER NO OF UNITS : ", font=("Verdana", 11), bg="#D2D7CE").place(relx=0.337, rely=0.145,
                                                                                                 anchor="center")

        self.tickerbox1 = tk.Entry(Trading, textvariable=self.units_no, background="#E9EFE5",
                                   fg="#639A36", font=("Verdana", 12),
                                   borderwidth=0)
        self.tickerbox1.place(relx=0.5, rely=0.145, relwidth=0.2, anchor="center")
        # buy button

        self.buybutton = tk.Button(Trading, text="BUY", bg='#878786', fg="white", height=2, width=20,
                                   font=("Verdana", 10), command=self.buy_stock).place(
            relx=0.5, rely=0.255, anchor="center")
        # table of trading

        self.id = 0
        self.iid = 0
        frm = tk.Frame(Trading)
        frm.place(relx=0.001, rely=0.5)
        self.tv = ttk.Treeview(frm, columns=(1, 2, 3, 4), show="headings", height="14")
        self.tv.pack(expand=True, ipadx=360, padx=0, fill=tk.X)

        self.tv.heading(1, text="company")
        self.tv.heading(2, text="units")
        self.tv.heading(3, text="buy at")
        self.tv.heading(4, text="Total amount")
        # delete button
        self.delete_button = tk.Button(Trading, text="SELL", bg='#878786', fg="white", height=2, width=20,
                                       font=("Verdana", 10), command=self.delete_data)
        self.delete_button.place(relx=0.5, rely=0.4, anchor="center")

        vsb = ttk.Scrollbar(self.tv, orient="vertical", command=self.tv.yview)
        vsb.place(relx=.988, rely=.08, height=280)

        self.tv.configure(yscrollcommand=vsb.set)
        # listbox for trading

        self.listbox1 = tk.Listbox(Trading, background="#E9EFE5", fg="#639A36",
                                   font=("Verdana", 12),
                                   borderwidth=0)
        vsb = ttk.Scrollbar(self.listbox1, orient="horizontal", command=self.listbox1.xview)
        vsb.place(relx=0, rely=0.9, relwidth=1)
        self.listbox1.configure(xscrollcommand=vsb.set, height=10)
        self.listbox1.place(relwidth=0.2, relx=0.5, rely=0.25, anchor="center")
        # listbox.bind('<Double-Button-1>', on_select)
        
        self.listbox1.place_forget()
        self.listbox1.bind('<<ListboxSelect>>', self.on_select1)
        self.listbox_update1(test_list1)

        thread1 = threading.Thread(target=self.print_data)
        thread1.start()

    def on_change(self, *args):

        value = self.tickerSymbol.get()
        value = value.strip().lower()
        
        # get data from test_list
        if value == '':

            self.listbox.place_forget()

            data3 = test_list
            if self.tickerSymbol.get() == "":
                self.listbox.place_forget()
            else:
                self.listbox.place(relwidth=0.2, relx=0.5, rely=0.25, anchor="center")

        else:

            self.listbox.place(relwidth=0.2, relx=0.5, rely=0.25, anchor="center")
            data3 = []
            for item in test_list:
                if value in item.lower():
                    data3.append(item)

                    # update data in listbox
        self.listbox_update(data3)

    def listbox_update(self, data3):
        # delete previous data
        self.listbox.delete(0, 'end')

        # sorting data
        data3 = sorted(data3, key=str.lower)
        z = 0
        # put new data
        for item in data3:
            self.listbox.insert('end', item)

    def on_select(self, event):
        # display element selected on list
        print('(event) previous:', event.widget.get('active'))
        self.name = event.widget.get(event.widget.curselection())
        self.ls1 = self.name.split("::")
        
        print('(event) current:', self.name)
        self.searchbox.delete(0, 'end')
        self.searchbox.insert(string=self.name, index=1)
        print("\n\n\n", self.tickerSymbol.get(), "             ", self.name)
        if self.tickerSymbol.get() == self.name:
            self.listbox.place_forget()
        else:
            self.listbox.place(relwidth=0.2, relx=0.5, rely=0.25, anchor="center")

    def on_change1(self, *args):
        # print(args)

        value1 = self.tickerSymbol1.get()
        value1 = value1.strip().lower()
        print("value : ", value1)
        # get data from test_list
        if value1 == '':

            print("222222222222222244444444")
            self.listbox1.place_forget()

            data4 = test_list1
            if self.tickerSymbol1.get() == "":
                self.listbox1.place_forget()
            else:
                self.listbox1.place(relwidth=0.2, relx=0.5, rely=0.25, anchor="center")
        # listbox.configure(height=1)
        else:

            self.listbox1.place(relwidth=0.2, relx=0.5, rely=0.25, anchor="center")
            data4 = []
            for item in test_list1:
                if value1 in item.lower():
                    data4.append(item)

                    # update data in listbox
        self.listbox_update1(data4)

    def listbox_update1(self, data4):
        # delete previous data
        self.listbox1.delete(0, 'end')

        # sorting data
        data4 = sorted(data4, key=str.lower)
        z = 0
        # put new data
        for item in data4:
            self.listbox1.insert('end', item)
        # for liItem in self.listbox.Items:
        #     z +=1
        # if z == 0:
        #     self.listbox.configure(height=0)

    def on_select1(self, event):
        # display element selected on list
        print('(event) previous1:', event.widget.get('active'))
        self.name1 = event.widget.get(event.widget.curselection())
        self.ls11 = self.name1.split("::")
        
        print('(event) current1:', self.name1)
        self.tickerbox.delete(0, 'end')
        self.tickerbox.insert(string=self.name1, index=1)
        print("\n\n\n", self.tickerSymbol.get(), "             ", self.name1)
        if self.tickerSymbol1.get() == self.name1:
            self.listbox1.place_forget()
        else:
            self.listbox1.place(relwidth=0.2, relx=0.5, rely=0.25, anchor="center")

    def buy_stock(self):
        tickers1 = self.ls11[1]
        print(tickers1)
        units = self.units_no.get()

        self.validation_for_Trade(tickers1, units)

        return tickers1, units

    def validation_for_Trade(self, tickers1, units):
        data = nsepy.live.get_quote(symbol=tickers1)
      
        if (len(data['data']) == 0):
            self.popupmsg("ENTER VALID NAME")
            self.searchbox.delete(0, 'END')
        elif units == 0:
            self.popupmsg("Please Select Days")
        else:
            liv_d = nsepy.live.get_quote(symbol=str(tickers1))
            liv_d2 = liv_d['data']
            liv_d3 = liv_d2[0]
            buy_at = liv_d3['lastPrice']
            buy_at = buy_at.replace(",","")
            
            total_amo = float(float(units) * float(buy_at))

            # sql command to insert values
            sql = """INSERT INTO stock_table (user_id, company_name,buy_at,units,total_amount)
                     VALUES (%s,%s,%s,%s,%s)"""
            values = (1, tickers1, buy_at, units, total_amo)
            my_cursor.execute(sql, values)

            my_connect.commit()
            print(my_cursor.rowcount, "record inserted.")
            self.tv.insert('', 'end', iid=self.iid, values=(values[1].upper(), values[3], values[2], values[4]))
            self.iid += 1
            self.id += 1

    # func for validation of tickers of predection

    # def disp_records(self):

    def validate(self, tickers, choice_p):
        self.data = get_history(symbol=tickers.upper(), start=date(2018, 12, 1), end=date.today())
        if self.data.empty:
            self.popupmsg("ENTER VALID NAME")
            self.searchbox.delete(0, 'END')
        elif choice_p == 1:
            self.popupmsg("Please Select Days")
        else:
            self.disp_graphs(self.data)

    # func for popup message
    def popupmsg(self, msg):
        popup = tk.Tk()
        popup.wm_title("!")
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
        B1.pack()
        popup.mainloop()

    # func for getting tickers
    def GetTickers(self):
        tickers = self.ls1[1]
        choice_p = self.ShowChoice()
        self.validate(tickers, choice_p)

        return tickers

    def ShowChoice(self):
        return self.v.get()

    # func for displaying graphs
    def disp_graphs(self, data):
        global times_enter

        self.graphl = []

        f1 = self.pred(self.data, self.v.get(), self.tickerSymbol.get())
        f2 = self.pred1(self.data)
        self.graphl.append(f1)
        self.graphl.append(f2)

        #  creating canvas

        self.canvas = FigureCanvasTkAgg(f1, Home_t)
        self.canvas.draw()
        if times_enter >= 1:
            self.toolbar.forget()

        self.canvas.get_tk_widget().place(relx=0.5, rely=0.54, anchor="center")

        self.toolbar = NavigationToolbar2Tk(self.canvas, Home_t)
        self.toolbar.pan()
        self.toolbar.update()
        self.toolbar.place(relx=0.5, rely=0.33, anchor="center")
        self.canvas._tkcanvas.place(relx=0.5, rely=0.65, anchor="center")

        # buttons for scrolling

        self.Previous = tk.Button(Home_t, text="<<", bg='#878786', fg="white", height=2, width=10,
                                  font=("Verdana", 10), command=self.PreviousG).place(relx=0.001, rely=0.5,
                                                                                      anchor="w")

        self.Next = tk.Button(Home_t, text=">>", bg='#878786', fg="white", height=2, width=10,
                              font=("Verdana", 10), command=self.NextG).place(relx=0.991, rely=0.5,
                                                                              anchor="e")

        times_enter += 1

    def PreviousG(self):
        global counter1
        counter1 = counter1 - 1
        if counter1 < 0:
            counter1 = 1
        self.canvas.get_tk_widget().place_forget()
        self.toolbar.place_forget()
        self.canvas = FigureCanvasTkAgg(self.graphl[counter1], Home_t)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.5, rely=0.65, anchor="center")
        self.toolbar = NavigationToolbar2Tk(self.canvas, Home_t)
        self.toolbar.pan()
        self.toolbar.place(relx=0.5, rely=0.33, anchor="center")
        self.toolbar.update()

    def NextG(self):
        global counter1
        counter1 = counter1 + 1
        if (counter1 >= 2):
            counter1 = 0
        self.canvas.get_tk_widget().place_forget()
        self.toolbar.place_forget()
        self.canvas = FigureCanvasTkAgg(self.graphl[counter1], Home_t)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.5, rely=0.54, anchor="center")
        self.toolbar = NavigationToolbar2Tk(self.canvas, Home_t)
        self.toolbar.place(relx=0.5, rely=0.33, anchor="center")
        self.toolbar.pan()
        self.toolbar.update()
        self.canvas._tkcanvas.place(relx=0.5, rely=0.65, anchor="center")

    def delete_data(self):

        row_id = int(self.tv.focus())
        values = self.tv.item(row_id)
        f_values = values['values']
        sql = """delete from stock_table where company_name = %s and units = %s and buy_at = %s and total_amount = %s"""
        val = (f_values[0], f_values[1], f_values[2], f_values[3])
        my_cursor.execute(sql, val)
        my_connect.commit()
        self.tv.delete(row_id)

    def print_data(self):

        self.iid = 0
        self.id = 0

        sql = """ select s.company_name,s.units,s.buy_at,s.total_amount
                 from stock_table as s
                 where s.user_id in (select user.user_id
                                    from user
                                    where user.user_name='pratik');
                 """
        my_cursor.execute(sql)

        row1 = my_cursor.fetchall()

        for i in row1:
            self.tv.insert('', 'end', iid=self.iid, values=i)
            self.iid = self.iid + 1
            self.id = self.id + 1

    def pred(self, data, choice, symbol):
       
        sym = symbol.split('::')

        company = sym[1]
        start = dt.date(2019, 1, 1)
        end = dt.date(2020, 1, 1)

        pd.set_option('display.max_columns', None)
        # Load Data
        data = get_history(symbol=company, start=start, end=end)
        # data = web.DataReader( company , 'yahoo',start , date.today())

        data = data.drop('Symbol', axis=1)
        data = data.drop('Series', axis=1)
        

        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))
        print("---------------------------scaled data-------------------------------")
       
        prediction_days = 60

        x_train = []
        y_train = []

        for x in range(prediction_days, len(scaled_data)):
            x_train.append(scaled_data[x - prediction_days:x, 0])
            y_train.append(scaled_data[x, 0])

        # print("---------------------------x train and y train-------------------------------")
        # print(x_train,"    ",y_train)
        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        # print("---------------------------x train reshape-------------------------------")
        # print(x_train)
        # Build The Model
        model = Sequential()

        model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))

        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(x_train, y_train, epochs=27, batch_size=50)

        '''' Test the Model Accuracy on Existing Data '''

        # Load Test Data

        test_start = dt.date(2020, 1, 1)
        test_end = dt.date.today()

        test_data = get_history(company, test_start, test_end)
        test_data = test_data.drop(['Symbol', 'Series'], axis=1)
        print("-------------------------------------test data----------------------------------")
        

        actual_prices = test_data['Close'].values
        print("---------------------------actual prices-------------------------------")
        

        total_dataset = pd.concat((data['Close'], test_data['Close']))

        print("---------------------------total dataset-------------------------------")
        

        model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
        model_inputs = model_inputs.reshape(-1, 1)
        model_inputs = scaler.transform(model_inputs)

        print("---------------------------model inputs-------------------------------")
        
        # make predictions on test data

        x_test = []

        for x in range(prediction_days, len(model_inputs)):
            x_test.append(model_inputs[x - prediction_days:x, 0])

        # print("---------------------------x test-------------------------------")
        # print(x_test)
        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        # print("---------------------------x test-------------------------------")
        # print(x_test)

        predictions_prices = model.predict(x_test)
        predictions_prices = scaler.inverse_transform(predictions_prices)

        print("---------------------------prediction prices-------------------------------")
     
        temp = list(test_data.index)

        # for i in range(6):
        #     temp.append(temp[-1] + dt.timedelta(days=1))



        print(type(predictions_prices), "                ", type(model_inputs))
        # predict next day
        for i in range(choice):
            real_data = [model_inputs[len(model_inputs) + 1 - prediction_days:len(model_inputs + 1), 0]]
            real_data = np.array(real_data)
            real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))

            prediction = model.predict(real_data)

            prediction = scaler.inverse_transform(prediction)
            predictions_prices = np.append(predictions_prices, prediction[0])
            predictions_prices = predictions_prices.reshape(-1, 1)
            model_inputs = np.append(model_inputs, prediction[0])
            model_inputs = model_inputs.reshape(-1, 1)

            print(f" Prediction :  {prediction}")
            temp.append(temp[-1] + dt.timedelta(days=1))
            print(temp[-1], "        ", predictions_prices[-1])
            i += 1

        f1 = plt1.figure(figsize=(13, 4.5))


        # print("Dates are ",data.iloc[:,0])
        date = data.index
        print("date2 \n\n", data, date)
        plt1.plot(test_data.index,actual_prices,color = "black",label = f"Actual {company} Price", marker='.')
        plt1.plot(temp,predictions_prices,color = 'green' , label = f"Predicted {company} Price", marker='.')
        plt1.title(f"{company} Share Price")
        plt1.xlabel('Time')
        plt1.ylabel(f'{company} Share Price')
        plt1.legend()
        plt1.grid()
        plt1.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt1.gca().xaxis.set_major_locator(mdates.DayLocator(interval=20))

        plt1.gcf().autofmt_xdate()

        plt1.legend(['Org', 'Value', 'Pred'])

        return f1

    def pred1(self, data):
        date = data.index
        data = data.drop('Symbol', axis=1)
        data = data.drop('Series', axis=1)
        f2 = plt1.figure(figsize=(13, 4.5))
        plt1.plot(date, data['Volume'], marker='.')
        plt1.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt1.gca().xaxis.set_major_locator(mdates.DayLocator(interval=40))
        plt1.xlabel('Days')
        plt1.ylabel('Volume')
        plt1.grid()
        plt1.title("days vs volume")
        plt1.gcf().autofmt_xdate()
        return f2


if __name__ == "__main__":
    root = tk.Tk()

    # styling tab headers
    style = ttk.Style()
    style.configure('TNotebook.Tab', font=('URW Gothic L', '10', 'italic'), padding=[10, 10])
    tabControl = ttk.Notebook(root)

    # creating Tabs
    Home_t = ttk.Frame(tabControl)
    Trading = ttk.Frame(tabControl)
    tabControl.add(Home_t, text='Home')
    tabControl.add(Trading, text='Trade')

    tabControl.pack(expand=1, fill="both")

    St1 = Stock()
    St1.PageOneGui()

    root.mainloop()
