class BaseModel:
    """Base functionality for Stochastic Models.

    This class includes several functions useful for stochastic models including a training function,
    magic string function, and a means of normalization along with a function definition for an overridable
    function for updating the model based on words found in the training files.

    Attributes:
        model_matrix: The matrix containing all the probabilities for the 26 letters.
    """

    def __init__(self, training_filenames: list[str], vector_length: int = 26) -> None:
        """Initializes the instance based on training files.

        Args:
          training_filenames: List of training files to use to update the probabilities in the matrix.
          vector_length: The maximum length of the vectors for each letter in the stochastic model.
        """
        self.model_matrix = [[0 for _ in range(vector_length)] for _ in range(26)]

        for i in range(len(training_filenames)):
            self.add_file(training_filenames[i])
        self.normalize()

    def add_word(self, word: str) -> None:
        """Updates probabilities in model based on the word.

        This function is meant to be overridden with the unique way to update the probabilities in the
        model matrix dependent on which type of stochastic model we are using.

        Args:
            word: The word used to update the probabilities in the model.
        """
        pass

    def add_file(self, filename: str) -> None:
        """High level function to train the model on a full file.

        This function iterates through every word in the training file and updates the model with each
        word using the overridden 'add_word' function.

        Args:
            filename: The path to the training file.
        """
        with open(filename, "r") as f:
            all_lines = f.readlines()

        for i in range(len(all_lines)):
            line = all_lines[i].strip().split()
            for word in line:
                self.add_word(word)

    def normalize(self) -> None:
        """Normalizes all stochastic information for proper comparison.

        This function normalizes all vector information for each letter in the model such that the sum
        of all elements in a single vector is 1.
        """
        for i in range(len(self.model_matrix)):
            s = sum(self.model_matrix[i])
            for j in range(len(self.model_matrix[i])):
                self.model_matrix[i][j] /= s

    def __str__(self) -> str:
        """Produces string for print methods.

        This function returns a string that is merely the matrix values of the model. This is useful
        for debugging.
        """
        s = ""
        for i in range(len(self.model_matrix)):
            for j in range(len(self.model_matrix[i])):
                s += str(self.model_matrix[i][j]) + ","
            s = s[:-1] + "\n"
        return s