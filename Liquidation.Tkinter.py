# ------------------ Importacion -----------------------

# Funciones de tkinter:

from tkinter import * 
from tkcalendar import *
from tkinter import messagebox 
from tkinter import filedialog 
import tkinter as tk

# Funciones fechas:
from datetime import datetime
from dateutil import relativedelta
import locale
locale.setlocale(locale.LC_ALL, '')

# ------------- Frame -----------------

# Ventana:

root = tk.Tk() 
root.title("Liquidación") 
root.resizable(1,1)
root.iconbitmap("PESO.ico") 
 
# Frame de la ventana:

miFrame = tk.Frame() 

miFrame.config(bd="35") 
miFrame.config(cursor="hand2") 
miFrame.pack(fill="both", expand="True") 

# ------------------------------- variables -------------------------------

var = tk.IntVar()
label_chck2 = BooleanVar()
var_indemnizacion_antiguedad = tk.IntVar()
var_preaviso = tk.IntVar()
var_SAC_preaviso = tk.IntVar()
var_integracion = tk.IntVar()
var_SAC_integracion = tk.IntVar()
var_doble_indemnizacion = tk.IntVar()

# ------------------------------- Funciones -------------------------------

# Funciones menu:

def acerca_del_autor(): 
    messagebox.showinfo("Autor", "Federico Irarrazaval \nAbogado \nCel: 1567887879 \nEmail: fedeirar@gmail.com")

def salir():
    valor = messagebox.askokcancel("Salir", "Desea salir de la aplicacion?") 
    if valor == True:
        root.destroy() 

# Funcion para abrir fichero:

def abreFichero():
    fichero=filedialog.askopenfilename(title="Abrir", initialdir="C:", filetypes=(("Ficheros de Excel", "*.xlsx"), ("Ficheros de texto", "*.txt"), ("Todos los ficheros","*.*"))) 
    print(fichero) 
    
# Funciones ejecutar liquidacion: 

def calculo_antiguedad(fecha_ingreso, fecha_egreso):
    global años_antiguedad
    global años
    global meses
    global mes_extincion
    global dia_extincion
    global año_extincion
    
    try:
        diferencia = relativedelta.relativedelta(fecha_egreso.get_date() , fecha_ingreso.get_date())

    except:
        try:
            day_1, month_1, year_1 = fecha_ingreso.get().split("-")
            day_2, month_2, year_2 = fecha_egreso.get().split("-")

            fecha_ingreso = datetime(year_1,month_1, day_1)
            fecha_egreso = datetime(year_2,month_2,day_2)
       
            diferencia = relativedelta.relativedelta(fecha_egreso.get_date() , fecha_ingreso.get_date())

        except ValueError as error:
            messagebox.showerror("ValueError", error)

    diferencia2 = relativedelta.relativedelta(fecha_egreso.get_date() , datetime(1,1,1))
    
    año_extincion = diferencia2.years + 1
    mes_extincion = diferencia2.months + 1
    dia_extincion = diferencia2.days + 1

    años = diferencia.years
    meses = diferencia.months
    dias = diferencia.days

    if meses >= 3:
        años_antiguedad = años + 1
    else:
        años_antiguedad = años

def calculo_indemnizacion_antiguedad():
    global mrmnh
    global indemnizacion_por_antiguedad

    mrmnh = float(cuadrotexto4.get())

    if var.get() == 1:
        mrmnh = mrmnh*0.67
    elif label_chck2.get() ==1:
        mrmnh = float(entry_tope.get())
    
    if var_indemnizacion_antiguedad.get() == 1:
        indemnizacion_por_antiguedad = int(años_antiguedad)*mrmnh 
        texto_indemnizacion_antiguedad.config(text= "$ " + str(indemnizacion_por_antiguedad))
    else:
        texto_indemnizacion_antiguedad.config(text= "")

def funcion_entry__tope():
    if label_chck2.get():
        entry_tope.grid(row=5, column=4, pady=2)
        entry_tope.config(justify="center")
    else:
        entry_tope.grid_forget()

