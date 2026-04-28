from encodings import koi8_r
import random
from scipy.stats import f
from sklearn.model_selection import train_test_split 
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from random import sample
import numpy as np
import os
#Variables globales
contadorMagna = 0
contadorPrem = 0
contadorDies = 0

bosqueMagna = None
bosquePremium = None
bosqueDiesel = None

columnaMagna = None
columnaPremium = None
columnaDiesel = None

base_dir = os.path.dirname(os.path.abspath(__file__))
rutaArchivo = os.path.join(base_dir, "..", "DataBase", "DatosHistoricoGasolina.xlsx")

#================================================================================================================


def simulacionesMonteCarloReg(idGasolinera, ano, mes):
    global contadorMagna, columnaMagna, rutaArchivo
    historico = pd.read_excel(rutaArchivo)

    print ("\n PREDICCION DE REGULAR . . .  \n")

    idGasP = idGasolinera
    anoC = ano
    mesC = mes
    iva = 0.16
    mesesPasados = (anoC - 2020) * 12 + (mesC - 1)
    n = 10000

    precioMagna= np.random.choice(historico['precio_magna'], n)
    precioCrudo = np.random.choice(historico['precio_crudo'], n)
    IEPS_Reg = np.random.choice(historico['IEPS_reg'], n)
    
    matrizMag = np.column_stack([ 
        np.full(n, idGasolinera), 
        np.full(n, ano), 
        np.full(n, mes), 
        np.full(n, mesesPasados), 
        precioMagna, 
        precioCrudo, 
        np.full(n, iva), 
        IEPS_Reg
    ])

    df_pred = pd.DataFrame(matrizMag, columns = columnaMagna)
    #prediccion

    pred = predecirRF_Reg(df_pred)


    p5 = np.percentile (pred, 5) # precio optimista
    p50 = np.percentile (pred, 50) # precio realista
    p95 = np.percentile (pred, 95) # precio pesimista

    print (f"percentil 5, optimista: {p5}" )
    print (f"percentil 50, realista: {p50}" )
    print (f"percentil 95, pesimista: {p95}" )
    print ("\n PREDICCION COMPLETA - - - ")
    
    return p5,p50,p95


def entrenarRF_reg():
    global rutaArchivo
    historico = pd.read_excel(rutaArchivo)
    historicoReg = historico.drop(columns=["municipio","permiso", "precio_premium", "precio_disel", "IEPS_prem", "IEPS_dis" ])

    historicoReg["precio_magna_f"] = historicoReg["precio_magna"].shift(-59)
    historicoReg = historicoReg.dropna().reset_index(drop=True)

    df_Y = historicoReg["precio_magna_f"]
    df_X = historicoReg.drop(columns = ["precio_magna_f"])

    df_X_train, df_X_test, df_Y_train, df_Y_test = train_test_split(df_X, df_Y, test_size=.30, shuffle = False)
    bosqueMag = RandomForestRegressor(n_estimators=200, criterion= "squared_error", max_features="sqrt", bootstrap =True, max_samples=80/100, oob_score = True)
    
    bosqueMag.fit(df_X_train[:], df_Y_train )
    
    print ('train accuracy : %.5f' % bosqueMag.score(df_X_train, df_Y_train))
    print ('test accuracy : %.5f' % bosqueMag.score(df_X_test, df_Y_test))

    return bosqueMag,df_X.columns 

def predecirRF_Reg(predArray):
    global contadorMagna, bosqueMagna, columnaMagna
    #asignar valores 
    if contadorMagna == 0:
        bosqueMagna, columnaMagna = entrenarRF_reg()
        contadorMagna +=1

    #predecir


    prediccion = bosqueMagna.predict(predArray)  

    return prediccion


#=======================================================================================================


def simulacionesMonteCarloPrem(idGasolinera, ano, mes):

    print ("\n PREDICCION DE PREMIUM. . . \n")
    global contadorPremium, columnaPremium, rutaArchivo
    historico = pd.read_excel(rutaArchivo)

    idGasP = idGasolinera
    anoC = ano
    mesC = mes
    iva = 0.16
    
    n = 10000
    mesesPasados = (anoC - 2020) * 12 + (mesC - 1)

    precioPremium = np.random.choice(historico['precio_premium'], n)
    precioCrudo = np.random.choice(historico['precio_crudo'], n)
    IEPS_Prem = np.random.choice(historico['IEPS_prem'], n)

    matrizPrem = np.column_stack([ 
        np.full(n, idGasolinera), 
        np.full(n, anoC), 
        np.full(n, mesC), 
        np.full(n, mesesPasados), 
        precioPremium, 
        precioCrudo, 
        np.full(n, iva), 
        IEPS_Prem
    ])

    df_pred = pd.DataFrame(matrizPrem, columns = columnaPremium)

    pred = predecirRF_Prem(df_pred)

    p5 = np.percentile (pred, 5) # precio optimista
    p50 = np.percentile (pred, 50) # precio realista
    p95 = np.percentile (pred, 95) # precio pesimista

    print (f"percentil 5, optimista: {p5}" )
    print (f"percentil 50, realista: {p50}" )
    print (f"percentil 95, pesimista: {p95}" )
    print ("\n PREDICCION COMPLETA - - - ")
  
    return p5,p50,p95


