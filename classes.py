from dataclasses import dataclass
import string
import requests
from collections import Counter
import json
import datetime
import os

@dataclass
class TextParser:
    _text: str | list

    def __post_init__(self):
        if not isinstance(self.text, str) and not isinstance(self.text, list):
            raise ValueError("Text must be a string or list")
        
    @property
    def text(self) -> str:
        return self._text
    
    @text.setter
    def text(self, value: str | list):
        if not isinstance(value, str) and not isinstance(value, list):
            raise ValueError("Text must be a string or list")
        self._text = value

    def eliminate_punctuation(self) -> str:
        for i in string.punctuation:
            self.text = self.text.replace(i, " ")
        return self.text
    
    def to_lowercase(self) -> str:
        self.text = self.text.lower()
        return self.text
    
    def to_list(self) -> list:
        self.text = self.text.split()
        return self.text

    def remove_stopwords(self, stopwords: set) -> list:
        self.text = [word for word in self.text if word not in stopwords]
        return self.text

    def tokenize(self) -> list:
        stopwords = open("english").read().splitlines()
        self.eliminate_punctuation()
        self.to_lowercase()
        self.to_list()
        self.remove_stopwords(set(stopwords))
        self.text = list(set(self.text))
        return self.text


@dataclass
class MeshDescriptor:
    _tokens: list
    
    def __post_init__(self):
        if not isinstance(self.tokens, list):
            raise ValueError("Tokens must be provided as a list")
    
    @property
    def tokens(self) -> list:
        return self._tokens
    
    @tokens.setter
    def tokens(self, value: list):
        if not isinstance(value, list):
            raise ValueError("Tokens must be provided as a list")
        self._tokens = value

    def get_descriptors(self) -> list:
        url = "https://id.nlm.nih.gov/mesh/lookup/descriptor?label={}&match=contains&year=current&limit=3"
        descriptors = []
        for token in self.tokens:
            response = requests.get(url.format(token))
            if response.status_code == 200:
                data = response.json()
                descriptors.extend([item['label'] for item in data])
        return descriptors
    
    def get_most_common_descriptors(self) -> dict:
        return Counter(self.get_descriptors()).most_common(10)
    

@dataclass
class MeshSession:
    _text: str

    def __post_init__(self):
        self._descriptors = []

    @property
    def text(self) -> str:
        return self._text
    
    @text.setter
    def text(self, value: str):
        self._text = value
    
    @property
    def descriptors(self) -> list:
        return self._descriptors
    
    @descriptors.setter
    def descriptors(self, value: list):
        self._descriptors = value
    
    def get_descriptors(self) -> list:
        parser = TextParser(self.text)
        tokens = parser.tokenize()
        mesh = MeshDescriptor(tokens)
        self.descriptors = mesh.get_most_common_descriptors()
        return self.descriptors
    
    def save_descriptors_to_txt(self, searchText) -> str:
        if not self.descriptors:
            return "First retrieve descriptors before saving."
        folder = json.load(open("config.json"))["text_file_save_path"]
        if not folder.endswith('/'):
            folder += '/'
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = f"mesh_descriptors_{datetime.datetime.now().strftime('%d%M%Y%H%M%S')}.txt"
        path = folder + filename
        with open(path, 'w') as f:
            f.write(f"Medical Text: {searchText}\n\nMost common MeSH Descriptors found:\n")
            for descriptor, count in self.descriptors:
                f.write(f"{descriptor} - {count}\n")
        return f"Descriptors saved successfully as {filename}"
