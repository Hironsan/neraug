import abc
import random
from collections import defaultdict
from itertools import chain
from typing import Callable, Dict, List, Type

from neraug.scheme import Entities, Token, create_tagger


class BaseReplacement(abc.ABC):
    @abc.abstractmethod
    def augment(self, x: List[str], y: List[str], n=1):
        raise NotImplementedError()


class DictionaryReplacement(BaseReplacement):
    def __init__(
        self, ne_dic: Dict[str, str], tokenize: Callable[[str], List[str]], scheme: Type[Token]
    ):
        self.dic = defaultdict(list)
        tagger = create_tagger(scheme)
        for entity, label in ne_dic.items():
            words = tokenize(entity)
            self.dic[label].append({"words": words, "tags": tagger.tag(words, label, scheme)})
        self.scheme = scheme

    def augment(self, x: List[str], y: List[str], n=1):
        xs = []
        ys = []
        entities = Entities([y], self.scheme)
        for i in range(n):
            x_ = []
            y_ = []
            start = 0
            for entity in chain(*entities.entities):
                if not self.dic[entity.tag]:
                    continue
                data = random.choice(self.dic[entity.tag])
                x_.extend(x[start : entity.start])
                x_.extend(data["words"])
                y_.extend(y[start : entity.start])
                y_.extend(data["tags"])
                start = entity.end
            x_.extend(x[start:])
            y_.extend(y[start:])
            xs.append(x_)
            ys.append(y_)
        return xs, ys


class LabelWiseTokenReplacement(BaseReplacement):
    pass


class SynonymReplacement(BaseReplacement):
    def __init__(self):
        pass

    def augment(self, x, y):
        pass


class MentionReplacement(BaseReplacement):
    def __init__(
        self,
        x: List[List[str]],
        y: List[List[str]],
        tokenize: Callable[[str], List[str]],
        scheme: Type[Token],
    ):
        entities = Entities(y, scheme)
        ne_dic = {}
        for tag in entities.unique_tags:
            for entity in entities.filter(tag):
                word = "".join(x[entity.sent_id][entity.start : entity.end])
                ne_dic[word] = tag
        self.replacement = DictionaryReplacement(ne_dic, tokenize, scheme)

    def augment(self, x: List[str], y: List[str], n=1):
        return self.replacement.augment(x, y, n)


class ShuffleWithinSegment(BaseReplacement):
    def __init__(self, scheme: Type[Token]):
        self.scheme = scheme
