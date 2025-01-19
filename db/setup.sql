-- Vytvoření databáze
-- create database Service;

-- Použití databáze 
use Service;

-- Vytvoření admin uživatele pro správu databáze
-- create user 'admin'@'localhost' identified by 'admin';

-- Vyhrazení všech práv administrátorovi
-- grant all privileges on Service.* to 'admin'@'localhost';
-- flush privileges;

-- drop table repair;
-- drop table car;
-- drop table repair_type;
-- drop table client;
-- drop table brand;
-- drop table employee;


-- Vytvoření tabulky pro Zaměstnance (Employee)
create table employee (
	id int primary key not null auto_increment,
    
    `name` varchar(50) not null,
    middle_name varchar(50),
    last_name varchar(50) not null,
    
    phone varchar(13) not null unique,
    email varchar(100) not null unique,
    
    is_free bit
);

-- Vytvoření tabulky pro Klienta (Client)
create table `client` (
	id int primary key not null auto_increment,
    
    `name` varchar(50) not null,
	middle_name varchar(50),
    last_name varchar(50) not null,
    
    phone varchar(13) not null unique,
    email varchar(100) not null unique
);

-- Vytvoření tabulky pro Značku (brand)
create table brand (
	id int primary key not null auto_increment,
    `name` varchar(50) not null unique
);

-- Vytvoření tabulky pro Auta (Car)
create table car (
	id int primary key not null auto_increment,
    client_id int not null,
		foreign key (client_id) references client(id),
	brand_id int not null,
		foreign key (brand_id) references brand(id),
    
    registration_number varchar(20) not null unique,
    registration_date date not null,
    
    model varchar(50) not null
);

-- Vytvoření tabulky pro Druh opravy (Repair type)
create table repair_type (
	id int primary key not null auto_increment,
    
	`name` varchar(50) not null,
    `description` varchar(255)
);

-- Vytvoření tabulky pro Opravu (Repair)
create table repair (
	id int primary key not null auto_increment,
    car_id int not null,
		foreign key (car_id) references car(id),
    employee_id int not null,
		foreign key (employee_id) references employee(id),
    repair_type_id int not null,
    		foreign key (repair_type_id) references repair_type(id),
            
    date_started date not null,
	date_finished date,
		check (date_started <= date_finished),
    
    price float not null,
    state enum('Pending', 'In process', 'Completed', 'Canceled') not null default 'Pending'
);


-- Vložení dat do tabulky zaměstannců (employee)
INSERT INTO employee (id, name, middle_name, last_name, phone, email, is_free)
	VALUES
	(1, 'Karel', NULL, 'Novotný', '555000111', 'karel.novotny@example.com', TRUE),
	(2, 'Anna', 'H.', 'Černá', '555000222', 'anna.cerna@example.com', FALSE),
	(3, 'Tomáš', NULL, 'Malý', '555000333', 'tomas.maly@example.com', TRUE),
	(4, 'Lucie', 'M.', 'Králová', '555000444', 'lucie.kralova@example.com', TRUE),
	(5, 'Pavel', 'N.', 'Vávra', '555000555', 'pavel.vavra@example.com', FALSE),
	(6, 'Tereza', 'O.', 'Procházková', '555000666', 'tereza.prochazkova@example.com', TRUE),
	(7, 'Jakub', 'P.', 'Vlček', '555000777', 'jakub.vlcek@example.com', TRUE),
	(8, 'Eliška', 'Q.', 'Krejčí', '555000888', 'eliska.krejci@example.com', FALSE),
	(9, 'Adam', 'R.', 'Roubíček', '555000999', 'adam.roubicek@example.com', TRUE),
	(10, 'Michaela', NULL, 'Pokorná', '555001000', 'michaela.pokorna@example.com', FALSE);

-- Vložení dat do tabulky klientů (client)
INSERT INTO client (id, name, middle_name, last_name, phone, email)
	VALUES
	(1, 'Jan', 'A.', 'Novák', '123456789', 'jan.novak@example.com'),
	(2, 'Jana', 'B.', 'Dvořáková', '987654321', 'jana.dvorakova@example.com'),
	(3, 'Alice', NULL, 'Kučerová', '123123123', 'alice.kucerova@example.com'),
	(4, 'Petr', 'C.', 'Veselý', '321321321', 'petr.vesely@example.com'),
	(5, 'Karolína', 'D.', 'Bartošová', '555555555', 'karolina.bartosova@example.com'),
	(6, 'Martin', NULL, 'Horák', '666666666', 'martin.horak@example.com'),
	(7, 'Zuzana', 'E.', 'Šimková', '777777777', 'zuzana.simkova@example.com'),
	(8, 'Eva', NULL, 'Pokorná', '888888888', 'eva.pokorna@example.com'),
	(9, 'Jiří', 'F.', 'Růžička', '999999999', 'jiri.ruzicka@example.com'),
	(10, 'Helena', 'G.', 'Kolářová', '101010101', 'helena.kolarova@example.com');
    
-- Vložení dat do tabulky značek aut (brand)
INSERT INTO brand (id, name)
	VALUES
	(1, 'Toyota'),
	(2, 'Honda'),
	(3, 'Ford'),
	(4, 'Chevrolet'),
	(5, 'Nissan'),
	(6, 'BMW'),
	(7, 'Mercedes'),
	(8, 'Volkswagen'),
	(9, 'Hyundai'),
	(10, 'Kia');
    
