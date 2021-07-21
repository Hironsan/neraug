import abc
from typing import List, Type

from seqeval import scheme as s

IOB2 = s.IOB2
BILOU = s.BILOU
IOBES = s.IOBES
Token = s.Token
Entities = s.Entities


def create_tagger(scheme: Type[Token]):
    if scheme == IOB2:
        return IOB2Tagger()
    elif scheme == IOBES:
        return StartInsideEndTagger()
    elif scheme == BILOU:
        return StartInsideEndTagger("U", "L")
    else:
        raise ValueError(f"The scheme value is invalid: {scheme}")


class BaseTagger(abc.ABC):
    @abc.abstractmethod
    def tag(self, words: List[str], label: str):
        assert len(words) > 0


class IOB2Tagger(BaseTagger):
    def tag(self, words: List[str], label: str):
        super().tag(words, label)
        return [f"B-{label}"] + [f"I-{label}"] * (len(words) - 1)


class StartInsideEndTagger(BaseTagger):
    def __init__(self, single="S", end="E"):
        self.single = single
        self.end = end

    def tag(self, words: List[str], label: str):
        super().tag(words, label)
        if len(words) == 1:
            return [f"{self.single}-{label}"]
        else:
            return [f"B-{label}"] + [f"I-{label}"] * (len(words) - 2) + [f"{self.end}-{label}"]
