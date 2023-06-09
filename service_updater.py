import redis
import csv
import time
import json


time.sleep(5)

r = redis.Redis(host='redis', port=6379, db=0)

stock1_str = r.get('stock1').decode()
stock1 = json.loads(stock1_str)

stock2_str = r.get('stock2').decode()
stock2 = json.loads(stock2_str)

stock3_str = r.get('stock3').decode()
stock3 = json.loads(stock3_str)


def calculate_performance(stock_price):
    time.sleep(1)
    return 0


with open('price_data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Stock'] == 'stock1':
            stock1['price'].append(int(row['Price']))
            stock1['time'].append(row['Time'])
            updated_json_string=json.dumps(stock1)
            r.set('stock1',updated_json_string)
        
        elif row['Stock'] == 'stock2':
            stock2['price'].append(int(row['Price']))
            stock2['time'].append(row['Time'])
            updated_json_string=json.dumps(stock2)
            r.set('stock2',updated_json_string)
        
        elif row['Stock'] == 'stock3':
            stock3['price'].append(int(row['Price']))
            stock3['time'].append(row['Time'])
            updated_json_string=json.dumps(stock3)
            r.set('stock3',updated_json_string)



pre_price = 0
while True:
    for stock in [stock1,stock2,stock3]:
        for price in stock['price']:
            if price != pre_price:
                calculate_performance(price)
                stock['performance'] += 1 
            pre_price = price
        pre_price = 0

        if stock == stock1:
            updated_json_string=json.dumps(stock1)
            r.set('stock1',updated_json_string)
        
        elif stock == stock2:
            updated_json_string=json.dumps(stock2)
            r.set('stock2',updated_json_string)
        
        elif stock == stock3:
            updated_json_string=json.dumps(stock3)
            r.set('stock3',updated_json_string)

    time.sleep(60)



