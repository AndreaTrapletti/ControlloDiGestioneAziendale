import tkinter as tk
from tkinter import *
import tkinter.messagebox as tkMessageBox
from secondo_frame import leggi_file
from secondo_frame import leggi_file
root = tk.Tk()
root.title("Controllo di Gestione -- login")
root.config(bg="white") 
width = 460
height = 260
root.geometry("460x260")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
USERNAME = StringVar()
PASSWORD = StringVar()
FIRSTNAME = StringVar()
LASTNAME = StringVar()
def LoginForm():
    global LoginFrame, lbl_result1
    LoginFrame = Frame(root, bg="white")
    LoginFrame.pack(side=TOP, pady=5)
    lbl_username = Label(LoginFrame, text="Username:", font=('arial', 25), bd=18, bg="white")
    lbl_username.grid(row=1)
    lbl_password = Label(LoginFrame, text="Password:", font=('arial', 25), bd=18, bg="white" )
    lbl_password.grid(row=2)
    lbl_result1 = Label(LoginFrame, text="", font=('arial', 18), bg="white" )
    lbl_result1.grid(row=3, columnspan=2)
    username = Entry(LoginFrame, font=('arial', 20), textvariable=USERNAME, width=15, bg="pink")
    username.grid(row=1, column=1)
    password = Entry(LoginFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*", bg="pink")
    password.grid(row=2, column=1)
    btn_login = Button(LoginFrame, text="Login", font=('arial', 18), width=30, bg="red",command=Login)
    btn_login.grid(row=4, columnspan=2, pady=8)
    
def Login():
    
    if USERNAME.get == "admin" or PASSWORD.get() == "admin":
        lbl_result1.config(text="You Successfully Login", fg="blue")
        leggi_file()
        root.destroy()
        

    else:
        lbl_result1.config(text="Invalid Username or password", fg="red")  

LoginForm()
if __name__ == "__main__":
    root.mainloop()