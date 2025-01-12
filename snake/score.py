class Score:

    MAX_LENGTH = 8

    def __init__(self, score: int, name: str) -> None:
        self._score = score
        self._name = name[:self.MAX_LENGTH]

    @property
    def name(self) -> str:
        return self._name

    @property
    def score(self)-> int:
        return self._score

    def __lt__(self, other: object) -> bool:
        return isinstance(object, Score) and self._score < other._score