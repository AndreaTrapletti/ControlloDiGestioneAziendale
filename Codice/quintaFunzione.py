import tkinter as tk
import pandas as pd
from tkinter import Label, ttk

def funzione_5(dfImpiegoBudget, dfImpiegoCons, df2, df3):
    
    dfImpiegoBudget = dfImpiegoBudget.groupby('nArticolo', as_index=False)['qtd_output'].sum()
    dfImpiegoCons = dfImpiegoCons.groupby('nArticolo', as_index=False)['qtd_output'].sum()
    dfImpiegoBudget = dfImpiegoBudget.rename(columns={'qtd_output':'qtd'})
    dfImpiegoCons = dfImpiegoCons.rename(columns={'qtd_output':'qtd'})
    df3 = df3.drop(['totale'],1)
    df2 = df2.drop(['totale'],1)
    dfQtdBudget = pd.merge(left=dfImpiegoBudget, right=df2, how='outer', on='nArticolo', suffixes=['_produzione','_venduta'])
    dfQtdBudget = dfQtdBudget.fillna(0)
    dfQtdCons = pd.merge(left=dfImpiegoCons, right=df3, how='outer', on='nArticolo', suffixes=['_produzione','_venduta'])
    dfQtdCons = dfQtdCons.fillna(0)
    dfQtdBudget['delta(prodotte - vendute)'] = dfQtdBudget['qtd_produzione'] - dfQtdBudget['qtd_venduta']
    dfQtdCons['delta(prodotte - vendute)'] = dfQtdCons['qtd_produzione'] - dfQtdCons['qtd_venduta']

    tempUnitari1 = dfQtdBudget.copy()
    index_names = tempUnitari1[tempUnitari1['qtd_venduta']/tempUnitari1['qtd_produzione'] < 1.5 ].index
    tempUnitari1.drop(index_names, inplace=True)

    tempUnitari2 = dfQtdCons.copy()
    index_names3 = tempUnitari2[tempUnitari2['qtd_venduta']/tempUnitari2['qtd_produzione'] < 1.5 ].index
    tempUnitari2.drop(index_names3, inplace=True)
    

    frames = [tempUnitari1, tempUnitari2]
    tempUnitari = pd.concat(frames)

    tempUnitari = tempUnitari.groupby('nArticolo', as_index=False)['delta(prodotte - vendute)'].min()


    root = tk.Tk()
    root.title("Controllo di Gestione -- selezionare una funzione")
    root.config(bg="white") 
    width = 800
    height = 650
    root.geometry("800x650")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0, 0)

    frame1 = tk.LabelFrame(root, text="quantità prodotte e vendute / BUDGET", bg="white")
    frame1.place(height=300, width=390,rely=0.0, relx=0.0)
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
    frame2 = tk.LabelFrame(root, text="quantità prodotte e vendute / CONSUNTIVO", bg="white")
    frame2.place(height=300, width=390,rely=0.5, relx=0)
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
    frame3 = tk.LabelFrame(root, text="Articoli con un delta(prodotti - venduti) negativo,\ncon uno scostamento maggiore al 50%", bg="white")
    frame3.place(height=300, width=390,rely=0.0, relx=0.5)
    tv3 = ttk.Treeview(frame3)
    style = ttk.Style(tv3)
    style.theme_use("clam")
    tv3.place(relheight=1, relwidth=1)
    treescrolly = tk.Scrollbar(frame3, orient="vertical", command=tv3.yview) 
    treescrollx = tk.Scrollbar(frame3, orient="horizontal", command=tv3.xview)
    tv3.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
    treescrollx.pack(side="bottom", fill="x") 
    treescrolly.pack(side="right", fill="y")
    tv3.tag_configure('red', background='red')
    tv3.tag_configure('green',background='green')

    framedestro = tk.LabelFrame(root,bg="white")
    framedestro.place(height=650, width=390, relx=0.5, rely=0.5)
    
     
    def inserisci():
        btnClose = tk.Button(framedestro, text="exit",font=('arial', 18), width=10, bg="red",command=exit )
        btnClose.place(rely=0.82, relx=0.67)
        count1 = 0
        count2 = 0
        tv1["column"] = list(dfQtdBudget.columns)
        tv1["show"] = "headings"
        for column in tv1["columns"]:
            tv1.heading(column, text=column) 
        df_rows = dfQtdBudget.to_numpy().tolist() 
        for row in range(0,503): 
            if(dfQtdBudget['delta(prodotte - vendute)'][row]<0):
                tv1.insert("", "end", values=df_rows[row], tags=('red',))
                count1 = count1 +1
            if(dfQtdBudget['delta(prodotte - vendute)'][row]>=0):
                tv1.insert("", "end", values=df_rows[row],  tags=('green',)) 
                count2 = count2 +1
        
        count3 = 0
        count4 = 0
        tv2["column"] = list(dfQtdCons.columns)
        tv2["show"] = "headings"
        for column in tv2["columns"]:
            tv2.heading(column, text=column) 
        df_rows = dfQtdCons.to_numpy().tolist() 
        for row in range(0,503): 
            if(dfQtdCons['delta(prodotte - vendute)'][row]<0):
                tv2.insert("", "end", values=df_rows[row], tags=('red',))
                count3 = count3 +1
            if(dfQtdCons['delta(prodotte - vendute)'][row]>=0):
                tv2.insert("", "end", values=df_rows[row],  tags=('green',)) 
                count4 = count4 +1

        tv3["column"] = list(tempUnitari.columns)
        tv3["show"] = "headings"
        for column in tv3["columns"]:
            tv3.heading(column, text=column)

        df_rows = tempUnitari.to_numpy().tolist() 
        for row in df_rows:
            tv3.insert("", "end", values=row)
        
        lb1 = Label(framedestro, text="Articoli con delta negativo a -Budget: "+ str(count1) +" articoli"
        +"\n( " + str(int(count1*100/len(dfQtdBudget))) + "% )"
        +"\n      - Consuntivo: "+str(count3) +" articoli"+
        "\n( " + str(int(count3*100/len(dfQtdBudget))) + "% )"
        "\n\nGli articoli con un delta negativo, che si\nscostano più del 50% tra quantità"+
        " vendute\ne quantità prodotte (sia a consuntivo che a\nbudget) sono: "+
        str(len(tempUnitari))+" articoli\n( "+
        str(int(len(tempUnitari)*100/len(dfQtdBudget)))+"% )", font=('arial', 12), bd=10, bg="white", anchor='center')
        lb1.place(rely=0.02, relx=0.0)
    
    def exit():
        root.destroy()
    inserisci()
    if __name__ == "__main__":
        root.mainloop()