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
![Events](https://github.com/LuisGaravaso/investment-platform/blob/main/readme_files/Events.png)

- `current_wallet.json`: Tabela com a carteira atual dos usuários
![CurrentWallet](https://github.com/LuisGaravaso/investment-platform/blob/main/readme_files/CurrentWallet.png)

# Outras Entregas do Desafio

## AWS Glue

Depois que os arquivos foram enviados com sucesso para o S3, é necessário entrar no AWS e criar dois Crawlers para extração do Schema das tabelas:
![image](https://github.com/LuisGaravaso/investment-platform/blob/main/readme_files/AWSGlue.png)

## AWS Athena

Com os Crawlers corretamente definidos e rodando, torna-se possível realizar consultas no AWS Athena.

As perguntas que tentei responder foram:

1. Quais são os clientes com as maiores posições em cada um dos Tickers das Ações ?

```
with renda_variavel as (
	select concat_ws(' ', "first_name", "last_name") as customer
    	,product
    	,value
	from "current_wallet"
	where REGEXP_LIKE(product, '^[A-Z]{4}[0-9]+$')
),
customer_ranking as (
	select * 
		,row_number() over (partition by product order by value desc) as ticker_rank
	from renda_variavel
)
select *
from customer_ranking
where ticker_rank = 1
```

![image](https://github.com/LuisGaravaso/investment-platform/blob/main/readme_files/Query1.png)

2. Quais os clientes que mais realizarem eventos no mês de Junho de 2023 ? Foram mais eventos de Compra ou Venda ?
![image](https://github.com/LuisGaravaso/investment-platform/blob/main/readme_files/Query2.png)

```
with events as (
select 
    date_trunc('month', date_parse("date",'%Y-%m-%d')) as month,
    concat_ws(' ', "first_name", "last_name") as customer,
    count("event") as number_of_events,
    count(if("event" = 'buy',"event",null)) as number_of_purchases,
    count(if("event" = 'sell',"event",null)) as number_of_sellings
from "wallet_events"
group by 1, 2
)
select * from events where "month" = date_parse('2023-06-01','%Y-%m-%d') order by number_of_events desc
```

3. Em quais meses mais entraram clientes na nossa plataforma ?

```
with events as (
select 
    concat_ws(' ', "first_name", "last_name") as customer,
    min(date_trunc('month', date_parse("date",'%Y-%m-%d'))) as first_month
from "wallet_events"
group by 1
)
select
    first_month,
    count(distinct customer) as new_customers
from events 
group by first_month
```

![image](https://github.com/LuisGaravaso/investment-platform/blob/main/readme_files/Query3.png)


