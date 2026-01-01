from dataclasses import dataclass
import string

@dataclass
class TextParser:
    text: str

    def __post_init__(self):
        if not isinstance(self.text, str):
            raise ValueError("Text must be a string")
        
    def eliminate_punctuation(self) -> str:
        for i in string.punctuation:
            self.text = self.text.replace(i, " ")
        return self.text
    
    def to_lowercase(self) -> str:
        self.text = self.text.lower()
        return self.text
    
    def to_list(self) -> list:
        self.text = self.text.split()

    def remove_stopwords(self, stopwords: set) -> list:
        self.text = [word for word in self.text if word not in stopwords]
        return self.text

    def tokenize(self) -> str:
        stopwords = open("english").read().splitlines()
        self.eliminate_punctuation()
        self.to_lowercase()
        self.to_list()
        self.remove_stopwords(set(stopwords))
        return self.text
