from aws import upload_file
from customers import Customer
import json
import random
from faker import Faker

fake = Faker('pt_BR')

def data2json(customer_list:list, data_method:str, filename:str):
    data = []
    for customer in customer_list:
        func = getattr(customer, data_method)
        data.extend(func())
        
    with open(f"{filename}.json", "w") as f:
        json.dump(data, f)
    
def json2s3(filename:str, main_bucket:str, subfolders:str = None):
    
    response = upload_file(f"{filename}.json", main_bucket, subfolders)

    if response:
        print('Successfully Uploaded Data to S3')
    else:
        print('Failed to Upload Data to S3')
    return response

def generate_customer_data(customers:int, events:int) -> list:
    
    customer_list = []
    for i in range(100):
        first_name = fake.first_name()
        last_name = fake.last_name()
        city = fake.city()
        customer = Customer(first_name, last_name, city)
        
        for c in range(40):
            choice = random.choice(['buy','sell'])
            if choice == 'buy':
                customer.buy()
            else:
                customer.sell()
                
        customer_list.append(customer)
        
    return customer_list