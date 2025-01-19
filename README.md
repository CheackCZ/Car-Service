# Systém pro správu autoservisu
## Obsah
- [Úvod](#úvod)
- [Architektura](#architektura)
- [Funkcionalita](#Funkcionalita)
- [Instalace](#instalace)
- [Spuštění Projektu](#spuštění-projektu)
- [Struktura projektu](#struktura-projektu)
   - [Databáze](#databáze)
- [Testování](#testování)
- [Deployment a odevzdání](#deployment-a-odevzdání)
- [Zdroje](#zdroje)


## Úvod
Tento projekt představuje databázovou aplikaci pro správu autoservisu. Aplikace obsahuje uživatelské rozhraní vytvořené v Pythonu pomocí knihovny CustomTkinter, databázovou část postavenou na MySQL a logiku aplikace v Pythonu.

## Architektura
Projekt je navržen jako modulární aplikace se strukturovanými komponentami:
- Frontend: GUI vytvořené pomocí knihovny customtkinter.
- Backend: Logika aplikace implementovaná v Pythonu.
- Databáze: Relace spravované pomocí MySQL s podporou transakcí.

## Funkcionalita
- CRUD operace pro správu dat tabulek auta, zaměstnanci, opravy.
- Import a export dat ve formátu CSV.
- Generování reportů ve formátu PDF.
- Možnost přepínání mezi různými režimy transakčních úrovní: Dirty Reading.
- Dynamické ovládání GUI podle vybraných tabulek.

## Instalace
1. Nainstalujte Python verze 3.10 nebo novější.
2. Naklonujte nebo stáhněte tento projekt z GitHubu:
   ```
   git clone https://github.com/vase_repo/autoservis.git
   ```

3. Přesuňte se do adresáře projektu:
   ```
   cd autoservis
   ```

4. Nainstalujte potřebné balíčky z requirements.txt:
   ```
   pip install -r requirements.txt
   ```

5. Vytvořte soubor .env ve složce projektu s následující konfigurací:
   ```
   DB_HOST=localhost
   DB_USER=admin
   DB_PASSWORD=admin
   DB_NAME=Service
   DB_PORT=3306
   ```
6. Importujte databázi do MySQL pomocí setup.sql:
   ```
   mysql -u [uživatel] -p [název_databáze] < db/setup.sql
   ```

## Spuštění projektu
1. Spusťte aplikaci (v hlavní složce):
   ```
   python app.py
   ```

2. Aplikace otevře GUI, kde můžete spravovat data autoservisu.


## Struktura projektu
```.
├── db/
│   ├── model.mwb(.bak)          # Model databáze
│   └── setup.sql                # Nastavení databáze
│
├── doc/                         # Jednotlivé testové scénáře
│
├── public/
│   ├── Cars/                    # Komponenty GUI pro správu aut
│   ├── Employees/               # Komponenty GUI pro správu zaměstnanců
│   ├── Repairs/                 # Komponenty GUI pro správu oprav
│   ├── dash.py                  # Dashboard pro práci s databází 
│   ├── sidebar.py               # Boční panel v dashboardu pro přepínání mezi tabulkami databáze
│   ├── tables.py                # Tabulky v bočním panelu 
│   ├── content.py               # Kontent v dashboardu  
│   ├── frame.py                 # Okno obsahující data z databáze 
│   ├── options.py               # Operace, které je možné provést na db
│   ├── import_and_export.py     # Import a Export (csv)
│   └── search.py                # Neufnkční vyhledávání mezi zrovna zobrazenými daty
│
├── src/
│   ├── controllers/             # Logika pro přístup k databázi
│   ├── models/                  # Datové modely
│   ├── connection.py            # Soubor pro připojení k databázi
│   └── report_generator.py      # Soubor pro generování reportu (i v pdf)
│
├── app.py                       # Hlavní soubor aplikace
├── requirements.txt             # Seznam Python knihoven
├── README.md                    # Dokumentace
└── .env.example                 # Příklad .env souboru
```

### Databáze
__Tabulka Employee__
| Column       | Data Type    | Description          |
|--------------|--------------|----------------------|
| id           | INT(11)      | Primary key          |
| name         | VARCHAR(50)  | Employee's name      |
| middle_name  | VARCHAR(50)  | Employee's middle name |
| last_name    | VARCHAR(50)  | Employee's last name |
| phone        | VARCHAR(13)  | Phone number         |
| email        | VARCHAR(100) | Email address        |
| is_free      | BIT(1)       | Availability (0 or 1)|

__Tabulka Repair__
| Column         | Data Type     | Description                 |
|----------------|---------------|-----------------------------|
| id             | INT(11)       | Primary key                 |
| car_id         | INT(11)       | Foreign key to `car.id`     |
| employee_id    | INT(11)       | Foreign key to `employee.id`|
| repair_type_id | INT(11)       | Foreign key to `repair_type.id`|
| date_started   | DATETIME      | Repair start date           |
| date_finished  | DATETIME      | Repair finish date          |
| price          | INT(11)       | Repair cost                 |
| state          | ENUM(...)     | Current repair state        |

__Tabulka Car__
| Column               | Data Type    | Description               |
|----------------------|--------------|---------------------------|
| id                   | INT(11)      | Primary key               |
| client_id            | INT(11)      | Foreign key to `client.id`|
| brand_id             | INT(11)      | Foreign key to `brand.id` |
| registration_number  | VARCHAR(20)  | Car registration number   |
| registration_date    | DATETIME     | Registration date         |
| model                | VARCHAR(50)  | Car model                 |

__Tabulka Repair Type__
| Column       | Data Type    | Description          |
|--------------|--------------|----------------------|
| id           | INT(11)      | Primary key          |
| name         | VARCHAR(50)  | Repair type name     |
| description  | VARCHAR(250) | Repair type details  |

__Tabulka Brand__
| Column       | Data Type    | Description          |
|--------------|--------------|----------------------|
| id           | INT(11)      | Primary key          |
| name         | VARCHAR(50)  | Brand name           |

__Tabulka Client__
| Column       | Data Type    | Description          |
|--------------|--------------|----------------------|
| id           | INT(11)      | Primary key          |
| name         | VARCHAR(50)  | Client's first name  |
| middle_name  | VARCHAR(50)  | Client's middle name |
| last_name    | VARCHAR(50)  | Client's last name   |
| phone        | VARCHAR(13)  | Phone number         |
| email        | VARCHAR(100) | Email address        |
---


### Použité knihovny
- CustomTkinter: Pro tvorbu GUI.
- mysql-connector-python: Pro připojení k databázi.
- Pillow: Práce s obrázky.
- reportlab: Generování PDF.
- CTkMessagebox: Dialogová okna.
- csv: Práce s datovými soubory.

### Testování
Pomocí jednotlivých test scénářů (TesCase) ve složce /doc.

### Deployment a odevzdání
- Export kódu a databáze:
  - Zdrojový kód je strukturovaný v adresáři src/ a doplněn o GUI komponenty v public/.
  - Databáze je exportována pomocí setup.sql.

- Archivace:
  - Veškeré soubory projektu jsou zabaleny do .zip archivu.


## Zdroje
- [w3schools - Python MySQL](https://www.w3schools.com/python/python_mysql_getstarted.asp)
- [customtkinter Dokumentace](https://customtkinter.tomschimansky.com/documentation/)
- [tkinter Dokumentace](https://www.geeksforgeeks.org/python-gui-tkinter/)
- [reportlab Dokumentace](https://docs.reportlab.com/reportlab/userguide/ch1_intro/)
- [CTkMessageBox Okno](https://github.com/Akascape/CTkMessagebox)
- [Testcase Dokument](https://moodle.spsejecna.cz/pluginfile.php/2605/mod_resource/content/0/TestCaseZabagovanaKalkulacka.pdf)
- [ChatGPT](https://chat.openai.com/)
- další ...

## Autor
- Ondřej Faltin
- Email: ondra.faltin@gmail.com
- Datum dokončení: 17. ledna 2025
- Škola: SPŠE Ječná