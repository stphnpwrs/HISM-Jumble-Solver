from typing import override
from jumble_solver.base_model import BaseModel

class PositionalModel(BaseModel):
    """Class for the Positional Stochastic Model.

    This class creates a positional stochastic model, the purpose of which is to determine the probability of
    one letter appearing in a certain position in a word. An example of this may be the probability for 'x'
    appearing in the first position of a word is significantly lower than the probability of 'a' being the
    first letter of a word.

    Attributes:
        model_matrix: The 26xN matrix containing all the probabilities for the 26 letters.
    """

    def __init__(self, training_filenames: list[str]) -> None:
        """Initializes the instance based on training files.

        Args:
          training_filenames: List of training files to use to update the probabilities in the matrix.
        """
        super().__init__(training_filenames, 12)

    @override
    def add_word(self, word: str):
        i = 0
        for c in word:
            if c.isalpha():
                idx = ord(c.lower()) - ord('a')
                try:
                    self.model_matrix[idx][i] += 1
                except IndexError:
                    pass
                i += 1