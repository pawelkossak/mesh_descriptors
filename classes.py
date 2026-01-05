from dataclasses import dataclass
import string
import requests
from collections import Counter
import json
import datetime
import os
import matplotlib.pyplot as plt
from matplotlib import ticker


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

    def tokenize(self) -> dict:
        stopwords = open("english").read().splitlines()
        self.eliminate_punctuation()
        self.to_lowercase()
        self.to_list()
        self.remove_stopwords(set(stopwords))
        # self.text = list(set(self.text))
        return Counter(self.text)


@dataclass
class MeshDescriptor:
    _tokens: dict

    def __post_init__(self):
        if not isinstance(self.tokens, dict):
            raise ValueError("Tokens must be provided as a dictionary")

    @property
    def tokens(self) -> dict:
        return self._tokens

    @tokens.setter
    def tokens(self, value: dict):
        if not isinstance(value, dict):
            raise ValueError("Tokens must be provided as a list")
        self._tokens = value

    def get_descriptors(self) -> list:
        url = "https://id.nlm.nih.gov/mesh/lookup/descriptor?label={}&match=contains&year=current&limit=3"
        descriptors = []
        for token, count in self.tokens.items():
            response = requests.get(url.format(token))
            if response.status_code == 200:
                data = response.json()
                descriptors.extend([item['label'] for item in data]*count)
        return descriptors

    def get_most_common_descriptors(self) -> list:
        return Counter(self.get_descriptors()).most_common(10)


@dataclass
class MeshSession:
    _text: str

    def __post_init__(self):
        self._descriptors = []
        self._config = json.load(open("config.json"))

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

    @property
    def config(self) -> dict:
        return self._config

    def get_descriptors(self) -> list:
        parser = TextParser(self.text)
        tokens = parser.tokenize()
        mesh = MeshDescriptor(tokens)
        self.descriptors = mesh.get_most_common_descriptors()
        return self.descriptors

    def save_descriptors_to_txt(self) -> str:
        if not self.descriptors:
            return "First retrieve descriptors before saving."
        folder = self.config["text_file_save_path"]
        if not folder.endswith('/'):
            folder += '/'
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = f"mesh_descriptors_{datetime.datetime.now().strftime('%d%M%Y%H%M%S')}.txt"
        path = folder + filename
        with open(path, 'w') as f:
            f.write(f"Medical Text: {self.text}\n\nMost common MeSH Descriptors found:\n")
            for descriptor, count in self.descriptors:
                f.write(f"{descriptor} - {count}\n")
        return f"Descriptors saved successfully as {filename}"

    def generate_and_save_chart(self) -> str:
        if not self.descriptors:
            return "First retrieve descriptors before saving."
        fig, ax = plt.subplots()
        descriptors, counts = zip(*self.descriptors)
        ax.bar(descriptors, counts)
        ax.set_ylabel("Count")
        ax.set_title("MeSH Descriptors Frequency")
        ax.set_yticks(range(0, max(counts)+1))
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        plt.xticks(rotation=45, ha='right')

        folder = self.config["chart_save_path"]
        if not folder.endswith('/'):
            folder += '/'
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = f"chart_{datetime.datetime.now().strftime('%d%M%Y%H%M%S')}.png"
        path = folder + filename
        plt.tight_layout()
        plt.savefig(path, format="png")
        return f"Chart saved successfully as {filename}"
