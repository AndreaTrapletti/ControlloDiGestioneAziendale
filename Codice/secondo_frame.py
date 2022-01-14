import tkinter as tk
import pandas as pd
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox as tkMessageBox
from dashboard import calcolatore
import os

def leggi_file():
    root = tk.Tk()
    root.title("Controllo di Gestione -- benvenuto")
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
    def inserisci():
        global login_frame
        login_frame = Frame(root, bg="white")
        login_frame.pack(side=TOP, pady=60)
        btn = Button(login_frame, text="INSERISCI I FILE EXCEL", font=('arial', 18), width=30, bg="red", command=openFile)
        btn.grid(row=4, columnspan=2, pady=20)
    
    def openFile():
        tk.Tk().withdraw()
        filepath = filedialog.askopenfilenames(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                          title="Open file okay?",
                                          filetypes= (("excell files","*.xlsx"),
                                          ("all files",".")))
        Consumi=""
        Clienti=""
        Budget=""
        Consuntivo=""
        Impiego=""
        Tassi=""
        Vendite=""
        count = 0
        for x in filepath:
            name = (os.path.basename(x))
            if name=='Consumi.xlsx': 
                Consumi= pd.read_excel(x)
                count += 1
            if name=='Clienti.xlsx': 
                Clienti= pd.read_excel(x)
                count += 1
            if name=='Costo orario risorse Budget.xlsx': 
                Budget = pd.read_excel(x)
                count += 1
            if name=='Costo orario risorse Consuntivo.xlsx' : 
                Consuntivo= pd.read_excel(x)
                count += 1
            if name=='Impiego orario risorse.xlsx' : 
                Impiego= pd.read_excel(x)
                count += 1
            if name=='Tassi di cambio.xlsx' : 
                Tassi= pd.read_excel(x)
                count += 1
            if name=='Vendite.xlsx' : 
                Vendite= pd.read_excel(x)
                count += 1
        if count==7:
            calcolatore(Consumi, Clienti, Budget, Consuntivo, Impiego, Tassi, Vendite)
            root.destroy()  
        else:
            lbl = Label(login_frame, text="ERRORE: inserire tutti gli excel \n file inseriti: "+str(count), font=('arial', 25), bd=18, bg="white")
            lbl.grid(row=7)  
            inserisci()    

    inserisci()
    if __name__ == "__main__":
        root.mainloop()