def entrenarRF_Prem():

    global rutaArchivo
    historico = pd.read_excel(rutaArchivo)
    historicoReg = historico.drop(columns=["municipio","permiso", "precio_magna", "precio_disel", "IEPS_reg", "IEPS_dis" ])

    historicoReg["precio_premium_f"] = historicoReg["precio_premium"].shift(-59)
    historicoReg = historicoReg.dropna().reset_index(drop=True)

    df_Y = historicoReg["precio_premium_f"]
    df_X = historicoReg.drop(columns = ["precio_premium_f"])

    df_X_train, df_X_test, df_Y_train, df_Y_test = train_test_split(df_X, df_Y, test_size=.30, shuffle = False)
    bosquePrem = RandomForestRegressor(n_estimators=200, criterion= "squared_error", max_features="sqrt", bootstrap =True, max_samples=80/100, oob_score = True)
    
    bosquePrem.fit(df_X_train[:], df_Y_train )
    
    print ('train accuracy : %.5f' % bosquePrem.score(df_X_train, df_Y_train))
    print ('test accuracy : %.5f' % bosquePrem.score(df_X_test, df_Y_test))
    


    return bosquePrem,df_X.columns 

def predecirRF_Prem(predArray):
    global contadorPrem, bosquePremium, columnaPremium
    
    if contadorPrem == 0:
        bosquePremium, columnaPremium = entrenarRF_Prem()
        contadorPrem +=1

    #predecir

    prediccion = bosquePremium.predict(predArray)  
    
    return prediccion
   
    

#=====================================================================================================================



def simulacionesMonteCarloDies(idGasolinera, ano, mes):

    print ("n PREDICCION DE DIESEL . . . \n" )

    global contadorDies, columnaDiesel, rutaArchivo
    historico = pd.read_excel(rutaArchivo)

    idGasP = idGasolinera
    anoC = ano
    mesC = mes
    iva = 0.16
    
    mesesPasados = (anoC - 2020) * 12 + (mesC - 1)
    n = 10000

    precioDies = np.random.choice(historico['precio_disel'], n)
    precioCrudo = np.random.choice(historico['precio_crudo'], n)
    IEPS_Dies = np.random.choice(historico['IEPS_dis'], n)

    matrizDies = np.column_stack([ 
        np.full(n, idGasolinera), 
        np.full(n, ano), 
        np.full(n, mes), 
        np.full(n, mesesPasados), 
        precioDies, 
        precioCrudo, 
        np.full(n, iva), 
        IEPS_Dies
    ])

    df_pred = pd.DataFrame(matrizDies, columns = columnaDiesel)

    pred = predecirRF_Dies(df_pred)

    p5 = np.percentile (pred, 5) # precio optimista
    p50 = np.percentile (pred, 50) # precio realista
    p95 = np.percentile (pred, 95) # precio pesimista

    print (f"percentil 5, optimista: {p5}" )
    print (f"percentil 50, realista: {p50}" )
    print (f"percentil 95, pesimista: {p95}" )
  
   
    print ("\n PREDICCION COMPLETA - - - ")
    return p5,p50,p95


def entrenarRF_Dies():

    global rutaArchivo
    historico = pd.read_excel(rutaArchivo)
    historicoReg = historico.drop(columns=["municipio","permiso", "precio_magna", "precio_premium", "IEPS_reg", "IEPS_prem" ])

    historicoReg["precio_disel_f"] = historicoReg["precio_disel"].shift(-59)
    historicoReg = historicoReg.dropna().reset_index(drop=True)

    df_Y = historicoReg["precio_disel_f"]
    df_X = historicoReg.drop(columns = ["precio_disel_f"])

    df_X_train, df_X_test, df_Y_train, df_Y_test = train_test_split(df_X, df_Y, test_size=.30, shuffle = False)
    bosqueDis = RandomForestRegressor(n_estimators=200, criterion= "squared_error", max_features="sqrt", bootstrap =True, max_samples=80/100, oob_score = True)
    
    bosqueDis.fit(df_X_train[:], df_Y_train )
    
    print ('train accuracy : %.5f' % bosqueDis.score(df_X_train, df_Y_train))
    print ('test accuracy : %.5f' % bosqueDis.score(df_X_test, df_Y_test))
    print (" ")
   
    return bosqueDis,df_X.columns 



def predecirRF_Dies(predArray):
    global contadorDies, bosqueDiesel, columnaDiesel
    #asignar valores 
    if contadorDies == 0:
        bosqueDiesel, columnaDiesel = entrenarRF_Dies()
        contadorDies +=1

    #definir dataframe

    #predecir
    prediccion = bosqueDiesel.predict(predArray)   
    
    return prediccion



#=====================================================================================================================
