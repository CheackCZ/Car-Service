-- Vytvoření databáze
-- create database Service;

-- Použití databáze 
use Service;

-- Vytvoření admin uživatele pro správu databáze
-- create user 'admin'@'localhost' identified by 'admin';

-- Vyhrazení všech práv administrátorovi
-- grant all privileges on Service.* to 'admin'@'localhost';
-- flush privileges;

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
    registration_date datetime not null,
    
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
            
    date_started datetime not null,
	date_finished datetime not null,
		check (date_started < date_finished),
    
    price int not null,
    state enum('Pending', 'In process', 'Done') not null default 'Pending'
);


-- Vložení defaultních dat
INSERT INTO employee (name, middle_name, last_name, phone, email, is_free) VALUES 
	('Petr', 'A.', 'Jelínek', '420774102991', 'petr.jelinek@gmail.com', 1),
	('Jan', 'B.', 'Novák', '111222333', 'jannovak@seznam.cz', 0),
	('Michal', NULL, 'Kopecký', '123456789', 'michal.kopecky@mail.com', 1);

insert into employee (name, middle_name, last_name, phone, email, is_free) values ('Jiří', 'Jan', 'Novák', '+420111222333', 'jiri.novak@seznam.cz', 0);

INSERT INTO client (name, middle_name, last_name, phone, email)
	VALUES
	('Anna', 'M.', 'Novotná', '223344556', 'anna.novotna@example.com'),
	('Karel', NULL, 'Král', '667788990', 'karel.kral@example.com');
    
INSERT INTO brand (name)
	VALUES
	('BMW'),
	('Volkswagen'),
	('ŠKODA');
    
INSERT INTO car (client_id, brand_id, registration_number, registration_date, model)
	VALUES
	(1, 1, 'ABC1234', '2021-05-10', 'Octavia'),
	(2, 2, 'XYZ7890', '2022-06-15', 'Passat');

INSERT INTO repair_type (name, description)
	VALUES
	('Výměna oleje', 'Výměna motorového oleje a filtru'),
	('Výměna pneumatik', 'Výmena starých pneumatik za nové'),
	('Kontrola brzd', 'Kontrola a oprava brzdového systému');
    
INSERT INTO repair (car_id, employee_id, repair_type_id, date_started, date_finished, price, state)
	VALUES
	(1, 1, 1, '2023-01-10', '2023-01-11', 2000, 'Hotovo'),
	(2, 2, 2, '2023-02-20', '2023-02-21', 4000, 'Hotovo'),
	(1, 3, 3, '2023-03-15', '2023-03-17', 3000, 'Probíhá');
    

-- Pohledy (Views) pro jednodušší a přehlednější použití
CREATE VIEW all_repairs AS
	SELECT 
		repair.id AS repair_id, repair.date_started AS date_started, repair.date_finished AS date_finished, repair.price AS price, repair.state AS state,
		brand.name AS brand_name,
        car.model AS car_model, car.registration_number AS car_registration_num, 
		employee.id AS employee_id, employee.name AS employee_name, 
		repair_type.name AS repair_type
	FROM repair
		JOIN car ON repair.car_id = car.id
		JOIN brand ON car.brand_id = brand.id
		JOIN employee ON repair.employee_id = employee.id
		JOIN repair_type ON repair.repair_type_id = repair_type.id;

    
select * from all_repairs;
