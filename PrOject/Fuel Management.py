from tkinter import*
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter.ttk import Treeview
from tkcalendar import *
import mysql.connector
'''
root = Tk()
root.geometry("900x550+200+70")
root.title("Fuel Management System Title Page")
root.iconbitmap(r"icon.ico")


def onclick(event):
    root.destroy()
'''
def main():

    def get_data_vehicle(ev):
        cursor_row = reg_vehicles_table.focus()
        contents = reg_vehicles_table.item(cursor_row)
        row = contents["values"]
        v_no.set(row[0])
        veh_fuel.set(row[1])

    def get_data_sale(ev):
        cursor_row = sale_report_table.focus()
        contents = sale_report_table.item(cursor_row)
        row = contents["values"]
        vehicle_no.set(row[0])
        sale_quantity.set(row[1])
        whom_concern.set(row[2])
        sl_fuel.set(row[3])
        sale_date.set(row[4])

    def get_data_pur(ev):
        cursor_row = purchase_report_table.focus()
        contents = purchase_report_table.item(cursor_row)
        row = contents["values"]
        outward_no.set(row[0])
        quantity.set(row[1])
        fuel.set(row[2])
        pur_date.set(row[3])

    def insert_vehicle():
        try:
            db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
            cur = db.cursor()
            cur.execute("INSERT INTO vehicle(v_no,fuel) VALUES ('%s','%s')" % (v_no.get(), veh_fuel.get()))
            db.commit()
            messagebox.showinfo("Successful", "Vehicle Added Successfully")
            clear_vehicle()
            db.close()
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Error", "Vehicle Number Already Exists \nTry new Number.")
        except TclError:
            messagebox.showerror("Error", "Entries Cannot be left blank \nPlease fill the all Entries.")

    def search_vehicles():
        try:
            db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
            cur = db.cursor()
            cur.execute("SELECT * FROM vehicle WHERE v_no='%s'" % (v_no.get()))
            rows = cur.fetchall()
            if len(rows) != 0:
                reg_vehicles_table.delete(*reg_vehicles_table.get_children())
                for row in rows:
                    reg_vehicles_table.insert('', END, values=row)
                db.commit()
                v_no.set("")
                messagebox.showinfo("Found", "Data Found Successfully!!!")
            db.close()
        except:
            messagebox.showerror("No Data", "No Such Data is Available!!!")

    def insert_sale():
        try:
            db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
            cur = db.cursor()
            cur.execute("INSERT INTO sale(v_no,quantity,w_concern,fuel,date) VALUES ('%s',%d,'%s','%s','%s')" %
                        (vehicle_no.get(), sale_quantity.get(), whom_concern.get(), sl_fuel.get(), sale_date.get()))
            if sl_fuel.get() == 'Diesel':
                cur.execute("SELECT fuel,SUM(quantity)-%d FROM stock WHERE fuel='Diesel'" % sale_quantity.get())
            elif sl_fuel.get() == 'Petrol':
                messagebox.showinfo("Hey", "Petrol")
            else:
                messagebox.showinfo("Hey", "Kjd")
            db.commit()
            clear_sale()
            messagebox.showinfo("Successful", "Fuel Sold Successfully")
            db.close()
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Error", "Vehicle is Not Registered \nPlease Add/Register First.")
        except TclError:
            messagebox.showerror("Error", "Entries Cannot be left blank \nPlease fill the all Entries.")

    def insert():
        try:
            db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
            cur = db.cursor()
            cur.execute("INSERT INTO purchase(out_no,quantity,fuel,date) VALUES (%d,%d,'%s','%s')" % (outward_no.get(),
                                                                                                      quantity.get(),
                                                                                                      fuel.get(),
                                                                                                      pur_date.get()))
            cur.execute("INSERT INTO stock(fuel,quantity) VALUES ('%s',%d)" % (fuel.get(), quantity.get()))
            db.commit()
            messagebox.showinfo("Successful", "Fuel Purchased Successfully")
            clear_purchase()
            db.close()
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Error", "Outward Number Already Exists \nTry Another Value.")
        except TclError:
            messagebox.showerror("Error", "Entries Cannot be left blank \nPlease fill the all Entries.")

    def update_data():
        db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
        cur = db.cursor()
        cur.execute("UPDATE purchase SET quantity=%d,fuel='%s',date='%s' WHERE out_no=%d " % (quantity.get(),
                                                                                              fuel.get(),
                                                                                              pur_date.get(),
                                                                                              outward_no.get()))
        db.commit()
        messagebox.showinfo("Updated", "Data Updated Successful")
        show_purchase()
        clear_purchase()
        db.close()

    def update_data_sale():
        db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
        cur = db.cursor()
        cur.execute("UPDATE sale SET quantity=%d,w_concern='%s',fuel='%s',date='%s'" % (sale_quantity.get(),
                                                                                        whom_concern.get(),
                                                                                        sl_fuel.get(), sale_date.get()))
        db.commit()
        messagebox.showinfo("Updated", "Data Updated Successful")
        show_sale()
        clear_sale()
        db.close()

    def search_sales():
        try:
            db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
            cur = db.cursor()
            cur.execute("SELECT * FROM sale WHERE v_no='%s'" % (vehicle_no.get()))
            rows = cur.fetchall()
            if len(rows) != 0:
                sale_report_table.delete(*sale_report_table.get_children())
                for row in rows:
                    sale_report_table.insert('', END, values=row)
                db.commit()
                vehicle_no.set("")
            db.close()
        except:
            messagebox.showerror("No Data", "No Such Data is Available")

    def update_data_vehicle():
        db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
        cur = db.cursor()
        cur.execute("UPDATE vehicle SET fuel='%s' WHERE v_no='%s'" % (veh_fuel.get(), v_no.get()))
        db.commit()
        messagebox.showinfo("Updated", "Data Updated Successful")
        show_vehicle()
        clear_vehicle()
        db.close()

    def search_purchases():
        try:
            db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
            cur = db.cursor()
            cur.execute("SELECT * FROM purchase WHERE out_no=%d" % (outward_no.get()))
            rows = cur.fetchall()
            if len(rows) != 0:
                purchase_report_table.delete(*purchase_report_table.get_children())
                for row in rows:
                    purchase_report_table.insert('', END, values=row)
                db.commit()
                messagebox.showerror("Data Found", "Data Found Successfully")
                outward_no.set("")
            db.close()
        except:
            messagebox.showerror("No Data", "No Such Data is Available")

    def delete_data():
        db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
        cur = db.cursor()
        cur.execute("DELETE FROM purchase WHERE out_no=%d" % (outward_no.get()))
        db.commit()
        messagebox.showinfo("Deleted", "Data Deleted Successful")
        show_purchase()
        clear_purchase()
        db.close()

    def delete_data_vehicle():
        db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
        cur = db.cursor()
        cur.execute("DELETE FROM vehicle WHERE v_no='%s'" % (v_no.get()))
        db.commit()
        messagebox.showinfo("Deleted", "Data Deleted Successful")
        show_vehicle()
        clear_vehicle()
        db.close()

    def delete_data_sale():
        db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
        cur = db.cursor()
        cur.execute("DELETE FROM sale WHERE v_no='%s'" % (vehicle_no.get()))
        db.commit()
        messagebox.showinfo("Deleted", "Data Deleted Successful")
        show_sale()
        clear_sale()
        db.close()

    def view_stockk():
        db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
        cur = db.cursor()
        cur.execute("SELECT(SELECT SUM(quantity) FROM stock WHERE fuel='Diesel'),"
                    "(SELECT SUM(quantity) FROM stock WHERE fuel='Petrol')")
        rows = cur.fetchall()
        if len(rows) != 0:
            stock_table.delete(*stock_table.get_children())
            for row in rows:
                stock_table.insert('', END, values=row)
            db.commit()
        db.close()

    def show_sale():
        db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
        cur = db.cursor()
        cur.execute("SELECT * FROM sale")
        rows = cur.fetchall()
        if len(rows) != 0:
            sale_report_table.delete(*sale_report_table.get_children())
            for row in rows:
                sale_report_table.insert('', END, values=row)
            db.commit()
        db.close()

    def show_vehicle():
        db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
        cur = db.cursor()
        cur.execute("SELECT * FROM vehicle")
        rows = cur.fetchall()
        if len(rows) != 0:
            reg_vehicles_table.delete(*reg_vehicles_table.get_children())
            for row in rows:
                reg_vehicles_table.insert('', END, values=row)
            db.commit()
        db.close()

    def show_purchase():
        db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
        cur = db.cursor()
        cur.execute("SELECT * FROM purchase")
        rows = cur.fetchall()
        if len(rows) != 0:
            purchase_report_table.delete(*purchase_report_table.get_children())
            for row in rows:
                purchase_report_table.insert('', END, values=row)
            db.commit()
        db.close()

    def view_stock():
        global stock_table

        def back_view_st():
            view_stock_frame.destroy()

        view_stock_frame = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50, text="Stock", font=("Arial", 15, "italic",
                                                                                               "bold"), bg="#202020",
                                      fg="white")
        view_stock_frame.place(x=315, y=106, width=885, height=595)

        stock_table = Treeview(view_stock_frame, columns=("diesel", "petrol"))
        stock_table.heading("diesel", text="Diesel")
        stock_table.heading("petrol", text="Petrol")
        stock_table["show"] = "headings"

        stock_table.column("diesel", width=100)
        stock_table.column("petrol", width=100)
        stock_table.place(x=0, y=0, width=775, height=525)
        view_st_b1 = Button(view_stock_frame, image=back, bg="#cccccc", command=back_view_st)
        view_st_b1.place(x=0, y=525)
        view_stockk()

    def sale_report():
        global sale_report_table

        def back_sale_report():
            sale_report_frame.destroy()

        sale_report_frame = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50, text="Sale Report", font=("Arial", 15,
                                                                                                      "italic", "bold"),

                                       bg="#202020", fg="white")
        sale_report_frame.place(x=315, y=106, width=885, height=595)

        scroll_x = Scrollbar(sale_report_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(sale_report_frame, orient=VERTICAL)
        sale_report_table = Treeview(sale_report_frame, columns=("vehicle_no", "quantity", "to_whom", "fuel_type",
                                                                 "date"), xscrollcommand=scroll_x,
                                     yscrollcommand=scroll_y)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=sale_report_table.xview)
        scroll_y.config(command=sale_report_table.yview)
        sale_report_table.heading("vehicle_no", text="Vehicle No")
        sale_report_table.heading("quantity", text="Quantity")
        sale_report_table.heading("to_whom", text="To Whom Concern")
        sale_report_table.heading("fuel_type", text="Fuel Type")
        sale_report_table.heading("date", text="Date")
        sale_report_table["show"] = "headings"

        sale_report_table.column("vehicle_no", width=50)
        sale_report_table.column("quantity", width=50)
        sale_report_table.column("to_whom", width=60)
        sale_report_table.column("fuel_type", width=50)
        sale_report_table.column("date", width=50)

        sale_report_table.place(x=0, y=0, width=750, height=542)
        show_sale()

        sale_report_b1 = Button(sale_report_frame, image=back, bg="#cccccc", command=back_sale_report)
        sale_report_b1.place(x=0, y=525)

    def purchase_report():
        global purchase_report_table

        def back_purchase_report():
            purchase_report_frame.destroy()

        purchase_report_frame = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50, text="Purchase Report", font=("Arial",
                                                                                                              15,
                                                                                                              "italic",
                                                                                                              "bold"),
                                           bg="#202020", fg="white")
        purchase_report_frame.place(x=315, y=106, width=885, height=595)

        scroll_x = Scrollbar(purchase_report_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(purchase_report_frame, orient=VERTICAL)
        purchase_report_table = Treeview(purchase_report_frame, columns=("outward_no", "quantity", "fuel_type", "date"),
                                         xscrollcommand=scroll_x, yscrollcommand=scroll_y)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=purchase_report_table.xview)
        scroll_y.config(command=purchase_report_table.yview)
        purchase_report_table.heading("outward_no", text="Outward No")
        purchase_report_table.heading("quantity", text="Quantity")
        purchase_report_table.heading("fuel_type", text="Fuel Type")
        purchase_report_table.heading("date", text="Date")
        purchase_report_table["show"] = "headings"

        purchase_report_table.column("outward_no", width=50)
        purchase_report_table.column("quantity", width=50)
        purchase_report_table.column("fuel_type", width=50)
        purchase_report_table.column("date", width=50)

        purchase_report_table.place(x=0, y=0, width=750, height=542)
        show_purchase()

        purchase_report_b1 = Button(purchase_report_frame, image=back, bg="#cccccc", command=back_purchase_report)
        purchase_report_b1.place(x=0, y=525)

    def reg_vehicles():
        global reg_vehicles_table

        def back_reg_vehicles():
            reg_vehicles_frame.destroy()

        reg_vehicles_frame = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50, text="Registered Vehicles", font=("Arial",
                                                                                                               15,
                                                                                                               "italic",
                                                                                                               "bold"),
                                        fg="white", bg="#202020")
        reg_vehicles_frame.place(x=315, y=106, width=885, height=595)

        scroll_x = Scrollbar(reg_vehicles_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(reg_vehicles_frame, orient=VERTICAL)
        reg_vehicles_table = Treeview(reg_vehicles_frame, columns=("vehicle_no", "fuel_type"))
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=reg_vehicles_table.xview)
        scroll_y.config(command=reg_vehicles_table.yview)
        reg_vehicles_table.heading("vehicle_no", text="Vehicle No")
        reg_vehicles_table.heading("fuel_type", text="Fuel Type")
        reg_vehicles_table["show"] = "headings"

        reg_vehicles_table.column("vehicle_no", width=60)
        reg_vehicles_table.column("fuel_type", width=60)

        reg_vehicles_table.place(x=0, y=0, width=750, height=542)
        show_vehicle()
        reg_vehicles_b1 = Button(reg_vehicles_frame, image=back, bg="#cccccc", command=back_reg_vehicles)
        reg_vehicles_b1.place(x=0, y=525)

    def home():
        def close_home():
            home_frame.destroy()

        home_frame = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50, bg="#202020", fg="white", font=("Arial", 15,
                                                                                                     "bold", "italic"),
                                text="Home")
        home_frame.place(x=315, y=106, width=885, height=595)

        home_background = Label(home_frame, image=all_frames_background)
        home_background.pack()

        b11 = Button(home_frame, image=home_stock, command=view_stock)
        b11.place(x=100, y=100)

        b22 = Button(home_frame, image=home_sale, command=sale_report)
        b22.place(x=300, y=100)

        b33 = Button(home_frame, image=home_purchase, command=purchase_report)
        b33.place(x=500, y=100)

        b66 = Button(home_frame, image=home_vehicle, command=reg_vehicles)
        b66.place(x=200, y=300)

        b77 = Button(home_frame, image=home_exit, command=close_home)
        b77.place(x=400, y=300)

    def close_main_win():
        win1.destroy()

    def clear_purchase():
        outward_no.set("")
        quantity.set("")
        cbox_f_type.set("Choose Fuel Type")
        pur_date.set("")

    def purchase_fuel():
        global cbox_f_type, date_entry

        def close_purchase():
            purchase_fuel_frame.destroy()

        purchase_fuel_frame = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50, bg="#202020", text="Purchase Fuel",
                                         font=("Arial", 15, "italic", "bold"), fg="white")
        purchase_fuel_frame.place(x=315, y=106, width=885, height=595)

        purchase_fuel_background = Label(purchase_fuel_frame, image=all_frames_background)
        purchase_fuel_background.pack()

        out_n = Label(purchase_fuel_frame, image=out_ward)
        out_n.place(x=50, y=30)

        purchase_lab_1 = Label(purchase_fuel_frame, image=quan_tity)
        purchase_lab_1.place(x=50, y=200)

        purchase_lab_2 = Label(purchase_fuel_frame, image=fuel_type)
        purchase_lab_2.place(x=420, y=30)

        purchase_lab_3 = Label(purchase_fuel_frame, image=date_)
        purchase_lab_3.place(x=420, y=200)

        out_n_entry = Entry(purchase_fuel_frame, textvariable=outward_no, font=("GUERRILLA", 15, "bold", "italic"),
                            bd=5, relief=SUNKEN, width=27)
        out_n_entry.place(x=48, y=130)

        purchase_entry_1 = Entry(purchase_fuel_frame, textvariable=quantity, font=("GUERRILLA", 15, "bold", "italic"),
                                 bd=5, relief=SUNKEN, width=27)
        purchase_entry_1.place(x=48, y=300)
        cbox_f_type = Combobox(purchase_fuel_frame, values=value3, width=18, textvariable=fuel, font=("GUERRILLA", 21,
                                                                                                      "bold", "italic"))
        cbox_f_type.set("Choose Fuel Type")
        cbox_f_type.place(x=418, y=130)

        date_entry = DateEntry(purchase_fuel_frame, textvariable=pur_date, font=("GUERRILLA", 15, "bold", "italic"),
                               bd=5, relief=SUNKEN, width=26)
        date_entry.place(x=418, y=300)

        purchase_btn_1 = Button(purchase_fuel_frame, image=pur_btn, command=insert)
        purchase_btn_1.place(x=10, y=450)

        purchase_btn_3 = Button(purchase_fuel_frame, image=clear_frames, command=clear_purchase)
        purchase_btn_3.place(x=260, y=450)

        purchase_btn_2 = Button(purchase_fuel_frame, image=close_frames, command=close_purchase)
        purchase_btn_2.place(x=500, y=450)

    def clear_sale():
        vehicle_no.set("")
        sale_quantity.set("")
        whom_concern.set("")
        cbox_f_type.set("Choose Fuel Type")
        sale_date.set("")

    def sale_fuel():
        global cbox_f_type, date_entry

        def close_sale():
            sale_fuel_frame.destroy()

        sale_fuel_frame = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50, bg="#202020", text="Sale Fuel",
                                     font=("Arial", 15, "italic", "bold"), fg="white")
        sale_fuel_frame.place(x=315, y=106, width=885, height=595)

        sale_fuel_background = Label(sale_fuel_frame, image=all_frames_background)
        sale_fuel_background.pack()

        sale_lab_2 = Label(sale_fuel_frame, image=vehicle_)
        sale_lab_2.place(x=50, y=10)

        sale_lab_3 = Label(sale_fuel_frame, image=quan_tity)
        sale_lab_3.place(x=240, y=330)

        sale_lab_4 = Label(sale_fuel_frame, image=whom_)
        sale_lab_4.place(x=420, y=10)

        sale_lab_5 = Label(sale_fuel_frame, image=fuel_type)
        sale_lab_5.place(x=420, y=180)

        sale_lab_6 = Label(sale_fuel_frame, image=date_)
        sale_lab_6.place(x=50, y=180)

        sale_entry_2 = Entry(sale_fuel_frame, textvariable=vehicle_no, font=("GUERRILLA", 15, "bold", "italic"), bd=5,
                             relief=SUNKEN, width=27)
        sale_entry_2.place(x=48, y=100)

        sale_entry_3 = Entry(sale_fuel_frame, textvariable=sale_quantity, font=("GUERRILLA", 15, "bold", "italic"),
                             bd=5, relief=SUNKEN, width=27)
        sale_entry_3.place(x=238, y=400)

        sale_entry_5 = Entry(sale_fuel_frame, textvariable=whom_concern, font=("GUERRILLA", 15, "bold", "italic"), bd=5,
                             relief=SUNKEN, width=27)
        sale_entry_5.place(x=418, y=100)

        cbox_f_type = Combobox(sale_fuel_frame, values=value3, width=18, font=("GUERRILLA", 21, "bold", "italic"),
                               textvariable=sl_fuel)
        cbox_f_type.set("Choose Fuel Type")
        cbox_f_type.place(x=418, y=270)

        date_entry_sale = DateEntry(sale_fuel_frame, textvariable=sale_date, font=("GUERRILLA", 21, "bold", "italic"),
                                    bd=5, relief=SUNKEN, width=18)
        date_entry_sale.place(x=48, y=270)

        sale_btn_1 = Button(sale_fuel_frame, image=sale_, command=insert_sale)
        sale_btn_1.place(x=5, y=470)

        sale_btn_2 = Button(sale_fuel_frame, image=clear_frames, command=clear_sale)
        sale_btn_2.place(x=255, y=470)

        sale_btn_3 = Button(sale_fuel_frame, image=close_frames, command=close_sale)
        sale_btn_3.place(x=505, y=470)

    def clear_vehicle():
        v_no.set("")
        cbox_fuel.set("Choose Fuel Type")

    def add_vehicle():
        global cbox_fuel

        def close_add_vehicle():
            add_vehicle_frame.destroy()

        add_vehicle_frame = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50, bg="#202020", text="Add Vehicle",
                                       font=("Arial", 15, "italic", "bold"), fg="white")
        add_vehicle_frame.place(x=315, y=106, width=885, height=595)

        add_vehicle_background = Label(add_vehicle_frame, image=all_frames_background)
        add_vehicle_background.pack()

        vehicle_lab_1 = Label(add_vehicle_frame, image=vehicle_)
        vehicle_lab_1.place(x=50, y=150)

        vehicle_lab_3 = Label(add_vehicle_frame, image=fuel_type)
        vehicle_lab_3.place(x=420, y=150)

        vehicle_entry_1 = Entry(add_vehicle_frame, textvariable=v_no, font=("GUERRILLA", 15, "bold", "italic"), bd=5,
                                relief=SUNKEN, width=27)
        vehicle_entry_1.place(x=48, y=250)

        cbox_fuel = Combobox(add_vehicle_frame, value=value3, width=18, font=("GUERRILLA", 21, "bold", "italic"),
                             textvariable=veh_fuel)
        cbox_fuel.set("Choose Fuel Type")
        cbox_fuel.place(x=418, y=250)

        add_v_btn1 = Button(add_vehicle_frame, image=add, command=insert_vehicle)
        add_v_btn1.place(x=5, y=400)

        add_v_btn3 = Button(add_vehicle_frame, image=clear_frames, command=clear_vehicle)
        add_v_btn3.place(x=255, y=400)

        add_v_btn2 = Button(add_vehicle_frame, image=close_frames, command=close_add_vehicle)
        add_v_btn2.place(x=505, y=400)

    def update():
        def update_sale_record():
            global cbox_f_type, date_entry
            global sale_report_table

            def close_sale_update():
                update_sale_record_frame_2.destroy()

            update_sale_record_frame_2 = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50, bg="#202020",
                                                    text="Update Sale Record", font=("Arial", 15, "italic", "bold"),
                                                    fg="white")
            update_sale_record_frame_2.place(x=315, y=106, width=885, height=595)

            update_sale_back = Label(update_sale_record_frame_2, image=frame_background_image)
            update_sale_back.place(x=0, y=0)

            update_sale_lab_1 = Label(update_sale_record_frame_2, image=vehicle_)
            update_sale_lab_1.place(x=5, y=0)

            update_sale_lab_2 = Label(update_sale_record_frame_2, image=quan_tity)
            update_sale_lab_2.place(x=5, y=100)

            update_sale_lab_3 = Label(update_sale_record_frame_2, image=whom_)
            update_sale_lab_3.place(x=5, y=200)

            update_sale_lab_4 = Label(update_sale_record_frame_2, image=fuel_type)
            update_sale_lab_4.place(x=400, y=30)

            update_sale_lab_5 = Label(update_sale_record_frame_2, image=date_)
            update_sale_lab_5.place(x=400, y=180)

            update_sale_entry_1 = Entry(update_sale_record_frame_2, textvariable=vehicle_no, font=("GUERRILLA", 15,
                                                                                                   "bold", "italic"),
                                        bd=5, relief=SUNKEN, width=27)
            update_sale_entry_1.place(x=0, y=60)

            update_sale_entry_2 = Entry(update_sale_record_frame_2, textvariable=sale_quantity, font=("GUERRILLA", 15,
                                                                                                      "bold", "italic"),
                                        bd=5, relief=SUNKEN, width=27)
            update_sale_entry_2.place(x=0, y=160)

            update_sale_entry_3 = Entry(update_sale_record_frame_2, textvariable=whom_concern, font=("GUERRILLA", 15,
                                                                                                     "bold", "italic"),
                                        bd=5, relief=SUNKEN, width=27)
            update_sale_entry_3.place(x=0, y=260)

            cbox_f_type = Combobox(update_sale_record_frame_2, values=value3, width=18, textvariable=sl_fuel,
                                   font=("GUERRILLA", 21, "bold", "italic"))
            cbox_f_type.set("Choose Fuel Type")
            cbox_f_type.place(x=398, y=100)

            date_entry_sale = DateEntry(update_sale_record_frame_2, textvariable=sale_date, font=("GUERRILLA", 15,
                                                                                                  "bold", "italic"),
                                        bd=5, relief=SUNKEN, width=26)
            date_entry_sale.place(x=398, y=250)

            update_sale_btn_1 = Button(update_sale_record_frame_2, image=update_, command=update_data_sale)
            update_sale_btn_1.place(x=0, y=300)

            update_sale_btn_2 = Button(update_sale_record_frame_2, image=clear_frames, command=clear_sale)
            update_sale_btn_2.place(x=250, y=300)

            update_sale_btn_3 = Button(update_sale_record_frame_2, image=close_frames, command=close_sale_update)
            update_sale_btn_3.place(x=500, y=300)

            scroll_x = Scrollbar(update_sale_record_frame_2, orient=HORIZONTAL)
            scroll_y = Scrollbar(update_sale_record_frame_2, orient=VERTICAL)
            sale_report_table = Treeview(update_sale_record_frame_2, columns=("vehicle_no", "quantity", "to_whom",
                                                                              "fuel_type", "date"),
                                         xscrollcommand=scroll_x, yscrollcommand=scroll_y)
            scroll_x.pack(side=BOTTOM, fill=X)
            scroll_y.pack(side=RIGHT, fill=Y)
            scroll_x.config(command=sale_report_table.xview)
            scroll_y.config(command=sale_report_table.yview)
            sale_report_table.heading("vehicle_no", text="Vehicle No")
            sale_report_table.heading("quantity", text="Quantity")
            sale_report_table.heading("to_whom", text="To Whom Concern")
            sale_report_table.heading("fuel_type", text="Fuel Type")
            sale_report_table.heading("date", text="Date")
            sale_report_table["show"] = "headings"

            sale_report_table.column("vehicle_no", width=50)
            sale_report_table.column("quantity", width=50)
            sale_report_table.column("to_whom", width=60)
            sale_report_table.column("fuel_type", width=50)
            sale_report_table.column("date", width=50)

            sale_report_table.place(x=0, y=360, width=748, height=185)
            sale_report_table.bind("<ButtonRelease-1>", get_data_sale)
            show_sale()
            clear_sale()

        def update_vehicle_record():
            global cbox_fuel
            global reg_vehicles_table

            def close_veh_update():
                update_veh_record_frame_2.destroy()

            update_veh_record_frame_2 = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50, text="Update Vehicle",
                                                   font=("Arial", 15, "italic", "bold"), fg="white", bg="#202020")
            update_veh_record_frame_2.place(x=315, y=106, width=885, height=595)

            update_veh_back = Label(update_veh_record_frame_2, image=frame_background_image)
            update_veh_back.place(x=0, y=0)

            update_vehicle_lab_1 = Label(update_veh_record_frame_2, image=vehicle_)
            update_vehicle_lab_1.place(x=30, y=10)

            update_vehicle_lab_3 = Label(update_veh_record_frame_2, image=fuel_type)
            update_vehicle_lab_3.place(x=420, y=10)

            update_vehicle_entry_1 = Entry(update_veh_record_frame_2, textvariable=v_no, font=("GUERRILLA", 15, "bold",
                                                                                               "italic"), bd=5,
                                           relief=SUNKEN, width=27)
            update_vehicle_entry_1.place(x=28, y=100)

            cbox_fuel = Combobox(update_veh_record_frame_2, value=value3, width=18, textvariable=veh_fuel,
                                 font=("GUERRILLA", 21, "bold", "italic"))
            cbox_fuel.set("Choose Fuel Type")
            cbox_fuel.place(x=418, y=100)

            update_vehicle_btn_1 = Button(update_veh_record_frame_2, image=update_, command=update_data_vehicle)
            update_vehicle_btn_1.place(x=0, y=150)

            update_vehicle_btn_2 = Button(update_veh_record_frame_2, image=clear_frames, command=clear_vehicle)
            update_vehicle_btn_2.place(x=250, y=150)

            update_vehicle_btn_3 = Button(update_veh_record_frame_2, image=close_frames, command=close_veh_update)
            update_vehicle_btn_3.place(x=500, y=150)

            scroll_x = Scrollbar(update_veh_record_frame_2, orient=HORIZONTAL)
            scroll_y = Scrollbar(update_veh_record_frame_2, orient=VERTICAL)
            reg_vehicles_table = Treeview(update_veh_record_frame_2, columns=("vehicle_no", "fuel_type"))
            scroll_x.pack(side=BOTTOM, fill=X)
            scroll_y.pack(side=RIGHT, fill=Y)
            scroll_x.config(command=reg_vehicles_table.xview)
            scroll_y.config(command=reg_vehicles_table.yview)
            reg_vehicles_table.heading("vehicle_no", text="Vehicle No")
            reg_vehicles_table.heading("fuel_type", text="Fuel Type")
            reg_vehicles_table["show"] = "headings"

            reg_vehicles_table.column("vehicle_no", width=60)
            reg_vehicles_table.column("fuel_type", width=60)

            reg_vehicles_table.place(x=0, y=210, width=748, height=335)
            reg_vehicles_table.bind("<ButtonRelease-1>", get_data_vehicle)
            show_vehicle()
            clear_vehicle()

        def update_pur_record():
            global cbox_f_type, date_entry
            global purchase_report_table

            def close_pur_updates():
                update_pur_record_frame_2.destroy()

            update_pur_record_frame_2 = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50, text="Update Purchase Record",
                                                   font=("Arial", 15, "bold", "italic"), bg="#202020", fg="white")
            update_pur_record_frame_2.place(x=315, y=106, width=885, height=595)

            update_pur_back = Label(update_pur_record_frame_2, image=frame_background_image)
            update_pur_back.place(x=0, y=0)

            update_purchase_lab_1 = Label(update_pur_record_frame_2, image=out_ward)
            update_purchase_lab_1.place(x=30, y=10)

            update_purchase_lab_2 = Label(update_pur_record_frame_2, image=quan_tity)
            update_purchase_lab_2.place(x=420, y=10)

            update_purchase_lab_3 = Label(update_pur_record_frame_2, image=fuel_type)
            update_purchase_lab_3.place(x=30, y=130)

            update_purchase_lab_4 = Label(update_pur_record_frame_2, image=date_)
            update_purchase_lab_4.place(x=420, y=130)

            update_purchase_entry_1 = Entry(update_pur_record_frame_2, font=("GUERRILLA", 15, "bold", "italic"), bd=5,
                                            relief=SUNKEN, textvariable=outward_no, width=27)
            update_purchase_entry_1.place(x=28, y=80)

            update_purchase_entry_2 = Entry(update_pur_record_frame_2, font=("GUERRILLA", 15, "bold", "italic"), bd=5,
                                            relief=SUNKEN, textvariable=quantity, width=27)
            update_purchase_entry_2.place(x=418, y=80)

            cbox_f_type = Combobox(update_pur_record_frame_2, values=value3, width=26, font=("GUERRILLA", 15, "bold",
                                                                                             "italic"),
                                   textvariable=fuel)
            cbox_f_type.set("Choose Fuel Type")
            cbox_f_type.place(x=28, y=200)

            date_entry = DateEntry(update_pur_record_frame_2, textvariable=pur_date, font=("GUERRILLA", 15, "bold",
                                                                                           "italic"), bd=5,
                                   relief=SUNKEN, width=26)
            date_entry.place(x=418, y=200)

            update_purchase_btn_1 = Button(update_pur_record_frame_2, image=update_, command=update_data)
            update_purchase_btn_1.place(x=0, y=260)

            update_purchase_btn_2 = Button(update_pur_record_frame_2, image=clear_frames, command=clear_purchase)
            update_purchase_btn_2.place(x=250, y=260)

            update_purchase_btn_3 = Button(update_pur_record_frame_2, image=close_frames, command=close_pur_updates)
            update_purchase_btn_3.place(x=500, y=260)

            scroll_x = Scrollbar(update_pur_record_frame_2, orient=HORIZONTAL)
            scroll_y = Scrollbar(update_pur_record_frame_2, orient=VERTICAL)
            purchase_report_table = Treeview(update_pur_record_frame_2, columns=("outward_no", "quantity", "fuel_type",
                                                                                 "date"), xscrollcommand=scroll_x,
                                             yscrollcommand=scroll_y)
            scroll_x.pack(side=BOTTOM, fill=X)
            scroll_y.pack(side=RIGHT, fill=Y)
            scroll_x.config(command=purchase_report_table.xview)
            scroll_y.config(command=purchase_report_table.yview)
            purchase_report_table.heading("outward_no", text="Outward No")
            purchase_report_table.heading("quantity", text="Quantity")
            purchase_report_table.heading("fuel_type", text="Fuel Type")
            purchase_report_table.heading("date", text="Date")
            purchase_report_table["show"] = "headings"

            purchase_report_table.column("outward_no", width=50)
            purchase_report_table.column("quantity", width=50)
            purchase_report_table.column("fuel_type", width=50)
            purchase_report_table.column("date", width=50)
            purchase_report_table.place(x=0, y=330, width=748, height=215)
            purchase_report_table.bind("<ButtonRelease-1>", get_data_pur)
            show_purchase()
            clear_purchase()

        def close_update():
            update_frame.destroy()

        update_frame = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50, font=("Algerian", 15, "italic"),
                                  text="Update Records", fg="white", bg="#202020")
        update_frame.place(x=315, y=106, width=885, height=595)

        update_back = Label(update_frame, image=all_frames_background)
        update_back.pack()

        update_pur = Button(update_frame, image=update_purchase, command=update_pur_record)
        update_pur.place(x=150, y=100)

        update_sl = Button(update_frame, image=update_sale, command=update_sale_record)
        update_sl.place(x=400, y=100)

        update_v = Button(update_frame, image=update_vehicle, command=update_vehicle_record)
        update_v.place(x=150, y=300)

        update_ex = Button(update_frame, image=home_exit, command=close_update)
        update_ex.place(x=400, y=300)

    def delete():

        def delete_vehicle():
            global cbox_fuel
            global reg_vehicles_table

            def close_veh_delete():
                delete_veh_record_frame_2.destroy()

            delete_veh_record_frame_2 = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50, text="Delete Vehicle",
                                                   font=("Arial", 15, "bold", "italic"), bg="#202020", fg="white")
            delete_veh_record_frame_2.place(x=315, y=106, width=885, height=595)

            delete_veh_back = Label(delete_veh_record_frame_2, image=frame_background_image)
            delete_veh_back.place(x=0, y=0)

            delete_vehicle_lab_1 = Label(delete_veh_record_frame_2, image=vehicle_)
            delete_vehicle_lab_1.place(x=30, y=10)

            delete_vehicle_lab_3 = Label(delete_veh_record_frame_2, image=fuel_type)
            delete_vehicle_lab_3.place(x=420, y=10)

            delete_vehicle_entry_1 = Entry(delete_veh_record_frame_2, textvariable=v_no, font=("GUERRILLA", 15, "bold",
                                                                                               "italic"), bd=5,
                                           relief=SUNKEN, width=27)
            delete_vehicle_entry_1.place(x=28, y=100)

            cbox_fuel = Combobox(delete_veh_record_frame_2, value=value3, width=18, font=("GUERRILLA", 21, "bold",
                                                                                          "italic"),
                                 textvariable=veh_fuel)
            cbox_fuel.set("Choose Fuel Type")
            cbox_fuel.place(x=418, y=100)

            delete_vehicle_btn_1 = Button(delete_veh_record_frame_2, image=delete_, command=delete_data_vehicle)
            delete_vehicle_btn_1.place(x=0, y=150)

            delete_vehicle_btn_2 = Button(delete_veh_record_frame_2, image=clear_frames, command=clear_vehicle)
            delete_vehicle_btn_2.place(x=250, y=150)

            delete_vehicle_btn_3 = Button(delete_veh_record_frame_2, image=close_frames, command=close_veh_delete)
            delete_vehicle_btn_3.place(x=500, y=150)

            scroll_x = Scrollbar(delete_veh_record_frame_2, orient=HORIZONTAL)
            scroll_y = Scrollbar(delete_veh_record_frame_2, orient=VERTICAL)
            reg_vehicles_table = Treeview(delete_veh_record_frame_2, columns=("vehicle_no", "fuel_type"))
            scroll_x.pack(side=BOTTOM, fill=X)
            scroll_y.pack(side=RIGHT, fill=Y)
            scroll_x.config(command=reg_vehicles_table.xview)
            scroll_y.config(command=reg_vehicles_table.yview)
            reg_vehicles_table.heading("vehicle_no", text="Vehicle No")
            reg_vehicles_table.heading("fuel_type", text="Fuel Type")
            reg_vehicles_table["show"] = "headings"

            reg_vehicles_table.column("vehicle_no", width=60)
            reg_vehicles_table.column("fuel_type", width=60)

            reg_vehicles_table.place(x=0, y=210, width=748, height=335)
            reg_vehicles_table.bind("<ButtonRelease-1>", get_data_vehicle)
            show_vehicle()
            clear_vehicle()

        def delete_pur_record():
            global cbox_f_type, date_entry
            global purchase_report_table

            def close_delete_pur():
                delete_pur_record_frame_2.destroy()

            delete_pur_record_frame_2 = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50, text="Delete Purchase Record",
                                                   font=("Arial", 15, "italic", "bold"), bg="#202020", fg="white")
            delete_pur_record_frame_2.place(x=315, y=106, width=885, height=595)

            delete_pur_back = Label(delete_pur_record_frame_2, image=frame_background_image)
            delete_pur_back.place(x=0, y=0)

            delete_purchase_lab_1 = Label(delete_pur_record_frame_2, image=out_ward)
            delete_purchase_lab_1.place(x=30, y=10)

            delete_purchase_lab_2 = Label(delete_pur_record_frame_2, image=quan_tity)
            delete_purchase_lab_2.place(x=420, y=10)

            delete_purchase_lab_3 = Label(delete_pur_record_frame_2, image=fuel_type)
            delete_purchase_lab_3.place(x=30, y=130)

            delete_purchase_lab_4 = Label(delete_pur_record_frame_2, image=date_)
            delete_purchase_lab_4.place(x=420, y=130)

            delete_purchase_entry_1 = Entry(delete_pur_record_frame_2, font=("GUERRILLA", 15, "bold", "italic"), bd=5,
                                            relief=SUNKEN, textvariable=outward_no, width=27)
            delete_purchase_entry_1.place(x=28, y=80)

            delete_purchase_entry_2 = Entry(delete_pur_record_frame_2, font=("GUERRILLA", 15, "bold", "italic"), bd=5,
                                            relief=SUNKEN, textvariable=quantity, width=27)
            delete_purchase_entry_2.place(x=418, y=80)

            cbox_f_type = Combobox(delete_pur_record_frame_2, values=value3, width=26, font=("GUERRILLA", 15, "bold",
                                                                                             "italic"),
                                   textvariable=fuel)
            cbox_f_type.set("Choose Fuel Type")
            cbox_f_type.place(x=28, y=200)

            date_entry = DateEntry(delete_pur_record_frame_2, textvariable=pur_date, font=("GUERRILLA", 15, "bold",
                                                                                           "italic"), bd=5,
                                   relief=SUNKEN, width=26)
            date_entry.place(x=418, y=200)

            delete_purchase_btn_1 = Button(delete_pur_record_frame_2, image=delete_, command=delete_data)
            delete_purchase_btn_1.place(x=0, y=260)

            delete_purchase_btn_2 = Button(delete_pur_record_frame_2, image=clear_frames, command=clear_purchase)
            delete_purchase_btn_2.place(x=250, y=260)

            delete_purchase_btn_3 = Button(delete_pur_record_frame_2, image=close_frames, command=close_delete_pur)
            delete_purchase_btn_3.place(x=500, y=260)

            scroll_x = Scrollbar(delete_pur_record_frame_2, orient=HORIZONTAL)
            scroll_y = Scrollbar(delete_pur_record_frame_2, orient=VERTICAL)
            purchase_report_table = Treeview(delete_pur_record_frame_2, columns=("outward_no", "quantity", "fuel_type",
                                                                                 "date"), xscrollcommand=scroll_x,
                                             yscrollcommand=scroll_y)
            scroll_x.pack(side=BOTTOM, fill=X)
            scroll_y.pack(side=RIGHT, fill=Y)
            scroll_x.config(command=purchase_report_table.xview)
            scroll_y.config(command=purchase_report_table.yview)

            purchase_report_table.heading("outward_no", text="Outward No")
            purchase_report_table.heading("quantity", text="Quantity")
            purchase_report_table.heading("fuel_type", text="Fuel Type")
            purchase_report_table.heading("date", text="Date")
            purchase_report_table["show"] = "headings"

            purchase_report_table.column("outward_no", width=50)
            purchase_report_table.column("quantity", width=50)
            purchase_report_table.column("fuel_type", width=50)
            purchase_report_table.column("date", width=50)

            purchase_report_table.place(x=0, y=330, width=748, height=215)
            purchase_report_table.bind("<ButtonRelease-1>", get_data_pur)
            show_purchase()
            clear_purchase()

        def delete_sale_record():
            global cbox_f_type, date_entry
            global sale_report_table

            def close_delete_sale():
                delete_sale_record_frame_2.destroy()

            delete_sale_record_frame_2 = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50, text="Delete Sale Record",
                                                    font=("Arial", 15, "italic", "bold"), bg="#202020", fg="white")
            delete_sale_record_frame_2.place(x=315, y=103, width=885, height=595)

            delete_sale_back = Label(delete_sale_record_frame_2, image=frame_background_image)
            delete_sale_back.place(x=0, y=0)

            delete_sale_lab_1 = Label(delete_sale_record_frame_2, image=vehicle_)
            delete_sale_lab_1.place(x=5, y=0)

            delete_sale_lab_2 = Label(delete_sale_record_frame_2, image=quan_tity)
            delete_sale_lab_2.place(x=5, y=100)

            delete_sale_lab_3 = Label(delete_sale_record_frame_2, image=whom_)
            delete_sale_lab_3.place(x=5, y=200)

            delete_sale_lab_4 = Label(delete_sale_record_frame_2, image=fuel_type)
            delete_sale_lab_4.place(x=400, y=30)

            delete_sale_lab_5 = Label(delete_sale_record_frame_2, image=date_)
            delete_sale_lab_5.place(x=400, y=180)

            delete_sale_entry_1 = Entry(delete_sale_record_frame_2, textvariable=vehicle_no, font=("GUERRILLA", 15,
                                                                                                   "bold", "italic"),
                                        bd=5, relief=SUNKEN, width=27)
            delete_sale_entry_1.place(x=0, y=60)

            delete_sale_entry_2 = Entry(delete_sale_record_frame_2, textvariable=sale_quantity, font=("GUERRILLA", 15,
                                                                                                      "bold", "italic"),
                                        bd=5, relief=SUNKEN, width=27)
            delete_sale_entry_2.place(x=0, y=160)

            delete_sale_entry_3 = Entry(delete_sale_record_frame_2, textvariable=whom_concern, font=("GUERRILLA", 15,
                                                                                                     "bold", "italic"),
                                        bd=5, relief=SUNKEN, width=27)
            delete_sale_entry_3.place(x=0, y=260)

            cbox_f_type = Combobox(delete_sale_record_frame_2, values=value3, width=18, textvariable=sl_fuel,
                                   font=("GUERRILLA", 21, "bold", "italic"))
            cbox_f_type.set("Choose Fuel Type")
            cbox_f_type.place(x=398, y=100)

            date_entry = DateEntry(delete_sale_record_frame_2, textvariable=sale_date, font=("GUERRILLA", 15, "bold",
                                                                                             "italic"), bd=5,
                                   relief=SUNKEN, width=26)
            date_entry.place(x=398, y=250)

            delete_sale_btn_1 = Button(delete_sale_record_frame_2, image=delete_, command=delete_data_sale)
            delete_sale_btn_1.place(x=0, y=300)

            delete_sale_btn_2 = Button(delete_sale_record_frame_2, image=clear_frames, command=clear_sale)
            delete_sale_btn_2.place(x=250, y=300)

            delete_sale_btn_3 = Button(delete_sale_record_frame_2, image=close_frames, command=close_delete_sale)
            delete_sale_btn_3.place(x=500, y=300)

            scroll_x = Scrollbar(delete_sale_record_frame_2, orient=HORIZONTAL)
            scroll_y = Scrollbar(delete_sale_record_frame_2, orient=VERTICAL)
            sale_report_table = Treeview(delete_sale_record_frame_2, columns=("vehicle_no", "quantity", "to_whom",
                                                                              "fuel_type", "date"),
                                         xscrollcommand=scroll_x, yscrollcommand=scroll_y)
            scroll_x.pack(side=BOTTOM, fill=X)
            scroll_y.pack(side=RIGHT, fill=Y)
            scroll_x.config(command=sale_report_table.xview)
            scroll_y.config(command=sale_report_table.yview)
            sale_report_table.heading("vehicle_no", text="Vehicle No")
            sale_report_table.heading("quantity", text="Quantity")
            sale_report_table.heading("fuel_type", text="Fuel Type")
            sale_report_table.heading("to_whom", text="To Whom Concern")
            sale_report_table.heading("date", text="Date")
            sale_report_table["show"] = "headings"

            sale_report_table.column("vehicle_no", width=50)
            sale_report_table.column("quantity", width=50)
            sale_report_table.column("fuel_type", width=50)
            sale_report_table.column("to_whom", width=60)
            sale_report_table.column("date", width=50)

            sale_report_table.place(x=0, y=360, width=748, height=185)
            sale_report_table.bind("<ButtonRelease-1>", get_data_sale)
            show_sale()
            clear_sale()

        def close_delete():
            delete_frame.destroy()
        delete_frame = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50, font=("Algerian", 15, "italic"),
                                  text="Delete Record", bg="#202020", fg="white")
        delete_frame.place(x=315, y=106, width=885, height=595)

        delete_back = Label(delete_frame, image=all_frames_background)
        delete_back.pack()

        delete_pur = Button(delete_frame, image=delete_purchase, command=delete_pur_record)
        delete_pur.place(x=150, y=100)

        delete_sl = Button(delete_frame, image=delete_sale, command=delete_sale_record)
        delete_sl.place(x=400, y=100)

        delete_v = Button(delete_frame, image=delete_veh, command=delete_vehicle)
        delete_v.place(x=150, y=300)

        delete_ex = Button(delete_frame, image=home_exit, command=close_delete)
        delete_ex.place(x=400, y=300)

    def search_rec():
        def close_search_rec():
            search_frame.destroy()

        def search_pur():
            global purchase_report_table

            def close_search_pur():
                search_pur_record_frame_2.destroy()

            search_pur_record_frame_2 = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50,
                                                   text="Search From Purchase Record", font=("Arial", 15, "italic",
                                                                                             "bold"), bg="#202020",
                                                   fg="white")
            search_pur_record_frame_2.place(x=315, y=106, width=885, height=595)

            search_pur_back = Label(search_pur_record_frame_2, image=frame_background_image)
            search_pur_back.place(x=0, y=0)

            search_pur_lab_1 = Label(search_pur_record_frame_2, image=out_ward)
            search_pur_lab_1.place(x=230, y=30)

            search_pur_entry_1 = Entry(search_pur_record_frame_2, font=("GUERRILLA", 15, "bold", "italic"), bd=5,
                                       relief=SUNKEN, width=27, textvariable=outward_no)
            search_pur_entry_1.place(x=228, y=110)

            search_purchase_btn_1 = Button(search_pur_record_frame_2, image=sear, command=search_purchases)
            search_purchase_btn_1.place(x=120, y=180)

            search_purchase_btn_2 = Button(search_pur_record_frame_2, image=close_frames, command=close_search_pur)
            search_purchase_btn_2.place(x=400, y=180)

            scroll_x = Scrollbar(search_pur_record_frame_2, orient=HORIZONTAL)
            scroll_y = Scrollbar(search_pur_record_frame_2, orient=VERTICAL)
            purchase_report_table = Treeview(search_pur_record_frame_2, columns=("outward_no", "quantity", "fuel_type",
                                                                                 "date"), xscrollcommand=scroll_x,
                                             yscrollcommand=scroll_y)
            scroll_x.pack(side=BOTTOM, fill=X)
            scroll_y.pack(side=RIGHT, fill=Y)
            scroll_x.config(command=purchase_report_table.xview)
            scroll_y.config(command=purchase_report_table.yview)
            purchase_report_table.heading("outward_no", text="Outward No")
            purchase_report_table.heading("quantity", text="Quantity")
            purchase_report_table.heading("fuel_type", text="Fuel Type")
            purchase_report_table.heading("date", text="Date")
            purchase_report_table["show"] = "headings"

            purchase_report_table.column("outward_no", width=50)
            purchase_report_table.column("quantity", width=50)
            purchase_report_table.column("fuel_type", width=50)
            purchase_report_table.column("date", width=50)

            purchase_report_table.place(x=0, y=265, width=748, height=280)

        def search_sale():
            global sale_report_table

            def close_search_sale():
                search_sale_record_frame_2.destroy()

            search_sale_record_frame_2 = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50, text="Search From Sale Record",
                                                    font=("Arial", 15, "italic", "bold"), bg="#202020", fg="white")
            search_sale_record_frame_2.place(x=315, y=106, width=885, height=592)

            search_background_image = Label(search_sale_record_frame_2, image=frame_background_image)
            search_background_image.place(x=0, y=0)

            search_sale_lab_1 = Label(search_sale_record_frame_2, image=vehicle_)
            search_sale_lab_1.place(x=230, y=30)

            search_sale_entry_1 = Entry(search_sale_record_frame_2, font=("GUERRILLA", 15, "bold", "italic"), bd=5,
                                        relief=SUNKEN, width=27, textvariable=vehicle_no)
            search_sale_entry_1.place(x=228, y=110)

            search_sale_btn_1 = Button(search_sale_record_frame_2, image=sear, command=search_sales)
            search_sale_btn_1.place(x=120, y=180)

            search_sale_btn_2 = Button(search_sale_record_frame_2, image=close_frames, command=close_search_sale)
            search_sale_btn_2.place(x=400, y=180)

            scroll_x = Scrollbar(search_sale_record_frame_2, orient=HORIZONTAL)
            scroll_y = Scrollbar(search_sale_record_frame_2, orient=VERTICAL)
            sale_report_table = Treeview(search_sale_record_frame_2, columns=("vehicle_no", "quantity", "to_whom",
                                                                              "fuel_type", "date"),
                                         xscrollcommand=scroll_x, yscrollcommand=scroll_y)
            scroll_x.pack(side=BOTTOM, fill=X)
            scroll_y.pack(side=RIGHT, fill=Y)
            scroll_x.config(command=sale_report_table.xview)
            scroll_y.config(command=sale_report_table.yview)
            sale_report_table.heading("vehicle_no", text="Vehicle No")
            sale_report_table.heading("quantity", text="Quantity")
            sale_report_table.heading("fuel_type", text="Fuel Type")
            sale_report_table.heading("to_whom", text="To Whom Concern")
            sale_report_table.heading("date", text="Date")
            sale_report_table["show"] = "headings"

            sale_report_table.column("vehicle_no", width=50)
            sale_report_table.column("quantity", width=50)
            sale_report_table.column("fuel_type", width=50)
            sale_report_table.column("to_whom", width=60)
            sale_report_table.column("date", width=50)

            sale_report_table.place(x=0, y=265, width=748, height=280)

        def search_vehicle():
            global reg_vehicles_table

            def close_search_vehicle():
                search_vehicle_record_frame_2.destroy()

            search_vehicle_record_frame_2 = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50,
                                                       text="Search From Vehicles Record", font=("Arial", 15, "bold",
                                                                                                 "italic"),
                                                       bg="#202020", fg="white")
            search_vehicle_record_frame_2.place(x=315, y=106, width=885, height=595)

            search_vehicle_back = Label(search_vehicle_record_frame_2, image=frame_background_image)
            search_vehicle_back.place(x=0, y=0)

            search_vehicle_lab_1 = Label(search_vehicle_record_frame_2, image=vehicle_)
            search_vehicle_lab_1.place(x=230, y=30)

            search_vehicle_entry_1 = Entry(search_vehicle_record_frame_2, font=("GUERRILLA", 15, "bold", "italic"),
                                           bd=5, relief=SUNKEN, width=27, textvariable=v_no)
            search_vehicle_entry_1.place(x=228, y=110)

            search_vehicle_btn_1 = Button(search_vehicle_record_frame_2, image=sear, command=search_vehicles)
            search_vehicle_btn_1.place(x=120, y=180)

            search_vehicle_btn_2 = Button(search_vehicle_record_frame_2, image=close_frames,
                                          command=close_search_vehicle)
            search_vehicle_btn_2.place(x=400, y=180)

            scroll_x = Scrollbar(search_vehicle_record_frame_2, orient=HORIZONTAL)
            scroll_y = Scrollbar(search_vehicle_record_frame_2, orient=VERTICAL)
            reg_vehicles_table = Treeview(search_vehicle_record_frame_2, columns=("vehicle_no", "fuel_type"))
            scroll_x.pack(side=BOTTOM, fill=X)
            scroll_y.pack(side=RIGHT, fill=Y)
            scroll_x.config(command=reg_vehicles_table.xview)
            scroll_y.config(command=reg_vehicles_table.yview)
            reg_vehicles_table.heading("vehicle_no", text="Vehicle No")
            reg_vehicles_table.heading("fuel_type", text="Fuel Type")
            reg_vehicles_table["show"] = "headings"

            reg_vehicles_table.column("vehicle_no", width=60)
            reg_vehicles_table.column("fuel_type", width=60)

            reg_vehicles_table.place(x=0, y=265, width=748, height=280)

        search_frame = LabelFrame(win1, bd=10, relief=SUNKEN, padx=50, font=("Algerian", 15, "italic"),
                                  text="Search Records", bg="#202020", fg="white")
        search_frame.place(x=315, y=106, width=885, height=592)

        search_back = Label(search_frame, image=all_frames_background)
        search_back.pack()

        search_pur = Button(search_frame, image=sear_pur, command=search_pur)
        search_pur.place(x=150, y=100)

        search_sl = Button(search_frame, image=sear_sale, command=search_sale)
        search_sl.place(x=400, y=100)

        search_v = Button(search_frame, image=sear_veh, command=search_vehicle)
        search_v.place(x=150, y=300)

        search_ex = Button(search_frame, image=home_exit, command=close_search_rec)
        search_ex.place(x=400, y=300)

    win1 = Tk()
    win1.geometry("1200x700+100+0")
    win1.resizable(0, 0)
    win1.title("Fuel Management System")
    win1.iconbitmap(r"icon.ico")
    win1.configure(background="white")

    picture = PhotoImage(file="b2.png")
    mypic = Label(win1, image=picture)
    mypic.place(x=0, y=0)

    main_title = PhotoImage(file="main_title.png")
    window_title = Label(win1, image=main_title)
    window_title.place(x=0, y=0)

    side = PhotoImage(file="sidebar.png")
    side_bar = Label(win1, image=side)
    side_bar.place(x=0, y=107)

    update_purchase = PhotoImage(file="update_purchase.png")
    update_sale = PhotoImage(file="update_sl.png")
    update_vehicle = PhotoImage(file="update_veh.png")

    delete_purchase = PhotoImage(file="del_pur.png")
    delete_sale = PhotoImage(file="del_sale.png")
    delete_veh = PhotoImage(file="del_veh.png")

    sear = PhotoImage(file="sear.png")
    sear_pur = PhotoImage(file="search_pur.png")
    sear_sale = PhotoImage(file="search_sale.png")
    sear_veh = PhotoImage(file="search_veh.png")

    value3 = ["Petrol", "Diesel"]

    outward_no = IntVar()
    vehicle_no = StringVar()
    quantity = IntVar()
    whom_concern = StringVar()
    pur_date = StringVar()
    fuel = StringVar()
    sale_quantity = IntVar()
    sale_date = StringVar()
    sl_fuel = StringVar()

    v_no = StringVar()
    veh_quantity = IntVar()
    veh_fuel = StringVar()
    outward_no.set("")
    sale_quantity.set("")
    quantity.set("")
    veh_quantity.set("")

    all_frames_background = PhotoImage(file="all_frames_back.png")
    frame_background_image = PhotoImage(file="back.png")
    '''
    Purchase Fuel
    '''
    out_ward = PhotoImage(file="outward.png")
    date_ = PhotoImage(file="date.png")
    fuel_type = PhotoImage(file="fuel_type.png")
    quan_tity = PhotoImage(file="quantity.png")
    pur_btn = PhotoImage(file="purchase.png")
    clear_frames = PhotoImage(file="clear.png")
    close_frames = PhotoImage(file="exit_main.png")
    back = PhotoImage(file="back_tables.png")
    '''
    Sale Fuel
    '''
    vehicle_ = PhotoImage(file="vehicle.png")
    sale_ = PhotoImage(file="sale.png")
    whom_ = PhotoImage(file="whom_concern.png")
    '''
    add vehicle
    '''
    add = PhotoImage(file="add.png")
    '''
    update & Delete
    '''
    update_ = PhotoImage(file="update.png")
    delete_ = PhotoImage(file="delete.png")
    '''
    home
    '''
    home_stock = PhotoImage(file="home_stock.png")
    home_purchase = PhotoImage(file="home_purchase.png")
    home_sale = PhotoImage(file="home_sale.png")
    home_vehicle = PhotoImage(file="home_vehicle.png")
    home_exit = PhotoImage(file="home_exit.png")

    main_home_image = PhotoImage(file="main_home.png")
    main_pur_image = PhotoImage(file="main_pur.png")
    main_sale_image = PhotoImage(file="main_sale.png")
    main_add_image = PhotoImage(file="main_add.png")
    main_update_image = PhotoImage(file="main_update.png")
    main_delete_image = PhotoImage(file="main_delete.png")
    main_search_image = PhotoImage(file="main_search.png")
    main_exit_image = PhotoImage(file="main_exit.png")

    main_home = Button(win1, image=main_home_image, command=home)
    main_home.place(x=370, y=230)

    main_pur = Button(win1, image=main_pur_image, command=purchase_fuel)
    main_pur.place(x=570, y=230)

    main_sale = Button(win1, image=main_sale_image, command=sale_fuel)
    main_sale.place(x=770, y=230)

    main_add = Button(win1, image=main_add_image, command=add_vehicle)
    main_add.place(x=970, y=230)

    main_update = Button(win1, image=main_update_image, command=update)
    main_update.place(x=370, y=450)

    main_delete = Button(win1, image=main_delete_image, command=delete)
    main_delete.place(x=570, y=450)

    main_search = Button(win1, image=main_search_image, command=search_rec)
    main_search.place(x=770, y=450)

    main_exit = Button(win1, image=main_exit_image, command=close_main_win)
    main_exit.place(x=970, y=450)

    win1.mainloop()