def calculo_indemnizacion_preaviso():
    global preaviso
    salario_promedio = float(cuadrotexto3.get())

    if var_preaviso.get() == 1 and años >= 5:
        preaviso = salario_promedio * 2
        texto_indemnizacion_preaviso.config(text= "$ " + str(preaviso))
    elif var_preaviso.get() == 1 and años < 5 and meses >= 3:
        preaviso = salario_promedio
        texto_indemnizacion_preaviso.config(text= "$ " + str(preaviso))
    elif var_preaviso.get() == 1 and años < 1 and meses < 3:
        preaviso = salario_promedio/2
        texto_indemnizacion_preaviso.config(text= "$ " + str(preaviso))
    else:
        texto_indemnizacion_preaviso.config(text= "")

def calculo_SAC_preaviso():
    global SAC_preaviso
    salario_promedio = float(cuadrotexto3.get())

    if años >= 5:
        preaviso = salario_promedio * 2
    elif años < 5 and meses >= 3:
        preaviso = salario_promedio 
    elif años < 1 and meses < 3:
        preaviso = salario_promedio/2 

    if var_SAC_preaviso.get() == 1:
        SAC_preaviso = preaviso / 12
        texto_SAC_preaviso.config(text= "$ " + str(SAC_preaviso))
    else:
        texto_SAC_preaviso.config(text= "")

def calculo_integracion():
    global integracion_mes_despido

    salario_promedio = float(cuadrotexto3.get())

    if var_integracion.get() == 1:
        if mes_extincion==1:
            dias_trabajados = float(salario_promedio) / 31 * dia_extincion
        elif mes_extincion==2 and (año_extincion%4)!=0:
            dias_trabajados = salario_promedio / 28 * dia_extincion
        elif mes_extincion==2 and (año_extincion%4)==0:
            dias_trabajados = salario_promedio / 29 * dia_extincion
        elif mes_extincion==3:
            dias_trabajados = salario_promedio / 31 * dia_extincion
        elif mes_extincion==4:
            dias_trabajados = salario_promedio / 30 * dia_extincion
        elif mes_extincion==5:
            dias_trabajados = salario_promedio / 31 * dia_extincion
        elif mes_extincion==6:
            dias_trabajados = salario_promedio / 30 * dia_extincion
        elif mes_extincion==7:
            dias_trabajados = salario_promedio / 31 * dia_extincion
        elif mes_extincion==8:
            dias_trabajados = salario_promedio / 31 * dia_extincion
        elif mes_extincion==9:
            dias_trabajados = salario_promedio / 30 * dia_extincion
        elif mes_extincion==10:
            dias_trabajados = salario_promedio / 31 * dia_extincion
        elif mes_extincion==11:
            dias_trabajados = salario_promedio / 30 * dia_extincion
        elif mes_extincion==12:
            dias_trabajados = salario_promedio / 31 * dia_extincion
        
        integracion_mes_despido = salario_promedio - dias_trabajados
        texto_integracion.config(text= "$ " + str(integracion_mes_despido))
    else:
        texto_integracion.config(text= "")

def calculo_SAC_integracion(): 
    global SAC_integracion
    salario_promedio = float(cuadrotexto3.get())

    if mes_extincion==1:
        dias_trabajados = float(salario_promedio) / 31 * dia_extincion
    elif mes_extincion==2 and (año_extincion%4)!=0:
        dias_trabajados = salario_promedio / 28 * dia_extincion
    elif mes_extincion==2 and (año_extincion%4)==0:
            dias_trabajados = salario_promedio / 29 * dia_extincion
    elif mes_extincion==3:
        dias_trabajados = salario_promedio / 31 * dia_extincion
    elif mes_extincion==4:
        dias_trabajados = salario_promedio / 30 * dia_extincion
    elif mes_extincion==5:
        dias_trabajados = salario_promedio / 31 * dia_extincion
    elif mes_extincion==6:
        dias_trabajados = salario_promedio / 30 * dia_extincion
    elif mes_extincion==7:
        dias_trabajados = salario_promedio / 31 * dia_extincion
    elif mes_extincion==8:
        dias_trabajados = salario_promedio / 31 * dia_extincion
    elif mes_extincion==9:
        dias_trabajados = salario_promedio / 30 * dia_extincion
    elif mes_extincion==10:
        dias_trabajados = salario_promedio / 31 * dia_extincion
    elif mes_extincion==11:
        dias_trabajados = salario_promedio / 30 * dia_extincion
    elif mes_extincion==12:
        dias_trabajados = salario_promedio / 31 * dia_extincion
        
    integracion_mes_despido = salario_promedio - dias_trabajados
       
    if var_SAC_integracion.get() == 1:
        SAC_integracion = integracion_mes_despido/12
        texto_SAC_integracion.config(text= "$ " + str(SAC_integracion))
    else:
        texto_SAC_integracion.config(text= "")

