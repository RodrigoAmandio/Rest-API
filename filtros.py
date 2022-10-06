def normalize_path_params(name = None,
                          limit=50,
                          offset = 0,
                          **dados): #A variável **dados irá substituir qualquer um dos valores caso seja passada pelo usuário.

#http://127.0.0.1:5000/itens?name=01CGP&limit=1 - Exemplo de API

    if name:
        return {
                'name': name,
                'limit': limit,
                'offset': offset}

    return {
            'limit': limit,
            'offset': offset}

consulta_num_mass_name = "SELECT * FROM usage WHERE name = ? LIMIT ? OFFSET ?"

consulta_num_mass_sem_name = "SELECT * FROM usage LIMIT ? OFFSET ?"

#Cada valor na tupla será substituido por uma ? na query na ordem em que aparecem. Seria o mesmo que escrever:
