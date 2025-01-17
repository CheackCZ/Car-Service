# Systém pro správu autoservisu
## Obsah
- [Úvod](#úvod)
- [Architektura](#architektura)
- [Funkcionalita](#Funkcionalita)
- [Instalace](#instalace)
- [Spuštění Projektu](#spuštění-projektu)
- [Struktura projektu](#struktura-projektu)
- [Testování](#testování)
- [Deployment a odevzdání](#deployment-a-odevzdání)
- [Zdroje](#zdroje)

## Úvod
Tento projekt představuje databázovou aplikaci pro správu autoservisu. Aplikace obsahuje uživatelské rozhraní vytvořené v Pythonu pomocí knihovny CustomTkinter, databázovou část postavenou na MySQL a logiku aplikace v pythonu.

## Architektura

## Funkcionalita
- CRUD operace pro správu dat a příslušných tabuleke v databázi.
- Import a export dat ve formátu CSV.
- Generování reportů ve formátu PDF.
- Možnost přepnutí mezi různými režimy transakčních úrovní: __Dirty Reading__.

## Deployment a odevzdání
1. Export kódu a databáze:
   - Zdrojový kód je strukturovaný v adresáři src/ a doplněn o GUI komponent v /public.
   - Databáze je exportována pomocí setup.sql.
2. Archivace:
   - Veškeré soubory projektu jsou zabaleny do .zip archivu.

## Zdroje
- CustomTkinter: Pro tvorbu GUI.
- mysql-connector-python: Pro připojení k databázi.
- Pillow: Práce s obrázky.
- reportlab: Generování PDF.
- CTkMessagebox: Dialogová okna.
- csv: Práce s datovými soubory.

## Autor
Ondřej Faltin  
Email: ondra.faltin@gmail.com  
Datum dokončení: 17. ledna 2025  
Škola: SPŠE Ječná  
