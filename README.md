# Desafio

Esse repositório contêm os entregáveis do primeiro desafio proposto no [Bootcamp Engenharia de Dados AWS](https://howedu.com.br/cohort/engenharia-de-dados/) da How Education.

O desafio consistia de criar um código capaz de gerar dados fictícios através da biblioteca Faker do Python e realizar a ingestão na AWS, armazenando os dados no S3, criando crawlers no AWS Glue e disponibilizando as tabelas para consulta no Athena.

Os pré-requisitos eram:
- Criar uma conta AWS
- Gerar dados necessários utilizando a biblioteca Faker do Python
- Realizar ingestão em um Bucket do AWS S3
- Criar um Crawler pelo AWS Glue para disponibilizar dados no AWS Athena
- Escrever exemplos de consultas nos dados utilizando o AWS Athena

# Como Utilizar Esse Repositório

O primeiro passo é clonar o repositório em seu computador
```
$ git clone https://github.com/LuisGaravaso/investment-platform.git
```

Em seguida, dentro da pasta crie o arquivo `.awsenv` que contém suas credenciais na AWS como no exemplo abaixo:
```
ACCOUNT_ID = XXXXXXXX #O seu identificador de conta da AWS
ACCESS_KEY = YYYYYYYYY #Chave Publica da Role no S3
ACCESS_SECRET_KEY = ZZZZZZZZZ #Chave Privada da Role no S3
```

Antes de rodar o arquivo, ative no seu terminal o ambiente virtual Python que contém todas as bibliotecas necessárias para rodar esse script corretamente
```
$ .myenv\Scripts\activate
```

Finalmente, rode o arquivo `main.py`
```
$ python main.py
```

# Projeto

Os códigos desse repositório são capazes de gerar usuários e eventos de compra e venda de Ações ou Títulos de Renda Fixa do Mercado Brasileiro
Os arquivos:
- `customers.py`: Consome a biblioteca `faker` e cria as classes que geram os usuários, os ativos e as taxas (no caso de títulos de renda fixa)
- `aws.py`: Contêm as funções que envolvem a criação dos Buckets no S3 e upload de arquivos.
- `datagen.py`: Combina as funções e classes das `customers.py` e da `aws.py` para geração de dados nos formatos adequados para o S3
- `main.py`: Chama as funções na ordem correta para gerar os dados, criar os buckets no S3 e realizar os uploads.

Ao rodar o script principal, dois arquivos `.json` serão gerados:
- `wallet_events.json`: Tabela com os eventos realizados por todos os usuários
![Events](https://github.com/LuisGaravaso/investment-platform/assets/44078988/bcaa2b31-71fa-488d-9591-1607d831e6c6)

- `current_wallet.json`: Tabela com a carteira atual dos usuários
![CurrentWallet](https://github.com/LuisGaravaso/investment-platform/assets/44078988/afeb284c-f487-4b00-be70-919b372c34c5)

# Outras Entregas do Desafio

## AWS Glue

Depois que os arquivos foram enviados com sucesso para o S3, é necessário entrar no AWS e criar dois Crawlers para extração do Schema das tabelas:
![image](https://github.com/LuisGaravaso/investment-platform/assets/44078988/3ac7a313-478d-4387-89d2-e1a2816aa5f2)

## AWS Athen

Com os Crawlers corretamente definidos e rodando, torna-se possível realizar consultas no AWS Athena.
As perguntas que tentei responder foram:



