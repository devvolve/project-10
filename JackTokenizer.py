import re

class JackTokenizer:
    SYMBOLS = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'}
    KEYWORDS = {
        'class', 'constructor', 'function', 'method', 'field', 'static', 'var',
        'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this',
        'let', 'do', 'if', 'else', 'while', 'return'
    }
    XML_ESCAPES = {'<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;'}

    def __init__(self, input_file_path):
        with open(input_file_path, 'r') as file:
            self.input = file.read()
        self.tokens = []
        self.current_token = None
        self._tokenize()

    def _remove_comments(self, text):
        text = re.sub(r'//.*', '', text)  # Remove single-line comments
        text = re.sub(r'/\*\*.*?\*/', '', text, flags=re.DOTALL)  # Remove documentation comments
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)  # Remove block comments
        return text

    def _tokenize(self):
        clean_input = self._remove_comments(self.input)
        pattern = re.compile(r'"[^"\n]*"|[{}()\[\].,;+\-*/&|<>=~]|\w+')
        self.tokens = pattern.findall(clean_input)
        self.tokens = [token.strip() for token in self.tokens if token.strip()]

    def has_more_tokens(self):
        return bool(self.tokens)

    def advance(self):
        if self.has_more_tokens():
            self.current_token = self.tokens.pop(0)

    def token_type(self):
        if self.current_token in self.KEYWORDS:
            return 'keyword'
        elif self.current_token in self.SYMBOLS:
            return 'symbol'
        elif self.current_token.isdigit():
            return 'integerConstant'
        elif self.current_token.startswith('"') and self.current_token.endswith('"'):
            return 'stringConstant'
        else:
            return 'identifier'

    def keyword(self):
        return self.current_token

    def symbol(self):
        return self.XML_ESCAPES.get(self.current_token, self.current_token)

    def identifier(self):
        return self.current_token

    def int_val(self):
        return int(self.current_token)

    def string_val(self):
        return self.current_token[1:-1]  # Strip quotes

    def get_token_xml(self):
        token_type = self.token_type()
        if token_type == 'keyword':
            value = self.keyword()
        elif token_type == 'symbol':
            value = self.symbol()
        elif token_type == 'integerConstant':
            value = self.int_val()
        elif token_type == 'stringConstant':
            value = self.string_val()
        else:  # identifier
            value = self.identifier()
        return f"<{token_type}> {value} </{token_type}>"
