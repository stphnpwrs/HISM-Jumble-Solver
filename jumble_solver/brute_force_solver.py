from jumble_solver.word_list import WordList

class BruteForce:
    """Class for the Brute Force method of finding all anagrams and subset anagrams.

    This class takes advantage of the hashing method in the Word List to optimize the runtime of
    finding all possible words that may be made by all subsets of the original Jumble. Final runtime complexity
    for this brute force solver is O(2^n) where n is the number of characters in the Jumble.

    Attributes:
        wl: Dictionary containing a list of all possible words to find in the Jumble.
    """

    def __init__(self, filename: str) -> None:
        """Initializes the instance based on the word list file.

        Args:
          filename: The path to the file containing all possible words.
        """
        self.wl = WordList(filename)

    def solve(self, word: str) -> list[str]:
        """Gives a list of all words that can possibly be made by any subset of the given word.

        This function uses the hashing function of the word list to alphabetize all letters in the word, eliminating
        the need to find all permutations during runtime and reduce the complexity of the search algorithm.

        Args:
            word: The word to test.

        Returns:
            The full list of all possible words that can be made.
        """
        h = self.wl.hash_word(word)
        word_list = []
        for i in range(1,2**len(h)):  # explicit definition of runtime: O(2^n) where n is the number of characters
            mask = bin(i)[2:]
            mask = "0"*(len(h)-len(mask)) + mask  # provide leading 0s
            encoding = binary_mask(mask, h)
            results = self.wl.get_words(encoding)
            if results:
                for word in results:
                    word_list.append(word)

        return word_list

def binary_mask(mask: str, src: str) -> str:
    """Utility function for using a binary string to mask a source string.

    This function is a basic masking and assumes the length of the mask is equal to the length of the src.
    Letters in the src are added to the result if the relative mask bit is 1. Example: "darn" masked with "1011"
    results in "drn".

    Args:
        mask: The masking string made only of 1s and 0s.
        src: The original word to apply the mask to.

    Returns:
        The subset of letters in the src that have been masked.
    """
    result = ""
    for i in range(len(mask)):
        if mask[i] == "1":
            result += src[i]
    return result