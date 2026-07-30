insert into users (name, email, password_hash)
values 
('Johan Liebert', 'johan.liebert@example.com', '$2b$12$dummyhash01'),
('Hikigaya Hachiman', 'hachiman@example.com', '$2b$12$dummyhash02'),
('Ayanokoji Kiyotaka', 'ayanokoji@example.com', '$2b$12$dummyhash03'),
('L Lawliet', 'lawliet@example.com', '$2b$12$dummyhash04'),
('Lelouch Lamperouge', 'lelouch@example.com', '$2b$12$dummyhash05'),
('Light Yagami', 'light.yagami@example.com', '$2b$12$dummyhash06'),
('Kiyotaka Ayanokoji', 'kiyotaka@example.com', '$2b$12$dummyhash07'),
('Oreki Houtarou', 'oreki@example.com', '$2b$12$dummyhash08'),
('Yuuichi Katagiri', 'yuuichi@example.com', '$2b$12$dummyhash09'),
('Ken Kaneki', 'kaneki@example.com', '$2b$12$dummyhash10'),
('Guts', 'guts@example.com', '$2b$12$dummyhash11'),
('Griffith', 'griffith@example.com', '$2b$12$dummyhash12'),
('Spike Spiegel', 'spike@example.com', '$2b$12$dummyhash13'),
('Vash Stampede', 'vash@example.com', '$2b$12$dummyhash14'),
('Frieren', 'frieren@example.com', '$2b$12$dummyhash15'),
('Klein Moretti', 'klein.moretti@example.com', '$2b$12$dummyhash16'),
('Cid Kagenou', 'cid.kagenou@example.com', '$2b$12$dummyhash17'),
('Osamu Dazai', 'dazai@example.com', '$2b$12$dummyhash18'),
('Izaya Orihara', 'izaya@example.com', '$2b$12$dummyhash19'),
('Makishima Shogo', 'makishima@example.com', '$2b$12$dummyhash20');

insert into categories(name)
values 
('PHYSICAL'),('MAGIC'),('DEFFENSE'),('MAGIC DEFENSE'),('BOOTS');

insert into products (categories_id, name, price, stock, description)
values
-- PHYSICAL (1)
(1, 'Blade of Despair', 10000, 25, 'Physical Attack tinggi dengan bonus damage saat musuh HP rendah.'),
(1, 'Malefic Roar', 8000, 30, 'Physical Penetration tinggi untuk menembus armor lawan.'),
(1, 'Berserker''s Fury', 7500, 20, 'Critical Damage dan Critical Chance tinggi.'),
(1, 'Hunter Strike', 6000, 18, 'Memberikan Physical Penetration dan Movement Speed.'),
(1, 'Sea Halberd', 9250, 15, 'Mengurangi efek regen dan lifesteal musuh.'),
(2, 'Holy Crystal', 25000, 22, 'Meningkatkan Magic Power secara signifikan.'),
(2, 'Lightning Truncheon', 12500, 19, 'Memberikan damage petir tambahan setiap beberapa detik.'),
(2, 'Genius Wand', 7500, 17, 'Mengurangi Magic Defense target.'),
(2, 'Blood Wings', 3000, 12, 'Magic Power sangat tinggi dengan tambahan HP.'),
(2, 'Divine Glaive', 8000, 14, 'Magic Penetration tinggi terhadap target dengan Magic Defense besar.'),
(3, 'Athena Shield', 8800, 20, 'Memberikan Magic Damage Reduction setelah menerima serangan.'),
(3, 'Blade Armor', 5900, 16, 'Memantulkan sebagian Basic Attack lawan.'),
(3, 'Antique Cuirass', 12350, 13, 'Mengurangi Physical Attack musuh yang menyerang.'),
(3, 'Dominance Ice', 6000, 21, 'Mengurangi Attack Speed dan Shield/Regen lawan.'),
(4, 'Radiant Armor', 9400, 18, 'Efektif melawan Magic Damage bertipe DPS.'),
(4, 'Oracle', 7250, 15, 'Meningkatkan efek Shield dan HP Regen.'),
(4, 'Cursed Helmet', 4750, 11, 'Memberikan Magic Damage area kepada musuh di sekitar.'),
(5, 'Warrior Boots', 2400, 40, 'Sepatu dengan tambahan Physical Defense.'),
(5, 'Tough Boots', 3000, 38, 'Sepatu dengan tambahan Magic Defense dan CC Reduction.'),
(5, 'Arcane Boots', 2690, 35, 'Sepatu dengan tambahan Magic Penetration.');

insert into orders (user_id, total_prices)
values
(1, 17500),   
(2, 25000),  
(3, 16000),  
(4, 2690),  
(5, 45500),  
(6, 8000),    
(7, 20000),   
(8, 15500),  
(9, 8800),  
(10, 9650),
(11, 7250), 
(12, 23500),
(13, 5400), 
(14, 35350),  
(15, 9400),   
(16, 14500),  
(17, 17250),  
(18, 3000),  
(19, 47800),  
(20, 18250);

insert into order_items (order_id, product_id, quantity, product_price)
values 
(1, 1, 1, 10000),
(1, 3, 1, 7500),

(2, 6, 1, 25000),

(3, 2, 2, 8000),

(4, 20, 1, 2690),

(5, 6, 1, 25000),
(5, 1, 1, 10000),
(5, 12, 1, 5900),

(6, 10, 1, 8000),

(7, 1, 2, 10000),

(8, 8, 1, 7500),
(8, 14, 1, 6000),
(8, 20, 1, 2690),

(9, 11, 1, 8800),

(10, 17, 1, 4750),
(10, 18, 1, 2400),
(10, 19, 1, 3000),

(11, 16, 1, 7250),

(12, 4, 1, 6000),
(12, 5, 1, 9250),
(12, 18, 1, 2400),
(12, 19, 1, 3000),

(13, 20, 2, 2690),

(14, 13, 1, 12350),
(14, 6, 1, 25000),

(15, 15, 1, 9400),

(16, 7, 1, 12500),
(16, 18, 1, 2400),

(17, 5, 1, 9250),
(17, 16, 1, 7250),
(17, 18, 1, 2400),

(18, 9, 1, 3000),

(19, 1, 1, 10000),
(19, 6, 1, 25000),
(19, 14, 1, 6000),
(19, 20, 1, 2690),

(20, 4, 1, 6000),
(20, 10, 1, 8000),
(20, 18, 1, 2400);