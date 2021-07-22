from neraug.augmentator import (
    DictionaryReplacement,
    LabelWiseTokenReplacement,
    MentionReplacement,
    ShuffleWithinSegment,
)
from neraug.scheme import IOBES


def test_dictionary_replacement():
    ne_dic = {"Tokyo Big Sight": "LOC"}
    augmentator = DictionaryReplacement(ne_dic, str.split, IOBES)
    x = ["I", "went", "to", "Osaka"]
    y = ["O", "O", "O", "S-LOC"]
    n = 3
    x_augs, y_augs = augmentator.augment(x, y, n=n)
    assert len(x_augs) == n
    assert isinstance(x_augs, list)
    assert isinstance(x_augs[0], list)
    for x_aug, y_aug in zip(x_augs, y_augs):
        assert x_aug == ["I", "went", "to", "Tokyo", "Big", "Sight"]
        assert y_aug == ["O", "O", "O", "B-LOC", "I-LOC", "E-LOC"]


def test_mention_replacement():
    x_train = [["I", "went", "to", "Osaka"]]
    y_train = [["O", "O", "O", "S-LOC"]]
    augmentator = MentionReplacement(x_train, y_train, IOBES)
    n = 3
    x = ["I", "went", "to", "Tokyo", "Big", "Sight"]
    y = ["O", "O", "O", "B-LOC", "I-LOC", "E-LOC"]
    x_augs, y_augs = augmentator.augment(x, y, n=n)
    assert len(x_augs) == n
    assert isinstance(x_augs, list)
    assert isinstance(x_augs[0], list)
    for x_aug, y_aug in zip(x_augs, y_augs):
        assert x_aug == ["I", "went", "to", "Osaka"]
        assert y_aug == ["O", "O", "O", "S-LOC"]


def test_label_with_replacement():
    x_train = [["I", "went", "to", "Osaka"]]
    y_train = [["O", "O", "O", "S-LOC"]]
    augmentator = LabelWiseTokenReplacement(x_train, y_train, p=1.0)
    n = 3
    x = ["I", "went", "to", "Tokyo"]
    y = ["O", "O", "O", "S-LOC"]
    x_augs, y_augs = augmentator.augment(x, y, n=n)
    assert len(x_augs) == n
    assert isinstance(x_augs, list)
    assert isinstance(x_augs[0], list)
    for x_aug, y_aug in zip(x_augs, y_augs):
        words = {"I", "went", "to"}
        assert x_aug[0] in words
        assert x_aug[1] in words
        assert x_aug[2] in words
        assert x_aug[3] == "Osaka"
        assert y_aug == ["O", "O", "O", "S-LOC"]


def test_shuffle_replacement():
    augmentator = ShuffleWithinSegment(IOBES, p=1.0)
    n = 3
    x = ["I", "went", "to", "Tokyo"]
    y = ["O", "O", "O", "S-LOC"]
    x_augs, y_augs = augmentator.augment(x, y, n=n)
    assert len(x_augs) == n
    assert isinstance(x_augs, list)
    assert isinstance(x_augs[0], list)
    for x_aug, y_aug in zip(x_augs, y_augs):
        words = {"I", "went", "to"}
        assert x_aug[0] in words
        assert x_aug[1] in words
        assert x_aug[2] in words
        assert x_aug[3] == "Tokyo"
        assert y_aug == ["O", "O", "O", "S-LOC"]
