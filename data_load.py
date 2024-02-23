#!/usr/bin/env python3  

import psycopg2 as pg 
import psycopg2.extras
import csv

  
# connect to DB on local server 
conn = pg.connect(database='postgres', user='postgres', password='125360')

# Psycopg2 can handle multiple concurrent queries (and their results). 
# For this reason each operation must go through a cursor.
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

def load_data(table, csv_file):
    '''
    function loads all the records from csv_file to table

    Parameters:
    table (str): a table to be loaded.
    csv_file (str): a csv file to take data from 
    '''

    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        
        column_names = [row for row in reader][0]
        column_num = len(column_names)

        # Query as a string 
        insert_query = f"INSERT INTO {table} ({', '.join(column_names)}) VALUES ({', '.join(['%s'] * column_num)}) \
            ON CONFLICT ({column_names[0]}) DO NOTHING;"

        # go back to the beginning of csv_file
        f.seek(0)

        # skip the header
        next(reader)

        # counting the number of records
        count = 0

        for row in reader:

            # Execute the query 
            cur.execute(insert_query, row)
            count += 1

        print(f'{count} records were successfully uploaded to table {table}')        
        
tables = {
    'customers': 'customers.csv',
    'cars': 'cars.csv',
    'orders': 'orders.csv'
}

for table, csv_file in tables.items():
    load_data(table, csv_file)    
 
# Close the cursor and connection
conn.commit() 
cur.close() 
conn.close()