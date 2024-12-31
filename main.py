import argparse
from jumble_solver import BruteForce, HISM

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A solver for Jumble Word Puzzles.")
    parser.add_argument("filename", help="path to the file containing the full list of words to consider")
    parser.add_argument("word", help="jumble set of letters to solve")
    parser.add_argument("training_files", help="any number of files to train the HISM on", nargs=argparse.REMAINDER)

    args = parser.parse_args()

    if len(args.training_files) == 0:
        b  = BruteForce(args.filename)
        full_word_list = b.solve(args.word)
    else:
        h = HISM(args.filename, args.training_files)
        full_word_list = h.solve(args.word)

    for word in full_word_list:
        print(word)