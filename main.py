from datagen import generate_customer_data, data2json, json2s3
from aws import create_bucket

#Create Buckets in S3    
landing_bucket, landing_status = create_bucket('customers-faker-landing')
athena_bucket, athena_status = create_bucket('customers-faker-athena')
assert landing_status == athena_status == True, 'Failure to create S3 Buckets'

#Generate Customers, Events and Wallets
customer_list = generate_customer_data(customers = 100, events = 40)

#Structure Data and Send to S3
data2json(customer_list, data_method = 'export_current_wallet', filename = 'current_wallet')
data2json(customer_list, data_method = 'export_wallet_events', filename = 'wallet_events')
del customer_list

#Send to S3
json2s3('current_wallet', landing_bucket, 'wallet/current-wallet')
json2s3('wallet_events', landing_bucket, 'wallet/wallet-events')