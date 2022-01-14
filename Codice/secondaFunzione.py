import tkinter as tk
from numpy import NaN
import pandas as pd
from tkinter import *
from dashboard import *
import matplotlib.pyplot as plt
from tkinter import ttk

def funzione_da_bottone2(vendite_budget_cons, vendite_quantita, vendite_nArticolo, vendite_totale_vendita, clienti_nr, clienti_valuta, vendite_nOrigine):
    for i in range(len(vendite_budget_cons)):
        if(vendite_budget_cons[i] == "CONSUNTIVO" ):
            vendite_budget_cons[i] = "Consuntivo"

    df = pd.DataFrame({'Budget/cons': vendite_budget_cons, 'nArticolo': vendite_nArticolo,'id_cliente': vendite_nOrigine,'qtd': vendite_quantita,
                        'totale': vendite_totale_vendita})
    indexNames = df[df['totale']==0].index
    df.drop(indexNames, inplace=True)

    dfbudget = df[df['Budget/cons']=="BUDGET"]
    
    dfbudgetUnit = dfbudget.groupby(['id_cliente', 'nArticolo'], as_index = False)['qtd','totale'].sum()
    dfbudgetUnit["media_unitaria_budget"] = dfbudgetUnit['totale']/dfbudgetUnit['qtd']
    dfbudgetUnitDelta = dfbudgetUnit.copy()
    dfbudgetTerritorio = dfbudgetUnit.copy()
    dfbudgetUnit = dfbudgetUnit.drop(['totale'], 1)
    dfbudgetUnit = dfbudgetUnit.rename(columns= {'qtd' : 'qtd_budget'}) 
    
    dfcons = df[df['Budget/cons']=='Consuntivo']

    dfconsUnit = dfcons.groupby(['id_cliente', 'nArticolo'], as_index=False)['qtd','totale'].sum()
    dfconsUnit["media_unitaria_consuntivo"] = dfconsUnit['totale']/dfconsUnit['qtd']
    dfconsTerritorio = dfconsUnit.copy()
    dfconsUnitDELTA = dfconsUnit.copy()
    dfconsUnit = dfconsUnit.drop(['totale'], 1)
    dfconsUnit = dfconsUnit.rename(columns= {'qtd' : 'qtd_cons'})

    dfUnit = pd.merge(left=dfbudgetUnit, right=dfconsUnit, how='outer',on=['id_cliente','nArticolo'])
    
    dfCliente = pd.DataFrame({'cliente': clienti_nr, 'valuta': clienti_valuta})
    dfCliente = dfCliente.rename(columns= {'cliente':'id_cliente'})
    dfconsTerritorio = pd.merge(left=dfconsTerritorio, right=dfCliente, how='outer', on = 'id_cliente')
    dfbudgetTerritorio = pd.merge(left=dfbudgetTerritorio, right=dfCliente, how='outer', on = 'id_cliente')
    
    dfconsTerritorio = dfconsTerritorio.dropna()
    dfbudgetTerritorio = dfbudgetTerritorio.dropna()
    dfbudgetTerritorio = dfbudgetTerritorio.groupby(['valuta'], as_index=False)['qtd','totale'].sum()
    dfbudgetTerritorio = dfbudgetTerritorio.rename(columns={'totale':'totale_budget','qtd':'qtd_budget'})
    dfconsTerritorio = dfconsTerritorio.groupby(['valuta'], as_index=False)['qtd','totale'].sum()
    dfconsTerritorio = dfconsTerritorio.rename(columns={'totale':'totale_cons','qtd':'qtd_cons'})

    dfconsTerritorio['valuta'] = dfconsTerritorio['valuta'].replace([1,2,3],['euro','dollaro','yen'])
    dfbudgetTerritorio['valuta'] = dfbudgetTerritorio['valuta'].replace([1,2,3],['euro','dollaro','yen'])
    dfTerritorio = pd.merge(left=dfbudgetTerritorio, right=dfconsTerritorio, how='outer', on = 'valuta')
    

    dfdelta = pd.merge(left=dfbudgetUnitDelta, right=dfconsUnitDELTA, how='outer', on='id_cliente')
    dfdelta = dfdelta.drop(['nArticolo_x','nArticolo_y','media_unitaria_budget','media_unitaria_consuntivo',],1)
    dfdelta = dfdelta.groupby(['id_cliente'], as_index=False)['qtd_x','qtd_y','totale_x','totale_y'].sum()
    dfnuoviClienti = dfdelta.copy()
    dfClientipersi= dfdelta.copy()
    '''dfdelta['media_unitaria_budget'] = dfdelta['totale_x']/dfdelta['qtd_x']
    dfdelta['media_unitaria_consuntivo'] = dfdelta['totale_y']/dfdelta['qtd_y']'''
    #dfdelta = dfdelta.drop(['totale_y','totale_x'],1)
    dfdelta = dfdelta.rename(columns={'qtd_x':'qtd_budget','qtd_y':'qtd_cons','totale_x':'totale_budget','totale_y':'totale_cons'})
    dfdelta = dfdelta.fillna(0)
    
    dfdelta['delta_qtd'] = dfdelta['qtd_cons'] - dfdelta['qtd_budget']
    dfdelta['delta_totale'] = dfdelta['totale_cons'] - dfdelta['totale_budget']
    dfdelta = dfdelta.drop(['totale_cons','totale_budget','qtd_budget','qtd_cons'],1)
    dfnuoviClienti = dfnuoviClienti.fillna(0)
    dfClientipersi = dfClientipersi.fillna(0)
    index_names4 =  dfnuoviClienti[dfnuoviClienti['qtd_x']>0.0].index
    dfnuoviClienti.drop(index_names4, inplace=True)
    index_names5 = dfClientipersi[dfClientipersi['qtd_y']>0.0].index
    dfClientipersi.drop(index_names5, inplace=True)
    
    dfClientipersi = dfClientipersi.drop(['qtd_x','qtd_y','totale_x','totale_y'],1)
    dfClientipersi = dfClientipersi.rename(columns={'id_cliente' : 'clienti_registrati_solo_a_budget (persi)'})
    dfnuoviClienti=dfnuoviClienti.drop(['qtd_x','qtd_y','totale_x','totale_y'],1)
    dfnuoviClienti = dfnuoviClienti.rename(columns={'id_cliente' : 'clienti_registrati_solo_a_consuntivo (nuovi)'})
    
    root = tk.Tk()
    root.title("Controllo di Gestione -- Analisi vendite per cliente")
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

    frame1 = tk.LabelFrame(root, text="divisione del nostro dataframe con doppia chiave: cliente e articolo / BUDGET CONSUNTIVO", bg="white")
    frame1.place(height=220, width=640,rely=0.0, relx=0)
    frame2 = tk.LabelFrame(root, text="delta media totale vendita e quantità per cliente ", bg="white")
    frame2.place(height=220, width=640,rely=0.33, relx=0)
    frame3 = tk.LabelFrame(root, text="totale vendite e quantità per TERRITORIO / BUDGET", bg="white")
    frame3.place(height=220, width=310,rely=0.65, relx=0)
    frame4 = tk.LabelFrame(root, text="totale vendite e quantità per TERRITORIO / CONSUNTIVO", bg="white")
    frame4.place(height=220, width=311,rely=0.65, relx=0.275)
    frameMezzo = tk.LabelFrame(root, text="Lista Clienti presenti a budget ma non a consuntivo (CL PERSI!)", bg="white")
    frameMezzo.place(height=220, width=280,rely=0.33, relx=0.5333333)
    frameMezzo2 = tk.LabelFrame(root, text="Lista Clienti presenti a consuntivo ma non a budget (CL ACQUISITI!)", bg="white")
    frameMezzo2.place(height=220, width=280,rely=0.33, relx=0.766666)
    frameBottoni = tk.LabelFrame(root, bg="white")
    frameBottoni.place(height=220, width=560,rely=0.0, relx=0.5333333)
    frameRisultati = tk.LabelFrame(root, bg="white")
    frameRisultati.place(height=220, width=560,rely=0.65, relx=0.5333333)
    tv1 = ttk.Treeview(frame1)
    tv1.place(relheight=1, relwidth=1)
    tv2 = ttk.Treeview(frame2)
    tv2.place(relheight=1, relwidth=1)
    treescrolly1 = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview) 
    treescrollx1 = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview)
    treescrolly2 = tk.Scrollbar(frame2, orient="vertical", command=tv2.yview) 
    treescrollx2 = tk.Scrollbar(frame2, orient="horizontal", command=tv2.xview) 
    tv1.configure(xscrollcommand=treescrollx1.set, yscrollcommand=treescrolly1.set) 
    tv2.configure(xscrollcommand=treescrollx2.set, yscrollcommand=treescrolly2.set)
    treescrollx1.pack(side="bottom", fill="x") 
    treescrolly1.pack(side="right", fill="y") 
    treescrollx2.pack(side="bottom", fill="x") 
    treescrolly2.pack(side="right", fill="y")
    tv3 = ttk.Treeview(frame3)
    tv3.place(relheight=1, relwidth=1)
    tv4 = ttk.Treeview(frame4)
    tv4.place(relheight=1, relwidth=1)
    treescrolly3 = tk.Scrollbar(frame3, orient="vertical", command=tv3.yview) 
    treescrollx3 = tk.Scrollbar(frame3, orient="horizontal", command=tv3.xview) 
    treescrolly4 = tk.Scrollbar(frame4, orient="vertical", command=tv4.yview) 
    treescrollx4 = tk.Scrollbar(frame4, orient="horizontal", command=tv4.xview) 
    tv3.configure(xscrollcommand=treescrollx3.set, yscrollcommand=treescrolly3.set) 
    tv4.configure(xscrollcommand=treescrollx4.set, yscrollcommand=treescrolly4.set)
    treescrollx3.pack(side="bottom", fill="x") 
    treescrolly3.pack(side="right", fill="y") 
    treescrollx4.pack(side="bottom", fill="x") 
    treescrolly4.pack(side="right", fill="y")
    tv5 = ttk.Treeview(frameMezzo)
    tv5.place(relheight=1, relwidth=1)
    tv6 = ttk.Treeview(frameMezzo2)
    tv6.place(relheight=1, relwidth=1)
    treescrolly5 = tk.Scrollbar(frameMezzo, orient="vertical", command=tv5.yview) 
    treescrollx5 = tk.Scrollbar(frameMezzo, orient="horizontal", command=tv5.xview)
    treescrolly6 = tk.Scrollbar(frameMezzo2, orient="vertical", command=tv6.yview) 
    treescrollx6 = tk.Scrollbar(frameMezzo2, orient="horizontal", command=tv6.xview) 
    tv5.configure(xscrollcommand=treescrollx5.set, yscrollcommand=treescrolly5.set) 
    tv6.configure(xscrollcommand=treescrollx6.set, yscrollcommand=treescrolly6.set)
    treescrollx5.pack(side="bottom", fill="x") 
    treescrolly5.pack(side="right", fill="y") 
    treescrollx6.pack(side="bottom", fill="x") 
    treescrolly6.pack(side="right", fill="y")
    def inserisci():
        btnGrafico2 = tk.Button(frameBottoni, text="Grafico delta quantità e \n totale prezzo di vendita per cliente",
            font=('arial', 18), width=34, bg="red",command=bottoneGraf2 )
        btnGrafico2.place(rely=0.4,relx=0.01)
        btnGrafico1 = tk.Button(frameBottoni, text="Grafico budget/cons prezzo totale di vendita \n e quantità totale diviso per Territorio",
            font=('arial', 18), width=34, bg="red",command=bottoneGraf1 )
        btnGrafico1.place(rely=0,relx=0.01)
        lb1 = Label(frameRisultati, text="La Nostra vendita è incentrata in luoghi dove si utilizza: " +str(funzioneValuta())+ ", "+
        " \n  a Budget ed a Consuntivo viene confermata questa assunzione ", font=('arial', 13), bd=10, bg="white")
        lb1.place(rely=0.00, relx=0.01)
        lb2 = Label(frameRisultati, text="DELTA (Consuntivo-Budget) Dollaro: " + "\nQuantità--> "+ str(int(dfconsTerritorio['qtd_cons'][1]-dfbudgetTerritorio['qtd_budget'][1])) +" ("
            +str(int((dfconsTerritorio['qtd_cons'][1]/dfbudgetTerritorio['qtd_budget'][1])*100)-100)+ "%)  Totale-->" +str(int(dfconsTerritorio['totale_cons'][1]-dfbudgetTerritorio['totale_budget'][1]))+'€'
            +"  ("+str(int(dfconsTerritorio['totale_cons'][1]/dfbudgetTerritorio['totale_budget'][1]*100 -100))+"%)", font=('arial', 13), bd=10, bg="white")
        lb2.place(rely=0.25, relx=0.03)
        lb3 = Label(frameRisultati, text="DELTA (Consuntivo-Budget) Euro: " +"\nQuantità--> "+ str(int(dfconsTerritorio['qtd_cons'][0]-dfbudgetTerritorio['qtd_budget'][0])) + " ("
            +str(int((dfconsTerritorio['qtd_cons'][0]/dfbudgetTerritorio['qtd_budget'][0])*100)-100)+ "%)  Totale-->" + str(int(dfconsTerritorio['totale_cons'][0]-dfbudgetTerritorio['totale_budget'][0]))+'€'
            +"  ("+str(int(dfconsTerritorio['totale_cons'][0]/dfbudgetTerritorio['totale_budget'][0]*100 -100))+"%)", font=('arial', 13), bd=10, bg="white")
        lb3.place(rely=0.5, relx=0.03)
        lb4 = Label(frameRisultati, text="DELTA (Consuntivo-Budget) Yen: "+ "\nQuantità--> "+ str(int(dfconsTerritorio['qtd_cons'][2]-dfbudgetTerritorio['qtd_budget'][2])) + " ("
            +str(int((dfconsTerritorio['qtd_cons'][2]/dfbudgetTerritorio['qtd_budget'][2])*100)-100)+ "%)  Totale-->" + str(int(dfconsTerritorio['totale_cons'][2]-dfbudgetTerritorio['totale_budget'][2]))+'€'
            +"  ("+str(int(dfconsTerritorio['totale_cons'][2]/dfbudgetTerritorio['totale_budget'][2]*100 -100))+"%)", font=('arial', 13), bd=10, bg="white")
        lb4.place(rely=0.75, relx=0.03)
        btnClose = tk.Button(frameRisultati, text="exit",font=('arial', 18), width=10, bg="red",command=exit )
        btnClose.place(rely=0.75, relx=0.733)

        tv1["column"] = list(dfUnit.columns)
        tv1["show"] = "headings"
        for column in tv1["columns"]:
            tv1.heading(column, text=column) 

        df_rows = dfUnit.to_numpy().tolist() 
        for row in df_rows:
            tv1.insert("", "end", values=row)
        tv2["column"] = list(dfdelta.columns)
        tv2["show"] = "headings"
        for column in tv2["columns"]:
            tv2.heading(column, text=column) 

        df_rows2 = dfdelta.to_numpy().tolist() 
        for row in df_rows2:
            tv2.insert("", "end", values=row)
        
        tv3["column"] = list(dfbudgetTerritorio.columns)
        tv3["show"] = "headings"
        for column in tv3["columns"]:
            tv3.heading(column, text=column) 

        df_rows = dfbudgetTerritorio.to_numpy().tolist() 
        for row in df_rows:
            tv3.insert("", "end", values=row)
        tv4["column"] = list(dfconsTerritorio.columns)
        tv4["show"] = "headings"
        for column in tv4["columns"]:
            tv4.heading(column, text=column) 

        df_rows2 = dfconsTerritorio.to_numpy().tolist()
        for row in df_rows2:
            tv4.insert("", "end", values=row)

        tv5["column"] = list(dfClientipersi.columns)
        tv5["show"] = "headings"
        for column in tv5["columns"]:
            tv5.heading(column, text=column) 

        df_rows = dfClientipersi.to_numpy().tolist()
        for row in df_rows:
            tv5.insert("", "end", values=row)

        tv6["column"] = list(dfnuoviClienti.columns)
        tv6["show"] = "headings"
        for column in tv6["columns"]:
            tv6.heading(column, text=column) 

        df_rows2 = dfnuoviClienti.to_numpy().tolist() 
        for row in df_rows2:
            tv6.insert("", "end", values=row)
    
    def bottoneGraf1():
        temp = dfTerritorio.copy()
        temp.set_index('valuta', inplace=True)
        figures, axes = plt.subplots(1,2)
        prova = temp.plot.bar(y=['qtd_budget','qtd_cons'],ax=axes[0])
        prova2 = temp.plot.bar(y=['totale_budget','totale_cons'],ax=axes[1])
        prova.set_title('quantità di articoli venduta in base al territorio')
        prova.set_ylabel('quantità')
        prova.set_xlabel('Territori')
        prova2.set_title(' totale vendite in base al territorio')
        prova2.set_ylabel('Totale Vendite')
        prova2.set_xlabel('Territori')
        plt.show()
    def bottoneGraf2():
        figure, axes = plt.subplots(1, 2)
        temp2a = dfdelta.copy()
        temp2a = temp2a.drop(['delta_totale'],1)
        temp2a.set_index('id_cliente',inplace=True)
        temp3a = dfdelta.copy()
        temp3a = temp3a.drop(['delta_qtd'],1)
        temp3a.set_index('id_cliente',inplace=True)
        prova3 = temp2a.plot.barh(ax =axes[0])
        prova4 = temp3a.plot.barh(ax =axes[1])
        prova3.set_title('delta delle quantità tra bud/cons per cliente')
        prova3.set_ylabel('clienti')
        prova3.set_xlabel('quantità (unità)')
        prova4.set_title('delta delle totale dei prezzi di vendita tra bud/cons per cliente')
        prova4.set_ylabel('clienti')
        prova4.set_xlabel('totale prezzo di vendita (€)')
        plt.show()
    def exit():
        root.destroy()
    def funzioneValuta():
       
      if dfbudgetTerritorio['totale_budget'][0]>dfbudgetTerritorio['totale_budget'][1] and dfbudgetTerritorio['totale_budget'][0]> dfbudgetTerritorio['totale_budget'][2]:
          return (dfbudgetTerritorio['valuta'][0])
      elif dfbudgetTerritorio['totale_budget'][1]>dfbudgetTerritorio['totale_budget'][0] and dfbudgetTerritorio['totale_budget'][1]>dfbudgetTerritorio['totale_budget'][2]:
               return (dfbudgetTerritorio['valuta'][1])
      else:
             return (dfbudgetTerritorio['valuta'][2])    
    


    inserisci()
    if __name__ == "__main__":
        root.mainloop()
