# EOF(end-of-file) token is used to indicate that there is no more inputleft for lexical analysis
INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'


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
        text = self.text
        # if self.pos index past the end of the self.text
        # return EOF token because there is no more input left to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character using self.pos and
        # decide what token to create based on single character

        current_char = text[self.pos]

        # if the character is digit then convert it into an integer
        # create an integer token, increment self.pos to point to the next character
        # and return the integer token

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        self.error()

    def process_token(self, token_type):
        # compare the current token type with the passed token type
        # if they match then 'processs' the current token
        # assign the next token to the self.current_token else raise an exception
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """ expression -> INTEGER PLUS IM=NTEGER"""
        # set current tokem to the first token taken from the input
        self.current_token = self.get_next_token()

        # We except the current token to be a single-digit integer
        left_operand = self.current_token
        self.process_token(INTEGER)

        # we except the current token to be a '+' token
        operator = self.current_token
        self.process_token(PLUS)

        # We except the current token to be a single-digit integer
        right_operator = self.current_token
        self.process_token(INTEGER)

        # after these above call the self.current_token is set to EOF token

        # INTEGER PLUS INTEGER sequence of tokens has been processed
        # method can just now return the result of addition of two number
        res = left_operand.value + right_operator.value
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
