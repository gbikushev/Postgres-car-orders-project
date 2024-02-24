#!/usr/bin/env python3  

'''

* query1:
print number of customers with total order_amount less or greater than "order_amount".
Require:
 - query number (1, 2, 3)
 - condition (greater, less)
 - order_amount (any number)

* query2:
print all cars that were sent to country = "country"
 - query number (1, 2, 3)
 - country (any country)


* query3:
print sum of order_amount made with credit_card_type = "credit_card_type"
 - query number (1, 2, 3)
 - credit_card_type (any credit_card_type)

'''


import argparse
import pandas as pd
import psycopg2 as pg
import sys

if __name__ == '__main__':
    conn = pg.connect(database='postgres', user='postgres', password='125360')

    parser = argparse.ArgumentParser(description='make queries to data')
    parser.add_argument('--query', type=int, default=1)
    parser.add_argument('--condition', type=str, default='greater')
    parser.add_argument('--order_amount', type=float, default='1000000')

    parser.add_argument('--country', type=str, default='Russia')
    
    parser.add_argument('--credit_card_type', type=str, default='visa')

    args = parser.parse_args()

    if args.query == 1:
        if args.condition == 'greater':
            
            select_query = f'SELECT COUNT(*) as number_of_customers \n\
                            FROM ( \n\
                            SELECT customers.customer_id \n\
                            FROM customers \n\
                            JOIN orders ON customers.customer_id = orders.customer_id \n\
                            GROUP BY customers.customer_id \n\
                            HAVING SUM(orders.order_amount) > {args.order_amount} \n\
                            ) AS subquery;'
            
            df = pd.read_sql_query(select_query, conn)
            print(df)
        
        elif args.condition == 'less':

            select_query = f'SELECT COUNT(*) as number_of_sutomers \n\
                            FROM ( \n\
                            SELECT customers.customer_id \n\
                            FROM customers \n\
                            JOIN orders ON customers.customer_id = orders.customer_id \n\
                            GROUP BY customers.customer_id \n\
                            HAVING SUM(orders.order_amount) < {args.order_amount} \n\
                            ) AS subquery;'
            
            df = pd.read_sql_query(select_query, conn)
            print(df)
        
        else:
            print(f'Error: {args.condition} is incorrect value for --condition argument. Have a look at README file.')        


    elif args.query == 2:
        select_query = f"SELECT DISTINCT cars.*, customers.country \n\
                        FROM cars \n\
                        JOIN orders ON cars.car_id = orders.car_id \n\
                        JOIN customers ON orders.customer_id = customers.customer_id \n\
                        WHERE customers.country = '{args.country}';"
        
        df = pd.read_sql_query(select_query, conn)
        print(df)
            
    elif args.query == 3:

        select_query = f"SELECT * \n\
                        FROM ( \n\
                        SELECT SUM(orders.order_amount) as total_order_amount, orders.credit_card_type \n\
                        FROM orders GROUP BY orders.credit_card_type \n\
                        ) AS subquery \n\
                        WHERE credit_card_type='{args.credit_card_type}';"
        
        credit_card_type_list = ['americanexpress', 'jcb', 'diners-club-us-ca', 'diners-club-carte-blanche', 
             'diners-club-enroute', 'mastercard', 'china-unionpay', 'bankcard', 'switch', 
             'laser', 'maestro', 'instapayment', 'solo', 'visa-electron', 'diners-club-international', 'visa']
        
        if args.credit_card_type not in credit_card_type_list:
            sys.exit(f"Error: {args.credit_card_type} is invalid credit_card_type")

        df = pd.read_sql_query(select_query, conn)
        print(df)

    else:
        print('Error: value {args.query} is incorrect value for --query argument. Have a look at README file.')
