import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import *
import numpy as np
from quintaFunzione import funzione_5
def funzione_da_bottone3( vendite_budget_cons, vendite_quantita,
            vendite_nArticolo, vendite_totale_vendita,  dfImpiegoBudgetDiretto, dfImpiegoConsDiretto,
            dfConsumiBudget, dfConsumiCons):
    
    dfImpiegoBudget = dfImpiegoBudgetDiretto.copy()
    dfImpiegoCons = dfImpiegoConsDiretto.copy()
    dfImpiegoBudgetDiretto['Cu_risorse(€/u)'] = dfImpiegoBudgetDiretto['tempo_x_costoRisorsa(€)'] / dfImpiegoBudgetDiretto['qtd_output']
    dfImpiegoConsDiretto['Cu_risorse(€/u)'] = dfImpiegoConsDiretto['tempo_x_costoRisorsa(€)'] / dfImpiegoConsDiretto['qtd_output']

    dfImpiegoBudgetDiretto = dfImpiegoBudgetDiretto.groupby('nArticolo', as_index=False)['Cu_risorse(€/u)'].mean()
    dfImpiegoConsDiretto = dfImpiegoConsDiretto.groupby('nArticolo', as_index=False)['Cu_risorse(€/u)'].mean()
   
    
    dfCostiDirettiBudget = pd.merge(left=dfImpiegoBudgetDiretto, right=dfConsumiBudget, how='outer', on='nArticolo')
    dfCostiDirettiConsuntivo = pd.merge(left=dfImpiegoConsDiretto, right=dfConsumiCons, how='outer', on='nArticolo')
    dfCostiDirettiBudget['Cu_totale(€/u)'] = dfCostiDirettiBudget['Cu_risorse(€/u)'] + dfCostiDirettiBudget['Cu_MP(€/u)']
    dfCostiDirettiConsuntivo['Cu_totale(€/u)'] = dfCostiDirettiConsuntivo['Cu_risorse(€/u)'] + dfCostiDirettiConsuntivo['Cu_MP(€/u)']
    dfCostiDirettiBudget = dfCostiDirettiBudget.fillna(0)
    dfCostiDirettiConsuntivo = dfCostiDirettiConsuntivo.fillna(0)

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
    
    dfCostiDirettiBudget = dfCostiDirettiBudget.rename(columns={'Cu_totale(€/u)':'Cu_Budget'})
    dfCostiDirettiBudget = dfCostiDirettiBudget.drop(['Cu_risorse(€/u)','Cu_MP(€/u)'],1)
    dfBUDGET = pd.merge(left=dfDaVedereBudget, right=dfCostiDirettiBudget, how='outer', on='nArticolo')
    dfCostiDirettiConsuntivo = dfCostiDirettiConsuntivo.rename(columns={'Cu_totale(€/u)':'Cu_Consuntivo'})
    dfCostiDirettiConsuntivo = dfCostiDirettiConsuntivo.drop(['Cu_risorse(€/u)','Cu_MP(€/u)'],1)
    dfCONSUNTIVO = pd.merge(left=dfDaVedereCons, right=dfCostiDirettiConsuntivo, how='outer', on='nArticolo')
    dfBUDGET = dfBUDGET.rename(columns={'media_unitaria':'Pu_Budget','qtd':'qtd_Budget'})
    dfCONSUNTIVO = dfCONSUNTIVO.rename(columns={'media_unitaria':'Pu_Consuntivo','qtd':'qtd_Consuntivo'})

    dfCONSUNTIVO.loc[len(dfCONSUNTIVO)] = ['totale', dfCONSUNTIVO['qtd_Consuntivo'].sum(), dfCONSUNTIVO['Pu_Consuntivo'].sum(), dfCONSUNTIVO['Cu_Consuntivo'].sum() ]
    dfBUDGET.loc[len(dfBUDGET)] = ['totale', dfBUDGET['qtd_Budget'].sum(), dfBUDGET['Pu_Budget'].sum(), dfBUDGET['Cu_Budget'].sum()]
    
    dfBUDGET['mix_prod_budget'] = dfBUDGET['qtd_Budget']/dfBUDGET.iloc[-1]['qtd_Budget']
    dfCONSUNTIVO['mix_prod_cons'] = dfCONSUNTIVO['qtd_Consuntivo']/dfCONSUNTIVO.iloc[-1]['qtd_Consuntivo']
    dfBUDGET = dfBUDGET.dropna()
    dfCONSUNTIVO = dfCONSUNTIVO.dropna()

    MIX_STANDARD = pd.DataFrame({'nArticolo': dfBUDGET['nArticolo'],'qtd_MixStandard': np.nan,'Pu_MixStandard':dfBUDGET['Pu_Budget'],
        'Cu_MixStandard':dfBUDGET['Cu_Budget'],'mix_prod_MixStandard':dfBUDGET['mix_prod_budget']})
    a = dfCONSUNTIVO.iloc[-1]['qtd_Consuntivo']
    MIX_STANDARD.at[504,'qtd_MixStandard'] = a
    for i in range(len(MIX_STANDARD)-1):
        MIX_STANDARD['qtd_MixStandard'][i] = MIX_STANDARD['mix_prod_MixStandard'][i] * MIX_STANDARD.iloc[-1]['qtd_MixStandard']
    
    MIX_EFFETTIVO = pd.DataFrame({'nArticolo': dfBUDGET['nArticolo'], 'qtd_MixEffettivo':dfCONSUNTIVO['qtd_Consuntivo'],
        'Pu_MixEffettivo':dfBUDGET['Pu_Budget'],'Cu_MixEffettivo':dfBUDGET['Cu_Budget'], 'mix_prod_MixEffettivo':dfCONSUNTIVO['mix_prod_cons']})

    ricavi_budget = 0
    costi_budget = 0
    for i in range(len(dfBUDGET)-1):
        ricavi_budget = ricavi_budget + (dfBUDGET['qtd_Budget'][i] * dfBUDGET['Pu_Budget'][i])
        costi_budget = costi_budget + (dfBUDGET['qtd_Budget'][i] * dfBUDGET['Cu_Budget'][i])
    
    ricavi_mixStandard= 0
    costi_mixStandard = 0
    for i in range(len(MIX_STANDARD)-1):
        ricavi_mixStandard = ricavi_mixStandard + (MIX_STANDARD['qtd_MixStandard'][i] * MIX_STANDARD['Pu_MixStandard'][i])
        costi_mixStandard = costi_mixStandard + (MIX_STANDARD['qtd_MixStandard'][i] * MIX_STANDARD['Cu_MixStandard'][i])
    
    ricavi_mixEffettivo  = 0
    costi_mixEffettivo = 0
    for i in range(len(MIX_EFFETTIVO)-1):
        ricavi_mixEffettivo = ricavi_mixEffettivo + (MIX_EFFETTIVO['qtd_MixEffettivo'][i] * MIX_EFFETTIVO['Pu_MixEffettivo'][i])
        costi_mixEffettivo = costi_mixEffettivo + (MIX_EFFETTIVO['qtd_MixEffettivo'][i] * MIX_EFFETTIVO['Cu_MixEffettivo'][i])
    
    ricavi_consuntivo = 0
    costi_consuntivo = 0
    for i in range(len(dfCONSUNTIVO)-1):
        ricavi_consuntivo = ricavi_consuntivo + (dfCONSUNTIVO['qtd_Consuntivo'][i] * dfCONSUNTIVO['Pu_Consuntivo'][i])
        costi_consuntivo = costi_consuntivo + (dfCONSUNTIVO['qtd_Consuntivo'][i] * dfCONSUNTIVO['Cu_Consuntivo'][i])
    
    mol_budget = ricavi_budget - costi_budget
    mol_mixStandard = ricavi_mixStandard - costi_mixStandard
    mol_mixEffettivo = ricavi_mixEffettivo - costi_mixEffettivo
    mol_consuntivo = ricavi_consuntivo - costi_consuntivo

    delta_ricavi_mixStandard_budget = ricavi_mixStandard - ricavi_budget
    delta_ricavi_mixEffettivo_mixStandard = ricavi_mixEffettivo - ricavi_mixStandard
    delta_ricavi_consuntivo_mixEffettivo = ricavi_consuntivo - ricavi_mixEffettivo

    delta_costi_mixStandard_budget = costi_mixStandard - costi_budget
    delta_costi_mixEffettivo_mixStandard = costi_mixEffettivo - costi_mixStandard
    delta_costi_consuntivo_mixEffettivo = costi_consuntivo - costi_mixEffettivo

    delta_mol_mixStandard_budget = mol_mixStandard - mol_budget
    delta_mol_mixEffettivo_mixStandard = mol_mixEffettivo - mol_mixStandard
    delta_mol_consuntivo_mixEffettivo = mol_consuntivo - mol_mixEffettivo 
    Cambio_prezzi_costi = mol_consuntivo - mol_budget

    dfMdC = pd.DataFrame({'nArticolo': dfBUDGET['nArticolo']})
    dfMdC['MdC_budget_unitario'] = dfBUDGET['Pu_Budget'] - dfBUDGET['Cu_Budget']
    dfMdC['MdC_budget_qtd']   = (dfBUDGET['Pu_Budget'] - dfBUDGET['Cu_Budget']) * dfBUDGET['qtd_Budget']
    dfMdC['MdC_consuntivo_unitario'] = dfCONSUNTIVO['Pu_Consuntivo'] - dfCONSUNTIVO['Cu_Consuntivo']
    dfMdC['MdC_consuntivo_qtd']   = (dfCONSUNTIVO['Pu_Consuntivo'] - dfCONSUNTIVO['Cu_Consuntivo']) * dfCONSUNTIVO['qtd_Consuntivo']
    
    index_names5 = dfMdC[dfMdC['nArticolo']=='totale'].index
    dfMdC.drop(index_names5, inplace=True)
    dfMdC.loc[len(dfMdC)] = ['totale', dfMdC['MdC_budget_unitario'].sum(), dfMdC['MdC_budget_qtd'].sum(), dfMdC['MdC_consuntivo_unitario'].sum(), dfMdC['MdC_consuntivo_qtd'].sum() ]
    
    root = tk.Tk()
    root.title("Controllo di Gestione -- Analisi degli scostamenti")
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
    frameLabel = tk.LabelFrame(root, bg="white")
    frameLabel.place(height=538, width=590, rely=0.228571428, relx=0.5 )
    frame1 = tk.LabelFrame(root, text="MdC tra budget e consuntivo", bg="white")
    frame1.place(height=160, width=590,rely=0.0, relx=0.5)
    tv1 = ttk.Treeview(frame1)
    style = ttk.Style(tv1)
    style.theme_use("clam")
    tv1.place(relheight=1, relwidth=1)
    treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview) 
    treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview)
    tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
    treescrollx.pack(side="bottom", fill="x") 
    treescrolly.pack(side="right", fill="y")
    tv1.tag_configure('red', background='red')
    tv1.tag_configure('green',background='green')
    tv1.tag_configure('aqua',background='aqua')
    tv1.tag_configure('yellow',background='yellow')
    frame2 = tk.LabelFrame(root, text="Analisi a BUDGET", bg="white")
    frame2.place(height=160, width=590,rely=0.0, relx=0)
    tv2 = ttk.Treeview(frame2)
    style2 = ttk.Style(tv2)
    style2.theme_use("clam")
    tv2.place(relheight=1, relwidth=1)
    treescrolly2 = tk.Scrollbar(frame2, orient="vertical", command=tv2.yview) 
    treescrollx2 = tk.Scrollbar(frame2, orient="horizontal", command=tv2.xview)
    tv2.configure(xscrollcommand=treescrollx2.set, yscrollcommand=treescrolly2.set)
    treescrollx2.pack(side="bottom", fill="x") 
    treescrolly2.pack(side="right", fill="y")
    tv2.tag_configure('red', background='red')
    tv2.tag_configure('green',background='green')
    frame3 = tk.LabelFrame(root, text="Analisi a MIX STANDARD", bg="white")
    frame3.place(height=160, width=590,rely=0.25, relx=0)
    tv3 = ttk.Treeview(frame3)
    style3 = ttk.Style(tv3)
    style3.theme_use("clam")
    tv3.place(relheight=1, relwidth=1)
    treescrolly3 = tk.Scrollbar(frame3, orient="vertical", command=tv3.yview) 
    treescrollx3 = tk.Scrollbar(frame3, orient="horizontal", command=tv3.xview)
    tv3.configure(xscrollcommand=treescrollx3.set, yscrollcommand=treescrolly3.set)
    treescrollx3.pack(side="bottom", fill="x") 
    treescrolly3.pack(side="right", fill="y")
    tv3.tag_configure('red', background='red')
    tv3.tag_configure('green',background='green')
    frame4 = tk.LabelFrame(root, text="Analisi a MIX EFFETTIVO", bg="white")
    frame4.place(height=160, width=590,rely=0.5, relx=0)
    tv4 = ttk.Treeview(frame4)
    style4 = ttk.Style(tv4)
    style4.theme_use("clam")
    tv4.place(relheight=1, relwidth=1)
    treescrolly4 = tk.Scrollbar(frame4, orient="vertical", command=tv4.yview) 
    treescrollx4 = tk.Scrollbar(frame4, orient="horizontal", command=tv4.xview)
    tv4.configure(xscrollcommand=treescrollx4.set, yscrollcommand=treescrolly4.set)
    treescrollx4.pack(side="bottom", fill="x") 
    treescrolly4.pack(side="right", fill="y")
    tv4.tag_configure('red', background='red')
    tv4.tag_configure('green',background='green')

    frame5 = tk.LabelFrame(root, text="Analisi a CONSUNTIVO", bg="white")
    frame5.place(height=160, width=590,rely=0.75, relx=0)
    tv5 = ttk.Treeview(frame5)
    style5 = ttk.Style(tv5)
    style5.theme_use("clam")
    tv5.place(relheight=1, relwidth=1)
    treescrolly5 = tk.Scrollbar(frame5, orient="vertical", command=tv5.yview) 
    treescrollx5 = tk.Scrollbar(frame5, orient="horizontal", command=tv5.xview)
    tv5.configure(xscrollcommand=treescrollx5.set, yscrollcommand=treescrolly5.set)
    treescrollx5.pack(side="bottom", fill="x") 
    treescrolly5.pack(side="right", fill="y")
    tv5.tag_configure('red', background='red')
    tv5.tag_configure('green',background='green')
    def inserisci():
        count1 = -1
        count2 = 0
        count3 = 0
        count4 = 0
        tv1["column"] = list(dfMdC.columns)
        tv1["show"] = "headings"
        for column in tv1["columns"]:
            tv1.heading(column, text=column) 
        df_rows = dfMdC.to_numpy().tolist() 
        for row in range(0,414): 
            if(dfMdC['MdC_budget_unitario'][row]<=0 and dfMdC['MdC_consuntivo_unitario'][row]<=0):
                tv1.insert("", "end", values=df_rows[row], tags=('red',))
                count1 = count1 +1
            if(dfMdC['MdC_budget_unitario'][row]>0 and dfMdC['MdC_consuntivo_unitario'][row]>0):
                tv1.insert("", "end", values=df_rows[row],  tags=('green',)) 
                count2 = count2 +1
            if((dfMdC['MdC_budget_unitario'][row]<=0 and dfMdC['MdC_consuntivo_unitario'][row]>0)):
                tv1.insert("", "end", values=df_rows[row], tags=('aqua',))
                count3 =  count3 +1
            if((dfMdC['MdC_budget_unitario'][row]>0 and dfMdC['MdC_consuntivo_unitario'][row] <=0)):
                tv1.insert("", "end", values=df_rows[row], tags=('yellow',))
                count4 =  count4 +1

        tv2["column"] = list(dfBUDGET.columns)
        tv2["show"] = "headings"
        for column in tv2["columns"]:
            tv2.heading(column, text=column) 

        df_rows = dfBUDGET.to_numpy().tolist() 
        for row in df_rows:
            tv2.insert("", "end", values=row)

        tv3["column"] = list(MIX_STANDARD.columns)
        tv3["show"] = "headings"
        for column in tv3["columns"]:
            tv3.heading(column, text=column) 

        df_rows = MIX_STANDARD.to_numpy().tolist() 
        for row in df_rows:
            tv3.insert("", "end", values=row)

        tv4["column"] = list(MIX_EFFETTIVO.columns)
        tv4["show"] = "headings"
        for column in tv4["columns"]:
            tv4.heading(column, text=column) 

        df_rows = MIX_EFFETTIVO.to_numpy().tolist() 
        for row in df_rows:
            tv4.insert("", "end", values=row)

        tv5["column"] = list(dfCONSUNTIVO.columns)
        tv5["show"] = "headings"
        for column in tv5["columns"]:
            tv5.heading(column, text=column) 

        df_rows = dfCONSUNTIVO.to_numpy().tolist() 
        for row in df_rows:
            tv5.insert("", "end", values=row)
        lb1 = Label(frameLabel, text="Il totale a budget è: -Ricavi " + str(int(ricavi_budget))+"€"
            +"  -Costi "+ str(int(costi_budget))+"€"+ "\nIl totale a Mix Standard è: -Ricavi "+
            str(int(ricavi_mixStandard))+"€"+"  -Costi "+str(int(costi_mixStandard))+"€" +
            "\nIl totale a Mix Effettivo è: -Ricavi "+
            str(int(ricavi_mixEffettivo))+"€"+"  -Costi "+str(int(costi_mixEffettivo))+"€"+
            "\nIl totale a Consuntivo è: -Ricavi "+
            str(int(ricavi_consuntivo))+"€"+"  -Costi "+str(int(costi_consuntivo))+"€"
            +"\n\nMargine operativo lordo (MOL): -Budget "+str(int(mol_budget))+"€"
            +"\n     -Mix Standard "+str(int(mol_mixStandard))+"€"
            +"\n     -Mix Effettivo "+str(int(mol_mixEffettivo))+"€"
            +"\n     -Consuntivo "+str(int(mol_consuntivo))+"€"
            +"\n\nDelta ricavi: Mix Standard - Budget: "+str(int(delta_ricavi_mixStandard_budget))+"€"
               +" ( "+str(int(int(ricavi_mixStandard)/int(ricavi_budget)*100 -100))+"%)"
            +"\n     Mix Effettivo - Mix Standard "+str(int(delta_ricavi_mixEffettivo_mixStandard))+"€"
            +" ( "+str(int(int(ricavi_mixEffettivo)/int(ricavi_mixStandard)*100 -100))+"%)"
            +"\n     Consuntivo - Mix Effettivo "+str(int(delta_ricavi_consuntivo_mixEffettivo))+"€"
            +" ( "+str(int(int(ricavi_consuntivo)/int(ricavi_mixEffettivo)*100 -100))+"%)"
            +"\nDelta costi: Mix Standard - Budget: "+str(int(delta_costi_mixStandard_budget))+"€"
            +" ( "+str(int(int(costi_mixStandard)/int(costi_budget)*100 -100))+"%)"
            +"\n     Mix Effettivo - Mix Standard "+str(int(delta_costi_mixEffettivo_mixStandard))+"€"
            +" ( "+str(int(int(costi_mixEffettivo)/int(costi_mixStandard)*100 -100))+"%)"
            +"\n     Consuntivo - Mix Effettivo "+str(int(delta_costi_consuntivo_mixEffettivo))+"€"
            +" ( "+str(int(int(costi_consuntivo)/int(costi_mixEffettivo)*100 -100))+"%)"
            +"\nDelta MOL: Mix Standard - Budget: "+str(int(delta_mol_mixStandard_budget))+"€"
            +" ( -"+str(int(int(mol_mixStandard)/int(mol_budget)*100 -100))+"%)"
            +"\n     Mix Effettivo - Mix Standard "+str(int(delta_mol_mixEffettivo_mixStandard))+"€"
            +" ( -"+str(int(int(mol_mixEffettivo)/int(mol_mixStandard)*100 -100))+"%)"
            +"\n     Consuntivo - Mix Effettivo "+str(int(delta_mol_consuntivo_mixEffettivo))+"€"
            +" ( -"+str(int(int(mol_consuntivo)/int(mol_mixEffettivo)*100 -100))+"%)"
            +"\n\nCambio Prezzi/Costi (MOL Consuntivo - MOL Budget) "+str(int(Cambio_prezzi_costi))+"€"
            +"\n(variazione percentuale=  -"+str(int(int(mol_consuntivo)/int(mol_budget)*100 -100))+"%)"
            +"\n\nAnalisi Margine di Contribuzione unitari: "
            +"\nMdC unitari negativi a Budget e a Consuntivo: "+str(int(count1))+" (valori in rosso nella tabella MdC)"
            +"\nMdC unitari positivi a Budget e a Consuntivo: "+str(int(count2))+" (valori in verde nella tabella MdC)"
            +"\nMdC unitari negativi a Budget e positivi a Consuntivo: "+str(int(count3))+" (valori in azzurro nella tabella MdC)"
            +"\nMdC unitari positivi a Budget e negativi a Consuntivo: "+str(int(count4))+" (valori in giallo nella tabella MdC)",font=('arial', 10), bd=10, bg="white", anchor='center')
        lb1.place(rely=0.0, relx=0.087)

        btnClose = tk.Button(frameLabel, text="exit",font=('arial', 18), width=10, bg="red",command=exit )
        btnClose.place(rely=0.91, relx=0.762)
        btnQtd = tk.Button(frameLabel, text="comparare quantità prodotte e vendute",font=('arial', 18), width=30, bg="red",command=quintaFunz)
        btnQtd.place(rely=0.91, relx=0.0)
    def quintaFunz():
        funzione_5(dfImpiegoBudget, dfImpiegoCons, df2, df3)

    def exit():
        root.destroy()

        
    inserisci()
    if __name__ == "__main__":
        root.mainloop()