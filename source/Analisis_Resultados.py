# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 21:50:30 2023

@author: Bryant Ibarra
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Grafica 3D de un resultado particular 
def analisispeso(usuario, numprueba, sensores):
    prueba = pd.read_csv(f"{sensores}s/{usuario}_{numprueba}_{sensores}s.csv", index_col=0, usecols=range(sensores*2+1)) 
    resultado = prueba.agg(np.mean)

    #Coordenadas sensores
    if sensores == 8:
        ord_sens = ['1','9','2','10','3','11','4','12','5','13','6','14','7','15','8','16']
        px = [133,495,220,408,128,500,88,540,78,550,155,473,238,390,200,428] 
        py = [645,645,645,645,440,400,370,370,300,300,270,270,240,240,125,125] 
    
    elif sensores == 11:
        ord_sens = ['1','12','2','13','3','14','4','15','5','16','6','17','7','18','8','19','9','20','10','21','11','22']
        px = [184,444,220,408,133,495,108,520,128,500,88,540,78,550,130,498,180,448,238,390,200,428] 
        py = [730,730,685,685,645,645,520,520,440,440,370,370,300,300,280,280,260,260,240,240,125,125]

    elif sensores == 16:
        ord_sens = ['1','17','2','18','3','19','4','20','5','21','6','22','7','23','8','24','9','25','10','26','11','27','12','28','13','29','14','30','15','31','16','32']
        px = [184,444,133,495,220,408,108,520,168,460,128,500,90,538,180,448,78,550,130,498,180,448,238,390,150,478,200,428,130,498,200,428] 
        py = [730,730,645,645,645,645,520,520,520,520,440,440,370,370,370,370,300,300,280,280,260,260,240,240,215,215,185,185,85,85,60,60]
        
    pz = np.zeros(len(px))
    dx = np.full(len(px),20)
    dy = np.full(len(py),20)
    
    #Datos usuario
    dz = resultado
    
    fig = plt.figure(layout="constrained") #figsize=(18, 9), 
    ax1 = fig.add_subplot(1,2,1, projection="3d", computed_zorder=False)
    ax2 = fig.add_subplot(1,2,2)
     
    #Imagen en plano 3d
    img = plt.imread("footprints.png") #Imagen base huellas plantares
    height, width = img.shape[:2]    
    x = np.arange(0, width)
    y = np.arange(0, height)
    x, y = np.meshgrid(x, y)
    ax1.plot_surface(x, y, np.atleast_2d(0), rstride=3, cstride=3, facecolors=img, shade=False, zorder=0)
    
    #Grafico de barras 3d
    ax1.bar3d(px,py,pz,dx,dy,dz, zorder=.01, edgecolor='black')
    for c,r,a,s in zip(px, py, dz, ord_sens):
        ax1.text(c, r-10, a*.9, s, bbox=(dict(facecolor='white', alpha=.4)))
    valor_ref = np.around(dz.max()/2)
    ax1.bar3d(width,0,0,-20,20,valor_ref, zorder=.01, color="aqua", edgecolor='black')  
    ax1.text(width, -80, valor_ref+.10, f"Referencia: {valor_ref} kg", bbox=(dict(facecolor='white')), zdir="y")
        
    #Grafico 2 - Pastel sensores
    dz = dz.set_axis(ord_sens)
    dz.index = dz.index.astype(int)
    dz = dz.sort_index()
    sensores_innecesarios = np.less_equal(dz, 0.01)
    dz.drop(dz.index[sensores_innecesarios], inplace=True)
    radio = 1.0
    _, labels, pct_texts = ax2.pie(dz, labels=dz.index, autopct=lambda pct: f"{pct:.1f}%\n({pct*np.sum(dz)/100:.2f} kg)", radius=radio, 
            wedgeprops={"edgecolor":"w","width":.3}, pctdistance=.85, labeldistance=1.03, rotatelabels = True) 
    for label, pct_text in zip(labels, pct_texts): 
        pct_text.set_rotation(label.get_rotation())
    #Pastel apoyo
    cambio_pie = 0
    for valor in dz.index:
        if valor <= sensores:
            cambio_pie += 1
        else:
            break
    pie_izq = dz.iloc[:cambio_pie].sum()
    pie_der = dz.iloc[cambio_pie:].sum()
    ax2.pie((pie_izq,pie_der), labels=["Pie izquierdo","Pie derecho"], 
            autopct=lambda pct: f"{pct:.1f}% ({pct*(pie_izq+pie_der)/100:.2f} kg)", radius=radio-.3, 
            wedgeprops={"edgecolor":"w", "width":.3}, pctdistance=.7, labeldistance=.8)
    
    #Configuraciones adcicionales 
    ax1.invert_xaxis()
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_zticks([])
    ax1.view_init(elev=22, azim=320)
    ax1.set_title("Representacion 3D", fontsize=16)
    ax2.set_title("Distribucion de peso captado en sensores", fontsize=16)
    fig.suptitle(f"Resultado de fuerzas captadas para {usuario} con {sensores} sensores", fontsize=20)# 
    plt.show()


    return resultado

# Ejemplo de como usar:
#analsis_detallado = analisispeso("BI",1,16) 



