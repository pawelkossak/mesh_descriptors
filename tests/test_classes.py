import pytest
from classes import TextParser, MeshDescriptor

# TextParser Tests

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

def test_text_parser_tokenize_duplicated_tokens():    
    tp = TextParser("Test test TEST!")
    result = tp.tokenize()
    assert result == ["test"]
# MeshDescriptor Tests

def test_mesh_descriptor_initialization():
    md = MeshDescriptor(["test", "example"])
    assert md.tokens == ["test", "example"]

def test_mesh_descriptor_invalid_initialization():
    with pytest.raises(ValueError):
        MeshDescriptor("not a list")

def test_mesh_descriptor_get_most_common_descriptors():
    md = MeshDescriptor(['patients', 'hypertension', 'disease', 'vascular', 'problems', 'known', 'pressure', 'increases', 'heart', 'also', 'stroke', 'chronic', 'high', 'risk', 'function', 'cardiac', 'blood', 'monitoring', 'essential'])
    result = md.get_most_common_descriptors()
    assert result == [('Essential Hypertension', 2), ('Moving and Lifting Patients', 1), ('No-Show Patients', 1), ('Patients', 1), ('Dietary Approaches To Stop Hypertension', 1), ('Familial Primary Pulmonary Hypertension', 1), ('Abducens Nerve Diseases', 1), ('Accessory Nerve Diseases', 1), ('Acute Disease', 1), ('Cardio Ankle Vascular Index', 1)]

def test_mesh_descriptor_get_most_common_descriptors_empty_tokens():
    md = MeshDescriptor([])
    result = md.get_most_common_descriptors()
    assert result == []

def test_mesh_descriptor_get_most_common_descriptors_no_matches():
    md = MeshDescriptor(['wafa', 'awfgesg', 'fwagres'])
    result = md.get_most_common_descriptors()
    assert result == []