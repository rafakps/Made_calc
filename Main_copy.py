
# Classe que cria / Calcula as propriedades geométricas

from Madeiras2 import *

import tkinter as tk
from tkinter import *
from tkinter import ttk


from tkinter import messagebox

# ------------- Janela Principal -----------------
janela_principal = Tk()
janela_principal.title("Programa de Dimensionamento Estrutural em Madeira")
janela_principal.geometry("800x600")
janela_principal.configure(background = "Black")
janela_principal.resizable(width="false", height="false")

# ------------- Label e Entry -----------------

leftframe = Frame(janela_principal,height = "600",width = "300",bg = "red", relief ="raise")
leftframe.pack(side=LEFT)

rightframe = Frame(janela_principal,height = "600",width = "495",bg = "white", relief ="raise")
rightframe.pack(side=RIGHT)

baseLebel = Label(leftframe, text="Base", bg="white",fg="black")
baseLebel.place(x=0,y=50,width=150,height=50)

baseEntry = ttk.Entry(leftframe)
baseEntry.place(x=150,y=50,width=150,height=50,bordermode=OUTSIDE)

alturaLabel = Label(leftframe,text="Altura",bg="white",fg="black")
alturaLabel.place(x=0,y=150,width=150,height=50)

alturaEntry = ttk.Entry(leftframe)
alturaEntry.place(x=150,y=150,width=150,height=50,bordermode=OUTSIDE)

comprimentoLabel = Label(leftframe,text="Comprimento",bg="white",fg="black")
comprimentoLabel.place(x=0,y=250,width=150,height=50)

comprimentoEntry = ttk.Entry(leftframe)
comprimentoEntry.place(x=150,y=250,width=150,height=50,bordermode=OUTSIDE)

forçaLabel = Label(leftframe,text="Força Normal",bg="white",fg="black")
forçaLabel.place(x=0,y=350,width=150,height=50)

forçaEntry = ttk.Entry(leftframe)
forçaEntry.place(x=150,y=350,width=150,height=50,bordermode=OUTSIDE)

momento_x_Label = Label(leftframe,text="Momento X",bg="white",fg="black")
momento_x_Label.place(x=0,y=450,width=150,height=50)

momento_x_Entry = ttk.Entry(leftframe)
momento_x_Entry.place(x=150,y=450,width=150,height=50,bordermode=OUTSIDE)

momento_y_Label = Label(leftframe,text="Momento Y",bg="white",fg="black")
momento_y_Label.place(x=0,y=550,width=150,height=50)

momento_y_Entry = ttk.Entry(leftframe)
momento_y_Entry.place(x=150,y=550,width=150,height=50,bordermode=OUTSIDE)

#resultado_Label = Label(rightframe,text="Resultado",bg="Gray",fg="black")
#resultado_Label.place(x=100,y=250,width=150,height=50)

#resultado_Entry = ttk.Entry(rightframe)
#resultado_Entry.place(x=250,y=250,width=150,height=50,bordermode=OUTSIDE)



#calculo_Label = Label(rightframe,textvariable=calcular_1,bg="gray",fg="black")
#calculo_Label.place(x=155,y=200,width=202,height=202)


resistencia=StringVar()
resultado_Label = Label(rightframe,text="resistencia",bg="Gray",fg="Blue")
resultado_Label.place(x=100,y=250,width=150,height=50)

# ---------- madeiras --------


# ------------ Botão ----------------------

def calcular_1():

    pine = Madeira(int(baseEntry.get()), int(alturaEntry.get()), int(comprimentoEntry.get()), 'C40', .56)
    resistencia = pine.compressão_verificação(int(forçaEntry.get()), int(momento_x_Entry.get()), int(momento_y_Entry.get()))
    resistencia1 = StringVar()
    resistencia1.set(resistencia)
    print(resistencia)
    resultado_Label.config(textvariable=resistencia1)






calcular_button = Button(rightframe,text="Calcular", width = 20, command = calcular_1)
#calcular_button = Button(rightframe,text="Calcular", width = 20, command = imprimir)
calcular_button.place(x=180,y = 440)




pinus = Madeira(10, 20, 100, 'C40', .56)
resistencia = pinus.compressão_verificação(2, 200, 300)
print(resistencia)

#calculo_Label = Button(rightframe,textvariable=resistencia,bg="gray",fg="black")
#calculo_Label.place(x=155,y=200,width=202,height=202)

#calculo_Label = messagebox.showinfo("2",resistencia)
#calculo_Label.place(x=155,y=200,width=202,height=202)



janela_principal.mainloop()