#Comparacion de los muestreos en todas pruebas
def prommuestreo(usuario, rep, plant):
    
    #Promedio de todos los muestreos seleccionados en un dataframe
    completo = pd.DataFrame()
    for num in rep:
        prueba = pd.read_csv(f"{plant}s/{usuario}_{num}_{plant}s.csv", index_col=0, usecols=range(plant*2+1))
        promprueba = prueba.mean()
        completo = pd.concat([completo , promprueba.rename(num)], axis=1)
    
    if plant == 8:
        ord_sens = ['1','9','2','10','3','11','4','12','5','13','6','14','7','15','8','16']
    elif plant == 11:
        ord_sens = ['1','12','2','13','3','14','4','15','5','16','6','17','7','18','8','19','9','20','10','21','11','22']
    elif plant == 16:
        ord_sens = ['1','17','2','18','3','19','4','20','5','21','6','22','7','23','8','24','9','25','10','26','11','27','12','28','13','29','14','30','15','31','16','32']
    completo.set_axis(ord_sens, inplace=True)
 
    plt.figure()
    plt.plot(completo, marker=".", lw=2)
    plt.title(f"Resultado de fuerzas captadas con plantilla de {plant}s para {usuario}", fontsize=20)
    plt.ylabel("Peso estimado (kg)")
    plt.xlabel("Sensor")
    plt.grid(axis="y")
    plt.legend(completo, title="Prueba")
    plt.show()
    
    return completo


#Ejemplo de como usar:
#comparacion_pruebas = prommuestreo("BI", [1,2,3,4,5,6,7,8,9,10], 16)



#Comparacion de fuerzas totales captadas con cada plantilla
def pesosplantillas(usuario):
   
    #Lectura de todas las pruebas 
    pesos8s = []
    pesos11s = []
    pesos16s = []
   
    for num in range(1,11):
        #Lectura del muestreo 8s
        prueba = pd.read_csv(f"8s/{usuario}_{num}_8s.csv", usecols=range(1,17))
        promprueba = prueba.mean().sum()
        pesos8s.append(promprueba)
        
        #Muestreo 11s 
        prueba = pd.read_csv(f"11s/{usuario}_{num}_11s.csv", usecols=range(1,23))
        promprueba = prueba.mean().sum()
        pesos11s.append(promprueba)
        
        #Muestreo 16s
        prueba = pd.read_csv(f"16s/{usuario}_{num}_16s.csv", usecols=range(1,33))        
        promprueba = prueba.mean().sum()
        pesos16s.append(promprueba)
    
    plt.figure()
    box = plt.boxplot([pesos8s, pesos11s, pesos16s], labels=["8 Sensores", "11 Sensores", "16 Sensores"], showmeans=True, meanline=True, patch_artist=True, medianprops={"linewidth": 1.7, "solid_capstyle": "butt"}, meanprops={"linewidth": 1.7})
    plt.title("Fuerzas Totales captadas con cada propuesta de plantilla ("+usuario+")")
    plt.ylabel("Peso total captado (kg)")
    plt.xlabel("Plantilla utilizada")
    plt.grid(axis="y")
    plt.legend([box['medians'][0], box['means'][0], box["caps"][0], box["fliers"][0]],["Mediana", "Media","Valor extremo","Valor atípico"])
    colores = ["lightblue", "pink", "lightsteelblue"]
    for box,color in zip(box['boxes'], colores):
        box.set_facecolor(color)
    plt.show()
    
#Ejemplo de como usar:
#pesosplantillas("BI")



#Comparacion entre usuarios, de resultados captados del mismo tipo de plantilla
def comp_desemplantilla(usuarios, pesos, plantilla):
    #Dataframe con todos los usuarios
    completo = pd.DataFrame()
    
    for user, peso in zip(usuarios,pesos):
        for num in range(1,11):
            #Lectura del muestreo
            prueba = pd.read_csv(f"{plantilla}s/{user}_{num}_{plantilla}s.csv", index_col=0, usecols=range(plantilla*2+1))
            promprueba = prueba.agg(np.mean)
            sujeto = [user]
            peso_usuario = peso
            promprueba = pd.DataFrame(promprueba).T
            promprueba["Usuario"]=sujeto
            promprueba["Peso (kg)"]=peso_usuario
            completo = pd.concat([completo , promprueba], ignore_index=True)
    
    completo["Total Captado"] =  completo.iloc[:,:plantilla*2].sum(axis=1)

    #Aqui se agrupa por usuario
    df_group = completo.groupby("Usuario")
   
    plt.figure(figsize=(11, 6))
    box = plt.boxplot([df_group["Total Captado"].get_group(name) for name in df_group.groups.keys()], labels=df_group.groups.keys(), showmeans=True, meanline=True, patch_artist=True, medianprops={"linewidth": 1.7, "solid_capstyle": "butt"}, meanprops={"linewidth": 1.7})
    plt.title(f"Fuerzas totales captadas con plantilla de {plantilla} sensores", fontsize = 18)
    plt.ylabel("Peso total captado (kg)", fontsize=12)
    plt.xlabel("Usuario", fontsize=12)
    plt.grid(axis="y")
    plt.legend([box['medians'][0], box['means'][0], box["caps"][0], box["fliers"][0]],["Mediana", "Media","Valor extremo","Valor atípico"])
    colores = ["lightblue", "pink", "azure", "snow", "plum", "beige", "lightsteelblue", "palegreen", "lightyellow", "lavender","peachpuff"]
    for box,color in zip(box['boxes'], colores):
        box.set_facecolor(color)
    plt.tight_layout()
    plt.show()
    
    df_std = df_group["Total Captado"].std()
    df_resumido = df_group.mean()
    df_resumido["std"] =  df_std
    
  #  return completo
    return df_resumido

 
