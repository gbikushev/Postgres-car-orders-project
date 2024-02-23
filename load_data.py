#!/usr/bin/env python3 
 
# psycopg library renamed to make shorter 
import psycopg2 as pg 
# needed to use DictCursor 
import psycopg2.extras
import csv
import pandas as pd
 
 
# connect to DB on local server 
conn = pg.connect(database='postgres', user='postgres', password='125360') 
 
# Psycopg2 can handle multiple concurrent queries (and their results). 
# For this reason each operation must go through a cursor. 
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
# NOT the same as server-side cursors which we will meet later. 

csv_file = "customers.csv" 
with open(csv_file, "r") as f:
    reader = csv.reader(f)

    next(reader)

    insert_query = 'INSERT INTO customers (customer_id, first_name, last_name, country, phone_number, email_address) \
        VALUES (%s, %s, %s, %s, %s, %s)'
    
    for row in reader:
        cur.execute(insert_query, row)


csv_file = "cars.csv" 
with open(csv_file, "r") as f:
    reader = csv.reader(f)

    next(reader)

    insert_query = 'INSERT INTO cars (car_id, car_brand, car_model, car_color, manufacture_year) \
        VALUES (%s, %s, %s, %s, %s)'
    
    for row in reader:
        cur.execute(insert_query, row)


# Query as a string 
query = "SELECT * from customers;" 


 
# Execute the query 
cur.execute(query) 

print(cur.rowcount)


 
# # Can see the number of rows returned 
# print("number of regions: %s" % cur.rowcount) 
 
# # Loop over each row 
# for row in cur: 
 
#     # Access by column name in dict 
#     print("%s. %s" % (row['id'], row['name'])) 
 
# optional: rewind the cursor (if we want to use it again) 
# cur.scroll(0, 'absolute') 
 
# Close the cursor and connection
conn.commit() 
cur.close() 
conn.close()