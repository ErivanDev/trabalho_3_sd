# Trabalho 3 de Sistemas Distribuidos

Foi programado um cliente de uma calculadora disponibilizados pelos professores, presente em **ClienteCalCuladoraREST**, utilizando python, a biblioteca requests para fazer requisições HTTP, e a biblioteca tkinter para a interface gráfica.

Foi programado um servidor REST usando python, a biblioteca flask. O servidor disponibiliza uma página HTML para fazer requisições, disponível em **ServidorREST**.

Foi programado um cliente mobile usando o flutter disponível em **cliente_mobile**

Criar ambiente virtual python

    python -m virtualenv env
    
Ativar ambiente virtual

    .\env\Scripts\activate

Instalar dependencias

    pip install requirements.txt
    
Todar servidor

    cd .\ServidorREST
    
    python .\main.py

Cliente Flutter

    .\adb reverse tcp:5000 tcp:5000

Requisitos da Tarefa

[x] Criar um cliente REST na linguagem da sua preferência

[x] Consultar o método Operations para listar as operações disponíveis

[x] Realizar as operações invocando o método adequado

[x] Fazer uma análise usando o Console do Postman de como são as requisições e as respostas em termos de cabeçalho e payload

[x] No caso das requisições POST, quais seriam as diferenças e similaridades se fosse uma página Web enviando dados de um formulário para o servidor?

[x] Criar um Servidor REST

[x] Um CRUD de dados que consome uma API externa para obter informações
    
    - add_review (obtém informações dos livros)
    - update_review
    - delete_review
    - get_reviews 

[x] Dar like nas reviews

[x] Um documento de especificação contendo todas as rotas da API a serem implementadas

[x] Rotas do tipo GET, POST e DELETE, sendo possível indicar o formato dos dados de resposta (XML ou JSON) como parâmetro da requisição

[x] Ao menos um método REST deve retornar uma resposta no formato Protocol Buffer

[x] Um cliente web

[x] Um cliente mobile

[x] Vídeo de no máximo 5 min demonstrando a execução das funcionalidades, processamento

[x] Comparar os tipos de representação de dados usados (XML, JSON e Protocol Buffer)


video demonstrativo: https://drive.google.com/file/d/1HTkSnYK8NqOmh-FdRIzrsIfqFhKTJ7vE/view?usp=drivesdk
