print("Bienvenido al calculador de liquidación final. La liquidación se va a crear en archivo aparte denominado Liquidación. Ingresa números sin puntos, y con punto en lugar de coma.")

# Crea el archivo donde se imprime la liquidación.

from io import open 
Liquidación = open("Liquidación.txt", "r+") #le agrego el mas para poder leer tambien

# Pregunta fecha de ingreso y fecha de egreso y calcula años de antigüedad.
from datetime import datetime
from dateutil import relativedelta

import locale
locale.setlocale(locale.LC_ALL, '')

while True:
    try:
        dia_ingreso = int(input("Ingresar día de ingreso:"))
        mes_ingreso = int(input("Ingresar mes de ingreso:"))
        año_ingreso = int(input("Ingresar año de ingreso:"))
        dia_egreso = int(input("Ingresar día de egreso:"))
        mes_egreso = int(input("Ingresar mes de egreso:"))
        año_egreso = int(input("Ingresar año de egreso:"))
        break
    
    except ValueError:
        print("Ingresaste una fecha erronea. Ingresar de vuelta.")

fecha_ingreso = datetime(año_ingreso,mes_ingreso, dia_ingreso)
fecha_egreso = datetime(año_egreso,mes_egreso,dia_egreso)

diferencia = relativedelta.relativedelta(fecha_egreso, fecha_ingreso)

años = diferencia.years
meses = diferencia.months
dias = diferencia.days

if meses >= 3:
    años_antiguedad = años + 1
else:
    años_antiguedad = años

total_liquidacion = [] # Creo una lista para ir sumando los subtotales de las liquidaciones.

# Se pregunta salario y mrmnh.

salario_promedio = float(input("Ingresar salario promedio: "))

mrmnh = float(input("Ingresar mejor remuneración mensual normal y habitual: ")) 

# ---------------- Liquidacion de indemnizaciones por despido sin causa ---------------------
print("Comenzamos con las indemnizaciones por despido sin causa.")

def indemnizaciones_despido_sin_causa ():

# Se consulta tope y calcula indemnización por antigüedad.

    tope = str(input("¿Queres aplicar tope Vizzoti, tope de convenio o ningún tope? INGRESAR: vizzoti / tope convenio / ninguno: "))

    tope1 = tope.lower()

    while tope1 != "vizzoti" and tope1 != "tope convenio" and tope1 != "ninguno":

        tope = str(input("Ingresaste algo incorrecto. INGRESAR: vizzoti / tope convenio / ninguno: "))
        tope1 = tope.lower()
        
    if tope1 == "ninguno":
        mrmnh_normal_vizotti_topeconvenio = mrmnh
        
    elif tope1 == "vizzoti":
        mrmnh_normal_vizotti_topeconvenio = mrmnh * 0.67
       
    elif tope1 == "tope convenio":
        mrmnh_normal_vizotti_topeconvenio = float(input("Ingresar tope de convenio: "))
        
    indemnizacion_antiguedad = mrmnh_normal_vizotti_topeconvenio * int(años_antiguedad)

    Provincia_capital1 = input("Trabaja en Provincia o Capital: INGRESAR: capital / provincia: ")

    Provincia_capital = Provincia_capital1.lower()

    while Provincia_capital != "capital" and Provincia_capital != "provincia":

        Provincia_capital1 = input("Ingresaste algo incorrecto. INGRESAR: capital / provincia: ")
        Provincia_capital = Provincia_capital1.lower()

    if Provincia_capital == "provincia":
            SAC_indemnizacion_antiguedad = indemnizacion_antiguedad / 12
            
    elif Provincia_capital == "capital":
        SAC_indemnizacion_antiguedad = 0
            
# Se calcula preaviso y pregunta si hubo preaviso.
    if años >= 5:
        preaviso = salario_promedio * 2
    
    elif años < 5 and meses >= 3:
        preaviso = salario_promedio 

    elif años < 1 and meses < 3:
        preaviso = salario_promedio/2 

    sac_sobre_preaviso = preaviso/12

    hubo_preaviso = input("¿Queres agregar indemnización por preaviso? Recorda que son 15 días en periodo de prueba, 1 mes con antigüedad menor a 5, y 2 meses con antigüedad igual o mayor a 5. INGRESAR: si \ no: ")

    if hubo_preaviso == "no":
        preaviso = 0
        sac_sobre_preaviso = 0
    elif  hubo_preaviso == "si":
        pass

