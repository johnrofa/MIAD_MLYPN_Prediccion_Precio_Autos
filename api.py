#!/usr/bin/python
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import joblib
from m09_model_deployment_01 import  Modelos
import json
import os

from flask_cors import CORS
from xgboost import XGBRegressor
import numpy as np

leMake = joblib.load('leMake_01.pkl')
leModel = joblib.load('leModel_01.pkl')
leState = joblib.load('leState_01.pkl')
regRF11 = joblib.load('phishing_clf_01.pkl')
xgboost1 = joblib.load('regresion.pkl')


# Definición aplicación Flask
app = Flask(__name__)

# Habilitación del modelo para todas las rutas y orígenes
CORS(app)

api = Api(
    app,
    version='1.0',
    title='Prediccion Precio Vehiculos',
    description='Prediccion Precio Vehiculos')

ns = api.namespace('predict',
                   description='Prediccion Precio Vehiculos')

parser = api.parser()


parser.add_argument(
    'Modelo',
    type = str,
    default='Seleccione un Modelo',
    choices=['Seleccione un Modelo', 'Random_Forest', 'XGBoost'],
    required = True
    )

parser.add_argument(
    'Year',
    type = int,
    required = True)

parser.add_argument(
    'Mileage',
    type = int,
    required = True)

parser.add_argument(
    'State',
    type = str,
    required = True)

parser.add_argument(
    'Make',
    type=str,
    required=True)

parser.add_argument(
    'Model',
    type=str,
    required=True)



resource_fields = api.model('Resource', {
    'result': fields.String,
})



@ns.route('/')
class PhishingApi(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        print(args)





        datos= {
            "Year": args['Year'],
            "Mileage": args['Mileage'],
            "State": args['State'],
            "Make": args['Make'],
            "Model": args['Model'],
        }

        print(datos)

        if args['Modelo'] == 'Random_Forest':
            aplicar_modelo = regRF11
        elif args['Modelo'] == 'XGBoost':
            aplicar_modelo = xgboost1
        else:
            aplicar_modelo = regRF11

        resultado = Modelos(datos, leMake, leModel, leState, aplicar_modelo)

        print('********resultado******** :', resultado)

        return {
                   "result": str(resultado)
               }, 200




if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)