def res():
    u.set("")
    p.set("")


def ex():
    win.destroy()


def forgot():
    def close_forgot_password():
        forgot_fr.destroy()

    def forgot_data():
        db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
        cur = db.cursor()
        cur.execute("SELECT * FROM admin")
        rows = cur.fetchall()
        for row in rows:
            temp_p = row[3]
            temp_nick_name = row[2]
            temp_teacher = row[5]
            if teach.get() == temp_teacher or n_name.get() == temp_nick_name:
                teach.set("")
                n_name.set("")
                messagebox.showinfo("Successful", "Your Password is : " + str(temp_p))
            elif teach.get() == "" or n_name.get() == "":
                messagebox.showwarning("Warning", "Entries Cannot be left blank.\nAnswer one of them.")
            else:
                messagebox.showinfo("Wrong", "Incorrect Name. Try Again")

    forgot_fr = LabelFrame(win, bd=10, relief=SUNKEN, padx=50, bg="#202020")
    forgot_fr.place(x=0, y=0, width=900, height=550)

    fr_lab = Label(forgot_fr, image=ph1)
    fr_lab.pack()

    frame_title = Label(forgot_fr, image=for_password_title)
    frame_title.place(x=0, y=0)

    forgot_note = Label(forgot_fr, image=note)
    forgot_note.place(x=0, y=55)

    t_name = Label(forgot_fr, image=teacher)
    t_name.place(x=400, y=60)

    or_label = Label(forgot_fr, image=or_option)
    or_label.place(x=400, y=200)

    nickname = Label(forgot_fr, image=nick)
    nickname.place(x=400, y=290)

    t_name_ent = Entry(forgot_fr, font=("GUERRILLA", 15, "bold", "italic"), bd=5, relief=SUNKEN, width=27,
                       textvariable=teach)
    t_name_ent.place(x=398, y=140)

    nickname_ent = Entry(forgot_fr, font=("GUERRILLA", 15, "bold", "italic"), bd=5, relief=SUNKEN, width=27,
                         textvariable=n_name)
    nickname_ent.place(x=398, y=370)

    bt_submit = Button(forgot_fr, image=sub, command=forgot_data)
    bt_submit.place(x=420, y=415)

    bt_cancel = Button(forgot_fr, image=cancel, command=close_forgot_password)
    bt_cancel.place(x=420, y=475)