#Ejemplo de como usar:
#usuarios que hicieron las pruebas en las tres plantillas
#usuarios = ["AA","AI","BI","DO","JA","JAI","JJ","JT","LI","SO","WI"] 
#pesos = [51.3,89.75,69.15,54.5,59.45,90.95,93.35,59,111.30,76.2,78.90]

#Usuarios con pie plano
#usuarios = ["DA","FF"] 
#pesos = [75,65]

#pesos_comparados = comp_desemplantilla(usuarios, pesos, 16)



#Comparacion entre resultados normalizados del mismo tipo de plantilla
def desemplantilla(usuarios, pesos, plantilla):
    #Dataframe con todos los usuarios
    completo = pd.DataFrame()
    
    for user, peso in zip(usuarios,pesos):
        for num in range(1,11):
            #Lectura del muestreo
            prueba = pd.read_csv(f"{plantilla}s/{user}_{num}_{plantilla}s.csv", index_col=0, usecols=range(plantilla*2+1))
            promprueba = prueba.agg(np.mean)
            sujeto = [user]
            peso_usuario = peso
            promprueba = pd.DataFrame(promprueba).T
            promprueba["Usuario"]=sujeto
            promprueba["Peso (kg)"]=peso_usuario
            completo = pd.concat([completo , promprueba], ignore_index=True)
    
    df_normalizado = completo.copy()
    
    #Normaliza
    df_normalizado.iloc[:,:plantilla*2] = df_normalizado.iloc[:,:plantilla*2].div(df_normalizado["Peso (kg)"], axis=0)
    df_normalizado["Total Captado"] =  df_normalizado.iloc[:,:plantilla*2].sum(axis=1)
    
    #Eliminar malos resultado
    if plantilla==8 and len(usuarios)>3:
        df_normalizado.drop([72], inplace=True)
    if plantilla==16 and len(usuarios)>3:
        df_normalizado.drop([81,84,85,86,89], inplace=True)
    
    normalizado_extendido = df_normalizado.copy()
    
    #Aqui se agrupa por usuario
    df_group = df_normalizado.groupby("Usuario")
    df_std = df_group["Total Captado"].std()
      
    df_normalizado = df_group.mean()
    df_normalizado["std"] =  df_std
    
    plt.figure()
    box = plt.boxplot([df_group["Total Captado"].get_group(name) for name in df_group.groups.keys()], labels=df_group.groups.keys(), showmeans=True, meanline=True, patch_artist=True, medianprops={"linewidth": 1.7, "solid_capstyle": "butt"}, meanprops={"linewidth": 1.7})
    plt.title(f"Comparación de fuerzas totales normalizadas captadas con plantilla {plantilla}s")
    plt.ylabel("Rango captado (%kg total)")
    plt.xlabel("Usuario")
    plt.grid(axis="y")
    plt.legend([box['medians'][0], box['means'][0], box["caps"][0], box["fliers"][0]],["Mediana", "Media","Valor extremo","Valor atípico"])
    colores = ["lightblue", "pink", "azure", "snow", "plum", "beige", "lightsteelblue", "palegreen", "lightyellow", "lavender","peachpuff"]
    for box,color in zip(box['boxes'], colores):
        box.set_facecolor(color)
    plt.show()
   
    return completo, normalizado_extendido, df_normalizado
    

#Ejemplo de como usar:
#USUARIOS QUE HICIERON LAS PRUEBAS EN LAS 3 PLANTILLAS
#usuarios = ["AA","AI","BI","DO","JA","JAI","JJ","JT","LI","SO","WI"] 
#pesos = [51.3,89.75,69.15,54.5,59.45,90.95,93.35,59,111.30,76.2,78.90]

#USUARIOS CON PIE PLANO
#usuarios = ["DA","FF"] 
#pesos = [75,65]

#original, comp_desem_ext, comparacion_desempeno = desemplantilla(usuarios, pesos, 16)



