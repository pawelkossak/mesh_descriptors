# Mesh Descriptors - Medical Text Analysis Tool
Author: Paweł Kossakowski
# Table of Contents
  1. [Project goal and description](#1-project-goal-and-description)
  2. [Program architecture and class description](#2-program-architecture-and-class-description)
  3. [User manual](#3-user-manual)
  4. [Reflections](#4-reflections)

## 1. Project goal and description
The goal of the project is to create a tool supporting the analysis of medical texts in terms of searching for ontologies compliant with the [MeSH (Medical Subject Headings)](https://en.wikipedia.org/wiki/Medical_Subject_Headings)standard. The project allows the user to input any medical text, from which it extracts keywords (tokens). The application then communicates with the [API National Library of Medicine (NLM)](https://id.nlm.nih.gov/mesh/swagger/ui) to match these words with medical descriptors.

The project offers both graphical (based on the PySide6 library) and text-based interfaces. Analysis results can be exported to text files or to an image file in the form of a bar chart.

## 2. Program architecture and class description
The program structure is based on the following classes:
* ```TextParser```: A class responsible for processing the input text into tokens. It handles punctuation removal, case normalization (converting to lowercase), stop-word removal, and splitting the text into "tokens" (keywords).
* ```MeshDescriptor```: A class used for communication with the NLM API. Based on the received tokens, it searches for corresponding MeSH descriptors and returns the top 10 most frequent results.
* ```MeshSession```: A session management class that oversees the entire analysis process. It utilizes the ```TextParser``` and ```MeshDescriptor``` classes. It is also responsible for handling configuration files, saving data to .txt files, and generating and saving the bar chart.
* ```MeshDescriptorsWindow```: A class that defines the main window of the Graphical User Interface (GUI). It handles signals (e.g., button clicks) and is responsible for displaying the results in a table format.

## 3. User manual
### Instalation and running
1. Downloading files:
```
git clone https://gitlab-stud.elka.pw.edu.pl/pkossako/mesh_descriptors.git
cd mesh_descriptors
```
2. Program needs Python in version at least 3.14. The packages needed to run the program can be installed using either the standard ```pip``` or ```uv```.

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
uv sync
```
3. Running:

Running in terminal:
```
python main.py
```
Running graphical interface:
```
python main.py --gui
```
### Settings
In config.json user can specify location in which exported text files and charts will be saved:
```
{
    "text_file_save_path": "{path to save exported text files}",
    "chart_save_path": "{path to save exported charts}"
}
```

## 4. Reflections
### Scope of work performed:
- Efficient text parsing and tokenization were implemented.
- Successful integration with the NLM API using the requests library was achieved.
- Both graphical and command-line interfaces were designed and implemented.
- Functionality for exporting results to text files and generating bar charts was added.
- Unit tests were developed.
- A configuration system based on a .json file was implemented.
