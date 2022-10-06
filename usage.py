from flask_restful import Resource, reqparse
from models.usage import UsageModel
from resources.filtros import normalize_path_params, consulta_num_mass_sem_name,consulta_num_mass_name
import sqlite3

path_params = reqparse.RequestParser()
path_params.add_argument('name', type=str)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

class usage_get(Resource):
    def get(self):
        connection = sqlite3.connect('usage_database.db')
        cursor = connection.cursor()
        dados = path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None} #Dictionary comprehension(Receberá apenas os dados válidos)
        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('name'): #Se o usuário não informar um nome

            tupla = tuple([parametros[chave] for chave in parametros]) #List comprehension para extrair de um dicionário somente os valores
            resultado = cursor.execute(consulta_num_mass_sem_name,tupla)

        else: #Se o usuário informar um nome

            tupla = tuple([parametros[chave] for chave in parametros]) #A tupla será com os valores na seguinte ordem: (num_mass_min, limit, offset)
            resultado = cursor.execute(consulta_num_mass_name,tupla)

        usage = []
        for linha in resultado:
            usage.append({
            'item_id': linha[0],
            'name': linha[1],
            'data': linha[2],
            'value': linha[3]
            })

        return {'usage': usage} # SELECT * FROM num_mass

class usage_put(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('name', type=str, required=True, help="The field 'name' cannot be left blank.")
    atributos.add_argument('data', type=str, required=True, help="The field 'data' cannot be left blank.")
    atributos.add_argument('value',type=float, required=True, help="The field 'value' cannot be left blank.")

    def put(self,item_id):
        dados = usage_put.atributos.parse_args()
        item_encontrado = UsageModel.find_item(item_id)

        if item_encontrado: #Se item não for None:
            item_encontrado.update_item(**dados) #Atualiza os dados
            item_encontrado.save_item() #Salva no banco de dados na tabela criada
            return item_encontrado.json(), 200

        else:
            item = UsageModel(item_id, **dados)
            try:
                item.save_item()
            except:
                return {'message': 'An internal error occurred trying to save item.'},500 #Internal Server Error
            return item.json()

    def delete(self,item_id):
        item = UsageModel.find_item(item_id)
        if item:
            try:
                item.delete_item()
            except:
                return {'message': 'An internal error occurred trying to delete item.'},500 #Internal Server Error

            return {'message': 'item deleted'}

        return {'message': 'item not found.'},404
