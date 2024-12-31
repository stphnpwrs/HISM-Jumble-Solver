import pickle
from typing import Optional

class WordList:
    """Class for the list of full potential words to be used in the jumble.

    This class creates a dictionary where each word is put into a list asssociated with a key equivalent to
    the letters of the word arranged in alphabetical order. Organization in this manner increases the memory
    required for dictionary storage (as opposed to a simple organized list of all words) but greatly decreases
    the time to search the words by removing the need to search specific permutations of alphabetical hash.

    Attributes:
        word_list: Dictionary containing a list of all possible words to find in the Jumble.
    """

    def __init__(self, filename: str) -> None:
        """Initializes the instance based on the word list file.

        Args:
          filename: The path to the file containing all possible words.
        """
        try:
            self.word_list = pickle.load(open(filename + "-wordlist.p", "rb"))
        except FileNotFoundError:
            self.word_list = {}
            with open(filename, "r") as f:
                all_lines = f.readlines()
            for i in range(len(all_lines)):
                line = all_lines[i].strip().split()
                for word in line:
                    h = WordList.hash_word(word)
                    try:
                        self.word_list[h].add(word)
                    except KeyError:
                        self.word_list[h] = {word}
            pickle.dump(self.word_list, open(filename + "-wordlist.p", "wb"))

    def is_anagram(self, word: str) -> bool:
        """Determines whether the word can be a true anagram.

        This function returns true if the letters in the word can be rearranged to form an anagram while
        using every letter available in the word.

        Args:
            word: The word to test.

        Returns:
            A boolean if the word can be rearranged to form any word in the original word list.
        """
        return self.get_words(word) is not None

    def is_word(self, character_list: list[str]) -> tuple[bool, str]:
        """Determines whether the word is in the original word list.

        Args:
            character_list: The word as an explicit list with each element being a separate letter.

        Returns:
            A boolean if the word is in the original word list in the exact order given and the word
            combined once again into a single string.
        """
        word = ""
        for i in range(len(character_list) - 1):  # ignore the termination character
            word += character_list[i]
        word_list = self.get_words(word)
        if word_list is not None:
            for w in word_list:
                if word == w.lower():
                    return True, w
        return False, word


    def get_words(self, word: str) -> Optional[list[str]]:
        """Get all words in the original word list that can be formed through any permutation of the word.

        Args:
            word: The set of letters to use to obtain all words in the original word file that can be made.

        Returns:
            The list of words that can be made with all the letters in the 'word' argument.
        """
        h = WordList.hash_word(word)
        words = None
        try:
            words = self.word_list[h]
        except KeyError:
            pass
        return words

    def __str__(self) -> None:
        """Produces string for print methods.

        This function returns a string that is the key-value pairs for the first 50 keys in the word list.
        Used for debugging.
        """
        s = ""
        k = list(self.word_list.keys())
        for i in range(50):
            s += k[i] + "\n"
            s += "\t" + str(self.word_list[k[i]]) + "\n"
        return s

    @staticmethod
    def hash_word(word: str) -> str:
        """Creates a hash from a given word.

        The function simply rearranges the letters in the word in alphabetical order.

        Args:
            word: The set of letters to create a hash from.

        Returns:
            The letters of the word in alphabetical order.
        """
        encoding = [0 for _ in range(26)]
        for c in word:
            if c.isalpha():
                idx = ord(c.lower())-ord('a')
                encoding[idx] += 1
        enc = ""
        for i in range(len(encoding)):
            for j in range(encoding[i]):
                enc += chr(ord('a') + i)
        return enc