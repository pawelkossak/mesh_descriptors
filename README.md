# Table of Contents
[Table of Contents](#table-of-contents)
  1. [Cel i opis projektu](#1-cel-i-opis-projektu)
  2. [Opis klas](#2-architektura-programu-i-opis-klas)
  3. [Instrukcja użytkowania](#3-instrukcja-użytkowania)
  4. [Refleksje](#4-refleksje)

## 1. Cel i opis projektu
Celem projektu jest stworzenie narzędzia wspomagającego analizę tekstów medycznych pod kątem wyszukiwania ontologii zgodnej ze standardem [MeSH (Medical Subject Headings)](https://en.wikipedia.org/wiki/Medical_Subject_Headings). Projekt umożliwia użytkownikowi wprowadzenie dowolnego tekstu medycznego, z którego ekstraktuje słowa kluczowe (tokeny). Następnie aplikacja komunikuje się z [API National Library of Medicine (NLM)](https://id.nlm.nih.gov/mesh/swagger/ui), aby dopasować te słowa do deskryptorów medycznych.

Projekt oferuje interface'y: graficzny (oparty na bibliotece PySide6) oraz tekstowy. Wyniki analizy mogą być eksportowane do plików tekstowych bądź do pliku graficznego w formie wykresu słupkowego.

## 2. Architektura programu i opis klas
Struktura programu opiera się na klasach:
* ```TextParser```: Klasa odpowiedzialna za przeróbkę tekstu wejściowego na tzw. tokeny - usuwanięcie interpunkcji, zmiany liter na małe, usunięcie słów "pustych" i rozbicie na "tokeny", czyli słowa kluczowe.
* ```MeshDescriptor```: Klasa służąca do komunikacji z API NLM. Na podstawie otrzymanych tokenów wyszukuje odpowiadające im deskryptory MeSH i zwraca 10 z nich, najczęściej się pojawiających.
* ```MeshSession```: Klasa sesji zarządzająca całym procesem analizy. Wykorzystuje klasy ```TextParser``` i ```MeshDescriptor```. Odpowiada również za obsługę plików konfiguracyjnych, zapis danych do pliku txt oraz wygenerowanie i zapis wykresu.
* ```MeshDescriptorsWindow```: Klasa definiująca okno główne graficznego interface'u użytkownika, obsługuje sygnały (np. naciśnięcie przycisku) oraz odpowiada za prezentację wyników w tabeli.

## 3. Instrukcja użytkowania
### Instalacja i uruchomienie
1. Pobranie repozytorium:
```
git clone https://gitlab-stud.elka.pw.edu.pl/pkossako/mesh_descriptors.git
cd mesh_descriptors
```
2. Program wymaga interpretera Python w wersji co najmniej 3.14. Pakiety potrzebne do uruchomienia programu można pobrać za pomocą tradycyjnego ```pip``` bądź ```uv```.

- ```pip```:

**Linux/MacOS:**
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
**Windows:**
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
- ```uv```:
```
uv venv --python 3.14
uv sync
```
3. Uruchamianie:

Uruchomienie interface'u CLI:
```
python main.py
```
Uruchomienie interface'u GUI:
```
python main.py --gui
```

## 4. Refleksje