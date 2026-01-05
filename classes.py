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
    """
    Handles the cleaning and tokenization of input text.

    :param _text: The source text or list of tokens to be processed.
    :type _text: str | list
    """
    _text: str | list

    def __post_init__(self):
        """
        Validates the input type after class initialization.

        :raises ValueError: If the text is neither a string nor a list.
        """
        if not isinstance(self.text, str) and not isinstance(self.text, list):
            raise ValueError("Text must be a string or list")

    @property
    def text(self) -> str:
        """
        Gets the current state of the text.

        :return: The current text or list of tokens.
        :rtype: str | list
        """
        return self._text

    @text.setter
    def text(self, value: str | list):
        """
        Sets a new value for the text with type validation.

        :param value: The new text or list of tokens.
        :type value: str | list
        :raises ValueError: If the value is neither a string nor a list.
        """
        if not isinstance(value, str) and not isinstance(value, list):
            raise ValueError("Text must be a string or list")
        self._text = value

    def eliminate_punctuation(self) -> str:
        """
        Removes all punctuation marks from the text, replacing them with spaces.

        :return: The cleaned string without punctuation.
        :rtype: str
        """
        for i in string.punctuation:
            self.text = self.text.replace(i, " ")
        return self.text

    def to_lowercase(self) -> str:
        """
        Converts the text to lowercase.

        :return: The lowercase version of the text.
        :rtype: str
        """
        self.text = self.text.lower()
        return self.text

    def to_list(self) -> list:
        """
        Splits the text into a list of words (tokens) based on whitespace.

        :return: A list of tokens.
        :rtype: list
        """
        self.text = self.text.split()
        return self.text

    def remove_stopwords(self, stopwords: set) -> list:
        """
        Filters out tokens that are present in the provided stopwords set.

        :param stopwords: A set of words to be excluded from the tokens.
        :type stopwords: set
        :return: The list of tokens after stopword removal.
        :rtype: list
        """
        self.text = [word for word in self.text if word not in stopwords]
        return self.text

    def tokenize(self) -> dict:
        """
        Executes the full tokenization pipeline: eliminates punctuation, 
        converts to lowercase, splits into a list, and removes stopwords.

        :return: A dictionary containing the frequency count of each token.
        :rtype: dict
        """
        stopwords = open("english").read().splitlines()
        self.eliminate_punctuation()
        self.to_lowercase()
        self.to_list()
        self.remove_stopwords(set(stopwords))
        return Counter(self.text)


@dataclass
class MeshDescriptor:
    """
    Communicates with the NLM API to retrieve MeSH descriptors for given tokens.

    :param _tokens: A dictionary of tokens and their respective frequencies.
    :type _tokens: dict
    """
    _tokens: dict

    def __post_init__(self):
        """
        Validates that the provided tokens are in a dictionary format.

        :raises ValueError: If tokens is not a dictionary.
        """
        if not isinstance(self.tokens, dict):
            raise ValueError("Tokens must be provided as a dictionary")

    @property
    def tokens(self) -> dict:
        """
        Gets the dictionary of tokens.

        :return: The dictionary of tokens.
        :rtype: dict
        """
        return self._tokens

    @tokens.setter
    def tokens(self, value: dict):
        """
        Sets a new dictionary of tokens.

        :param value: A dictionary of tokens.
        :type value: dict
        :raises ValueError: If the value is not a dictionary.
        """
        if not isinstance(value, dict):
            raise ValueError("Tokens must be provided as a dictionary")
        self._tokens = value

    def get_descriptors(self) -> list:
        """
        Queries the MeSH API for each token and retrieves corresponding labels.

        :return: A list of all found descriptor labels (multiplied by token count) 
                 or an error list if the request fails.
        :rtype: list
        """
        url = "https://id.nlm.nih.gov/mesh/lookup/descriptor?label={}&match=contains&year=current&limit=3"
        descriptors = []
        for token, count in self.tokens.items():
            try:
                response = requests.get(url.format(token))
                if response.status_code == 200:
                    data = response.json()
                    descriptors.extend([item['label'] for item in data] * count)
            except Exception as e:
                return [("error", e)]
        return descriptors

    def get_most_common_descriptors(self) -> list:
        """
        Retrieves all descriptors and returns the 10 most frequent ones.

        :return: A list of tuples containing (descriptor_label, frequency).
        :rtype: list
        """
        descriptors = self.get_descriptors()
        if not descriptors:
            return []
        if descriptors[0][0] == "error":
            return descriptors
        return Counter(descriptors).most_common(10)


@dataclass
class MeshSession:
    """
    Coordinates the process of analyzing medical text, retrieving MeSH 
    descriptors, and saving results.

    :param _text: The medical text to be analyzed.
    :type _text: str
    """
    _text: str

    def __post_init__(self):
        """
        Initializes an empty list for descriptors and loads session 
        configuration from a JSON file.
        """
        self._descriptors = []
        self._config = json.load(open("config.json"))

    @property
    def text(self) -> str:
        """
        Gets the source text.

        :return: The medical text string.
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, value: str):
        """
        Sets a new source text for analysis.

        :param value: The new medical text string.
        :type value: str
        """
        self._text = value

    @property
    def descriptors(self) -> list:
        """
        Gets the list of found MeSH descriptors.

        :return: A list of descriptors and their counts.
        :rtype: list
        """
        return self._descriptors

    @descriptors.setter
    def descriptors(self, value: list):
        """
        Sets the list of MeSH descriptors.

        :param value: A list of descriptors.
        :type value: list
        """
        self._descriptors = value

    @property
    def config(self) -> dict:
        """
        Gets the session configuration.

        :return: Configuration settings.
        :rtype: dict
        """
        return self._config

    def get_descriptors(self) -> list:
        """
        Runs the full pipeline to tokenize the text and fetch the most common MeSH descriptors.

        :return: The 10 most frequent MeSH descriptors found.
        :rtype: list
        """
        parser = TextParser(self.text)
        tokens = parser.tokenize()
        mesh = MeshDescriptor(tokens)
        self.descriptors = mesh.get_most_common_descriptors()
        return self.descriptors

    def save_descriptors_to_txt(self) -> str:
        """
        Saves the results of the analysis to a text file in the configured directory.

        :return: A status message indicating success or failure.
        :rtype: str
        """
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
        """
        Generates a bar chart of the descriptor frequencies and saves it as a PNG file.

        :return: A status message indicating success or failure.
        :rtype: str
        """
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