#Comparacion secciones normalizadas con el mismo tipo de plantilla con desviaciones estandar
def desemplantilla_det(usuarios, pesos, plantilla):
    #Dataframe con todos los usuarios
    completo = pd.DataFrame()
    
    for user, peso in zip(usuarios,pesos):
        for num in range(1,11):
            #Lectura del muestreo
            prueba = pd.read_csv(f"{plantilla}s/{user}_{num}_{plantilla}s.csv", index_col=0, usecols=range(plantilla*2+1))
            promprueba = prueba.agg(np.mean)
            sujeto = [user]
            peso_usuario = peso
            promprueba = pd.DataFrame(promprueba).T
            promprueba["Sujeto"]=sujeto
            promprueba["Peso (kg)"]=peso_usuario
            completo = pd.concat([completo , promprueba], ignore_index=True)

    df_normalizado = completo.copy()
    
    #Normaliza
    df_normalizado.iloc[:,:plantilla*2] = df_normalizado.iloc[:,:plantilla*2].div(df_normalizado["Peso (kg)"], axis=0)
   
    if plantilla == 8: 
        df_normalizado["Retropie Izq"] =  df_normalizado.iloc[:,0:3:2].sum(axis=1)
        df_normalizado["Mediopie Izq"] =  df_normalizado.iloc[:,4:7:2].sum(axis=1)
        df_normalizado["Antepie Izq"] =  df_normalizado.iloc[:,8:15:2].sum(axis=1)
        df_normalizado["Retropie Der"] =  df_normalizado.iloc[:,1:4:2].sum(axis=1)
        df_normalizado["Mediopie Der"] =  df_normalizado.iloc[:,5:8:2].sum(axis=1)
        df_normalizado["Antepie Der"] =  df_normalizado.iloc[:,9:16:2].sum(axis=1)

    elif plantilla == 11: 
        df_normalizado["Retropie Izq"] =  df_normalizado.iloc[:,0:5:2].sum(axis=1)
        df_normalizado["Mediopie Izq"] =  df_normalizado.iloc[:,6:11:2].sum(axis=1)
        df_normalizado["Antepie Izq"] =  df_normalizado.iloc[:,12:21:2].sum(axis=1)
        df_normalizado["Retropie Der"] =  df_normalizado.iloc[:,1:6:2].sum(axis=1)
        df_normalizado["Mediopie Der"] =  df_normalizado.iloc[:,7:12:2].sum(axis=1)
        df_normalizado["Antepie Der"] =  df_normalizado.iloc[:,13:22:2].sum(axis=1)
        
    elif plantilla == 16: 
        df_normalizado["Retropie Izq"] =  df_normalizado.iloc[:,0:5:2].sum(axis=1)
        df_normalizado["Mediopie Izq"] =  df_normalizado.iloc[:,6:15:2].sum(axis=1)
        df_normalizado["Antepie Izq"] =  df_normalizado.iloc[:,16:31:2].sum(axis=1)
        df_normalizado["Retropie Der"] =  df_normalizado.iloc[:,1:6:2].sum(axis=1)
        df_normalizado["Mediopie Der"] =  df_normalizado.iloc[:,7:16:2].sum(axis=1)
        df_normalizado["Antepie Der"] =  df_normalizado.iloc[:,17:32:2].sum(axis=1)

    normalizado_extendido = df_normalizado.copy()
    
    #Aqui se agrupa por usuario
    df_group = df_normalizado.groupby("Sujeto")
    std_ai = df_group["Antepie Izq"].std()
    std_mi = df_group["Mediopie Izq"].std()
    std_ri = df_group["Retropie Izq"].std()
    std_ad = df_group["Antepie Der"].std()
    std_md = df_group["Mediopie Der"].std()
    std_rd = df_group["Retropie Der"].std()
      
    df_normalizado = df_group.mean()
    df_normalizado["std_ai"] =  std_ai
    df_normalizado["std_mi"] =  std_mi
    df_normalizado["std_ri"] =  std_ri
    df_normalizado["std_ad"] =  std_ad
    df_normalizado["std_md"] =  std_md
    df_normalizado["std_rd"] =  std_rd
    
    df_normalizado["ai"] =  df_normalizado["Antepie Izq"].round(5).astype(str) + " (" + df_normalizado["std_ai"].round(4).astype(str) + ")" 
    df_normalizado["mi"] =  df_normalizado["Mediopie Izq"].round(5).astype(str) + " (" + df_normalizado["std_mi"].round(4).astype(str) + ")"
    df_normalizado["ri"] =  df_normalizado["Retropie Izq"].round(5).astype(str) + " (" + df_normalizado["std_ri"].round(4).astype(str) + ")"
    df_normalizado["ad"] =  df_normalizado["Antepie Der"].round(5).astype(str) + " (" + df_normalizado["std_ad"].round(4).astype(str) + ")" 
    df_normalizado["md"] =  df_normalizado["Mediopie Der"].round(5).astype(str) + " (" + df_normalizado["std_md"].round(4).astype(str) + ")"
    df_normalizado["rd"] =  df_normalizado["Retropie Der"].round(5).astype(str) + " (" + df_normalizado["std_rd"].round(4).astype(str) + ")"
    
    return completo, normalizado_extendido, df_normalizado
    

#Ejemplo de como usar:
#USUARIOS QUE HICIERON LAS PRUEBAS EN LAS 3 PLANTILLAS
#usuarios = ["AA","AI","BI","DO","JA","JAI","JJ","JT","LI","SO","WI"] 
#pesos = [51.3,89.75,69.15,54.5,59.45,90.95,93.35,59,111.30,76.2,78.90]

#USUARIOS CON PIE PLANO
#usuarios = ["DA","FF"] 
#pesos = [75,65]

#original, comp_desem_ext, comparacion_desempeno = desemplantilla_det(usuarios, pesos, 16)



