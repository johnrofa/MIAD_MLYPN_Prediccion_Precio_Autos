#!/usr/bin/python
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor

def Modelos(datos1, leMake, leModel, leState, Modelo):

    # Leer los datos post

    Year = datos1["Year"]
    Mileage = datos1["Mileage"]
    State = datos1["State"]
    Make = datos1["Make"]
    Model = datos1["Model"]
    ID = 0

    columnas = ['Year', 'Mileage', 'State', 'Make', 'Model', 'ID']
    datos = [[Year, Mileage, State, Make, Model, ID]]

    domain_01 = pd.DataFrame(datos, columns=columnas)
    db_02 = domain_01.set_index('ID')

    print('db_02 :', db_02)


    db_02["State"] = leState.transform(db_02.State)
    db_02["Make"] = leMake.transform(db_02.Make)
    db_02["Model"] = leModel.transform(db_02.Model)

    print('----------------realizar predicción----------------------')

    # Make prediction
    ypredRF11 = Modelo.predict(db_02)
    ypredRF11 = str(ypredRF11[0])

    return ypredRF11
