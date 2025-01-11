-- Vytvoření databáze
create database Service;

-- Použití databáze 
use Service;

-- Vytvoření admin uživatele pro správu databáze
create user 'admin'@'localhost' identified by 'admin';

-- Vyhrazení všech práv administrátorovi
grant all privileges on Service.* to 'admin'@'localhost';
flush privileges;


-- Vytvoření tabulky pro Zaměstnance (Employee)
create table employee (
	id int primary key not null auto_increment,
    
    `name` varchar(50) not null,
    middle_name varchar(50),
    last_name varchar(50) not null,
    
    phone varchar(12) not null unique,
    email varchar(100) not null unique
);

-- Vytvoření tabulky pro Klienta (Client)
create table `client` (
	id int primary key not null auto_increment,
    
    `name` varchar(50) not null,
	middle_name varchar(50),
    last_name varchar(50) not null,
    
    phone varchar(12) not null unique,
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
	date_finished date not null,
		check (date_started < date_finished),
    
    price int not null,
    state enum('Pending', 'In process', 'Done') not null default 'Pending'
);
