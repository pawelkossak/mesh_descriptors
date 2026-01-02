import pytest
from classes import TextParser

def test_text_parser_initialization():
    tp = TextParser("This is a test.")
    assert tp.text == "This is a test."

def test_text_parser_invalid_initialization():
    with pytest.raises(ValueError):
        TextParser(123)

def test_text_parser_eliminate_punctuation():
    tp = TextParser("This is, a test!")
    result = tp.eliminate_punctuation()
    assert result == "This is  a test "

def test_text_parser_to_lowercase():
    tp = TextParser("THiS iS A TeSt")
    result = tp.to_lowercase()
    assert result == "this is a test"

def test_text_parser_to_list():
    tp = TextParser("this is a test")
    result = tp.to_list()
    assert result == ["this", "is", "a", "test"]

def test_text_parser_remove_stopwords():
    tp = TextParser(["this", "is", "a", "test"])
    stopwords = {"is", "a"}
    result = tp.remove_stopwords(stopwords)
    assert result == ["this", "test"]

def test_text_parser_tokenize():    
    tp = TextParser("This is a test!")
    result = tp.tokenize()
    assert result == ["test"]