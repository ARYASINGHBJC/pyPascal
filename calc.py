# EOF(end-of-file) token is used to indicate that there is no more inputleft for lexical analysis
INTEGER, PLUS, MINUS, PROD, DIV, EOF = 'INTEGER', 'PLUS', 'MINUS', 'PROD', 'DIV', 'EOF'


class Token():
    def __init__(self, type, value):
        # token type -> INTEGER, PLUS, EOF
        self.type = type
        # token value -> 0,1,2...9, '+', None
        self.value = value

    def __str__(self):
        """
        String representation of class instance
            Example:
                Token(INTEGER, 9)
                Token(PLUS, '+')
        """
        return f"Token ({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()

    ###################################
    #              Lexer              #
    ###################################


class Lexer:
    def __init__(self, text):
        # User string input, e.g. "5+ 4", "10-5+22", etc
        self.text = text
        # self.pos is an index for self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance_forward(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip(self):
        """Skips whitespace characters"""
        while self.current_char is not None and self.current_char.isspace():
            self.advance_forward()

    def integer(self):
        """Return a (multidigit) integer consumed from the input"""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance_forward()
        return int(result)

    def get_next_token(self):
        """
            Lexical analyzer (also known as scanner)
            This method is reponsible for breaking a sentence apart 
            into tokens. One taken at a time
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip()
                continue
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            if self.current_char == "+":
                self.advance_forward()
                return Token(PLUS, '+')
            if self.current_char == '-':
                self.advance_forward()
                return Token(MINUS, '-')
            if self.current_char == '*':
                self.advance_forward()
                return Token(PROD, '*')
            if self.current_char == '/':
                self.advance_forward()
                return Token(DIV, '/')
            self.error()
        return Token(EOF, None)

    ###################################
    #       Parser/Interpreter        #
    ###################################


class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid Syntax')

    def process_token(self, token_type):
        # compare the current token type with the passed token type
        # if they match then 'processs' the current token
        # assign the next token to the self.current_token else raise an exception
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """
        Return an INTEGER token value
        factor -> Integer
        """
        token = self.current_token
        self.process_token(INTEGER)
        return token.value

    def expr(self):
        """
          expression -> INTEGER PLUS INTEGER
          expression -> INTEGER MINUS INTEGER
          expression -> INTEGER PROD INTEGER
          expression -> INTEGER DIV INTEGER
        """
        res = self.factor()
        while self.current_token.type in (PLUS, MINUS, PROD, DIV):
            token = self.current_token
            if token.type == PLUS:
                self.process_token(PLUS)
                res += self.factor()
            elif token.type == MINUS:
                self.process_token(MINUS)
                res -= self.factor()
            elif token.type == PROD:
                self.process_token(PROD)
                res *= self.factor()
            elif token.type == DIV:
                self.process_token(DIV)
                res /= self.factor()
        return res


def main():
    while True:
        try:
            user_input = input("Please enter: ")
        except EOFError:
            break
        if not user_input:
            continue
        lexer = Lexer(user_input)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == "__main__":
    main()

"""
->Only single digit integers are allowed
->Only addition is allowed till now
->No whitespace allowed anywhere
"""
