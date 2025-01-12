import typing
import yaml
from schema import Schema, And, Use, SchemaError

from .score import Score

DEFAULT_SCORES = [
    {"name": "Joe", "value": 100},
    {"name": "Jack", "value": 80},
    {"name": "William", "value": 60},
    {"name": "Averell", "value": 40},
]

class Scores:
    def __init__(self, max_scores: int, scores: list[Score]) -> None:
        self._max_scores = max_scores
        scores.sort(reverse = True)
        self._scores = scores[:self._max_scores]

    def add_score(self, score: int) -> None:
        """
        Ajoute un score et trie la liste par ordre décroissant.

        Limite le nombre de scores à max_scores.
        """
        self._scores.append(score)
        self._scores = sorted(self._scores, key=lambda x: x.value, reverse=True)[:self._max_scores]

    @classmethod
    def default(cls, max_scores: int) -> "Scores":
        return cls(max_scores, [Score(name="Joe", score=100), Score(name="Jack", score=80), Score(name="Averell", score=60), Score(name="William", score=40)])

    def __iter__(self) -> typing.Iterator[Score]:
        return iter(self._scores)

    def is_high_score(self, score: int) -> bool:
        return score > self._scores[-1]

    def save_to_file(self, file_path):
        """Sauvegarde les scores actuels dans un fichier YAML."""
        with open(file_path, "w") as file:
            yaml.dump([score.to_dict() for score in self._scores], file)

    def load_from_file(self, file_path):
        """Charge les scores depuis un fichier YAML et valide les données."""
        schema = Schema([{"name": And(str, lambda s: len(s) <= 8), "value": And(int, lambda n: n >= 0)}])

        try:
            with open(file_path, "r") as file:
                data = yaml.safe_load(file)
                validated_data = schema.validate(data)
                self._scores = [Score.from_dict(item) for item in validated_data]
        except FileNotFoundError:
            print(f"File {file_path} not found. Initializing empty scores.")
            self._scores = []
        except SchemaError as e:
            print(f"Invalid score data in {file_path}: {e}")
            self._scores = []

    def validate_scores(file_path):
        schema = Schema([
            {"name": And(str, lambda s: len(s) <= 8), "value": And(int, lambda v: v >= 0)}
        ])
        try:
            with open(file_path, "r") as file:
                scores_data = yaml.safe_load(file)
            schema.validate(scores_data)
            return scores_data
        except Exception as e:
            print(f"Invalid scores file: {e}")
            return []

    def initialize_scores_file(file_path):
        try:
            with open(file_path, "x") as file:  # "x" crée un nouveau fichier
                yaml.dump(DEFAULT_SCORES, file)
            print(f"Scores file created at {file_path}.")
        except FileExistsError:
            print(f"Scores file already exists at {file_path}.")

    def get_scores(self) -> list[Score]:
        return self._scores