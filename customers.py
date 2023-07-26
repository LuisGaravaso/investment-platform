from faker import Faker
from faker.providers import BaseProvider
import random
from collections import defaultdict
from datetime import datetime

fake = Faker('pt_BR')

def generate_value(low: float, high: float) -> float:
    return round(random.uniform(low, high), 2)

class RendaFixa(BaseProvider):
    def cdb_prefixado(self) -> str:
        interest = generate_value(6, 20)
        return f'CDB Pré {interest}%'
    
    def cdb_posfixado(self) -> str:
        interest = generate_value(100, 120)
        return f'CDB {interest}% CDI'
    
    def debenture_ipca(self) -> str:
        interest = generate_value(4, 12)
        return f'Deb IPCA+{interest}%'
    
class Acoes(BaseProvider):
    
    def stock(self) -> str:
        stocks= [
                'VALE3', 'KLBN11', 'ALUP11', 'PETR3', 'TAEE11',
            ]
        return random.choice(stocks)
        
fake.add_provider(RendaFixa)
fake.add_provider(Acoes)

class Customer:
    
    def __init__(self, first_name, last_name, city) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.account_id = fake.sha1(raw_output=False)
        self.city = city
        self.wallet_events = defaultdict(list)
        self.current_wallet = defaultdict(list)
        
    def _generate_date(self, start:str = '2023-01-01', stop:str = 'today') -> str:
        start = datetime.strptime(start,'%Y-%m-%d')
        if stop != 'today':
            stop = datetime.strptime(stop,'%Y-%m-%d')
        
        date = fake.date_between(start, stop)
        return date.strftime('%Y-%m-%d')
    
    def _update_current_wallet(self, product):
        if not self.current_wallet[product]:
            if self.wallet_events[product][-1][1] != 'quit':
                self.current_wallet[product] = self.wallet_events[product][-1][1]
        else:
            _, value, date = self.wallet_events[product][-1]
            new_value = self.current_wallet[product] + value
            if new_value == 0:
                self.current_wallet.pop(product)
                self.wallet_events[product].append(('quit', 0, date))
            else:
                self.current_wallet[product] = new_value
        
    def buy(self) -> None:
        possible_products = [
            ('stock', fake.stock()),
            ('cdb', fake.cdb_prefixado()),
            ('cdb', fake.cdb_posfixado()),
            ('deb', fake.debenture_ipca())
        ]
        product_type, product = random.choice(possible_products)
        
        if product in self.wallet_events:
            last_event = self.wallet_events[product][-1][0]
            if last_event == 'quit':
                return
            
        if (product_type == 'stock') or (product not in self.wallet_events):
            try:
                _, _, starting_date = self.wallet_events[product][-1]
            except:
                starting_date = '2023-01-01'
                    
            value = generate_value(1000, 100000)
            purchase_date = self._generate_date(start = starting_date)
            
            self.wallet_events[product].append(('buy', value, purchase_date))
            self._update_current_wallet(product)
    
    def sell(self) -> None:
        
        if not self.wallet_events:
            return
        
        product = random.choice(list(self.current_wallet.keys()))
        _, value, purchase_date = self.wallet_events[product][-1]
        
        value = generate_value(-1, 0)*value
        selling_date =  self._generate_date(start = purchase_date)
        self.wallet_events[product].append(('sell', value, selling_date))
        self._update_current_wallet(product)
        
    def export_current_wallet(self):
        structured_data = []
        for item, value in self.current_wallet.items():
            data = {
                'first_name': self.first_name,
                'last_name': self.last_name,
                'city': self.city,
                'product': item,
                'value': value
            }
            structured_data.append(data)
            
        return structured_data
    
    def export_wallet_events(self):
        structured_data = []
        for product in self.wallet_events:
            for event, value, date in self.wallet_events[product]: 
                data = {
                    'first_name': self.first_name,
                    'last_name': self.last_name,
                    'city': self.city,
                    'product': product,
                    'event': event,
                    'value': value,
                    'date': date
                }
                structured_data.append(data)
                
        return structured_data