def change_password():
    def close_change_password():
        change_fr.destroy()
        clean()

    def clean():
        p.set("")
        old.set("")
        confirm.set("")

    def save():
        db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
        cur = db.cursor()
        cur.execute("SELECT * FROM admin")
        rows = cur.fetchall()
        for row in rows:
            temp = row[3]
            if old.get() == temp:
                if confirm.get() == p.get():
                    cur.execute("UPDATE admin SET pass = '%s'" % p.get())
                    db.commit()
                    close_change_password()
                    messagebox.showinfo("Successful", "Password Changed Successfully")
                    db.close()
                else:
                    messagebox.showwarning("Error", "Password Not Matched")
            elif old.get() != p:
                messagebox.showerror("Error", "Incorrect Current Password")
            else:
                messagebox.showerror("Error", "Something went wrong")

    change_fr = LabelFrame(win, bd=10, relief=SUNKEN, padx=50, bg="#202020")
    change_fr.place(x=0, y=0, width=900, height=550)

    fr_lab = Label(change_fr, image=ph1)
    fr_lab.pack()

    frame_title = Label(change_fr, image=change_password_title)
    frame_title.place(x=0, y=0)

    curr_password = Label(change_fr, image=current_pass)
    curr_password.place(x=250, y=70)

    new_password = Label(change_fr, image=new_pass)
    new_password.place(x=250, y=200)

    con_password = Label(change_fr, image=confirm_pass)
    con_password.place(x=250, y=330)

    old = StringVar()
    confirm = StringVar()

    curr_password_ent = Entry(change_fr, show="*", font=("GUERRILLA", 15, "bold", "italic"), bd=5, relief=SUNKEN,
                              width=27, textvariable=old)
    curr_password_ent.place(x=248, y=150)

    new_password_ent = Entry(change_fr, show="*", font=("GUERRILLA", 15, "bold", "italic"), bd=5, relief=SUNKEN,
                             width=27, textvariable=p)
    new_password_ent.place(x=248, y=280)

    con_password_ent = Entry(change_fr, show="*", font=("GUERRILLA", 15, "bold", "italic"), bd=5, relief=SUNKEN,
                             width=27, textvariable=confirm)
    con_password_ent.place(x=248, y=410)

    change_btn = Button(change_fr, image=change_pass, command=save)
    change_btn.place(x=100, y=470)

    exit_btn = Button(change_fr, image=cancel, command=close_change_password)
    exit_btn.place(x=450, y=470)


