import tkinter as tk
import time
from tkinter import font  as tkfont
from tkinter import messagebox
            

class ATM(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("ATM KIOSK")
        
        container = tk.Frame(self)
        container.pack(side="top", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frame("StartPage")



class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        global account
        tk.Frame.__init__(self, parent, bg = "#4B0082")
        self.controller = controller
        label = tk.Label(self, text="ATM KIOSK",width=20,height=1,fg="white",bg="black",font=('Acme', 60, 'bold'),highlightcolor="orange")
        label.pack(side="top", pady=(30,10))

        localtime=time.asctime(time.localtime(time.time()))

        label2=tk.Label(self,text=localtime,width=20,height=1,fg="blue",font=('robotic',20,'bold'))
        label2.pack(side="top", pady=20)

        self.label1=tk.Label(self,text="Enter Account Number",width=20,height=2,fg="black",bg="powder blue",font=('robotic',30,'bold'))
        self.label1.pack(side="top", pady=20)

        self.entry1 = tk.Entry(self,relief="sunken",bd=3,validate="key",insertwidth=4)
        def acc_validation():
            global account
            acc=int(self.entry1.get())
            
            self.conn=pymysql.connect(host='localhost',database='atm',user='root',password='root')
            cursor=self.conn.cursor()
            cursor.execute("SELECT name FROM user_details WHERE account_no='%d'"%(acc))
            row=cursor.fetchall()
            if(row!=()):
                cursor.execute("SELECT name FROM user_details WHERE account_no='%d'"%(acc))
                out=cursor.fetchone()
                account = acc
                self.entry1.delete(0,'end')
                controller.show_frame("PageOne")
            else:
                tk.messagebox.showinfo("Validation", "Account Not Found")
                self.entry1.delete(0,"end")

        button1 = tk.Button(self, text="Submit", command=lambda:acc_validation())
        
        self.entry1.pack(side = "top", pady="10")
        button1.pack(side = "top", pady="20")

    


if __name__ == "__main__":
    app = ATM()
    app.geometry("800x600+420+50")
    app.resizable(0,0)
    app.mainloop()
