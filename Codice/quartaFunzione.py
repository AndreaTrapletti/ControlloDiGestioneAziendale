from contextlib import nullcontext
from os import name
import tkinter as tk
from tkinter.font import names
import pandas as pd
from tkinter import *
import numpy as np
from tkinter import ttk
import matplotlib.pyplot as plt


def funzione_da_bottone4(dfImpiegoBudgetDiretto, dfImpiegoConsDiretto,dfConsumiBudget, dfConsumiCons, dfImpiegoBudget, dfImpiegoCons):
    
    dfImpiegoBudgetDiretto['Cu_risorse(€/u)'] = dfImpiegoBudgetDiretto['tempo_x_costoRisorsa(€)'] / dfImpiegoBudgetDiretto['qtd_output']
    dfImpiegoConsDiretto['Cu_risorse(€/u)'] = dfImpiegoConsDiretto['tempo_x_costoRisorsa(€)'] / dfImpiegoConsDiretto['qtd_output']

    dfImpiegoBudgetDiretto = dfImpiegoBudgetDiretto.groupby('nArticolo', as_index=False)['Cu_risorse(€/u)'].mean()
    dfImpiegoConsDiretto = dfImpiegoConsDiretto.groupby('nArticolo', as_index=False)['Cu_risorse(€/u)'].mean()

    dfCostiDirettiBudget = pd.merge(left=dfImpiegoBudgetDiretto, right=dfConsumiBudget, how='outer', on='nArticolo')
    dfCostiDirettiConsuntivo = pd.merge(left=dfImpiegoConsDiretto, right=dfConsumiCons, how='outer', on='nArticolo')
    dfCostiDirettiBudget = dfCostiDirettiBudget.fillna(0)
    dfCostiDirettiConsuntivo = dfCostiDirettiConsuntivo.fillna(0)
    dfCostiDirettiBudget['Cu_totale(€/u)'] = dfCostiDirettiBudget['Cu_risorse(€/u)'] + dfCostiDirettiBudget['Cu_MP(€/u)']
    dfCostiDirettiConsuntivo['Cu_totale(€/u)'] = dfCostiDirettiConsuntivo['Cu_risorse(€/u)'] + dfCostiDirettiConsuntivo['Cu_MP(€/u)']
    
    
    dfDeltaBudget = dfCostiDirettiBudget.copy()
    dfDeltaCons = dfCostiDirettiConsuntivo.copy()
    dfDelta = pd.merge(left=dfDeltaBudget, right=dfDeltaCons, how='outer', on='nArticolo', suffixes=['_budget','_consuntivo'])
    dfDelta2 = dfDelta.copy()
    index_names1 = dfDelta[dfDelta['Cu_totale(€/u)_consuntivo']/dfDelta['Cu_totale(€/u)_budget'] < 1.5 ].index
    dfDelta.drop(index_names1, inplace=True)
    index_names11 = dfDelta2[dfDelta2['Cu_totale(€/u)_budget']/dfDelta2['Cu_totale(€/u)_consuntivo'] < 1.5 ].index
    dfDelta2.drop(index_names11, inplace=True)
    frames = [dfDelta2, dfDelta]
    dfDelta3 = pd.concat(frames)
    dfDelta3 = dfDelta3.drop(['Cu_risorse(€/u)_budget','Cu_risorse(€/u)_consuntivo','Cu_MP(€/u)_budget','Cu_MP(€/u)_consuntivo'],1)
    
    
    root = tk.Tk()
    root.title("Controllo di Gestione -- Analisi dei costi ")
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

    frame1 = tk.LabelFrame(root, text="divisione del nostro dataframe con chiavi: Articolo, Risorsa, Area di Produzione, Ordine di Produzione / BUDGET ", bg="white")
    frame1.place(height=160, width=590,rely=0.0, relx=0)
    frame2 = tk.LabelFrame(root, text="divisione del nostro dataframe con chiavi: Articolo, Risorsa, Area di Produzione, Ordine di Produzione / CONSUNTIVO ", bg="white")
    frame2.place(height=160, width=590,rely=0.25, relx=0)
    frame3 = tk.LabelFrame(root, text="Costi Diretti per articolo / BUDGET", bg="white")
    frame3.place(height=160, width=590,rely=0.50, relx=0)
    frame4 = tk.LabelFrame(root, text="Costi Diretti per articolo / CONSUNTIVO", bg="white")
    frame4.place(height=160, width=590,rely=0.75, relx=0)
    framedestro = tk.LabelFrame(root,bg="white")
    framedestro.place(height=510, width=590, relx=0.5083333, rely=0.25)
    frame5 = tk.LabelFrame(root, text="Costi Unitari che discostano +/- del 50% tra Budget/Consuntivo", bg="white")
    frame5.place(height=160, width=590,rely=0.0, relx=0.5083333)
    tv1 = ttk.Treeview(frame1)
    tv1.place(relheight=1, relwidth=1)
    tv2 = ttk.Treeview(frame2)
    tv2.place(relheight=1, relwidth=1)
    tv3 = ttk.Treeview(frame3)
    tv3.place(relheight=1, relwidth=1)
    tv4 = ttk.Treeview(frame4)
    tv4.place(relheight=1, relwidth=1)
    tv5 = ttk.Treeview(frame5)
    tv5.place(relheight=1, relwidth=1)
    treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview)
    treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview)
    treescrolly2 = tk.Scrollbar(frame2, orient="vertical", command=tv2.yview) 
    treescrollx2 = tk.Scrollbar(frame2, orient="horizontal", command=tv2.xview)
    treescrolly3 = tk.Scrollbar(frame3, orient="vertical", command=tv3.yview)
    treescrollx3 = tk.Scrollbar(frame3, orient="horizontal", command=tv3.xview)
    treescrolly4 = tk.Scrollbar(frame4, orient="vertical", command=tv4.yview) 
    treescrollx4 = tk.Scrollbar(frame4, orient="horizontal", command=tv4.xview) 
    treescrolly5 = tk.Scrollbar(frame5, orient="vertical", command=tv5.yview) 
    treescrollx5 = tk.Scrollbar(frame5, orient="horizontal", command=tv5.xview) 
    tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) 
    tv2.configure(xscrollcommand=treescrollx2.set, yscrollcommand=treescrolly2.set)
    tv3.configure(xscrollcommand=treescrollx3.set, yscrollcommand=treescrolly3.set)
    tv4.configure(xscrollcommand=treescrollx4.set, yscrollcommand=treescrolly4.set)
    tv5.configure(xscrollcommand=treescrollx5.set, yscrollcommand=treescrolly5.set)
    treescrollx.pack(side="bottom", fill="x") 
    treescrolly.pack(side="right", fill="y") 
    treescrollx2.pack(side="bottom", fill="x") 
    treescrolly2.pack(side="right", fill="y")
    treescrollx3.pack(side="bottom", fill="x") 
    treescrolly3.pack(side="right", fill="y")
    treescrollx4.pack(side="bottom", fill="x") 
    treescrolly4.pack(side="right", fill="y")
    treescrollx5.pack(side="bottom", fill="x") 
    treescrolly5.pack(side="right", fill="y")
    
    totale_Cbudget=int(sum(dfCostiDirettiBudget['Cu_totale(€/u)']))
    totale_Ccons=int(sum(dfCostiDirettiConsuntivo['Cu_totale(€/u)']))

    def inserisci():
        btnClose = tk.Button(framedestro, text="exit",font=('arial', 18), width=10, bg="red",command=exit )
        btnClose.place(rely=0.91, relx=0.762)
        lb12 = Label(framedestro, text="La tabella soprastante è composta da articoli che si discostano" +
            "\n+/- 50% tra budget e consuntivo: " + "\nCosti unitari--> totale= " + str(int(len(dfDelta3)))+" ("+
            str(int(len(dfDelta3)/len(dfCostiDirettiConsuntivo)*100))+"%" +" dei valori totali)"
            + "\n------------------------------------------------------"
            + "\nIl totale costo unitario a budget è: " + str(totale_Cbudget)+"€"
            + "\nIl totale costo unitario a consuntivo è: " + str(totale_Ccons)+"€"
            + "\nDELTA COSTI: " + str(totale_Ccons - totale_Cbudget)+"€"+ "  ("+
            str(int(((totale_Ccons / totale_Cbudget)*100)-100))+"%)",font=('arial', 14), bd=10, bg="white")
        lb12.place(rely=0.01, relx=0.05)

        btnGraf = tk.Button(framedestro, text="grafico costi unitari Budget/Consuntivo +/- 50%",font=('arial', 18), width=37, bg="red",command=bottoneGrafico )
        btnGraf.place(rely=0.4,relx=0.075)
        
        tv1["column"] = list(dfImpiegoBudget.columns)
        tv1["show"] = "headings"
        for column in tv1["columns"]:
            tv1.heading(column, text=column)

        df_rows = dfImpiegoBudget.to_numpy().tolist() 
        for row in df_rows:
            tv1.insert("", "end", values=row)

        tv2["column"] = list(dfImpiegoCons.columns)
        tv2["show"] = "headings"
        for column in tv2["columns"]:
            tv2.heading(column, text=column)

        df_rows2 = dfImpiegoCons.to_numpy().tolist() 
        for row in df_rows2:
            tv2.insert("", "end", values=row)

        tv3["column"] = list(dfCostiDirettiBudget.columns)
        tv3["show"] = "headings"
        for column in tv3["columns"]:
            tv3.heading(column, text=column)

        df_rows3 = dfCostiDirettiBudget.to_numpy().tolist()
        for row in df_rows3:
            tv3.insert("", "end", values=row)

        tv4["column"] = list(dfCostiDirettiConsuntivo.columns)
        tv4["show"] = "headings"
        for column in tv4["columns"]:
            tv4.heading(column, text=column)

        df_rows4 = dfCostiDirettiConsuntivo.to_numpy().tolist() 
        for row in df_rows4:
            tv4.insert("", "end", values=row)
        tv5["column"] = list(dfDelta3.columns)
        tv5["show"] = "headings"
        for column in tv5["columns"]:
            tv5.heading(column, text=column) 

        df_rows5 = dfDelta3.to_numpy().tolist()
        for row in df_rows5:
            tv5.insert("", "end", values=row)
    def exit():
        root.destroy()

    def bottoneGrafico():
        temp = dfDelta3.copy()
        temp.set_index('nArticolo', inplace=True)
        figure = temp.plot.bar()
        figure.set_title('costo unitario per articolo Budget/consuntivo')
        figure.set_ylabel('costo')
        figManager = plt.get_current_fig_manager()
        plt.show()
     
    inserisci()
    
    if __name__ == "__main__":
        root.mainloop()