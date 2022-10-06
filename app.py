from flask import Flask, jsonify
from flask_restful import Api
from resources.usage import usage_get, usage_put

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usage_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
api = Api(app)

@app.before_first_request
def cria_banco():
    usage_database.create_all()

#Recursos da API vindo da pasta resources
api.add_resource(usage_get, '/itens') #GET para todos os dados
api.add_resource(usage_put, '/itens/<int:item_id>') #PUT

if __name__ == '__main__':
    from sql_alchemy import usage_database
    usage_database.init_app(app)
    app.run(debug=True)
