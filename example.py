#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mike
#
# Created:     21/10/2017
# Copyright:   (c) mike 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import tkinter as tk
import tkinter.ttk as ttk
import sqlite3

class Foodlife:
    def create_gui():
    #==functions==========================================================
       # ----------------------------------------
        def quit_button():
            root.destroy()
        # ----------------------------------------
        def create_sql(item_name):

            c = sqlite3.connect("fooddb.db")
            c.isolation_level=None
            c.execute("BEGIN")
            item_code = c.execute("""
                        SELECT item_code FROM item
                        WHERE item_name = '{}'
                        """.format(item_name))
            item_code = item_code.fetchone()[0]
            acc_name = entry1.get()
            acc_date_a = entry3a.get()
            acc_date_b = entry3b.get()
            acc_date_c = entry3c.get()
            try:
                c.execute("""
                INSERT INTO acc_data(acc_name,item_code,acc_date_a,acc_date_b,acc_date_c)
                VALUES('{}',{},{},{},{});
                """.format(acc_name,item_code,acc_date_a,acc_date_b,acc_date_c))
                c.execute("COMMIT;")
                c.close()
                print("1 data inserted")
                refresh()
            except:
                print("nothing was inserted")
                c.close()

        # ----------------------------------------
        def createitemname():
            c = sqlite3.connect("fooddb.db")
            c.isolation_level=None
            c.execute("BEGIN")
            li = []
            for r in c.execute("SELECT item_name FROM item"):
                li.append(r)
            return tuple(li)
            c.close()
        # ----------------------------------------

        # ----------------------------------------
        # remake database
        dbname="fooddb.db"
        c = sqlite3.connect(dbname)
        c.isolation_level=None
        c.execute("PRAGMA foreign_keys = 1")
        try:
            ddl = """
            CREATE TABLE item
            (
               item_code INTEGER PRIMARY KEY AUTOINCREMENT,
               item_name TEXT NOT NULL UNIQUE
            )
             """
            c.execute(ddl)
            ddl = """
            CREATE TABLE acc_data
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                acc_name TEXT NOT NULL,
                item_code INTEGER NOT NULL,
                acc_date_a INTEGER NOT NULL,
                acc_date_b INTEGER NOT NULL,
                acc_date_c INTEGER NOT NULL,
                FOREIGN KEY(item_code) REFERENCES item(item_code)
            )
            """
            c.execute(ddl)
            c.execute("INSERT INTO item VALUES(1,'food')")
            c.execute("INSERT INTO item VALUES(2,'sauce')")
            c.execute("INSERT INTO item VALUES(3,'drinks')")
            c.execute("COMMIT")
            c.close()
        except:
    # if exist then pass
            c.close()
    # ----------------------------------------
    #==function end=======================================================




    #==GUI start==========================================================

        root = tk.Tk()
        root.title("Food Supply")
        #root.geometry("700x280")

    #-------------------------------------------------------------------------------
        [frame_name,frame_name0,label1_text,label2_text,label3_text,label4_text,label5_text]=["viewer","inputs","name","category","year","month","date"]
    #-------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------
    #frame=tree frame
        frame = tk.LabelFrame(root,width=600,bd=2,relief="ridge",text=frame_name)
        frame.pack(side="left",fill="y")
        tree = ttk.Treeview(frame)
        tree["columns"] = (1,2,3,4,5)
        tree["show"] = "headings"
        tree.column(1,width=100)
        tree.column(2,width=75)
        tree.column(3,width=50)
        tree.column(4,width=30)
        tree.column(5,width=30)
        tree.heading(1,text=label1_text)
        tree.heading(2,text=label2_text)
        tree.heading(3,text=label3_text)
        tree.heading(4,text=label4_text)
        tree.heading(5,text=label5_text)
        sql3 = """
            SELECT acc_name,item_name,acc_date_a,acc_date_b,acc_date_c
            FROM acc_data as a,item as i
            WHERE a.item_code = i.item_code
            """
        def refresh():
            c = sqlite3.connect("fooddb.db")
            cd=c.cursor()
            tree.delete(*tree.get_children())
            for r in cd.execute(sql3):
                r = (r[0],r[1],r[2],r[3],r[4])
                tree.insert("","end",values=r)
            c.close()

        tree.pack(side="left",fill="y",padx=20,pady=20)
        ysb=ttk.Scrollbar(frame,orient="vertical",command=tree.yview)
        ysb.pack(side="right",fill="y")
    #-------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------
    #frame0=input frame
        frame0 = tk.LabelFrame(root,width=300,bd=2,relief="ridge",text=frame_name0)
        frame0.pack(side="left",fill="both",ipadx=10,ipady=10)

    #   input large frames
        frame1 = tk.Frame(frame0,pady=10)
        frame1.pack()
        frame2 = tk.Frame(frame0,pady=10)
        frame2.pack()
        frame3 = tk.Frame(frame0,pady=10)
        frame3.pack()
        frame4 = tk.Frame(frame0,pady=10)
        frame4.pack()

        #   input labels and inputs
        #label1
        label1 = tk.Label(frame1,font=("",14),text=label1_text,width=10)
        label1.pack(side="left")
        entry1 = tk.Entry(frame1,font=("",14),width=15)
        entry1.pack(side="left")
        #label2
        label2 = tk.Label(frame2,font=("",14),text=label2_text,width=10)
        label2.pack(side="left")
        combo = ttk.Combobox(frame2, state='readonly',font=("",14),width=13)
        combo["values"] = createitemname()
        combo.current(1)
        combo.pack()
        #label3
        label3 = tk.Label(frame3,font=("",14),text=label3_text,width=8)
        label3.pack(side="left")
        label3a = tk.Label(frame3,font=("",14),text="Y",width=2)
        label3a.pack(side="left")
        entry3a = tk.Entry(frame3,font=("",14),width=4)
        entry3a.pack(side="left")
        label3b = tk.Label(frame3,font=("",14),text="M",width=2)
        label3b.pack(side="left")
        entry3b = tk.Entry(frame3,font=("",14),width=2)
        entry3b.pack(side="left")
        label3c = tk.Label(frame3,font=("",14),text="D",width=2)
        label3c.pack(side="left")
        entry3c = tk.Entry(frame3,font=("",14),width=2)
        entry3c.pack(side="left")

        button4 = tk.Button(frame4,text="intsert\ndata",
                            font=("",12),
                            width=10,bg="gray",
                            command=lambda:create_sql(combo.get()))
        button5 = tk.Button(frame4,text="refresh",
                            font=("",12),
                            width=10,bg="gray",
                            command=lambda:refresh())
        button6 = tk.Button(frame4,text="print select",
                            font=("",12),
                            width=10,bg="gray",
                            command=lambda:on_tree_select())

        def on_tree_select():
            print("selected items:")
            for item in tree.selection():
                item_text = tree.item(item,"values")
                print(item_text)
        button4.pack(side="left",fill="y")
        button5.pack(side="left",fill="y")
        button6.pack(side="left",fill="y")
    #-------------------------------------------------------------------------------
        refresh()
        root.mainloop()
        #==GUI end==========================================================
Foodlife.create_gui()