def doble_indemnizacion():
    if var_doble_indemnizacion.get() == 1:
        doble_indemnizacion = integracion_mes_despido/12
        texto_doble_indemnizacion.config(text= "$ " + str(doble_indemnizacion))
# ------------------------------------- Menu -----------------------------------

barraMenu=Menu(root) 
root.config(menu=barraMenu, width=300, height=300)

archivoMenu=Menu(barraMenu, tearoff = 0) 
barraMenu.add_cascade(label="Archivo", menu=archivoMenu) 
archivoMenu.add_command(label="Guardar")
archivoMenu.add_command(label="Guardar como")
archivoMenu.add_separator() 
archivoMenu.add_command(label="Salir", command = salir)

archivoHerramientas=Menu(barraMenu, tearoff = 0)
barraMenu.add_cascade(label="Herramientas", menu=archivoHerramientas)
archivoHerramientas.add_command(label="Diccionario")

archivoAyuda=Menu(barraMenu, tearoff = 0)
barraMenu.add_cascade(label="Ayuda", menu=archivoAyuda)
archivoAyuda.add_command(label="Acerca del autor", command = acerca_del_autor) 

# ------------------------------------------------------------------- Labels, entry dates y botones ------------------------------------------------------------

# Fecha de ingreso:

primer_label=Label(miFrame, text="Fecha de ingreso: ").grid(row=0, column=0, sticky="e", pady=2) 

fecha_ingreso = DateEntry(miFrame)
fecha_ingreso.grid(row = 0, column = 1)

# Fecha de egreso:

segundo_label=Label(miFrame, text="Fecha de egreso: ").grid(row=2, column=0, sticky="e", pady=2) 

fecha_egreso = DateEntry(miFrame)
fecha_egreso.grid(row = 2, column = 1)

# Salario promedio:

tercer_label=Label(miFrame, text="Salario promedio: ").grid(row=4, column=0, sticky="e", pady=2)

cuadrotexto3 = tk.Entry(miFrame)
cuadrotexto3.grid(row=4, column=1, pady=2)
cuadrotexto3.config(justify="center")

# Mejor remuneracion, mensual, normal y habitual:

cuarto_label=tk.Label(miFrame, text ="MRMNH:").grid(row=5, column=0, sticky="e", pady=2)

cuadrotexto4 = tk.Entry(miFrame)
cuadrotexto4.grid(row=5, column=1, pady=2)
cuadrotexto4.config(justify="center")

# Topes:

chk3 = tk.Checkbutton(miFrame, text = "Tope Vizzoti", variable=var).grid(row=5, column=2)

chk4 = tk.Checkbutton(miFrame, text = "Tope Convenio", variable=label_chck2, command=funcion_entry__tope).grid(row=5, column=3)

entry_tope=Entry(miFrame,width=50)

#Rubros a incorporar en la liquidacion:

septimo_label=Label(miFrame, text="RUBROS DE LIQUIDACION").grid(row=6, column=0, sticky="w", pady=2)

# ---------------------------------- label para proporcionales ------------------------------

octavo_label=Label(miFrame, text="-Proporcionales:").grid(row=7, column=0, sticky="w", pady=2)

# ---------------------------------- botones para proporcionales ------------------------------

chk5 = tk.Checkbutton(miFrame, text = "Dias trabajados del mes de despido").grid(row=8, column=0, sticky="w")

chk6 = tk.Checkbutton(miFrame, text = "SAC proporcional").grid(row=9, column=0, sticky="w")

chk7 = tk.Checkbutton(miFrame, text = "Vacaciones no gozadas").grid(row=10, column=0, sticky="w")

chk8 = tk.Checkbutton(miFrame, text = "SAC s/ Vacaciones no gozadas").grid(row=11, column=0, sticky="w")

# ---------------------------------- label para indemnizaciones por despido sin causa ------------------------------

noveno_label=Label(miFrame, text="-Indemnizaciones por despido sin causa:" ).grid(row=12, column=0, sticky="w", pady=2)

