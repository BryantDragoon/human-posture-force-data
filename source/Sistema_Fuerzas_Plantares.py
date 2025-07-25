 # -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 21:03:55 2023

@author: Bryant Ibarra
"""

from tkinter import *
import serial
import numpy as np
import pandas as pd


def ventana_menu(ventana): # Ventana menu

    limpiar_ventana(ventana)
    ventana.title("Sistema de Adquisicion Fuerzas en Postura Doble")
    
    # Widgets
    frm_opciones = Frame(ventana)
    frm_opciones.grid(row=0, column=0, padx=200, pady=10)
    
    lbl_menu = Label(frm_opciones, text="Plantilla a utilizar")
    btn_prueba_11s = Button(frm_opciones, text="Prueba Sistema 11 sensores", width=25, height=5, command=lambda:ventana_prueba_11s(ventana))
    btn_prueba_8s = Button(frm_opciones, text="Prueba Sistema 8 sensores", width=25, height=5, command= lambda:ventana_prueba_8s(ventana))
    btn_prueba_16s = Button(frm_opciones, text="Prueba Sistema 16 sensores", width=25, height=5, command = lambda:ventana_prueba_16s(ventana))
    
    lbl_menu.grid(row=0, column=0)
    btn_prueba_11s.grid(row=1, column=0, pady=5)
    btn_prueba_8s.grid(row=2, column=0, pady=5)
    btn_prueba_16s.grid(row=3, column=0, pady=5)
    
    
def limpiar_ventana(ventana): # Limpieza de todos los elementos
    for widget in ventana.winfo_children():
       widget.destroy()


def ventana_prueba_11s(ventana):
    global img_huellaplantar, btn_conectar, btn_desconectar, btn_iniciolectura, btn_finlectura
    global lbl_procesoact2, lbls_sensores, lbl_pieizq2, lbl_pieder2, frm_registro, almacenar_registro
    
    limpiar_ventana(ventana)
    
    # Configuracion de ventana
    ventana.title("Pruebas - Sistema de Adquisicion Fuerzas en Postura Doble")
    
    # Frames para widgets
    lblfrm_conexion = LabelFrame(ventana, relief=GROOVE, borderwidth=5, text="Conexion con sistema")
    lblfrm_conexion.grid(row=0, column=0, sticky="n")
    lblfrm_huellas = LabelFrame(ventana, relief=RIDGE, borderwidth=5, text="Visualizacion de sensores")
    lblfrm_huellas.grid(row=0, column=1, rowspan=2, columnspan=2) 
    frm_lecturas = LabelFrame(ventana, relief=GROOVE, borderwidth=5, text="Lecturas")
    frm_lecturas.grid(row=1, column=0)
    frm_estado = Frame(ventana)
    frm_estado.grid(row=2, column=1, sticky="w") 
    frm_sensordata = Frame(ventana)
    frm_sensordata.grid(row=2, column=2, sticky="w") 
    frm_registro = Frame(ventana)
    frm_registro.grid(row=0, column=3, padx=5)
    
    # Declaracion de widgets
    btn_conectar = Button(lblfrm_conexion, text="Iniciar Conexion", height=5, width=20, command=activar_conexion)
    btn_desconectar = Button(lblfrm_conexion, text="Detener Conexion", height=5, width=20, state=DISABLED, command=desactivar_conexion) 
    img_huellaplantar = PhotoImage(file="Imagenes/footprints.png") #Imagen base huellas plantares
    bg_huella = Canvas(lblfrm_huellas, width=img_huellaplantar.width(), height=img_huellaplantar.height()) 
    bg_huella.create_image(2,2, image=img_huellaplantar, anchor="nw")
    btn_iniciolectura = Button(frm_lecturas, text="Iniciar Lecturas", height=5, width=20, state=DISABLED, command=lambda:inicio_lectura(ventana))
    btn_finlectura = Button(frm_lecturas, text="Detener Lecturas", height=5, width=20, state=DISABLED, command=fin_lectura) 
    btn_regresar = Button(ventana, text="Regresar", command=lambda:ventana_menu(ventana)) 
    lbl_procesoact1 = Label(frm_estado, text="Estado Actual:")
    lbl_procesoact2 = Label(frm_estado, text="Desconectado")
    lbl_pieizq1 = Label(frm_sensordata, text="Total pie izq:")
    lbl_pieizq2 = Label(frm_sensordata, text=" ")
    lbl_pieder1 = Label(frm_sensordata, text= "Total pie der:")
    lbl_pieder2 = Label(frm_sensordata, text= " ")
    
    # Registro de muestreo
    almacenar_registro = BooleanVar()
    btn_registro = Checkbutton(frm_registro, text="Guardar Registro", variable=almacenar_registro, command=lambda:activar_registro(ventana, almacenar_registro.get()))
    
    #Posicionamiento de widgets
    btn_conectar.grid(row=0, column=0) 
    btn_desconectar.grid(row=1, column=0)
    bg_huella.grid(row=0, column=0)
    btn_iniciolectura.grid(row=0, column=0)
    btn_finlectura.grid(row=1, column=0)
    lbl_procesoact1.grid(row=0, column=0)
    lbl_procesoact2.grid(row=0, column=1)
    lbl_pieizq1.grid(row=0, column=0)
    lbl_pieizq2.grid(row=0, column=1)
    lbl_pieder1.grid(row=0, column=2)
    lbl_pieder2.grid(row=0, column=3)
    btn_regresar.grid(row=2, column=0)
    btn_registro.grid(row=0, column=0)
    
    # Sensores
    lbls_sensores=[]
    for sensor in range(22):
        lbl_sensor = Label(lblfrm_huellas, text="0")
        lbls_sensores.append(lbl_sensor)
    
    # Posicion pie izquierdo 
    lbls_sensores[0].place(x=184, y=730)
    lbls_sensores[2].place(x=220, y=685)
    lbls_sensores[4].place(x=133, y=645)
    lbls_sensores[6].place(x=108, y=520)
    lbls_sensores[8].place(x=128, y=440)
    lbls_sensores[10].place(x=88, y=370)
    lbls_sensores[12].place(x=78, y=300)
    lbls_sensores[14].place(x=130, y=280)
    lbls_sensores[16].place(x=180, y=260)   
    lbls_sensores[18].place(x=238, y=240)
    lbls_sensores[20].place(x=200, y=125)
    
    # Posicion pie derecho, pixel medio 314
    lbls_sensores[1].place(x=444, y=730)
    lbls_sensores[3].place(x=408, y=685)
    lbls_sensores[5].place(x=495, y=645)
    lbls_sensores[7].place(x=520, y=520)
    lbls_sensores[9].place(x=500, y=440)
    lbls_sensores[11].place(x=540, y=370) 
    lbls_sensores[13].place(x=550, y=300) 
    lbls_sensores[15].place(x=498, y=280) 
    lbls_sensores[17].place(x=448, y=260) 
    lbls_sensores[19].place(x=390, y=240)
    lbls_sensores[21].place(x=428, y=125)
    
    ventana.protocol("WM_DELETE_WINDOW", lambda:cierrepruebas(ventana)) 


def ventana_prueba_8s(ventana):
    global img_huellaplantar, btn_conectar, btn_desconectar, btn_iniciolectura, btn_finlectura
    global lbl_procesoact2, lbls_sensores, lbl_pieizq2, lbl_pieder2, frm_registro, almacenar_registro
    
    limpiar_ventana(ventana)
    
    # Configuracion de ventana
    ventana.title("Pruebas - Sistema de Adquisicion Fuerzas en Postura Doble")
    
    # Frames para widgets
    lblfrm_conexion = LabelFrame(ventana, relief=GROOVE, borderwidth=5, text="Conexion con sistema")
    lblfrm_conexion.grid(row=0, column=0, sticky="n")
    lblfrm_huellas = LabelFrame(ventana, relief=RIDGE, borderwidth=5, text="Visualizacion de sensores")
    lblfrm_huellas.grid(row=0, column=1, rowspan=2, columnspan=2) 
    frm_lecturas = LabelFrame(ventana, relief=GROOVE, borderwidth=5, text="Lecturas")
    frm_lecturas.grid(row=1, column=0)
    frm_estado = Frame(ventana)
    frm_estado.grid(row=2, column=1, sticky="w") 
    frm_sensordata = Frame(ventana)
    frm_sensordata.grid(row=2, column=2, sticky="w") 
    frm_registro = Frame(ventana)
    frm_registro.grid(row=0, column=3, padx=5)
    
    # Declaracion de widgets
    btn_conectar = Button(lblfrm_conexion, text="Iniciar Conexion", height=5, width=20, command=activar_conexion)
    btn_desconectar = Button(lblfrm_conexion, text="Detener Conexion", height=5, width=20, state=DISABLED, command=desactivar_conexion) 
    img_huellaplantar = PhotoImage(file="Imagenes/footprints.png") #Imagen base huellas plantares
    bg_huella = Canvas(lblfrm_huellas, width=img_huellaplantar.width(), height=img_huellaplantar.height()) 
    bg_huella.create_image(2,2, image=img_huellaplantar, anchor="nw")
    btn_iniciolectura = Button(frm_lecturas, text="Iniciar Lecturas", height=5, width=20, state=DISABLED, command=lambda:inicio_lectura(ventana))
    btn_finlectura = Button(frm_lecturas, text="Detener Lecturas", height=5, width=20, state=DISABLED, command=fin_lectura) 
    btn_regresar = Button(ventana, text="Regresar", command=lambda:ventana_menu(ventana)) 
    lbl_procesoact1 = Label(frm_estado, text="Estado Actual:")
    lbl_procesoact2 = Label(frm_estado, text="Desconectado")
    lbl_pieizq1 = Label(frm_sensordata, text="Total pie izq:")
    lbl_pieizq2 = Label(frm_sensordata, text=" ")
    lbl_pieder1 = Label(frm_sensordata, text= "Total pie der:")
    lbl_pieder2 = Label(frm_sensordata, text= " ")
    
    # Registro de muestreo
    almacenar_registro = BooleanVar()
    btn_registro = Checkbutton(frm_registro, text="Guardar Registro", variable=almacenar_registro, command=lambda:activar_registro(ventana, almacenar_registro.get()))
    
    #Posicionamiento de widgets
    btn_conectar.grid(row=0, column=0) 
    btn_desconectar.grid(row=1, column=0)
    bg_huella.grid(row=0, column=0)
    btn_iniciolectura.grid(row=0, column=0)
    btn_finlectura.grid(row=1, column=0)
    lbl_procesoact1.grid(row=0, column=0)
    lbl_procesoact2.grid(row=0, column=1)
    lbl_pieizq1.grid(row=0, column=0)
    lbl_pieizq2.grid(row=0, column=1)
    lbl_pieder1.grid(row=0, column=2)
    lbl_pieder2.grid(row=0, column=3)
    btn_regresar.grid(row=2, column=0)
    btn_registro.grid(row=0, column=0)
    
    # Sensores
    lbls_sensores=[]
    for sensor in range(16):
        lbl_sensor = Label(lblfrm_huellas, text="0")
        lbls_sensores.append(lbl_sensor)
    
    # Posicion pie izquierdo 
    lbls_sensores[0].place(x=133, y=645)
    lbls_sensores[2].place(x=220, y=645)
    lbls_sensores[4].place(x=128, y=440)
    lbls_sensores[6].place(x=88, y=370)
    lbls_sensores[8].place(x=78, y=300)
    lbls_sensores[10].place(x=155, y=270)
    lbls_sensores[12].place(x=238, y=240)
    lbls_sensores[14].place(x=200, y=125)
    
    # Posicion pie derecho, pixel medio 314
    lbls_sensores[1].place(x=495, y=645)   
    lbls_sensores[3].place(x=408, y=645)
    lbls_sensores[5].place(x=500, y=440)
    lbls_sensores[7].place(x=540, y=370)
    lbls_sensores[9].place(x=550, y=300)
    lbls_sensores[11].place(x=473, y=270)
    lbls_sensores[13].place(x=390, y=240)
    lbls_sensores[15].place(x=428, y=125) 
      
    ventana.protocol("WM_DELETE_WINDOW", lambda:cierrepruebas(ventana)) 
        
        
def ventana_prueba_16s(ventana):
    global img_huellaplantar, btn_conectar, btn_desconectar, btn_iniciolectura, btn_finlectura
    global lbl_procesoact2, lbls_sensores, lbl_pieizq2, lbl_pieder2, frm_registro, almacenar_registro
    
    limpiar_ventana(ventana)
    
    # Configuracion de ventana
    ventana.title("Pruebas - Sistema de Adquisicion Fuerzas en Postura Doble")
    
    # Frames para widgets
    lblfrm_conexion = LabelFrame(ventana, relief=GROOVE, borderwidth=5, text="Conexion con sistema")
    lblfrm_conexion.grid(row=0, column=0, sticky="n")
    lblfrm_huellas = LabelFrame(ventana, relief=RIDGE, borderwidth=5, text="Visualizacion de sensores")
    lblfrm_huellas.grid(row=0, column=1, rowspan=2, columnspan=2) 
    frm_lecturas = LabelFrame(ventana, relief=GROOVE, borderwidth=5, text="Lecturas")
    frm_lecturas.grid(row=1, column=0)
    frm_estado = Frame(ventana)
    frm_estado.grid(row=2, column=1, sticky="w") 
    frm_sensordata = Frame(ventana)
    frm_sensordata.grid(row=2, column=2, sticky="w") 
    frm_registro = Frame(ventana)
    frm_registro.grid(row=0, column=3, padx=5)
    
    # Declaracion de widgets
    btn_conectar = Button(lblfrm_conexion, text="Iniciar Conexion", height=5, width=20, command=activar_conexion)
    btn_desconectar = Button(lblfrm_conexion, text="Detener Conexion", height=5, width=20, state=DISABLED, command=desactivar_conexion) 
    img_huellaplantar = PhotoImage(file="Imagenes/footprints.png") #Imagen base huellas plantares
    bg_huella = Canvas(lblfrm_huellas, width=img_huellaplantar.width(), height=img_huellaplantar.height()) 
    bg_huella.create_image(2,2, image=img_huellaplantar, anchor="nw")
    btn_iniciolectura = Button(frm_lecturas, text="Iniciar Lecturas", height=5, width=20, state=DISABLED, command=lambda:inicio_lectura(ventana))
    btn_finlectura = Button(frm_lecturas, text="Detener Lecturas", height=5, width=20, state=DISABLED, command=fin_lectura) 
    btn_regresar = Button(ventana, text="Regresar", command=lambda:ventana_menu(ventana)) 
    lbl_procesoact1 = Label(frm_estado, text="Estado Actual:")
    lbl_procesoact2 = Label(frm_estado, text="Desconectado")
    lbl_pieizq1 = Label(frm_sensordata, text="Total pie izq:")
    lbl_pieizq2 = Label(frm_sensordata, text=" ")
    lbl_pieder1 = Label(frm_sensordata, text= "Total pie der:")
    lbl_pieder2 = Label(frm_sensordata, text= " ")
    
    # Registro de muestreo
    almacenar_registro = BooleanVar()
    btn_registro = Checkbutton(frm_registro, text="Guardar Registro", variable=almacenar_registro, command=lambda:activar_registro(ventana, almacenar_registro.get()))
    
    #Posicionamiento de widgets
    btn_conectar.grid(row=0, column=0) 
    btn_desconectar.grid(row=1, column=0)
    bg_huella.grid(row=0, column=0)
    btn_iniciolectura.grid(row=0, column=0)
    btn_finlectura.grid(row=1, column=0)
    lbl_procesoact1.grid(row=0, column=0)
    lbl_procesoact2.grid(row=0, column=1)
    lbl_pieizq1.grid(row=0, column=0)
    lbl_pieizq2.grid(row=0, column=1)
    lbl_pieder1.grid(row=0, column=2)
    lbl_pieder2.grid(row=0, column=3)
    btn_regresar.grid(row=2, column=0)
    btn_registro.grid(row=0, column=0)
    
    # Sensores
    lbls_sensores=[]
    for sensor in range(32):
        lbl_sensor = Label(lblfrm_huellas, text="0")
        lbls_sensores.append(lbl_sensor)

    # Posicion pie izquierdo 
    lbls_sensores[0].place(x=184, y=730)
    lbls_sensores[2].place(x=133, y=645)
    lbls_sensores[4].place(x=220, y=645)
    lbls_sensores[6].place(x=108, y=520) 
    lbls_sensores[8].place(x=168, y=520)  
    lbls_sensores[10].place(x=128, y=440)
    lbls_sensores[12].place(x=90, y=370)     
    lbls_sensores[14].place(x=180, y=370)
    lbls_sensores[16].place(x=78, y=300)
    lbls_sensores[18].place(x=130, y=280)
    lbls_sensores[20].place(x=180, y=260)   
    lbls_sensores[22].place(x=238, y=240)
    lbls_sensores[24].place(x=150, y=215)
    lbls_sensores[26].place(x=200, y=185)
    lbls_sensores[28].place(x=130, y=85)
    lbls_sensores[30].place(x=200, y=60)
    
    # Posicion pie derecho, pixel medio 314
    lbls_sensores[1].place(x=444, y=730)
    lbls_sensores[3].place(x=495, y=645)
    lbls_sensores[5].place(x=408, y=645)
    lbls_sensores[7].place(x=520, y=520) 
    lbls_sensores[9].place(x=460, y=520)  
    lbls_sensores[11].place(x=500, y=440)
    lbls_sensores[13].place(x=538, y=370)     
    lbls_sensores[15].place(x=448, y=370)
    lbls_sensores[17].place(x=550, y=300)
    lbls_sensores[19].place(x=498, y=280)
    lbls_sensores[21].place(x=448, y=260)   
    lbls_sensores[23].place(x=390, y=240)
    lbls_sensores[25].place(x=478, y=215)
    lbls_sensores[27].place(x=428, y=185)
    lbls_sensores[29].place(x=498, y=85)
    lbls_sensores[31].place(x=428, y=60)
    
    ventana.protocol("WM_DELETE_WINDOW", lambda:cierrepruebas(ventana)) 


def activar_registro(ventana, activar):
    global lbl_nombre, ent_nombre
    if (activar==True):
        lbl_nombre = Label(frm_registro, text="Nombre de archivo:")
        lbl_nombre.grid(row=1, column=0)
        ent_nombre = Entry(frm_registro)
        ent_nombre.grid(row=2, column=0)
    else:
        lbl_nombre.grid_remove()
        ent_nombre.grid_remove()

 
def activar_conexion():
    global Esp32
    try: 
        Esp32 = serial.Serial('COM6', timeout = 0)
        lbl_procesoact2["text"]="Conexion establecida con " + Esp32.name
        btn_conectar["state"]=DISABLED
        btn_desconectar["state"]=NORMAL
        btn_iniciolectura["state"]=NORMAL
    
    except:
        lbl_procesoact2["text"]="No se pudo conectar con el dispositivo"

def desactivar_conexion():
    Esp32.close()
    lbl_procesoact2["text"]="Desconectado"
    btn_conectar["state"]=NORMAL
    btn_desconectar["state"]=DISABLED
    btn_iniciolectura["state"]=DISABLED
    btn_finlectura["state"]=DISABLED
    
def inicio_lectura(ventana):
    global validacion, df_lecturas, df_lecturasADC
    
    btn_iniciolectura["state"]=DISABLED
    btn_finlectura["state"]=NORMAL
    lbl_procesoact2["text"]="Lecturas Activas"
    validacion=True
    Esp32.write("<a>".encode())
    
    #Almacenamiento de los datos
    if (len(lbls_sensores)==16):
        df_lecturas = pd.DataFrame(columns=["Sensor1", "Sensor9", "Sensor2", "Sensor10", "Sensor3", "Sensor11", "Sensor4", "Sensor12", "Sensor5", "Sensor13", 
                               "Sensor6", "Sensor14", "Sensor7", "Sensor15", "Sensor8", "Sensor16", "Sensor17", "Sensor18", "Sensor19", "Sensor20", 
                               "Sensor21", "Sensor22", "Sensor23", "Sensor24", "Sensor25", "Sensor26", "Sensor27", "Sensor28", "Sensor29", "Sensor30", 
                               "Sensor31", "Sensor32"])
        df_lecturasADC = pd.DataFrame(columns=["Sensor1", "Sensor9", "Sensor2", "Sensor10", "Sensor3", "Sensor11", "Sensor4", "Sensor12", "Sensor5", "Sensor13", 
                               "Sensor6", "Sensor14", "Sensor7", "Sensor15", "Sensor8", "Sensor16", "Sensor17", "Sensor18", "Sensor19", "Sensor20", 
                               "Sensor21", "Sensor22", "Sensor23", "Sensor24", "Sensor25", "Sensor26", "Sensor27", "Sensor28", "Sensor29", "Sensor30", 
                               "Sensor31", "Sensor32"])
    
    elif (len(lbls_sensores)==22):
        df_lecturas = pd.DataFrame(columns=["Sensor1", "Sensor12", "Sensor2", "Sensor13", "Sensor3", "Sensor14", "Sensor4", "Sensor15", "Sensor5", "Sensor16", 
                               "Sensor6", "Sensor17", "Sensor7", "Sensor18", "Sensor8", "Sensor19", "Sensor9", "Sensor20", "Sensor10", "Sensor21", 
                               "Sensor11", "Sensor22", "Sensor23", "Sensor24", "Sensor25", "Sensor26", "Sensor27", "Sensor28", "Sensor29", "Sensor30", 
                               "Sensor31", "Sensor32"])
        df_lecturasADC = pd.DataFrame(columns=["Sensor1", "Sensor12", "Sensor2", "Sensor13", "Sensor3", "Sensor14", "Sensor4", "Sensor15", "Sensor5", "Sensor16", 
                               "Sensor6", "Sensor17", "Sensor7", "Sensor18", "Sensor8", "Sensor19", "Sensor9", "Sensor20", "Sensor10", "Sensor21", 
                               "Sensor11", "Sensor22", "Sensor23", "Sensor24", "Sensor25", "Sensor26", "Sensor27", "Sensor28", "Sensor29", "Sensor30", 
                               "Sensor31", "Sensor32"])
    
    elif (len(lbls_sensores)==32):
        df_lecturas = pd.DataFrame(columns=["Sensor1", "Sensor17", "Sensor2", "Sensor18", "Sensor3", "Sensor19", "Sensor4", "Sensor20", "Sensor5", "Sensor21", 
                               "Sensor6", "Sensor22", "Sensor7", "Sensor23", "Sensor8", "Sensor24", "Sensor9", "Sensor25", "Sensor10", "Sensor26", 
                               "Sensor11", "Sensor27", "Sensor12", "Sensor28", "Sensor13", "Sensor29", "Sensor14", "Sensor30", "Sensor15", "Sensor31", 
                               "Sensor16", "Sensor32"])
        df_lecturasADC = pd.DataFrame(columns=["Sensor1", "Sensor17", "Sensor2", "Sensor18", "Sensor3", "Sensor19", "Sensor4", "Sensor20", "Sensor5", "Sensor21", 
                               "Sensor6", "Sensor22", "Sensor7", "Sensor23", "Sensor8", "Sensor24", "Sensor9", "Sensor25", "Sensor10", "Sensor26", 
                               "Sensor11", "Sensor27", "Sensor12", "Sensor28", "Sensor13", "Sensor29", "Sensor14", "Sensor30", "Sensor15", "Sensor31", 
                               "Sensor16", "Sensor32"])
    lectura_sensores(ventana)
    

def fin_lectura():
    global validacion
    
    btn_finlectura["state"]=DISABLED
    btn_iniciolectura["state"]=NORMAL
    lbl_procesoact2["text"]="Desactivo"
    validacion = False
    Esp32.write("<s>".encode())
    limpia_buffer()
    
    #Dataframe a csv
    if(almacenar_registro.get()==True):
        if(len(lbls_sensores)==22):
            df_lecturas.to_csv(f"Resultados/11s/{ent_nombre.get()}_11s.csv")
            df_lecturasADC.to_csv(f"Resultados/11s/ADC/{ent_nombre.get()}_ADC_11s.csv")
        elif(len(lbls_sensores)==16):
            df_lecturas.to_csv(f"Resultados/8s/{ent_nombre.get()}_8s.csv")
            df_lecturasADC.to_csv(f"Resultados/8s/ADC/{ent_nombre.get()}_ADC_8s.csv")
        elif(len(lbls_sensores)==32):
            df_lecturas.to_csv(f"Resultados/16s/{ent_nombre.get()}_16s.csv")
            df_lecturasADC.to_csv(f"Resultados/16s/ADC/{ent_nombre.get()}_ADC_16s.csv")
    
def lectura_sensores(ventana):

    if(validacion==True):
        data = sensordata()
        valores = data.split(",")
        if (len(valores)>1):
            Vin = 3.3
            R1 = 10000  
            Rmux = 62.1857
            msensor = np.zeros(len(valores))
            msensorADC = np.zeros(len(valores))
            
            for sensor in range(len(lbls_sensores)):
                val = int(valores[sensor])
                msensorADC[sensor]=val
                if (val > 0):
                    Vout = (val * Vin)/4095;
                    rs = (R1 * ((Vin/Vout) - 1))-Rmux
                    
                    #Ecuacion de 32 sensores
                    ecuaciones = [np.exp((np.log(rs/4912.8))/-0.650), #sensor 1
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/3955.4))/-0.551),
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/4356.4))/-0.600), #sensor 5
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/5903.8))/-0.716), 
                                  np.exp((np.log(rs/4527.7))/-0.598), #sensor 10
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/4527.7))/-0.598), #sensor 15
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/4527.7))/-0.598), #sensor 20
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/4527.7))/-0.598), #sensor 25
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/4527.7))/-0.598),
                                  np.exp((np.log(rs/4527.7))/-0.598), #29 
                                  np.exp((np.log(rs/4527.7))/-0.598), #30
                                  np.exp((np.log(rs/4527.7))/-0.598), 
                                  np.exp((np.log(rs/4527.7))/-0.598) ]  
            
                    msensor[sensor] = np.around(ecuaciones[sensor],3)
                    lbls_sensores[sensor]["text"]=msensor[sensor]
                else:
                    lbls_sensores[sensor]["text"]=msensor[sensor]
            
            df_lecturasADC.loc[len(df_lecturasADC)]=msensorADC
            df_lecturas.loc[len(df_lecturas)]=msensor
            if(len(lbls_sensores)==16):
                lbl_pieizq2["text"]=np.around(msensor[0]+msensor[2]+msensor[4]+msensor[6]+msensor[8]+msensor[10]+msensor[12]+msensor[14],3), "kg"
                lbl_pieder2["text"]=np.around(msensor[1]+msensor[3]+msensor[5]+msensor[7]+msensor[9]+msensor[11]+msensor[13]+msensor[15],3), "kg" 
             
            elif(len(lbls_sensores)==22):
                lbl_pieizq2["text"]=np.around(msensor[0]+msensor[2]+msensor[4]+msensor[6]+msensor[8]+msensor[10]+msensor[12]+msensor[14]+msensor[16]+msensor[18]+msensor[20],3), "kg"
                lbl_pieder2["text"]=np.around(msensor[1]+msensor[3]+msensor[5]+msensor[7]+msensor[9]+msensor[11]+msensor[13]+msensor[15]+msensor[17]+msensor[19]+msensor[21],3), "kg" 
#           
            
            elif(len(lbls_sensores)==32):
                lbl_pieizq2["text"]=np.around(msensor[0]+msensor[2]+msensor[4]+msensor[6]+msensor[8]+msensor[10]+msensor[12]+msensor[14]+msensor[16]+msensor[18]+msensor[20]+msensor[22]+msensor[24]+msensor[26]+msensor[28]+msensor[30],3), "kg"
                lbl_pieder2["text"]=np.around(msensor[1]+msensor[3]+msensor[5]+msensor[7]+msensor[9]+msensor[11]+msensor[13]+msensor[15]+msensor[17]+msensor[19]+msensor[21]+msensor[23]+msensor[25]+msensor[27]+msensor[29]+msensor[31],3), "kg" 
            
        ventana.after(40, lambda:lectura_sensores(ventana))
        

def sensordata(): #Recibe la cadena de datos 
    DataTransmision = False
    NuevosDatos = False
    Inidata = '<'
    Findata = '>'
    Dato = '\0'
    
    DatosSensor = ""
    if Esp32.inWaiting(): 
        while Esp32.inWaiting() and NuevosDatos == False:
            Dato = Esp32.read().decode()
            if (DataTransmision == True):
                if (Dato != Findata):
                    DatosSensor += Dato 
                else:
                    NuevosDatos = True
            elif (Dato == Inidata):
                DataTransmision = True  
        return DatosSensor
    return DatosSensor


        
def cierrepruebas(ventana):
    try:
        if validacion==True:
            Esp32.write("<s>".encode())
        Esp32.close()
        ventana.destroy()
    
    except:
        ventana.destroy()

def limpia_buffer():
    while Esp32.inWaiting(): 
        Esp32.read()
        
    
    
# Llamada principal
root = Tk()
ventana_menu(root)
root.mainloop()


