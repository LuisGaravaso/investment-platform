from customers import Customer
from faker import Faker
import random

fake = Faker('pt_BR')

#Generate Customers, Events and Wallets
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

#Export Current Wallet
current_wallets = []
for customer in customer_list:
    current_wallets.extend(customer.export_current_wallet())

#Export Wallet Events
wallet_events = []
for customer in customer_list:
    wallet_events.extend(customer.export_wallet_events())