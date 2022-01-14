import tkinter as tk
from numpy import fabs, nan
import pandas as pd
from tkinter import *
import os
import numpy as np
from primaFunzione import funzione_da_bottone1
from secondaFunzione import funzione_da_bottone2
from terzaFunzione import funzione_da_bottone3
from quartaFunzione import funzione_da_bottone4
from pandastable import Table, TableModel

trovato2 = False
trovato1 = False
trovato3 = False
dfImpiegoBudgetDiretto = nan
dfImpiegoConsDiretto = nan
dfConsumiBudget = nan
dfConsumiCons = nan
dfImpiegoBudget = nan
dfImpiegoCons = nan

    
def estrai_codice_valuta(nr, clienti_nr, valuta):
    for i in range(len(clienti_nr)):
        if clienti_nr[i] == nr:
            return valuta[i]
        
def calcolatore(Consumi, Clienti, Budget, Consuntivo, Impiego, Tassi, Vendite):
    consumi_budget_cons = Consumi['Budget/cons']
    consumi_codiceMP = Consumi['Codice MP']
    consumi_nArticolo = Consumi['Nr articolo']
    consumi_nDocumento = Consumi['Nr. documento']
    consumi_quantitaMP = Consumi['Quantità MP impiegata']
    consumi_importo_costo = Consumi['Importo costo (TOTALE)']
    clienti_nr=Clienti['Nr.']
    clienti_valuta=Clienti['Valuta']
    budget_risorsa=Budget['Risorsa']
    budget_area_prod=Budget['Area di produzione']
    budget_costoOrario = Budget['Costo orario (€/h)']
    consuntivo_risorsa=Consuntivo['Risorsa']
    consuntivo_area_prod=Consuntivo['Area di produzione']
    consuntivo_costoOrario = Consuntivo['Costo orario (€/h)']
    tassi_tasso_medio = Tassi['Tasso di cambio medio']

    for i in range(len(tassi_tasso_medio)):
       tassi_tasso_medio[i] = str(tassi_tasso_medio[i])
       tassi_tasso_medio[i] = tassi_tasso_medio[i].replace(',','.')
       tassi_tasso_medio[i] = float(tassi_tasso_medio[i])

    vendite_budget_cons = Vendite['budget/cons']
    vendite_nArticolo = Vendite['Nr articolo']
    vendite_nOrigine = Vendite['Nr. origine']
    vendite_quantita = Vendite['Quantità']
    vendite_totale_vendita = Vendite['Importo vendita in valuta locale (TOTALE VENDITA)']
    impiego_nArticolo = Impiego['nr articolo']
    impiego_budget_cons = Impiego['budget/consuntivo']
    impiego_ordineProduzione = Impiego['Nr. Ordine di produzione']
    impiego_nAreaProduzione = Impiego['Nr. Area di produzione']
    impiego_risorsa = Impiego['Risorsa']
    impiego_tempo_risorsa = Impiego['Tempo risorsa']
    impiego_quant_output = Impiego['Quantità di output']


    

    for i in range(len(vendite_nOrigine)):
        valuta = estrai_codice_valuta(vendite_nOrigine[i], clienti_nr, clienti_valuta)
    
        if valuta == 2:
 
            if vendite_budget_cons[i]=="BUDGET":
                vendite_totale_vendita[i] = vendite_totale_vendita[i] / tassi_tasso_medio[1]
            else:
                vendite_totale_vendita[i] = vendite_totale_vendita[i] / tassi_tasso_medio[4]
        if valuta == 3:
            if vendite_budget_cons[i] == "BUDGET":
                vendite_totale_vendita[i] = vendite_totale_vendita[i] / tassi_tasso_medio[2]
            else:
                vendite_totale_vendita[i] = vendite_totale_vendita[i] / tassi_tasso_medio[5]
    print(tassi_tasso_medio[0])
    print(tassi_tasso_medio[1])
    root = tk.Tk()
    root.title("Controllo di Gestione -- selezionare una funzione")
    root.config(bg="white") 
    width = 485
    height = 320
    root.geometry("485x320")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0, 0)
    
    
     
    def inserisci():
        btn1 = tk.Button(root, text="Analisi vendite per articolo", font=('arial', 18), width=30, bg="red",command=prima_funzione)
        btn1.place(rely=0.1, relx=0.05)
        btn2 = tk.Button(root, text="Analisi vendite per cliente", font=('arial', 18), width=30, bg="red",command=seconda_funzione)
        btn2.place(rely=0.25, relx=0.05)
        btn3 = tk.Button(root, text="Analisi degli scostamenti", font=('arial', 18), width=30, bg="red",command=terza_funzione)
        btn3.place(rely=0.55 ,relx=0.05)
        btn4 = tk.Button(root, text="Analisi dei costi", font=('arial', 18), width=30, bg="red",command=quarta_funzione)
        btn4.place(rely=0.4 ,relx=0.05)
        btnClose = tk.Button(root, text="exit",font=('arial', 18), width=10, bg="red",command=exit )
        btnClose.place(rely=0.85, relx=0.6275)
        
    
    
    def exit():
        root.destroy()

    def prima_funzione():
        funzione_da_bottone1(vendite_budget_cons, vendite_quantita, vendite_nArticolo, vendite_totale_vendita)
        global trovato1
        trovato1 = True
        
    def seconda_funzione():
        funzione_da_bottone2(vendite_budget_cons, vendite_quantita, vendite_nArticolo, vendite_totale_vendita, clienti_nr, clienti_valuta, vendite_nOrigine)
        global trovato2
        trovato2 = True
    def terza_funzione():
        global trovato2, trovato1, trovato3
        if(trovato1 == True and trovato2 == True and trovato3 == True):
            funzione_da_bottone3( vendite_budget_cons, vendite_quantita,
            vendite_nArticolo, vendite_totale_vendita,  dfImpiegoBudgetDiretto, dfImpiegoConsDiretto,
            dfConsumiBudget, dfConsumiCons)
        else:
            lbl = Label(root, text="Prima dell'analisi degli scostamenti bisogna utilizzare\nle altre funzioni", font=('arial', 13), bd=10, bg="white")
            lbl.place(rely=0.68, relx=0.05)  
            inserisci()
    def quarta_funzione():
        global dfImpiegoBudgetDiretto, dfImpiegoConsDiretto,dfConsumiBudget, dfConsumiCons, dfImpiegoBudget, dfImpiegoCons
        dfConsumi = pd.DataFrame({'Budget/cons': consumi_budget_cons,'nArticolo': consumi_nArticolo,'MP': consumi_codiceMP,
                        'Cu_MP': consumi_importo_costo, 'quantità_MP':consumi_quantitaMP, 'ordine_produzione':consumi_nDocumento})
        dfConsumiBudget = dfConsumi.copy()
        dfConsumiBudget = dfConsumiBudget[dfConsumiBudget['Budget/cons']=="BUDGET"]
        dfConsumiCons = dfConsumi.copy()
        dfConsumiCons = dfConsumiCons[dfConsumiCons['Budget/cons']=="CONSUNTIVO"]

        dfConsumiBudget = dfConsumiBudget.groupby(['nArticolo','ordine_produzione'], as_index=False)['Cu_MP','quantità_MP'].sum()
        dfConsumiCons = dfConsumiCons.groupby(['nArticolo','ordine_produzione'], as_index=False)['Cu_MP', 'quantità_MP'].sum()

        dfConsumiBudget['prezzo_x_qtd'] = dfConsumiBudget['Cu_MP'] * dfConsumiBudget['quantità_MP']
        dfConsumiCons['prezzo_x_qtd'] = dfConsumiCons['Cu_MP'] * dfConsumiCons['quantità_MP']

        dfConsumiBudget = dfConsumiBudget.groupby('nArticolo', as_index=False)['prezzo_x_qtd','quantità_MP'].sum()
        dfConsumiCons = dfConsumiCons.groupby('nArticolo', as_index=False)['prezzo_x_qtd','quantità_MP'].sum()

        dfConsumiBudget['Cu_MP(€/u)'] = dfConsumiBudget['prezzo_x_qtd'] / dfConsumiBudget['quantità_MP']
        dfConsumiCons['Cu_MP(€/u)'] = dfConsumiCons['prezzo_x_qtd'] / dfConsumiCons['quantità_MP']

        dfConsumiBudget = dfConsumiBudget.drop(['prezzo_x_qtd','quantità_MP'],1)
        dfConsumiCons = dfConsumiCons.drop(['prezzo_x_qtd','quantità_MP'],1)
        

        
        dfImpiego = pd.DataFrame({'Budget/cons': impiego_budget_cons,'nArticolo': impiego_nArticolo,'risorsa': impiego_risorsa,
                            'nAreaProduzione': impiego_nAreaProduzione, 'qtd_output':impiego_quant_output,'tempo_risorsa':impiego_tempo_risorsa,
                            'ordine_produzione': impiego_ordineProduzione})
        dfImpiegoBudget = dfImpiego.copy()
        dfImpiegoBudget = dfImpiegoBudget[dfImpiegoBudget['Budget/cons']=="BUDGET"]
        dfImpiegoCons = dfImpiego.copy()
        dfImpiegoCons = dfImpiegoCons[dfImpiegoCons['Budget/cons']=="CONSUNTIVO"]
        dfImpiegoConsOutput = dfImpiegoCons.copy()
        dfImpiegoBudgetOutput = dfImpiegoBudget.copy()

        dfCostoOrarioBudget = pd.DataFrame({'risorsa':budget_risorsa,'area_prod':budget_area_prod,'costoOrario_Risorsa':budget_costoOrario})
        dfCostoOrarioCons = pd.DataFrame({'risorsa':consuntivo_risorsa,'area_prod':consuntivo_area_prod,'costoOrario_Risorsa':consuntivo_costoOrario})
        
        index_namesC = dfImpiegoConsOutput[dfImpiegoConsOutput['qtd_output']<=0.0].index
        dfImpiegoConsOutput.drop(index_namesC, inplace=True)
        index_names5 = dfImpiegoBudgetOutput[dfImpiegoBudgetOutput['qtd_output']<=0.0].index
        dfImpiegoBudgetOutput.drop(index_names5, inplace=True)
        index_namesD = dfImpiegoConsOutput[dfImpiegoConsOutput['nAreaProduzione']=='CQ'].index
        dfImpiegoConsOutput.drop(index_namesD, inplace=True)
        index_names6 = dfImpiegoBudgetOutput[dfImpiegoBudgetOutput['nAreaProduzione']=='CQ'].index
        dfImpiegoBudgetOutput.drop(index_names6, inplace=True)

        dfImpiegoBudgetOutput = dfImpiegoBudgetOutput.groupby(['nArticolo','ordine_produzione'], as_index=False)['qtd_output'].min()
        dfImpiegoConsOutput = dfImpiegoConsOutput.groupby(['nArticolo','ordine_produzione'], as_index=False)['qtd_output'].min()

        dfImpiegoBudget = dfImpiegoBudget.groupby(['nArticolo','risorsa','nAreaProduzione','ordine_produzione'], as_index=False)['tempo_risorsa'].sum()
        dfImpiegoCons = dfImpiegoCons.groupby(['nArticolo','risorsa','nAreaProduzione','ordine_produzione'], as_index=False)['tempo_risorsa'].sum()

        dfImpiegoBudget["Costo_orario_risorse_budget"] = np.nan
        dfImpiegoCons["Costo_orario_risorse_consuntivo"] = np.nan
        
        for i in range(len(dfImpiegoBudget)):
            for j in range(len(dfCostoOrarioBudget)):
                if(dfImpiegoBudget['risorsa'][i] == dfCostoOrarioBudget['risorsa'][j] 
                    and dfImpiegoBudget['nAreaProduzione'][i] == dfCostoOrarioBudget['area_prod'][j]):
                    dfImpiegoBudget['Costo_orario_risorse_budget'][i] = float(dfCostoOrarioBudget['costoOrario_Risorsa'][j])

        for i in range(len(dfImpiegoCons)):
            for j in range(len(dfCostoOrarioCons)):
                if(dfImpiegoCons['risorsa'][i] == dfCostoOrarioCons['risorsa'][j] 
                    and dfImpiegoCons['nAreaProduzione'][i] == dfCostoOrarioCons['area_prod'][j]):
                    dfImpiegoCons['Costo_orario_risorse_consuntivo'][i] = float(dfCostoOrarioCons['costoOrario_Risorsa'][j])
        
        dfImpiegoBudget['tempo_x_costoRisorsa(€)'] = dfImpiegoBudget['tempo_risorsa'] * dfImpiegoBudget['Costo_orario_risorse_budget']
        dfImpiegoCons['tempo_x_costoRisorsa(€)'] = dfImpiegoCons['tempo_risorsa'] * dfImpiegoCons['Costo_orario_risorse_consuntivo']
        dfImpiegoBudgetDiretto = dfImpiegoBudget.copy()
        dfImpiegoConsDiretto = dfImpiegoCons.copy()
        dfImpiegoBudgetDiretto = dfImpiegoBudgetDiretto.groupby(['nArticolo','ordine_produzione'], as_index=False)['tempo_x_costoRisorsa(€)'].sum()
        dfImpiegoConsDiretto = dfImpiegoConsDiretto.groupby(['nArticolo','ordine_produzione'], as_index=False)['tempo_x_costoRisorsa(€)'].sum()
        
        dfImpiegoBudgetDiretto["qtd_output"] = np.nan
        dfImpiegoConsDiretto["qtd_output"] = np.nan
        for i in range(len(dfImpiegoConsDiretto)):
            for j in range(len(dfImpiegoConsOutput)):
                if (dfImpiegoConsOutput['nArticolo'][j]==dfImpiegoConsDiretto['nArticolo'][i] and 
                dfImpiegoConsOutput['ordine_produzione'][j]==dfImpiegoConsDiretto['ordine_produzione'][i]):
                    dfImpiegoConsDiretto['qtd_output'][i] = dfImpiegoConsOutput['qtd_output'][j]
        for i in range(len(dfImpiegoBudgetDiretto)):
            for j in range(len(dfImpiegoBudgetOutput)):
                if (dfImpiegoBudgetOutput['nArticolo'][j]==dfImpiegoBudgetDiretto['nArticolo'][i] and 
                dfImpiegoBudgetOutput['ordine_produzione'][j]==dfImpiegoBudgetDiretto['ordine_produzione'][i]):
                    dfImpiegoBudgetDiretto['qtd_output'][i] = dfImpiegoBudgetOutput['qtd_output'][j]

        funzione_da_bottone4(dfImpiegoBudgetDiretto, dfImpiegoConsDiretto,dfConsumiBudget, dfConsumiCons, dfImpiegoBudget, dfImpiegoCons)
        global trovato3
        trovato3 = True
        
    inserisci()
    if __name__ == "__main__":
        root.mainloop()