#Resultado normalizado del tosdo un mismo tipo de plantilla con desviacion estandar
def desemplantilla_total(usuarios, pesos, plantilla):
    #Dataframe con todos los usuarios
    completo = pd.DataFrame()
    
    for user, peso in zip(usuarios,pesos):
        for num in range(1,11):
            #Lectura del muestreo
            prueba = pd.read_csv(f"{plantilla}s/{user}_{num}_{plantilla}s.csv", index_col=0, usecols=range(plantilla*2+1))
            promprueba = prueba.agg(np.mean)
            sujeto = [user]
            peso_usuario = peso
            promprueba = pd.DataFrame(promprueba).T
            promprueba["Sujeto"]=sujeto
            promprueba["Peso (kg)"]=peso_usuario
            completo = pd.concat([completo , promprueba], ignore_index=True)
    
    df_normalizado = completo.copy()
    
    #Normaliza
    df_normalizado.iloc[:,:plantilla*2] = df_normalizado.iloc[:,:plantilla*2].div(df_normalizado["Peso (kg)"], axis=0)
   
    if plantilla == 8: 
        df_normalizado["Retropie Izq"] =  df_normalizado.iloc[:,0:3:2].sum(axis=1)
        df_normalizado["Mediopie Izq"] =  df_normalizado.iloc[:,4:7:2].sum(axis=1)
        df_normalizado["Antepie Izq"] =  df_normalizado.iloc[:,8:15:2].sum(axis=1)
        df_normalizado["Retropie Der"] =  df_normalizado.iloc[:,1:4:2].sum(axis=1)
        df_normalizado["Mediopie Der"] =  df_normalizado.iloc[:,5:8:2].sum(axis=1)
        df_normalizado["Antepie Der"] =  df_normalizado.iloc[:,9:16:2].sum(axis=1)

    elif plantilla == 11: 
        df_normalizado["Retropie Izq"] =  df_normalizado.iloc[:,0:5:2].sum(axis=1)
        df_normalizado["Mediopie Izq"] =  df_normalizado.iloc[:,6:11:2].sum(axis=1)
        df_normalizado["Antepie Izq"] =  df_normalizado.iloc[:,12:21:2].sum(axis=1)
        df_normalizado["Retropie Der"] =  df_normalizado.iloc[:,1:6:2].sum(axis=1)
        df_normalizado["Mediopie Der"] =  df_normalizado.iloc[:,7:12:2].sum(axis=1)
        df_normalizado["Antepie Der"] =  df_normalizado.iloc[:,13:22:2].sum(axis=1)
        
    elif plantilla == 16: 
        df_normalizado["Retropie Izq"] =  df_normalizado.iloc[:,0:5:2].sum(axis=1)
        df_normalizado["Mediopie Izq"] =  df_normalizado.iloc[:,6:15:2].sum(axis=1)
        df_normalizado["Antepie Izq"] =  df_normalizado.iloc[:,16:31:2].sum(axis=1)
        df_normalizado["Retropie Der"] =  df_normalizado.iloc[:,1:6:2].sum(axis=1)
        df_normalizado["Mediopie Der"] =  df_normalizado.iloc[:,7:16:2].sum(axis=1)
        df_normalizado["Antepie Der"] =  df_normalizado.iloc[:,17:32:2].sum(axis=1)
    
    #Aqui se agrupa por usuario
    df_group = df_normalizado.groupby("Sujeto")
    std_ai = df_group["Antepie Izq"].std()
    std_mi = df_group["Mediopie Izq"].std()
    std_ri = df_group["Retropie Izq"].std()
    std_ad = df_group["Antepie Der"].std()
    std_md = df_group["Mediopie Der"].std()
    std_rd = df_group["Retropie Der"].std()
      
    df_normalizado = df_group.mean()
    df_normalizado["std_ai"] =  std_ai
    df_normalizado["std_mi"] =  std_mi
    df_normalizado["std_ri"] =  std_ri
    df_normalizado["std_ad"] =  std_ad
    df_normalizado["std_md"] =  std_md
    df_normalizado["std_rd"] =  std_rd
    
    df_normalizado["ai"] =  df_normalizado["Antepie Izq"].round(5).astype(str) + " (" + df_normalizado["std_ai"].round(4).astype(str) + ")" 
    df_normalizado["mi"] =  df_normalizado["Mediopie Izq"].round(5).astype(str) + " (" + df_normalizado["std_mi"].round(4).astype(str) + ")"
    df_normalizado["ri"] =  df_normalizado["Retropie Izq"].round(5).astype(str) + " (" + df_normalizado["std_ri"].round(4).astype(str) + ")"
    df_normalizado["ad"] =  df_normalizado["Antepie Der"].round(5).astype(str) + " (" + df_normalizado["std_ad"].round(4).astype(str) + ")" 
    df_normalizado["md"] =  df_normalizado["Mediopie Der"].round(5).astype(str) + " (" + df_normalizado["std_md"].round(4).astype(str) + ")"
    df_normalizado["rd"] =  df_normalizado["Retropie Der"].round(5).astype(str) + " (" + df_normalizado["std_rd"].round(4).astype(str) + ")"
    
    df_final = df_normalizado.copy()
 
    std_ai = df_final["Antepie Izq"].std()
    std_mi = df_final["Mediopie Izq"].std()
    std_ri = df_final["Retropie Izq"].std()
    std_ad = df_final["Antepie Der"].std()
    std_md = df_final["Mediopie Der"].std()
    std_rd = df_final["Retropie Der"].std()
    df_final =  df_final.mean()
    
    df_final["std_ai"] =  std_ai
    df_final["std_mi"] =  std_mi
    df_final["std_ri"] =  std_ri
    df_final["std_ad"] =  std_ad
    df_final["std_md"] =  std_md
    df_final["std_rd"] =  std_rd
    
    df_final = pd.DataFrame(df_final).T        
    
    df_final["ai"] =  df_final["Antepie Izq"].round(5).astype(str) + " (" + df_final["std_ai"].round(4).astype(str) + ")" 
    df_final["mi"] =  df_final["Mediopie Izq"].round(5).astype(str) + " (" + df_final["std_mi"].round(4).astype(str) + ")"
    df_final["ri"] =  df_final["Retropie Izq"].round(5).astype(str) + " (" + df_final["std_ri"].round(4).astype(str) + ")"
    df_final["ad"] =  df_final["Antepie Der"].round(5).astype(str) + " (" + df_final["std_ad"].round(4).astype(str) + ")" 
    df_final["md"] =  df_final["Mediopie Der"].round(5).astype(str) + " (" + df_final["std_md"].round(4).astype(str) + ")"
    df_final["rd"] =  df_final["Retropie Der"].round(5).astype(str) + " (" + df_final["std_rd"].round(4).astype(str) + ")"
   
    
    return df_final
    