-- Vložení dat do tabulky aut (car)
INSERT INTO car (id, client_id, brand_id, registration_number, registration_date, model)
	VALUES
	(1, 1, 1, 'ABC1234', '2023-01-01', 'Octavia'),
	(2, 2, 2, 'DEF5678', '2023-01-15', 'i30'),
	(3, 3, 3, 'GHI9012', '2023-02-01', 'Golf'),
	(4, 4, 4, 'JKL3456', '2023-02-15', '308'),
	(5, 5, 5, 'MNO7890', '2023-03-01', 'Clio'),
	(6, 6, 6, 'PQR2345', '2023-03-15', '3 Series'),
	(7, 7, 7, 'STU6789', '2023-04-01', 'C-Class'),
	(8, 8, 8, 'VWX9012', '2023-04-15', 'Corolla'),
	(9, 9, 9, 'YZA3456', '2023-05-01', 'Ceed'),
	(10, 10, 10, 'BCD7890', '2023-05-15', 'Civic');

-- Vložení dat do tabulky typů oprav
INSERT INTO repair_type (id, name, description)
	VALUES
	(1, 'Výměna oleje', 'Výměna motorového oleje a filtru'),
	(2, 'Výměna brzd', 'Výměna brzdových destiček a kotoučů'),
	(3, 'Rotace pneumatik', 'Rotace pneumatik pro rovnoměrné opotřebení'),
	(4, 'Výměna baterie', 'Výměna autobaterie'),
	(5, 'Seřízení geometrie', 'Seřízení geometrie kol'),
	(6, 'Oprava motoru', 'Diagnostika a oprava motoru'),
	(7, 'Oprava převodovky', 'Oprava nebo výměna převodovky'),
	(8, 'Výměna filtru', 'Výměna vzduchového filtru motoru'),
	(9, 'Oprava zavěšení', 'Oprava problémů se zavěšením vozidla'),
	(10, 'Oprava výfuku', 'Oprava nebo výměna dílů výfukového systému');
    
-- Vložení dat do tabulky oprav
INSERT INTO repair (id, car_id, employee_id, repair_type_id, date_started, date_finished, price, state)
	VALUES
	(1, 1, 1, 1, '2023-01-05', '2023-01-10', 1000.00, 'Completed'),
	(2, 2, 2, 2, '2023-01-20', '2023-01-25', 2000.00, 'Canceled'),
	(3, 3, 3, 3, '2023-02-05', NULL, 0.00, 'Canceled'),
	(4, 4, 4, 4, '2023-02-20', '2023-02-25', 2500.00, 'Completed'),
	(5, 5, 5, 5, '2023-03-05', NULL, 3000.00, 'In process'),
	(6, 6, 6, 6, '2023-03-20', '2023-03-25', 1200.00, 'Completed'),
	(7, 7, 7, 7, '2023-04-05', '2023-04-10', 1800.00, 'Completed'),
	(8, 8, 8, 8, '2023-04-20', Null, 2200.00, 'In process'),
	(9, 9, 9, 9, '2023-05-05', '2023-05-10', 2500.00, 'Completed'),
	(10, 10, 10, 10, '2023-05-20', NULL, 4000.00, 'In process');


-- Pohled pro vypsání všech oprav
CREATE VIEW all_repairs AS
	SELECT 
		repair.id AS repair_id, repair.date_started AS date_started, repair.date_finished AS date_finished, 
        repair.price AS price, repair.state AS state,
		car.id as car_id,
        brand.name AS brand_name,
        car.model AS car_model, car.registration_number AS car_registration_num, 
		employee.id AS employee_id, employee.name AS employee_name, 
		repair_type.name AS repair_type
	FROM repair
		JOIN car ON repair.car_id = car.id
		JOIN brand ON car.brand_id = brand.id
		JOIN employee ON repair.employee_id = employee.id
		JOIN repair_type ON repair.repair_type_id = repair_type.id;
        
-- Pohle pro vypsání všech aut
CREATE VIEW all_cars AS
	SELECT 
		car.id AS car_id, car.registration_number, car.registration_date, car.model, 
		client.id AS client_id, client.name AS client_name, client.middle_name AS client_middle_name, client.last_name AS client_last_name, 
		client.phone AS client_phone, client.email AS client_email, 
		brand.id AS brand_id, brand.name AS brand_name
	FROM car
		JOIN client ON car.client_id = client.id
		JOIN brand ON car.brand_id = brand.id;
        
-- Pohled pro report (shrnutí)
CREATE VIEW summary_report AS
	SELECT 
		COUNT(repair.id) AS total_repairs,
		AVG(repair.price) AS average_repair_price,
		MAX(repair.price) AS max_repair_price,
		MIN(repair.price) AS min_repair_price,
		employee.name AS employee_name,
		COUNT(employee.id) AS repairs_per_employee,
		COUNT(DISTINCT car.id) AS cars_delivered
	FROM repair
	JOIN employee ON repair.employee_id = employee.id
	JOIN car ON repair.car_id = car.id
	GROUP BY employee.name
	ORDER BY COUNT(employee.id) DESC;
    
    
    
    
    select * from repair;
    
    UPDATE repair
                SET state = 'Completed'
                WHERE id = 8;
    
    
SELECT 
    OBJECT_NAME AS table_name, 
    LOCK_TYPE, 
    LOCK_STATUS, 
    OWNER_THREAD_ID
FROM 
    performance_schema.data_locks;
    
    SHOW OPEN TABLES WHERE In_use > 0;
    
    SHOW CREATE TABLE repair;
