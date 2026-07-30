create table users(
id serial primary key,
name varchar(100) not null,
email varchar(100) not null unique,
password_hash varchar(255) not null,
created_at timestamptz default now());

create table categories(
id serial primary key,
name varchar(100) not null,
created_at timestamptz default now());

create table products(
id serial primary key,
categories_id integer references categories(id),
name varchar(100) not null,
price  numeric (12,2),
description text,
stock integer not null,
created_at timestamptz default now());

create table orders(
id serial primary key,
user_id integer references users(id),
total_prices numeric (12,2),
created_at timestamptz default now());

create table  order_items(
order_id integer not null,
product_id integer not null,
quantity integer not null check (quantity > 0),
product_price numeric (12,2),
primary key (order_id, product_id),

constraint fk_order_id foreign key (order_id) references orders(id) on delete cascade,
constraint fk_products_id foreign key (product_id) references products(id));