#Ejemplo de como usar:
#USUARIOS QUE HICIERON LAS PRUEBAS EN LAS 3 PLANTILLAS
#usuarios = ["AA","AI","BI","DO","JA","JAI","JJ","JT","LI","SO","WI"] 
#pesos = [51.3,89.75,69.15,54.5,59.45,90.95,93.35,59,111.30,76.2,78.90]

#comparacion_total = desemplantilla_total(usuarios, pesos, 16)



#Comparacion normalizadas entre ambas piernas (postura) , y detalle resumido a max
def desemplantilla_postura(usuarios, pesos, plantilla):
    #Dataframe con todos los usuarios
    completo = pd.DataFrame()
    
    for user, peso in zip(usuarios,pesos):
        for num in range(1,11):
            #Lectura del muestreo
            prueba = pd.read_csv(f"{plantilla}s/{user}_{num}_{plantilla}s.csv", index_col=0, usecols=range(plantilla*2+1))
            promprueba = prueba.agg(np.mean)
            sujeto = [user]
            peso_usuario = peso
            promprueba = pd.DataFrame(promprueba).T
            promprueba["Sujeto"]=sujeto
            promprueba["Peso (kg)"]=peso_usuario
            completo = pd.concat([completo , promprueba], ignore_index=True)
    
    df_normalizado = completo.copy()
    
    #Normaliza
    df_normalizado.iloc[:,:plantilla*2] = df_normalizado.iloc[:,:plantilla*2].div(df_normalizado["Peso (kg)"], axis=0)
   
    if plantilla == 8: 
        df_normalizado["Retropie Izq"] =  df_normalizado.iloc[:,0:3:2].sum(axis=1)
        df_normalizado["Mediopie Izq"] =  df_normalizado.iloc[:,4:7:2].sum(axis=1)
        df_normalizado["Antepie Izq"] =  df_normalizado.iloc[:,8:15:2].sum(axis=1)
        df_normalizado["Retropie Der"] =  df_normalizado.iloc[:,1:4:2].sum(axis=1)
        df_normalizado["Mediopie Der"] =  df_normalizado.iloc[:,5:8:2].sum(axis=1)
        df_normalizado["Antepie Der"] =  df_normalizado.iloc[:,9:16:2].sum(axis=1)

    elif plantilla == 11: 
        df_normalizado["Retropie Izq"] =  df_normalizado.iloc[:,0:5:2].sum(axis=1)
        df_normalizado["Mediopie Izq"] =  df_normalizado.iloc[:,6:11:2].sum(axis=1)
        df_normalizado["Antepie Izq"] =  df_normalizado.iloc[:,12:21:2].sum(axis=1)
        df_normalizado["Retropie Der"] =  df_normalizado.iloc[:,1:6:2].sum(axis=1)
        df_normalizado["Mediopie Der"] =  df_normalizado.iloc[:,7:12:2].sum(axis=1)
        df_normalizado["Antepie Der"] =  df_normalizado.iloc[:,13:22:2].sum(axis=1)
        
    elif plantilla == 16: 
        df_normalizado["Retropie Izq"] =  df_normalizado.iloc[:,0:5:2].sum(axis=1)
        df_normalizado["Mediopie Izq"] =  df_normalizado.iloc[:,6:15:2].sum(axis=1)
        df_normalizado["Antepie Izq"] =  df_normalizado.iloc[:,16:31:2].sum(axis=1)
        df_normalizado["Retropie Der"] =  df_normalizado.iloc[:,1:6:2].sum(axis=1)
        df_normalizado["Mediopie Der"] =  df_normalizado.iloc[:,7:16:2].sum(axis=1)
        df_normalizado["Antepie Der"] =  df_normalizado.iloc[:,17:32:2].sum(axis=1)
    
    df_normalizado["Pie Izq"] =  df_normalizado.loc[:,["Retropie Izq","Mediopie Izq","Antepie Izq"]].sum(axis=1)
    df_normalizado["Pie Der"] =  df_normalizado.loc[:,["Retropie Der","Mediopie Der","Antepie Der"]].sum(axis=1)
    
    normalizado_extendido = df_normalizado.copy()
    
    #Aqui se agrupa por usuario
    df_group = df_normalizado.groupby("Sujeto")
    df_normalizado = df_group.mean() 
    
    return completo, normalizado_extendido, df_normalizado
    