# Calcula integración mes de despido y su SAC.

    if mes_egreso==1:
        dias_trabajados = salario_promedio / 31 * dia_egreso
    elif mes_egreso==2 and (fecha_egreso.year%4)!=0:
        dias_trabajados = salario_promedio / 28 * dia_egreso
    elif mes_egreso==2 and (fecha_egreso.year%4)==0:
        dias_trabajados = salario_promedio / 29 * dia_egreso
    elif mes_egreso==3:
        dias_trabajados = salario_promedio / 31 * dia_egreso
    elif mes_egreso==4:
        dias_trabajados = salario_promedio / 30 * dia_egreso
    elif mes_egreso==5:
        dias_trabajados = salario_promedio / 31 * dia_egreso
    elif mes_egreso==6:
        dias_trabajados = salario_promedio / 30 * dia_egreso
    elif mes_egreso==7:
        dias_trabajados = salario_promedio / 31 * dia_egreso
    elif mes_egreso==8:
        dias_trabajados = salario_promedio / 31 * dia_egreso
    elif mes_egreso==9:
        dias_trabajados = salario_promedio / 30 * dia_egreso
    elif mes_egreso==10:
        dias_trabajados = salario_promedio / 31 * dia_egreso
    elif mes_egreso==11:
        dias_trabajados = salario_promedio / 30 * dia_egreso
    elif mes_egreso==12:
        dias_trabajados = salario_promedio / 31 * dia_egreso

    integracion_mes_despido = salario_promedio - dias_trabajados

    sac_integracion_mes_despido = integracion_mes_despido / 12

# Calcula doble indemnización para ingresos anteriores al 13/12/2019 hasta tope de $ 500.000. 

    if dia_ingreso < 13 and mes_ingreso == 12 and año_ingreso == 2019 and indemnizacion_antiguedad + preaviso + sac_sobre_preaviso + integracion_mes_despido + sac_integracion_mes_despido > 500000:
        doble_indemnizacion = 500000

    elif dia_ingreso < 13 and mes_ingreso == 12 and año_ingreso == 2019 and indemnizacion_antiguedad + preaviso + sac_sobre_preaviso + integracion_mes_despido + sac_integracion_mes_despido < 500000:
        doble_indemnizacion = indemnizacion_antiguedad + preaviso + sac_sobre_preaviso + integracion_mes_despido + sac_integracion_mes_despido

    elif año_ingreso == 2019 and mes_ingreso < 12 and indemnizacion_antiguedad + preaviso + sac_sobre_preaviso + integracion_mes_despido + sac_integracion_mes_despido > 500000:
        doble_indemnizacion = 500000

    elif año_ingreso == 2019 and mes_ingreso < 12 and indemnizacion_antiguedad + preaviso + sac_sobre_preaviso + integracion_mes_despido + sac_integracion_mes_despido < 500000:
        doble_indemnizacion = indemnizacion_antiguedad + preaviso + sac_sobre_preaviso + integracion_mes_despido + sac_integracion_mes_despido

    elif año_ingreso < 2019 and indemnizacion_antiguedad + preaviso + sac_sobre_preaviso + integracion_mes_despido + sac_integracion_mes_despido > 500000:
        doble_indemnizacion = 500000

    elif año_ingreso < 2019 and indemnizacion_antiguedad + preaviso + sac_sobre_preaviso + integracion_mes_despido + sac_integracion_mes_despido < 500000:
        doble_indemnizacion = indemnizacion_antiguedad + preaviso + sac_sobre_preaviso + integracion_mes_despido + sac_integracion_mes_despido

    else:
        doble_indemnizacion = 0

# Calcula el total de la liquidación por despido sin causa.

    total_liquidacion1 = indemnizacion_antiguedad + preaviso + sac_sobre_preaviso + integracion_mes_despido + sac_integracion_mes_despido + doble_indemnizacion

    total_liquidacion.append (float(total_liquidacion1))  # AGREGO A LIQUIDACION LAS INDEMNIZACIONES POR DESPIDO
