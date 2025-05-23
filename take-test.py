"""Take the 100 HEXACO-PI-R test."""
import argparse
import pandas as pd
from model import start_message, end_message, questions100

def ask(questions: dict):
    """TODO: Docstring for ask.

    :questions: TODO
    :returns: TODO

    """
    answers = {}
    i = 1
    while i <= len(questions):
        ans = input(f"{i}) {questions[i]} ")
        if ans == 'b' :
            if i != 1:
                i -= 2
            else:
                print('You are on the first item, cannot go back')
                continue
        else:
            try:
                ans = int(ans)
            except ValueError:
                print('Not an integer, cannot proceed')
                continue
            if not 1 <= ans <= 5:
                print('Number not in range (1-5), cannot proceed')
                continue
        answers[i] = ans
        i += 1
    return answers

def save_as(unindexd_dictionary: dict, filename: str, format: str = 'csv'):
    """TODO: Docstring for save_as_csv.
    :unindexd_dictionary: TODO
    :filename: TODO
    :returns: TODO

    """
    df = pd.DataFrame(unindexd_dictionary, index= [0])
    if format == 'csv':
        df.to_csv(filename)
    elif format == 'json':
        df.to_json(filename)
    elif format == 'string':
        df.to_string(filename)
    # elif format == 'excel':
    #     df.to_excel(filename)
    # elif format == 'dict':
    #     df.to_dict(filename)
    else:
        raise ValueError('Format not recognized')

def main():
    """TODO: Docstring for main.

    """
    parser = argparse.ArgumentParser(
        prog = "python3 take-test.py",
        description = "Take the 100 HEXACO-PI-R test.",
    )
    parser.add_argument("answers_file", help="file to which output answers")
    parser.add_argument("-f", "--format", required=False, choices=['csv', 'json', 'string'], default='csv', help="format of output file")
    args = parser.parse_args()
    answers_file = args.answers_file
    print("answer file :",answers_file)
    format = args.format
    print("Format :",format)
    print(start_message)
    answers = ask(questions100)
    print(end_message)
    save_as(answers, answers_file, format)

if __name__ == "__main__":
    main()
