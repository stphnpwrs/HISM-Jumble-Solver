from jumble_solver.word_list import WordList
from jumble_solver.positional_model import PositionalModel
from jumble_solver.sequential_model import SequentialModel

import heapq
from typing import Optional

class HISM:
    """Class for the Human Imitating Stochastic Model method of finding all anagrams and subset anagrams.

    This class trains a positional and a sequential model on one or more training files. This model can be
    trained on literature or transcripts from a particular human to replicate how a human may
    attempt to solve a word Jumble.

    Attributes:
        wl: Dictionary containing a list of all possible words to find in the Jumble.
        pos_mod: The positional model indicating probabilities of a letter appearing at a given location in a word.
        seq_mod: The sequential model indicating probabilities of a letter appearing after another letter.
        heap: The priority queue used to determine which subset of letters should be checked next.
        base_prob: The probability below which we don't bother to consider subsets of words.
    """

    def __init__(self, filename: str, training_files: list[str]) -> None:
        """Initializes the instance based on the word list and training files.

        Args:
          filename: The path to the file containing all possible words.
          training_files: The paths to all training files to use on the positional and sequential models.
        """
        self.wl = WordList(filename)
        self.pos_mod = PositionalModel(training_files)
        self.seq_mod = SequentialModel(training_files)
        self.heap = []
        self.base_prob = 0.05

    def solve(self, word: str) -> list[str]:
        """Gives a list of all words that can possibly be made by any subset of the given word.

        This function uses the sequential and positional models to create subsets of letters that have the highest
        probability of being words found in the training files. This solution does not take advantage of the hashing
        in the word list and thus worst-case scenario (i.e. base_prob = 0), it has a run time of O(n!*log(n!)) where n
        is the number of characters in the jumble.

        Args:
            word: The jumble word to test.

        Returns:
            The full list of all possible words that can be made.
        """
        full_word_list = []
        h = self.wl.hash_word(word)
        encoding = []
        for c in h:
            encoding.append(ord(c)-ord('a'))
        encoding.append(-1)

        heapq.heappush(self.heap, (-1,[],encoding))
        next_item = [-1]
        while -next_item[0] > self.base_prob:
            next_item = heapq.heappop(self.heap)
            result = self.__itersolve(next_item[1], next_item[2])
            if result:
                full_word_list.append(result)

        return full_word_list

    def __itersolve(self, word: list[str], remaining: list[str]) -> Optional[str]:
        """Utility function to handle probability computations and heap functions.

        This function help builds a word by determining which character in the 'remaining' subset of letters is
        most likely to come next. It combines (multiplies) the probability of the sequential model with the
        probability of the positional model to create a final probability. For comparison's sake, all probabilities
        are normalized after calculation.

        Args:
            word: The list of characters making up the word so far.
            remaining: The list of characters that may potentially be added to the end of the word.
        """
        idx = len(word)

        if idx != 0 and word[-1] == chr(ord('a')-1):
            result = None
            is_word, final_word = self.wl.is_word(word)
            if is_word:
                result = final_word
            return result

        from_letter = -1 if idx == 0 else ord(word[-1])-ord('a')

        data = []
        for i in range(len(remaining)):
            seq_prob = self.seq_mod.model_matrix[from_letter][remaining[i]]
            pos_prob = self.pos_mod.model_matrix[remaining[i]][idx]
            combined_prob = seq_prob * pos_prob

            # deep copy the new word and remaining variables
            new_word = [val for val in word]
            character = remaining[i] + ord('a')
            new_word.append(chr(character))
            new_remaining = remaining[:i]
            new_remaining.extend(remaining[i+1:])

            data.append((combined_prob, new_word, new_remaining))

        # normalize
        cumulative_probs = sum([data[i][0] for i in range(len(data))])
        for i in range(len(data)):
            prob = data[i][0] / cumulative_probs
            heapq.heappush(self.heap, (-prob, data[i][1], data[i][2]))