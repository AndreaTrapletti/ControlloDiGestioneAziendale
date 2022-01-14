import tkinter as tk
import pandas as pd
from tkinter import *
from dashboard import *
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np

def funzione_da_bottone1(vendite_budget_cons, vendite_quantita, vendite_nArticolo, vendite_totale_vendita):
    
    for i in range(len(vendite_budget_cons)):
        if(vendite_budget_cons[i] == "CONSUNTIVO" ):
            vendite_budget_cons[i] = "Consuntivo"
            
    
    df = pd.DataFrame({'Budget/cons': vendite_budget_cons,'nArticolo': vendite_nArticolo,'qtd': vendite_quantita,
                        'totale': vendite_totale_vendita})

    indexNames = df[df['totale']==0].index
    df.drop(indexNames, inplace=True)
    
    dfbudget = df[df['Budget/cons']=="BUDGET"]
    df2 = dfbudget.groupby('nArticolo', as_index = False)['qtd','totale'].sum()
    
    dfcons = df[df['Budget/cons']=="Consuntivo"]
    df3 = dfcons.groupby('nArticolo', as_index = False)['qtd','totale'].sum()

    dfbudgetUnitari = df2.copy()
    dfbudgetUnitari["media_unitaria"] = dfbudgetUnitari['totale']/dfbudgetUnitari['qtd']
    dfunitarioBudget = dfbudgetUnitari.copy()
    dfDaVedereBudget = dfbudgetUnitari.copy()
    dfunitarioBudget = dfbudgetUnitari.drop(['qtd','totale'], 1)
    dfDaVedereBudget = dfDaVedereBudget.drop(['totale'],1)

    dfconsUnitari = df3.copy()
    dfconsUnitari["media_unitaria"] = dfconsUnitari['totale']/dfconsUnitari['qtd']
    dfunitarioCons = dfconsUnitari.copy()
    dfDaVedereCons = dfconsUnitari.copy()
    dfunitarioCons = dfconsUnitari.drop(['qtd','totale'], 1)
    dfDaVedereCons = dfDaVedereCons.drop(['totale'],1)

    dfunitiUnitario = pd.merge(left = dfunitarioBudget, right = dfunitarioCons, how = 'outer', on = 'nArticolo')
    dfunitiUnitario = dfunitiUnitario.rename(columns= {'media_unitaria_x' : 'prezzo_unitario_Budget','media_unitaria_y' : 'prezzo_unitario_cons'})
    dfDaVedere = pd.merge(left=dfDaVedereBudget, right=dfDaVedereCons, how='outer', on='nArticolo')
    dfDaVedere = dfDaVedere.rename(columns={'media_unitaria_x' : 'prezzo_unitario_Budget','media_unitaria_y' : 'prezzo_unitario_cons',
        'qtd_x':'qtd_budget','qtd_y':'qtd_consuntivo'})

    tempUnitari1 = dfunitiUnitario.copy()
    index_names = tempUnitari1[tempUnitari1['prezzo_unitario_Budget']/tempUnitari1['prezzo_unitario_cons'] < 1.5 ].index
    tempUnitari1.drop(index_names, inplace=True)
    
    tempUnitari2 = dfunitiUnitario.copy()
    index_names2 = tempUnitari2[(tempUnitari2['prezzo_unitario_cons']/tempUnitari2['prezzo_unitario_Budget']) < 1.5 ].index
    tempUnitari2.drop(index_names2, inplace=True)
    frames = [tempUnitari1, tempUnitari2]
    tempUnitari = pd.concat(frames)
    
    dfunitiTotaleTemp = pd.merge(left=df2, right=df3, how = 'outer', on = 'nArticolo')
    dfunitiTotale = dfunitiTotaleTemp.copy()
    dfunitiTotale = dfunitiTotale.drop(['totale_x','totale_y'],1)
    dfunitiTotale = dfunitiTotale.rename(columns= {'qtd_x' : 'qtd_Budget', 'qtd_y' : 'qtd_cons'})

    dfunitiTotaleDelta1 = dfunitiTotale.copy()
    index_names3 = dfunitiTotaleDelta1[(dfunitiTotaleDelta1['qtd_Budget']/dfunitiTotaleDelta1['qtd_cons'])<1.5].index
    dfunitiTotaleDelta1.drop(index_names3, inplace=True)
    dfunitiTotaleDelta2 = dfunitiTotale.copy()
    index_names4 = dfunitiTotaleDelta2[(dfunitiTotaleDelta2['qtd_cons']/dfunitiTotaleDelta2['qtd_Budget'])<1.5].index
    dfunitiTotaleDelta2.drop(index_names4, inplace=True)
    frames2 = [dfunitiTotaleDelta1, dfunitiTotaleDelta2]
    dfunitiTotaleDelta = pd.concat(frames2)
    
    root = tk.Tk()
    root.title("Controllo di Gestione -- Analisi Vendite per articolo ")
    root.config(bg="white") 
    width = 1200
    height = 700
    root.geometry("1200x700")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0, 0)
    root.pack_propagate(False)
    
    frame1 = tk.LabelFrame(root, text="Prezzi unitari che si discostano +/- 50% tra Budget e Consuntivo", bg="white")
    frame1.place(height=211, width=640)
    frame2 = tk.LabelFrame(root, text="Quantità che si discostano +/- 50% tra Budget e Consuntivo", bg="white")
    frame2.place(height=211, width=640, rely=0.33, relx=0)
    frame3= tk.LabelFrame(root, text="Prezzi Unitari BUDGET/CONSUNTIVO", bg="white")
    frame3.place(height=213.6, width=640, rely=0.64, relx=0)
    file_frame = tk.LabelFrame(root, bg="white")
    file_frame.place(height=665, width=500, relx=0.55)
    tv1 = ttk.Treeview(frame1)
    tv1.place(relheight=1, relwidth=1)
    tv2 = ttk.Treeview(frame2)
    tv2.place(relheight=1, relwidth=1)
    tv3 = ttk.Treeview(frame3)
    tv3.place(relheight=1, relwidth=1)
    treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview)
    treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview)
    treescrolly2 = tk.Scrollbar(frame2, orient="vertical", command=tv2.yview) 
    treescrollx2 = tk.Scrollbar(frame2, orient="horizontal", command=tv2.xview) 
    treescrolly3 = tk.Scrollbar(frame3, orient="vertical", command=tv3.yview) 
    treescrollx3 = tk.Scrollbar(frame3, orient="horizontal", command=tv3.xview)
    tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) 
    tv2.configure(xscrollcommand=treescrollx2.set, yscrollcommand=treescrolly2.set)
    tv3.configure(xscrollcommand=treescrollx3.set, yscrollcommand=treescrolly3.set)
    
    treescrolly.pack(side="right", fill="y") 
    treescrolly2.pack(side="right", fill="y")
    treescrollx3.pack(side="bottom", fill="x") 
    treescrolly3.pack(side="right", fill="y")

    def inserisci():
        btnUnitari = tk.Button(file_frame, text="grafico prezzi unitari di vendita",font=('arial', 18), width=25, bg="red",command=bottoneUniti )
        btnUnitari.place(rely=0,relx=0.05)
        btnTotale = tk.Button(file_frame, text="grafico quantità di vendita",font=('arial', 18), width=25, bg="red",command=bottonetotale )
        btnTotale.place(rely=0.48, relx=0.05)
        totale_Vbudget = int(dfbudget['totale'].sum())
        lb1 = Label(file_frame, text="Il totale vendita a budget è: " + str(totale_Vbudget)+"€", font=('arial', 14), bd=10, bg="white")
        lb1.place(rely=0.07, relx=0.05)
        totale_Vcons = int(dfcons['totale'].sum())
        lb2 = Label(file_frame, text="Il totale vendita a consuntivo è: " + str(totale_Vcons)+"€", font=('arial', 14), bd=10, bg="white")
        lb2.place(rely=0.12, relx=0.05)
        lb3 = Label(file_frame, text="DELTA VENDITE: " + str(totale_Vcons - totale_Vbudget)+"€"+ "  (+"+
            str(int((totale_Vcons*100 / totale_Vbudget) - 100))+"%)", font=('arial', 14), bd=10, bg="white")
        lb3.place(rely=0.17, relx=0.05)
        totale_VUbudget = int(dfunitarioBudget['media_unitaria'].sum())
        lb4 = Label(file_frame, text="Il totale vendita unitario a budget è: " + str(totale_VUbudget)+"€", font=('arial', 14), bd=10, bg="white")
        lb4.place(rely=0.26, relx=0.05)
        totale_VUcons = int(dfunitarioCons['media_unitaria'].sum())
        lb5 = Label(file_frame, text="Il totale vendita unitario a consuntivo è: " + str(totale_VUcons)+"€", font=('arial', 14), bd=10, bg="white")
        lb5.place(rely=0.31, relx=0.05)
        lb6 = Label(file_frame, text="DELTA VENDITE UNITARIO: " + str(totale_VUcons - totale_VUbudget)+"€"+ "  ("+
            str(int(((totale_VUcons*100 / totale_VUbudget))-100))+"%)", font=('arial', 14), bd=10, bg="white")
        lb6.place(rely=0.36, relx=0.05)
        tot_qtdB = int(dfbudget['qtd'].sum())
        lb7 = Label(file_frame, text="Totale articoli venduti a budget: " + str(tot_qtdB)+" pezzi", font=('arial', 14), bd=10, bg="white")
        lb7.place(rely=0.55, relx=0.05)
        tot_qtdC = int(dfcons['qtd'].sum())
        lb8 = Label(file_frame, text="Totale articoli venduti a consuntivo: " + str(tot_qtdC)+" pezzi", font=('arial', 14), bd=10, bg="white")
        lb8.place(rely=0.60, relx=0.05)
        lb9 = Label(file_frame, text="DELTA QUANTITA': " + str(tot_qtdC - tot_qtdB)+" pezzi  (+" + str(int(((tot_qtdC*100/tot_qtdB))-100)) +
            "%)",font=('arial', 14), bd=10, bg="white")
        lb9.place(rely=0.65, relx=0.05)
        lb10 = Label(file_frame, text="-----------------------------------------------------------------------",font=('arial', 14), bd=10, bg="white")
        lb10.place(rely=0.70, relx=0.05)
        lb12 = Label(file_frame, text="Le tabelle a sinistra composte da articoli che si discostano     ",font=('arial', 12), bd=8, bg="white")
        lb12.place(rely=0.74, relx=0.05)
        lb13 = Label(file_frame, text="+/- 50% tra budget e consuntivo:        ",font=('arial', 12), bd=8, bg="white")
        lb13.place(rely=0.78, relx=0.05)
        lb14 = Label(file_frame, text="Prezzi unitari--> totale= " + str(int(len(tempUnitari)))+" ("+
            str(int(len(tempUnitari)/len(dfbudgetUnitari)*100))+"%" +" dei valori totali)",font=('arial', 12), bd=8, bg="white")
        lb14.place(rely=0.825, relx=0.05)
        lb15 = Label(file_frame, text="Quantità--> totale= " + str(int(len(dfunitiTotaleDelta)))+" ("+
            str(int(len(dfunitiTotaleDelta)/len(dfbudgetUnitari)*100))+"%" +" dei valori totali)",font=('arial', 12), bd=8, bg="white")
        lb15.place(rely=0.87, relx=0.05)
        print(len(dfbudgetUnitari))
        btnClose = tk.Button(file_frame, text="exit",font=('arial', 18), width=10, bg="red",command=exit )
        btnClose.place(rely=0.93, relx=0.7)
        
        tv1["column"] = list(tempUnitari.columns)
        tv1["show"] = "headings"
        for column in tv1["columns"]:
            tv1.heading(column, text=column) 

        df_rows = tempUnitari.to_numpy().tolist() 
        for row in df_rows:
            tv1.insert("", "end", values=row)
        tv2["column"] = list(dfunitiTotaleDelta.columns)
        tv2["show"] = "headings"
        for column in tv2["columns"]:
            tv2.heading(column, text=column) 

        df_rows2 = dfunitiTotaleDelta.to_numpy().tolist() 
        for row in df_rows2:
            tv2.insert("", "end", values=row)
        tv3["column"] = list(dfDaVedere.columns)
        tv3["show"] = "headings"
        for column in tv3["columns"]:
            tv3.heading(column, text=column) 

        df_rows3 = dfDaVedere.to_numpy().tolist() 
        for row in df_rows3:
            tv3.insert("", "end", values=row)

    def exit():
        root.destroy()
    def bottoneUniti():
        x = dfunitiUnitario['nArticolo']
        y = dfunitiUnitario['prezzo_unitario_Budget']
        z = dfunitiUnitario['prezzo_unitario_cons']
        fig, ax=plt.subplots()
        ax.scatter(z,y)
        ax.set_title('Rapporto prezzi unitari da budget a consuntivo')
        ax.set_xlabel('prezzo_unitario_cons')
        ax.set_ylabel('prezzo_unitario_Budget')
        figManager = plt.get_current_fig_manager()
        plt.show()
    def bottonetotale():
        dfmomt =  dfunitiTotaleDelta.copy()
        dfmomt.set_index('nArticolo', inplace= True)
        pr= dfmomt.plot.bar()
        pr.set_title('Rapporto quantità per articolo da budget a consuntivo \n si consiglia di zoomare utilizzando la lente di ingrandimento sulla sezione desiderata')
        pr.set_ylabel('quantità')
        figManager = plt.get_current_fig_manager()
        plt.show()

    inserisci()
    
  
    if __name__ == "__main__":
        root.mainloop()