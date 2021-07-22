import abc
import random
from collections import Counter, defaultdict
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
            self.dic[label].append({"words": words, "tags": tagger.tag(words, label)})
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
    def __init__(self, x: List[List[str]], y: List[List[str]], p=0.8):
        self.p = p
        self.distribution = defaultdict(Counter)
        for words, tags in zip(x, y):
            for word, tag in zip(words, tags):
                self.distribution[tag][word] += 1

    def augment(self, x: List[str], y: List[str], n=1):
        xs = []
        ys = []
        for i in range(n):
            x_ = []
            for word, tag in zip(x, y):
                if random.random() <= self.p:
                    counter = self.distribution[tag]
                    words = list(counter.keys())
                    weights = list(counter.values())
                    word = random.choices(words, weights=weights, k=1)[0]
                x_.append(word)
            xs.append(x_)
            ys.append(y)
        return xs, ys


class MentionReplacement(BaseReplacement):
    def __init__(
        self,
        x: List[List[str]],
        y: List[List[str]],
        scheme: Type[Token],
    ):
        entities = Entities(y, scheme)
        dic = defaultdict(list)
        for tag in entities.unique_tags:
            for entity in entities.filter(tag):
                words = x[entity.sent_id][entity.start : entity.end]
                tags = y[entity.sent_id][entity.start : entity.end]
                dic[tag].append({"words": words, "tags": tags})
        self.replacement = DictionaryReplacement({}, str.split, scheme)
        self.replacement.dic = dic

    def augment(self, x: List[str], y: List[str], n=1):
        return self.replacement.augment(x, y, n)


class ShuffleWithinSegment(BaseReplacement):
    def __init__(self, scheme: Type[Token], p=0.8):
        self.scheme = scheme
        self.p = p

    def augment(self, x: List[str], y: List[str], n=1):
        xs = []
        ys = []
        segments = self.make_segments(y)
        for i in range(n):
            x_ = []
            for s, e in segments:
                words = x[s:e]
                if random.random() <= self.p:
                    random.shuffle(words)
                x_.extend(words)
            xs.append(x_)
            ys.append(y)
        return xs, ys

    def make_segments(self, y: List[str]):
        segments = []
        entities = Entities([y], self.scheme)
        start = 0
        for entity in chain(*entities.entities):
            segments.append((start, entity.start))
            segments.append((entity.start, entity.end))
            start = entity.end
        segments.append((start, len(y)))
        return [(s, e) for s, e in segments if s != e]