def signup():
    def close_signup():
        sign_fr.destroy()

    def clean_signup():
        name.set("")
        u.set("")
        n_name.set("")
        p.set("")
        m_num.set("")
        teach.set("")

    def signup_data():
        db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
        cur = db.cursor()
        cur.execute("SELECT * FROM admin")
        rows = cur.fetchall()
        if len(rows) == 0:
            cur.execute("INSERT INTO admin(full,user,nick,pass,mobile,teacher) VALUES ('%s','%s','%s','%s','%s','%s')"
                        % (name.get(), u.get(), n_name.get(), p.get(), m_num.get(), teach.get()))
            db.commit()
            clean_signup()
            messagebox.showinfo("Successful", "Account Created Successfully")
            sign_fr.destroy()
            db.close()
        elif len(rows) != 0:
            cur.execute("DELETE FROM admin")
            cur.execute("INSERT INTO admin(full,user,nick,pass,mobile,teacher) VALUES ('%s','%s','%s','%s','%s','%s')"
                        % (name.get(), u.get(), n_name.get(), p.get(), m_num.get(), teach.get()))
            db.commit()
            clean_signup()
            messagebox.showinfo("Successful", "Account Created Successfully")
            sign_fr.destroy()
            db.close()
        else:
            messagebox.showerror("Error", "Something went wrong.\nTry Again.")

    sign_fr = LabelFrame(win, bd=10, relief=SUNKEN, padx=50, bg="#202020")
    sign_fr.place(x=0, y=0, width=900, height=550)

    fr_lab = Label(sign_fr, image=ph1)
    fr_lab.pack()

    frame_title = Label(sign_fr, image=sign_title)
    frame_title.place(x=0, y=0)

    full_name = Label(sign_fr, image=full)
    full_name.place(x=20, y=70)

    user_n = Label(sign_fr, image=user_main_pic)
    user_n.place(x=20, y=200)

    user_p = Label(sign_fr, image=user_main_pass)
    user_p.place(x=20, y=330)

    user_nick = Label(sign_fr, image=nick)
    user_nick.place(x=450, y=70)

    user_ph = Label(sign_fr, image=mobile)
    user_ph.place(x=450, y=200)

    user_teacher = Label(sign_fr, image=teacher)
    user_teacher.place(x=450, y=330)

    full_name_en = Entry(sign_fr, font=("GUERRILLA", 15, "bold", "italic"), bd=5, relief=SUNKEN, width=27,
                         textvariable=name)
    full_name_en.place(x=18, y=150)

    user_n_en = Entry(sign_fr, textvariable=u, font=("GUERRILLA", 15, "bold", "italic"), bd=5, relief=SUNKEN, width=27)
    user_n_en.place(x=18, y=280)

    user_p_en = Entry(sign_fr, show="*", textvariable=p, font=("GUERRILLA", 15, "bold", "italic"), bd=5, relief=SUNKEN,
                      width=27)
    user_p_en.place(x=18, y=410)

    user_nick_en = Entry(sign_fr, font=("GUERRILLA", 15, "bold", "italic"), bd=5, relief=SUNKEN, width=27,
                         textvariable=n_name)
    user_nick_en.place(x=448, y=150)

    user_ph_en = Entry(sign_fr, width=27, font=("GUERRILLA", 15, "bold", "italic"), bd=5, relief=SUNKEN,
                       textvariable=m_num)
    user_ph_en.place(x=448, y=280)

    user_teacher_en = Entry(sign_fr, font=("GUERRILLA", 15, "bold", "italic"), bd=5, relief=SUNKEN, width=27,
                            textvariable=teach)
    user_teacher_en.place(x=448, y=410)

    sign = Button(sign_fr, image=sign_photo, command=signup_data)
    sign.place(x=0, y=470)

    clr = Button(sign_fr, image=clear, command=clean_signup)
    clr.place(x=260, y=470)

    can = Button(sign_fr, image=cancel, command=close_signup)
    can.place(x=520, y=470)


