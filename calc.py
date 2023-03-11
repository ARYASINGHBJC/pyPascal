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


class Interpreter:
    def __init__(self, text):
        # User string input, e.g. "5+ 4"
        self.text = text
        # self.pos is an index for self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance_forward(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def whitespace_check(self):
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
                self.whitespace_check()
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

    def process_token(self, token_type):
        # compare the current token type with the passed token type
        # if they match then 'processs' the current token
        # assign the next token to the self.current_token else raise an exception
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """
          expression -> INTEGER PLUS INTEGER
          expression -> INTEGER MINUS INTEGER
          expression -> INTEGER PROD INTEGER
          expression -> INTEGER DIV INTEGER
        """
        # set current tokem to the first token taken from the input
        self.current_token = self.get_next_token()

        # We except the current token to be a single-digit integer
        left_operand = self.current_token
        self.process_token(INTEGER)

        # we except the current token to be a '+' token
        operator = self.current_token
        if operator.type == PLUS:
            self.process_token(PLUS)
        elif operator.type == MINUS:
            self.process_token(MINUS)
        elif operator.type == PROD:
            self.process_token(PROD)
        else:
            self.process_token(DIV)

        # We except the current token to be a single-digit integer
        right_operand = self.current_token
        self.process_token(INTEGER)

        # after these above call the self.current_token is set to EOF token

        # INTEGER OPERAND INTEGER sequence of tokens has been processed
        # method can just now return the result of operation between two integers

        if operator.type == PLUS:
            res = left_operand.value + right_operand.value
        elif operator.type == MINUS:
            res = left_operand.value - right_operand.value
        elif operator.type == PROD:
            res = left_operand.value * right_operand.value
        else:
            if right_operand.value == 0:
                raise ZeroDivisionError
            else:
                res = left_operand.value / right_operand.value
        return res


def main():
    while True:
        try:
            user_input = input("Please enter: ")
        except EOFError:
            break
        if not user_input:
            continue
        interpreter = Interpreter(user_input)
        result = interpreter.expr()
        print(result)


if __name__ == "__main__":
    main()

"""
->Only single digit integers are allowed
->Only addition is allowed till now
->No whitespace allowed anywhere
"""
