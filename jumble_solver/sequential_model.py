from typing import override
from jumble_solver.base_model import BaseModel

class SequentialModel(BaseModel):
    """Class for the Sequential Stochastic Model.

    This class creates a sequential stochastic model, the purpose of which is to determine the probability of
    one letter following another letter immediately. An example of this might be the probability of the letter
    'w' following the letter 'z' is effectively 0, while 'a' following 'r' may be significantly high.

    Attributes:
        model_matrix: The 26x26 matrix containing all the probabilities for the 26 letters.
    """

    def __init__(self, training_filenames: list[str]) -> None:
        """Initializes the instance based on training files.

        Args:
          training_filenames: List of training files to use to update the probabilities in the matrix.
        """
        super().__init__(training_filenames)

    @override
    def add_word(self, word: str) -> None:
        last_character = -1
        idx = None
        for c in word:
            if c.isalpha():
                idx = ord(c.lower())-ord('a')
                self.model_matrix[last_character][idx] += 1
                last_character = idx
        if idx is not None:
            self.model_matrix[idx][-1] += 1