def log_in():
    def log_data():
        db = mysql.connector.connect(host="localhost", user="root", password="password", database="fuel_management")
        cur = db.cursor()
        try:
            cur.execute("SELECT * FROM admin WHERE user='%s' AND pass='%s' " % (u.get(), p.get()))
            return cur.fetchone()
        except:
            return False

    if u.get() == "":
        messagebox.showerror("Error", "Please Type Username")
    elif p.get() == "":
        messagebox.showerror("Error", "Please Type Password")
    elif u.get() == "" and p.get() == "":
        messagebox.showerror("Error", "Please Type Username & Password")
    else:
        result = log_data()
        if result:
            res()
            win.destroy()
            main()
        else:
            messagebox.showerror("Error", "Invalid Username/Password.\nTry Again.")


win = Tk()
win.geometry("900x550+200+70")
win.resizable(0, 0)
win.title("Fuel Management System")
win.iconbitmap(r"icon.ico")

ph1 = PhotoImage(file="title.png")
p2 = Label(win, image=ph1)
p2.pack()

user_pic = PhotoImage(file="user.png")
user_photo = Label(win, image=user_pic)
user_photo.place(x=500, y=5)

name = StringVar()
teach = StringVar()
n_name = StringVar()
m_num = StringVar()
u = StringVar()
p = StringVar()