# Se escribe en el archivo la liquidación.

    Liquidación.write("\n \n LA LIQUIDACIÓN POR INDEMNIZACIONES POR DESPIDO SIN CAUSA ES LA SIGUIENTE: " "\n Antigüedad: $" + str(indemnizacion_antiguedad) +
     "\n SAC s/ antigüedad: $" + str(SAC_indemnizacion_antiguedad) + "\n Preaviso: $" + str(preaviso) + "\n SAC s/ Preaviso: $" + str(sac_sobre_preaviso) +"\n Integración mes de despido: $" 
     + str(integracion_mes_despido) +"\n SAC s/ Integración mes de despido: $" + str(sac_integracion_mes_despido) + "\n Doble indemnización: $" + str(doble_indemnizacion) 
     + "\n El subtotal de la liquidación por despido sin causa es de: $" + str(total_liquidacion1)) 


liquidacion_indemnizaciones_despido_sin_causa = input("¿Deseas incorporarlas a la liquidación final? INGRESAR: si/no: ")

if liquidacion_indemnizaciones_despido_sin_causa == "si":
    indemnizaciones_despido_sin_causa ()
else: 
    pass

# ----------------------------- Liquidacion de proporcionales por extinción del contrato de trabajo -----------------------------------

print("Continuamos con la liquidacion de los proporcionales por extinción del contrato de trabajo.")

def proporcionales_liquidacion ():

# Calcula días trabajados.

    if mes_egreso==1:
        dias_trabajados = salario_promedio / 31 * dia_egreso
    elif mes_egreso==2 and (fecha_egreso.year%4)!=0:
        dias_trabajados = salario_promedio / 28 * dia_egreso
    elif mes_egreso==2 and (fecha_egreso.year%4)==0:
        dias_trabajados = salario_promedio / 29 * dia_egreso
    elif mes_egreso==3:
        dias_trabajados = salario_promedio / 31 * dia_egreso
    elif mes_egreso==4:
        dias_trabajados = salario_promedio / 30 * dia_egreso
    elif mes_egreso==5:
        dias_trabajados = salario_promedio / 31 * dia_egreso
    elif mes_egreso==6:
        dias_trabajados = salario_promedio / 30 * dia_egreso
    elif mes_egreso==7:
        dias_trabajados = salario_promedio / 31 * dia_egreso
    elif mes_egreso==8:
        dias_trabajados = salario_promedio / 31 * dia_egreso
    elif mes_egreso==9:
        dias_trabajados = salario_promedio / 30 * dia_egreso
    elif mes_egreso==10:
        dias_trabajados = salario_promedio / 31 * dia_egreso
    elif mes_egreso==11:
        dias_trabajados = salario_promedio / 30 * dia_egreso
    elif mes_egreso==12:
        dias_trabajados = salario_promedio / 31 * dia_egreso

# Calcula SAC proporcional. Para eso tengo que calcular días y descontarle 182,5 (días) si supera 182,5 días. Además, calcula vacaciones y su SAC.
    inicio_periodo_SAC = datetime(año_egreso, 1, 1)
    fin_periodo_SAC = datetime(año_egreso, mes_egreso, dia_egreso)

    dias_vacaciones = fin_periodo_SAC - inicio_periodo_SAC

    if mes_egreso > 6:
        inicio_periodo_SAC = datetime(año_egreso, 7, 1)
        fin_periodo_SAC = datetime(año_egreso, mes_egreso, dia_egreso)

    dias_SAC = fin_periodo_SAC - inicio_periodo_SAC

    sac_proporcional = mrmnh/2/182.5*dias_SAC.days

