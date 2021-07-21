import pytest

from neraug.scheme import (
    BILOU,
    IOB2,
    IOBES,
    IOB2Tagger,
    StartInsideEndTagger,
    create_tagger,
)


@pytest.mark.parametrize(
    "scheme, expected",
    [(IOB2, IOB2Tagger), (IOBES, StartInsideEndTagger), (BILOU, StartInsideEndTagger)],
)
def test_create_tagger(scheme, expected):
    tagger = create_tagger(scheme)
    assert isinstance(tagger, expected)


@pytest.mark.parametrize(
    "words, label, expected", [([""], "LOC", ["B-LOC"]), (["", ""], "LOC", ["B-LOC", "I-LOC"])]
)
def test_iob2tagger(words, label, expected):
    tagger = IOB2Tagger()
    tags = tagger.tag(words, label)
    assert tags == expected


@pytest.mark.parametrize(
    "words, label, expected",
    [
        ([""], "LOC", ["S-LOC"]),
        (["", ""], "LOC", ["B-LOC", "E-LOC"]),
        (["", "", ""], "LOC", ["B-LOC", "I-LOC", "E-LOC"]),
    ],
)
def test_iobestagger(words, label, expected):
    tagger = StartInsideEndTagger()
    tags = tagger.tag(words, label)
    assert tags == expected