#Ejemplo de como usar:
#USUARIOS QUE HICIERON LAS PRUEBAS EN LAS 3 PLANTILLAS
#usuarios = ["AA","AI","BI","DO","JA","JAI","JJ","JT","LI","SO","WI"] 
#pesos = [51.3,89.75,69.15,54.5,59.45,90.95,93.35,59,111.30,76.2,78.90]

#usuarios = ["FF"]
#pesos = [65]

#original, comp_desem_ext, comparacion_desempeno = desemplantilla_postura(usuarios, pesos, 16)



#MODIFICADO Comparacion entre ambas piernas (postura) , y detalle resumido a max con valores ADC
def desemplantilla_postura2(usuarios, pesos, plantilla):
    #Dataframe con todos los usuarios
    completo = pd.DataFrame()
    
    for user, peso in zip(usuarios,pesos):
        for num in range(1,11):
            #Lectura del muestreo
            prueba = pd.read_csv(f"{plantilla}s/ADC/{user}_{num}_ADC_{plantilla}s.csv", index_col=0, usecols=range(plantilla*2+1))
            #prueba = pd.read_csv(f"{plantilla}s/{user}_{num}_{plantilla}s.csv", index_col=0, usecols=range(plantilla*2+1))
            promprueba = prueba.agg(np.mean)
            promprueba = pd.DataFrame(promprueba).T
            promprueba["Sujeto"]= user
            promprueba["Peso (kg)"]= peso
            completo = pd.concat([completo , promprueba], ignore_index=True)
    
    df_normalizado = completo.copy()
   
    if plantilla == 8: 
        df_normalizado["Retropie Izq"] =  df_normalizado.iloc[:,0:3:2].sum(axis=1)
        df_normalizado["Mediopie Izq"] =  df_normalizado.iloc[:,4:7:2].sum(axis=1)
        df_normalizado["Antepie Izq"] =  df_normalizado.iloc[:,8:15:2].sum(axis=1)
        df_normalizado["Retropie Der"] =  df_normalizado.iloc[:,1:4:2].sum(axis=1)
        df_normalizado["Mediopie Der"] =  df_normalizado.iloc[:,5:8:2].sum(axis=1)
        df_normalizado["Antepie Der"] =  df_normalizado.iloc[:,9:16:2].sum(axis=1)

    elif plantilla == 11: 
        df_normalizado["Retropie Izq"] =  df_normalizado.iloc[:,0:5:2].sum(axis=1)
        df_normalizado["Mediopie Izq"] =  df_normalizado.iloc[:,6:11:2].sum(axis=1)
        df_normalizado["Antepie Izq"] =  df_normalizado.iloc[:,12:21:2].sum(axis=1)
        df_normalizado["Retropie Der"] =  df_normalizado.iloc[:,1:6:2].sum(axis=1)
        df_normalizado["Mediopie Der"] =  df_normalizado.iloc[:,7:12:2].sum(axis=1)
        df_normalizado["Antepie Der"] =  df_normalizado.iloc[:,13:22:2].sum(axis=1)
        
    elif plantilla == 16: 
        df_normalizado["Retropie Izq"] =  df_normalizado.iloc[:,0:5:2].sum(axis=1)
        df_normalizado["Mediopie Izq"] =  df_normalizado.iloc[:,6:15:2].sum(axis=1)
        df_normalizado["Antepie Izq"] =  df_normalizado.iloc[:,16:31:2].sum(axis=1)
        df_normalizado["Retropie Der"] =  df_normalizado.iloc[:,1:6:2].sum(axis=1)
        df_normalizado["Mediopie Der"] =  df_normalizado.iloc[:,7:16:2].sum(axis=1)
        df_normalizado["Antepie Der"] =  df_normalizado.iloc[:,17:32:2].sum(axis=1)
    
    df_normalizado["Pie Izq"] =  df_normalizado.loc[:,["Retropie Izq","Mediopie Izq","Antepie Izq"]].sum(axis=1)
    df_normalizado["Pie Der"] =  df_normalizado.loc[:,["Retropie Der","Mediopie Der","Antepie Der"]].sum(axis=1)
    df_normalizado["Apoyo Izq"] = df_normalizado.loc[:,"Pie Izq"].div(df_normalizado.loc[:,["Pie Izq","Pie Der"]].sum(axis=1))              
    df_normalizado["Apoyo Der"] = df_normalizado.loc[:,"Pie Der"].div(df_normalizado.loc[:,["Pie Izq","Pie Der"]].sum(axis=1))
    df_normalizado["Diferencia"] = (df_normalizado.loc[:,"Apoyo Izq"] - df_normalizado.loc[:,"Apoyo Der"]).abs()
    
    normalizado_extendido = df_normalizado.copy()
    
    #Aqui se agrupa por usuario
    df_group = df_normalizado.groupby("Sujeto")
    df_normalizado = df_group.mean() 

    return completo, normalizado_extendido, df_normalizado
    

#Ejemplo de como usar: 
#USUARIOS QUE HICIERON LAS PRUEBAS EN LAS 3 PLANTILLAS
#usuarios = ["AA","AI","BI","DO","JA","JAI","JJ","JT","LI","SO","WI"] 
#pesos = [51.3,89.75,69.15,54.5,59.45,90.95,93.35,59,111.30,76.2,78.90]

#usuarios = ["FF"]
#pesos = [65]