# Calcula vacaciones y su SAC.

    fecha_ingreso_vacaciones = datetime(año_ingreso,mes_ingreso, dia_ingreso)
    fecha_egreso_vacaciones = datetime(año_egreso,12,31)

    if fecha_egreso_vacaciones.day-fecha_ingreso_vacaciones.day >= 0:
        numero_meses_vacaciones = (fecha_egreso_vacaciones.year - fecha_ingreso_vacaciones.year) * 12 + (fecha_egreso_vacaciones.month - fecha_ingreso_vacaciones.month)
    else: 
        numero_meses_vacaciones = (fecha_egreso_vacaciones.year - fecha_ingreso_vacaciones.year) * 12 + (fecha_egreso_vacaciones.month - fecha_ingreso_vacaciones.month)-1

    años_vacaciones = numero_meses_vacaciones//12

    inicio_periodo_vacaciones = datetime(año_egreso, 1, 1)
    fin_periodo_vacaciones = datetime(año_egreso, mes_egreso, dia_egreso)

    dias_vacaciones = fin_periodo_vacaciones - inicio_periodo_vacaciones

    vacaciones_ley = input("Si tiene vacaciones por ley ingresá si. Si tiene vacaciones por encima de la ley ingresá no. INGRESAR: si/no: ")

    if vacaciones_ley == "no":
        vacaciones = float(input("Ingresar dias de vacaciones según política de la Empresa: "))
        vacaciones = dias_vacaciones.days * vacaciones / 365

    elif vacaciones_ley == "si" and dias_vacaciones.days < 123 and años_vacaciones == 0:
        vacaciones = dias_vacaciones.days * 0.7 / 20

    elif vacaciones_ley == "si" and dias_vacaciones.days > 123 and años_vacaciones == 0:
        vacaciones = dias_vacaciones.days * 14 / 365

    elif vacaciones_ley == "si" and 1<=años_vacaciones<5:
        vacaciones = dias_vacaciones.days * 14 / 365

    elif vacaciones_ley == "si" and 5<= años_vacaciones<10:
        vacaciones = dias_vacaciones.days * 21 / 365 

    elif vacaciones_ley == "si" and 10<= años_vacaciones<20:
        vacaciones = dias_vacaciones.days * 28 / 365  

    elif vacaciones_ley == "si" and 20<= años_vacaciones:
        vacaciones = dias_vacaciones.days * 35 / 365   

    vacaciones_adeudadas = salario_promedio/25*vacaciones

    sac_sobre_vacaciones_adeudadas = vacaciones_adeudadas / 12

# Calcula el total de la liquidación.

    total_liquidacion2 = dias_trabajados + sac_proporcional + vacaciones_adeudadas + sac_sobre_vacaciones_adeudadas

    total_liquidacion.append (float(total_liquidacion2))  # AGREGO A LIQUIDACION LOS PROPORCIONALES.

# Se escribe en el archivo la liquidación.

    Liquidación.write("\n \n LA LIQUIDACIÓN POR PROPORCIONALES POR EXTINCIÓN DEL CONTRATO DE TRABAJO ES LA SIGUIENTE: " "\n Días trabajados: $" + str(dias_trabajados) +  "\n SAC proporcional: $" 
    + str(sac_proporcional) + "\n Vacaciones adeudadas: $" + str(vacaciones_adeudadas) + "\n SAC s/ Vacaciones adeudadas: $" + str(sac_sobre_vacaciones_adeudadas) + "\n El subtotal de la liquidación es de: $" 
    + str(total_liquidacion2)) 


proporcionales = input("¿Deseas incorporarlas a la liquidación final? INGRESAR: si/no: ")

if proporcionales == "si":
    proporcionales_liquidacion()
else: 
    pass

# --------------- AHORA PASAMOS A LIQUIDACIÓN DE MULTAS Y ADICIONALES -------------------
print("Procederemos ahora a calcular multas e indemnizaciones adicionales.")

def multas_e_indemnizaciones_adicionales ():