user_main_pic = PhotoImage(file="user_name_main.png")
user_name = Label(win, image=user_main_pic)
user_name.place(x=490, y=250)

user_main_pass = PhotoImage(file="user_pass_main.png")
user_pass = Label(win, image=user_main_pass)
user_pass.place(x=490, y=390)

e1 = Entry(win, textvariable=u, font=("GUERRILLA", 15, "bold"), bd=5, relief=SUNKEN, width=27)
e1.place(x=490, y=330)
e2 = Entry(win, show="*", width=29, textvariable=p, font=("Harlow Solid Italic", 15, "bold"), bd=5, relief=SUNKEN)
e2.place(x=491, y=470)

for_password_title = PhotoImage(file="forgot_pass_title.png")
sub = PhotoImage(file="submit.png")
or_option = PhotoImage(file="or.png")
note = PhotoImage(file="note_forgot_password.png")

change_password_title = PhotoImage(file="change_pass_title.png")
current_pass = PhotoImage(file="current_pass.png")
new_pass = PhotoImage(file="new_pass.png")
confirm_pass = PhotoImage(file="confirm_pass.png")

sign_title = PhotoImage(file="signup.png")
full = PhotoImage(file="full.png")
teacher = PhotoImage(file="teacher_name.png")
nick = PhotoImage(file="nickname.png")
mobile = PhotoImage(file="mobile_number.png")
cancel = PhotoImage(file="cancel.png")