#original, comp_desem_ext, comparacion_desempeno = desemplantilla_postura2(usuarios, pesos, 16)



#Grafica 3D de un resultado particular, dos gráficas
def analisispeso2(usuario, numprueba, sensores):
    prueba = pd.read_csv(f"{sensores}s/{usuario}_{numprueba}_{sensores}s.csv", index_col=0, usecols=range(sensores*2+1)) 
    resultado = prueba.agg(np.mean)

    #Coordenadas sensores
    if sensores == 8:
        ord_sens = ['1','9','2','10','3','11','4','12','5','13','6','14','7','15','8','16']
        px = [133,495,220,408,128,500,88,540,78,550,155,473,238,390,200,428] 
        py = [645,645,645,645,440,400,370,370,300,300,270,270,240,240,125,125] 
    
    elif sensores == 11:
        ord_sens = ['1','12','2','13','3','14','4','15','5','16','6','17','7','18','8','19','9','20','10','21','11','22']
        px = [184,444,220,408,133,495,108,520,128,500,88,540,78,550,130,498,180,448,238,390,200,428] 
        py = [730,730,685,685,645,645,520,520,440,440,370,370,300,300,280,280,260,260,240,240,125,125]

    elif sensores == 16:
        ord_sens = ['1','17','2','18','3','19','4','20','5','21','6','22','7','23','8','24','9','25','10','26','11','27','12','28','13','29','14','30','15','31','16','32']
        px = [184,444,133,495,220,408,108,520,168,460,128,500,90,538,180,448,78,550,130,498,180,448,238,390,150,478,200,428,130,498,200,428] 
        py = [730,730,645,645,645,645,520,520,520,520,440,440,370,370,370,370,300,300,280,280,260,260,240,240,215,215,185,185,85,85,60,60]
        
    pz = np.zeros(len(px))
    dx = np.full(len(px),20)
    dy = np.full(len(py),20)
    
    #Datos usuario
    dz = resultado
    
    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(1,1,1, projection="3d", computed_zorder=False)
     
    #Imagen en plano 3d
    img = plt.imread("footprints.png") #Imagen huellas plantares base
    height, width = img.shape[:2]    
    x = np.arange(0, width)
    y = np.arange(0, height)
    x, y = np.meshgrid(x, y)
    ax1.plot_surface(x, y, np.atleast_2d(0), rstride=3, cstride=3, facecolors=img, shade=False, zorder=0)
    
    #Grafico de barras 3d
    ax1.bar3d(px,py,pz,dx,dy,dz, zorder=.01, edgecolor='black')
    for c,r,a,s in zip(px, py, dz, ord_sens):
        ax1.text(c, r-10, a*.9, s, bbox=(dict(facecolor='white', alpha=.4)))
    valor_ref = np.around(dz.max()/2)
    ax1.bar3d(width,0,0,-20,20,valor_ref, zorder=.01, color="aqua", edgecolor='black')  
    ax1.text(width, -80, valor_ref+.10, f"Referencia: {valor_ref} kg", bbox=(dict(facecolor='white')), zdir="y")
        
    ax1.invert_xaxis()
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_zticks([])
    ax1.view_init(elev=22, azim=320)
    ax1.set_title("Representación 3D", fontsize=16)
    fig.suptitle(f"Resultado de fuerzas captadas para {usuario} con {sensores} sensores", fontsize=20)# 
    plt.tight_layout()
    plt.savefig("Nombre_representacion_3d.png", dpi=300)
    plt.show()
    
    
    #Grafico 2 - Pastel sensores
    fig2 = plt.figure( figsize=(8, 8)) 
    ax2 = fig2.add_subplot(1,1,1)
    dz = dz.set_axis(ord_sens)
    dz.index = dz.index.astype(int)
    dz = dz.sort_index()
    sensores_innecesarios = np.less_equal(dz, 0.01)
    dz.drop(dz.index[sensores_innecesarios], inplace=True)
    radio = 1.0
    _, labels, pct_texts = ax2.pie(dz, labels=dz.index, autopct=lambda pct: f"{pct:.1f}%\n({pct*np.sum(dz)/100:.2f} kg)", radius=radio, 
            wedgeprops={"edgecolor":"w","width":.3}, pctdistance=.85, labeldistance=1.03, rotatelabels = True) 
    for label, pct_text in zip(labels, pct_texts):
        pct_text.set_rotation(label.get_rotation())
    #Pastel apoyo
    cambio_pie = 0
    for valor in dz.index:
        if valor <= sensores:
            cambio_pie += 1
        else:
            break
    pie_izq = dz.iloc[:cambio_pie].sum()
    pie_der = dz.iloc[cambio_pie:].sum()
    ax2.pie((pie_izq,pie_der), labels=["Pie izquierdo","Pie derecho"], 
            autopct=lambda pct: f"{pct:.1f}% ({pct*(pie_izq+pie_der)/100:.2f} kg)", radius=radio-.3, 
            wedgeprops={"edgecolor":"w", "width":.3}, pctdistance=.7, labeldistance=.8)
    
    #Configuraciones adcicionales 
    ax2.set_title("Distribución de fuerzas captadas por sensor", fontsize=16)
    plt.tight_layout()
    plt.show()

    return resultado

#Ejemplo de como usar:
#analsis_detallado = analisispeso2("AA",7,16)


