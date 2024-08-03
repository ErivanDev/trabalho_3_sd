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

[ ] Fazer uma análise usando o Console do Postman de como são as requisições e as respostas em termos de cabeçalho e payload

[ ] No caso das requisições POST, quais seriam as diferenças e similaridades se fosse uma página Web enviando dados de um formulário para o servidor?

[x] Criar um Servidor REST

[x] Um CRUD de dados que consome uma API externa para obter informações
    
    - add_review (obtém informações dos livros)
    - update_review
    - delete_review
    - get_reviews 

[ ] Dar like nas reviews

[ ] Um documento de especificação contendo todas as rotas da API a serem implementadas

[ ] Rotas do tipo GET, POST e DELETE, sendo possível indicar o formato dos dados de resposta (XML ou JSON) como parâmetro da requisição

[x] Ao menos um método REST deve retornar uma resposta no formato Protocol Buffer
    [ ] Mais endpoints poderiam receber Protocol, talvez os clientes podessem enviar

[x] Um cliente web
    [ ] Usar protobuf, até o momento só o servidor está retornando, mas o cliente não recupera os dados

[x] Um cliente mobile

[ ] Vídeo de no máximo 5 min demonstrando a execução das funcionalidades, processamento

[ ] Comparar os tipos de representação de dados usados (XML, JSON e Protocol Buffer)