# Necesito traer los valores de indemnizacion por antiguedad, preaviso y su SAC e integracion mes de despido y su SAC para calcular las multas. 
    indemnizacion_antiguedad = mrmnh * int(años_antiguedad)

    if años > 5:
        preaviso = salario_promedio * 2
    else:
        preaviso = salario_promedio 

    sac_sobre_preaviso = preaviso/12

    if mes_egreso==1:
        dias_trabajados = salario_promedio / 31 * dia_egreso
    elif mes_egreso==2 and (fecha_egreso.year%4)!=0:
        dias_trabajados = salario_promedio / 28 * dia_egreso
    elif mes_egreso==2 and (fecha_egreso.year%4)==0:
        dias_trabajados = salario_promedio / 29 * dia_egreso
    elif mes_egreso==3:
        dias_trabajados = salario_promedio / 31 * dia_egreso
    elif mes_egreso==4:
        dias_trabajados = salario_promedio / 30 * dia_egreso
    elif mes_egreso==5:
        dias_trabajados = salario_promedio / 31 * dia_egreso
    elif mes_egreso==6:
        dias_trabajados = salario_promedio / 30 * dia_egreso
    elif mes_egreso==7:
        dias_trabajados = salario_promedio / 31 * dia_egreso
    elif mes_egreso==8:
        dias_trabajados = salario_promedio / 31 * dia_egreso
    elif mes_egreso==9:
        dias_trabajados = salario_promedio / 30 * dia_egreso
    elif mes_egreso==10:
        dias_trabajados = salario_promedio / 31 * dia_egreso
    elif mes_egreso==11:
        dias_trabajados = salario_promedio / 30 * dia_egreso
    elif mes_egreso==12:
        dias_trabajados = salario_promedio / 31 * dia_egreso

    integracion_mes_despido = salario_promedio - dias_trabajados

    sac_integracion_mes_despido = integracion_mes_despido / 12

# Calcula indemnización art. 1 ley 25.323.
    art1_ley25323 = input("¿Queres agregar la multa del Art. 1, Ley 25.323? Recordá que: (i) procede con irregularidad registral reclamada luego de la desvinculación y (ii) no es acumulativa con las multas de la ley 24.013. INGRESAR: si/no: ")

    if art1_ley25323 == "si":
        indemnizacion_art1_ley25323 = indemnizacion_antiguedad 
    elif art1_ley25323 == "no":
        indemnizacion_art1_ley25323 = 0

# Calcula indemnización Art. 2 ley 25.323.
 
    art2_ley25323 = input("¿Queres agregar la multa del Art. 2, Ley 25.323? Recorda que corresponde si la empresa no pagó indemnizaciones por despido habiendo sido intimada. INGRESAR: si/no: ")

    if art2_ley25323 == "si":
        indemnizacion_art2_ley25323 = (indemnizacion_antiguedad + preaviso + sac_sobre_preaviso + integracion_mes_despido + sac_integracion_mes_despido)/2
    elif art2_ley25323 == "no":
        indemnizacion_art2_ley25323 = 0

# Calcula indemnización Art. 15 ley 24.013. 

    art15_ley24013 = input("¿Queres agregar la multa del Art. 15, Ley 24.013? Recordá que: (i) debe haber intimado por registro deficiente antes de la extinción del vínculo, y (ii) no es acumulativa con la multa del art. 1 de la ley 25.323. INGRESAR: si/no: ")

    if art15_ley24013 == "si":
        indemnizacion_art15_ley24013 = indemnizacion_antiguedad + preaviso + sac_sobre_preaviso + integracion_mes_despido + sac_integracion_mes_despido

    else:
        indemnizacion_art15_ley24013 = 0

# Calcula indemnización Art. 8 ley 24.013.
 
    indemnizacion_art8_ley24013 = ((años*13*salario_promedio) + (meses*salario_promedio) + (meses*salario_promedio/12) + (salario_promedio/30*dias) + (salario_promedio/30*dias/12)) / 4

    art8_ley24013 = input("¿Queres agregar la multa del Art. 8, Ley 24.031? Recorda que corresponde por omisión total de registro reclamada antes del despido. INGRESAR: si/no: ")

    if art8_ley24013 == "si" and indemnizacion_art8_ley24013 < mrmnh*3:
        indemnizacion_art8_ley24013 = mrmnh*3

    elif art8_ley24013 == "no":
        indemnizacion_art8_ley24013 = 0

    elif art8_ley24013 == "si":
        pass

