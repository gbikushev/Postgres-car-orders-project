BEGIN;

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS cars;
DROP TABLE IF EXISTS customers;
DROP TYPE IF EXISTS credit_card;

CREATE TYPE credit_card as ENUM
(
	'americanexpress', 'jcb', 'diners-club-us-ca',
    'diners-club-carte-blanche', 'diners-club-enroute', 'mastercard',
    'china-unionpay', 'bankcard', 'switch', 'laser', 'maestro',
    'instapayment', 'solo', 'visa-electron',
    'diners-club-international', 'visa'
);

CREATE TABLE cars
(
    car_id bigserial PRIMARY KEY,
    car_brand text NOT NULL,
    car_model text NOT NULL,
    car_color text NOT NULL,
    manufacture_year integer CHECK (manufacture_year >= 1900 AND manufacture_year <= EXTRACT(YEAR FROM CURRENT_DATE)) NOT NULL
);

CREATE TABLE customers
(
    customer_id bigserial PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL,
    country text,
    phone_number text CHECK (phone_number LIKE '+%') UNIQUE NOT NULL,
    email_address text CHECK (email_address LIKE '%@%') UNIQUE
);

CREATE TABLE orders
(
    order_id bigserial PRIMARY KEY,
    customer_id integer NOT NULL,
    car_id integer NOT NULL,
    credit_card_type credit_card,
    order_amount numeric(20, 2) CHECK (order_amount > 0) NOT NULL,
	FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
	FOREIGN KEY (car_id) REFERENCES cars(car_id)
);

END;