# ---------------------------------- botones para indemnizaciones por despido sin causa ------------------------------

chk9 = tk.Checkbutton(miFrame, text = "Indemnizacion por antiguedad", variable=var_indemnizacion_antiguedad).grid(row=13, column=0, sticky="w")

chk10 = tk.Checkbutton(miFrame, text = "Preaviso", variable = var_preaviso).grid(row=14, column=0, sticky="w")

chk11 = tk.Checkbutton(miFrame, text = "SAC s/ Preaviso", variable = var_SAC_preaviso).grid(row=15, column=0, sticky="w")

chk12 = tk.Checkbutton(miFrame, text = "Integracion mes de despido", variable = var_integracion).grid(row=16, column=0, sticky="w")

chk13 = tk.Checkbutton(miFrame, text = "SAC s/ Integracion mes de despido", variable = var_SAC_integracion).grid(row=17, column=0, sticky="w")

chk14 = tk.Checkbutton(miFrame, text = "Doble indemnizacion", variable = var_doble_indemnizacion).grid(row=18, column=0, sticky="w")

# ---------------------------------- label para multas e indemnizaciones adicionales ------------------------------

noveno_label=Label(miFrame, text="-Sanciones y multas:").grid(row=19, column=0, sticky="w", pady=2)

decimo_label =Label(miFrame, text="Bruto:").grid(row=7, column=2, sticky="w", pady=2)

onceavo_label =Label(miFrame, text="Neto:").grid(row=7, column=3, sticky="w", pady=2)

# ---------------------------------- botones para multas e indemnizaciones adicionales ------------------------------

chk14 = tk.Checkbutton(miFrame, text = "Indemnizacion art. 1 Ley 25.323").grid(row=20, column=0, sticky="w")

chk15 = tk.Checkbutton(miFrame, text = "Indemnizacion art. 2 Ley 25.323").grid(row=21, column=0, sticky="w")

chk16 = tk.Checkbutton(miFrame, text = "Indemnizacion art. 8 Ley 24.013").grid(row=22, column=0, sticky="w")

chk17 = tk.Checkbutton(miFrame, text = "Indemnizacion art. 9 Ley 24.013").grid(row=23, column=0, sticky="w")

chk18 = tk.Checkbutton(miFrame, text = "Indemnizacion art. 10 Ley 24.013").grid(row=24, column=0, sticky="w")

chk19 = tk.Checkbutton(miFrame, text = "Indemnizacion art. 15 Ley 24.013").grid(row=25, column=0, sticky="w")

chk20 = tk.Checkbutton(miFrame, text = "Indemnizacion art. 80 LCT").grid(row=26, column=0, sticky="w")

# ------------------------ Label y boton para ejecutar liquidacion ---------------------

boton1 = Button(miFrame, text="Ejecutar liquidación", command = lambda: [calculo_antiguedad(fecha_ingreso, fecha_egreso), calculo_indemnizacion_antiguedad(), calculo_indemnizacion_preaviso(), calculo_SAC_preaviso(), calculo_integracion(),calculo_SAC_integracion(), doble_indemnizacion()]) 
boton1.grid(row=27, column=0, pady=2) 

# ------------------------ Labels de rubros de liquidacion ---------------------

texto_indemnizacion_antiguedad=Label(miFrame)
texto_indemnizacion_antiguedad.grid(row=13, column=2, pady=2, sticky="w")

texto_indemnizacion_preaviso=Label(miFrame)
texto_indemnizacion_preaviso.grid(row=14, column=2, pady=2, sticky="w")

texto_SAC_preaviso=Label(miFrame)
texto_SAC_preaviso.grid(row=15, column=2, pady=2, sticky="w")

texto_integracion=Label(miFrame)
texto_integracion.grid(row=16, column=2, pady=2, sticky="w")

texto_SAC_integracion=Label(miFrame)
texto_SAC_integracion.grid(row=17, column=2, pady=2, sticky="w")

texto_doble_indemnizacion=Label(miFrame)
texto_doble_indemnizacion.grid(row=18, column=2, pady=2, sticky="w")

#--------------------------------- Fichero -----------------------------------------

Button (root, text = "Abrir fichero", command=abreFichero).pack() 

# --------------------------------- End ------------------------------------

root.mainloop()