# Calcula indemnización Art. 9 ley 24.013.
 
    art9_ley24013 = input("¿Queres agregar la multa del Art. 9, Ley 24.013? Recorda que corresponde si hubo registro deficiente de fecha de ingreso y se intimó a su registro antes del despido. INGRESAR: si/no: ")

    if art9_ley24013 == "si":
       
        dia_ingreso_falso = int(input("Ingresa día de ingreso deficientemente registrado:"))
        mes_ingreso_falso = int(input("Ingresa mes de ingreso deficientemente registrado:"))
        año_ingreso_falso = int(input("Ingresa año de ingreso deficientemente registrado:"))

        fecha_ingreso_falsa = datetime(año_ingreso_falso, mes_ingreso_falso, dia_ingreso_falso)
        diferencia3 = relativedelta.relativedelta(fecha_ingreso_falsa, fecha_ingreso)

        while art9_ley24013 == "si" and int(diferencia3.years) < 1 and int(diferencia3.months) < 1 and int(diferencia3.days) < 1:  
            print("Ingresaste una fecha de ingreso deficiente anterior a la fecha de ingreso real. Es incorrecto.")
            dia_ingreso_falso = int(input("Ingresa día de ingreso deficientemente registrado:"))
            mes_ingreso_falso = int(input("Ingresa mes de ingreso deficientemente registrado:"))
            año_ingreso_falso = int(input("Ingresa año de ingreso deficientemente registrado:"))

            fecha_ingreso_falsa = datetime(año_ingreso_falso, mes_ingreso_falso, dia_ingreso_falso)
            diferencia3 = relativedelta.relativedelta(fecha_ingreso_falsa, fecha_ingreso)

        años3 = diferencia3.years
        meses3 = diferencia3.months
        dias3 = diferencia3.days

        indemnizacion_art9_ley24013 = ((años3*13*salario_promedio) + (meses3*salario_promedio) + (meses3*salario_promedio/12) + (salario_promedio/30*dias3) + (salario_promedio/30*dias3/12)) /4

    elif art9_ley24013 == "no":
        indemnizacion_art9_ley24013 = 0

# Calcula indemnización Art. 10 ley 24.013. 

    art10_ley24013 = input("¿Queres agregar la multa del Art. 10, ley 24.013? Recorda que corresponde cuando se registro deficientemente el salario y se intimó antes del despido. INGRESAR: si/no: ")

    if art10_ley24013 == "si":
       
        salario_no_registrado = float(input("Ingresa la totalidad del salario no registrado: "))
        dia_salario_falso = int(input("Ingresa día desde registro deficiente de salario: "))
        mes_salario_falso = int(input("Ingresa mes desde registro deficiente de salario: "))
        año_salario_falso = int(input("Ingresa año desde registro deficiente de salario: "))

        fecha_salario_falsa = datetime(año_salario_falso, mes_salario_falso, dia_salario_falso)
        diferencia2 = relativedelta.relativedelta(fecha_egreso, fecha_salario_falsa)
        diferencia4 = relativedelta.relativedelta(fecha_salario_falsa, fecha_ingreso)

        while art10_ley24013 == "si" and int(diferencia4.years) < 1 and int(diferencia4.months) < 1 and int(diferencia4.days) < 1:  
            print("Ingresaste fecha de registro deficiente de salario anterior a la fecha de ingreso real. Es incorrecto.")
            dia_salario_falso = int(input("Ingresa día desde registro deficiente de salario: "))
            mes_salario_falso = int(input("Ingresa mes desde registro deficiente de salario: "))
            año_salario_falso = int(input("Ingresa año desde registro deficiente de salario: "))

            fecha_salario_falsa = datetime(año_salario_falso, mes_salario_falso, dia_salario_falso)
            diferencia4 = relativedelta.relativedelta(fecha_salario_falsa, fecha_ingreso)

        fecha_salario_falsa = datetime(año_salario_falso, mes_salario_falso, dia_salario_falso)
        diferencia2 = relativedelta.relativedelta(fecha_egreso, fecha_salario_falsa)

        años2 = diferencia2.years
        meses2 = diferencia2.months
        dias2 = diferencia2.days

        indemnizacion_art10_ley24013 = ((años2*13*salario_no_registrado) + (meses2*salario_no_registrado) + (meses2*salario_no_registrado/12) + (salario_no_registrado/30*dias2) + (salario_no_registrado/30*dias2/12)) /4
    
    elif art10_ley24013 == "no":
        indemnizacion_art10_ley24013 = 0

  
