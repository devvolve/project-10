import os
import sys
from JackTokenizer import JackTokenizer

def analyze_file(file_path):
    output_path = file_path.replace('.jack', 'T.xml')
    tokenizer = JackTokenizer(file_path)

    with open(output_path, 'w') as out_file:
        out_file.write("<tokens>\n")
        while tokenizer.has_more_tokens():
            tokenizer.advance()
            out_file.write(tokenizer.get_token_xml() + '\n')
        out_file.write("</tokens>\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python JackAnalyzer.py <input_file_or_directory>")
        return

    input_path = sys.argv[1]

    if os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            if filename.endswith('.jack'):
                analyze_file(os.path.join(input_path, filename))
    elif input_path.endswith('.jack'):
        analyze_file(input_path)
    else:
        print("Please provide a valid .jack file or a directory containing .jack files.")

if __name__ == '__main__':
    main()