sign_photo = PhotoImage(file="sign_up.png")
login = PhotoImage(file="log_in.png")
clear = PhotoImage(file="clear.png")
close = PhotoImage(file="exit_main.png")
forgot_password = PhotoImage(file="forgot_pass.png")
change_pass = PhotoImage(file="change.png")

btn1 = Button(win, image=login, padx=50, command=log_in)
btn1.place(x=120, y=40)
btn2 = Button(win, image=close, padx=50, command=ex)
btn2.place(x=120, y=440)
btn3 = Button(win, image=clear, padx=50, command=res)
btn3.place(x=120, y=360)
btn4 = Button(win, image=sign_photo, padx=50, command=signup)
btn4.place(x=120, y=120)
btn5 = Button(win, image=forgot_password, padx=50, command=forgot)
btn5.place(x=120, y=200)
btn6 = Button(win, image=change_pass, padx=50, command=change_password)
btn6.place(x=120, y=280)

win.mainloop()

'''
title_pic = PhotoImage(file="title.png")
title = Label(root, image=title_pic)
title.place(x=0, y=0)

title_1 = Label(root, text="Welcome to Fuel Management System", font=("Harlow Solid Italic", 25, "italic", "bold"),
                padx=200)
title_1.place(x=0, y=0)
title_2 = Label(root, text="University Of Sindh,Jamshoro", font=("Harlow Solid Italic", 25, "italic", "bold"), padx=250)
title_2.place(x=0, y=45)

title_3 = Label(root, text="***Created & Designed Under Supervision Of***",
                font=("GUERRILLA", 20, "bold", "italic"), padx=150)
title_3.place(x=0, y=170)
title_4 = Label(root, text="Prof.Dr.Imtiaz Korejo", font=("Harlow Solid Italic", 15, "italic", "bold"))
title_4.place(x=340, y=220)
title_5 = Label(root, text="***Created & Designed By***", font=("GUERRILLA", 20, "bold", "italic"), padx=270)
title_5.place(x=0, y=265)
title_6 = Label(root, text="Students Of BS(CS) Part-II (Pre-Engineering)",
                font=("Harlow Solid Italic", 15, "italic", "bold"))
title_6.place(x=235, y=315)
title_7 = Label(root, text="Abdul Salam Shaikh", font=("Harlow Solid Italic", 15, "italic", "bold"))
title_7.place(x=350, y=350)
title_8 = Label(root, text="(2k18 / CSE / 8)", font=("Harlow Solid Italic", 15, "italic", "bold"))
title_8.place(x=365, y=375)
title_9 = Label(root, text="Muhammad Ismail Soomro", font=("Harlow Solid Italic", 15, "italic", "bold"))
title_9.place(x=320, y=410)
title_10 = Label(root, text="(2k18 / CSE / 74)", font=("Harlow Solid Italic", 15, "italic", "bold"))
title_10.place(x=365, y=440)


root.bind('<Return>', onclick)
button = Button(root, text="Press Enter to Continue...", font=("GUERRILLA", 20, "italic", "bold"),
                padx=285, command=onclick)
button.place(x=0, y=500)

root.mainloop()
'''