# Calcula indemnización Art. 80 Ley de Contrato de Trabajo. 

    art80_lct = input("¿Queres agregar la multa del Art. 80 LCT? Recorda que corresponde cuando no se le entregaron los certificados de trabajo correctamente confeccionados dentro del plazo de 30 días. INGRESAR: si/no: ")

    if art80_lct == "si":
        indemnizacion_art80_lct = mrmnh * 3

    else:
        indemnizacion_art80_lct = 0

# Calcula indemnización por cientela. 

    viajante_de_comercio = input("Indemnización por clientela: ¿Era viajante de comercio? INGRESAR: si/no: ")

    if viajante_de_comercio == "si":
        indemnizacion_clientela = (indemnizacion_antiguedad + preaviso + sac_sobre_preaviso + integracion_mes_despido + sac_integracion_mes_despido)/4
    elif viajante_de_comercio == "no":
        indemnizacion_clientela = 0


# Calcula el total de la liquidación por multas e indemnizaciones adicionales.

    total_liquidacion_multas = indemnizacion_art1_ley25323 + indemnizacion_art2_ley25323 + indemnizacion_art8_ley24013 + indemnizacion_art9_ley24013 + indemnizacion_art10_ley24013 + indemnizacion_art15_ley24013 + indemnizacion_art80_lct + indemnizacion_clientela

    total_liquidacion.append (float(total_liquidacion_multas))  # AGREGO A LIQUIDACION MULTAS E INDEMNIZACIONES ADICIONALES.

# Se imprime la liquidación por multas e indemnizaciones adicionales.

    Liquidación.write("\n \n LA LIQUIDACIÓN POR MULTAS E INDEMNIZACIONES ADICIONALES ES LA SIGUIENTE: " "\n Indemnizacion art. 1 ley 25.323: $" + str(indemnizacion_art1_ley25323) + "\n Indemnizacion art. 2 ley 25.323: $" 
    + str(indemnizacion_art2_ley25323) + "\n Indemnizacion art. 8 ley 24.013: $" + str(indemnizacion_art8_ley24013) + "\n Indemnizacion art. 9 ley 24.013: $" + str(indemnizacion_art9_ley24013) 
    + "\n Indemnizacion art. 10 ley 24.013: $" + str(indemnizacion_art10_ley24013) + "\n Indemnizacion art. 15 ley 24.013: $" + str(indemnizacion_art15_ley24013) + "\n Indemnizacion art. 80 LCT: $" 
    + str(indemnizacion_art80_lct) + "\n Indemnizacion por clientela: $" + str(indemnizacion_clientela) + "\n El subtotal por multas e indemnizaciones adicionales es de: $" + str(total_liquidacion_multas))

calcula_indemnizaciones_adicionales = input("¿Deseas que se agreguen multas e indemnizaciones adicionales a la liquidación? INGRESAR: si/no: ")

if calcula_indemnizaciones_adicionales == "si":
    multas_e_indemnizaciones_adicionales()
else:
    pass

# Calcula el TOTAL de la liquidación.

Liquidación.write("\n \n EL TOTAL DE LA LIQUIDACION ES DE $ " + locale.format('%.2f', sum(total_liquidacion),grouping=True, monetary=True)) 


#Agrego esta parte para que aparte de escribirse en documento aparte, te lea el contenido del documento.

Liquidación.seek(0) 

print((Liquidación.read()) + "\n La liquidación quedará guardada en archivo con nombre Liquidación.") #en read puedo pedir hasta que punto del cursor leer

# Cierra el documento.

Liquidación.close()




"""COSAS A AGREGAR

1)INTERFAZ GRAFICA: en construcción

2) CAMBIO A COMAS

import locale

locale.setlocale(locale.LC_ALL, '')

area = 2.34 * 4.9284

print(locale.format('%.2f', area, grouping=True, monetary=True))

3) Calculo de horas extras

4) Calculo de comisiones adeudadas

5) Calculador de promedio de salario

6) Me calcula preaviso para art. 2 ley 25.323 incluso cuando se pago el preaviso. 
"""

