##############################################################################################
# This is the compiler for SimpelC | development start: 18.12.2021 | release date: ?         #
##############################################################################################
#                                                                                            #
# - SimpelC is mixture of many C-like programming languages                                  #
# - It's kind of an interpretation of what a C-like programming language could look like     #
# - It's supposed to be an easy to use language with library, namespace, [...] support       #
# - The syntax is also supposed to be clean and easy to read                                 #
# - This language is my first big project that I’m publishing on Git Hub                     #
# - I am trying to improve the performance and usage of this language constantly!            #
#                                                                                            #
# I hope you enjoy my language :)                                                            #
##############################################################################################


from typing import Counter
import string
import os
import numpy


#############################
# - Keywords / Operations - #
#############################

# Variable types
VAR = 'var'  # [variable]
BYT = 'byt'  # [byte]
CHR = 'chr'  # [character]
STR = 'str'  # [string]
INT = 'int'  # [integer]
FLT = 'flt'  # [floating point]
DBL = 'dbl'  # [double]
BOL = 'bol'  # [boolean]
TYP = 'typ'  # [type]

VARTYPE = 'VARIABLE'
VARTYPES = [
    VAR,
    BYT,
    CHR,
    STR,
    INT,
    FLT,
    DBL,
    BOL,
    TYP
]

# Keywords
IF = 'if'
ELIF = 'elif'
ELSE = 'else'
WHILE = 'while'
DO = 'do'
FOR = 'for'
EACH = 'each'
CLASS = 'class'
STRUCT = 'struct'
PUBLIC = 'public'
PRIVATE = 'private'
PROTECTED = 'protected'
CONST = 'const'
STATIC = 'static'
VOID = 'void'
OVERRIDE = 'override'
OPERATION = 'operation'
RETURN = 'return'
CONTINUE = 'continue'
BREAK = 'break'
SIZEOF = 'sizeof'
TYPEOF = 'typeof'
LENGHTOF = 'lenghtof'
NULL = 'null'
FALSE = 'false'
TRUE = 'true'
THIS = 'this'
USING = 'using'
NAMESPACE = 'namespace'

KEYWORD = 'KEYWORD'
IDENTIFIER = 'IDENTIFIER'
KEYWORDS = [
    IF,
    ELIF,
    ELSE,
    WHILE,
    DO,
    FOR,
    EACH,
    CLASS,
    STRUCT,
    PUBLIC,
    PRIVATE,
    PROTECTED,
    CONST,
    STATIC,
    VOID,
    OVERRIDE,
    OPERATION,
    RETURN,
    CONTINUE,
    BREAK,
    SIZEOF,
    TYPEOF,
    LENGHTOF,
    NULL,
    FALSE,
    TRUE,
    THIS,
    USING,
    NAMESPACE
]

# Operations
PLUS = '+'
PLUSEQUALS = '+='
PLUSPLUS = '++'
MINUS = '-'
MINUSEQUALS = '-='
MINUSMINUS = '--'
DIVIDE = '/'
DIVIDEEQUALS = '/='
COMMENT = '//'
MULTIPLY = '*'
MULTIPLYEQUALS = '*='
MODULUS = '%'
POWER = '^'
ISEQUALTO = '?'
EQUALS = '='
NOT = '!'
LESS = '<'
GREATER = '>'
LESSEQUAL = '<='
GREATEREQUAL = '>='
TOCODE = '>>'
QUOTE = '"'
SQUOTE = '\''
DOT = '.'
OR = '|'
AND = '&'
BYTESTART = '$'
COLON = ':'

OPERATOR = 'OPERATOR'

# Metacode keywords
METACODE = '#'
LIB = 'lib'
DEFINE = 'define'
METIF = 'metif'
METELIF = 'metelif'
METELSE = 'metelse'
METENDIF = 'metendif'

METAKEYWORD = 'METAKEYWORD'
METAKEYWORDS = [
    LIB,
    DEFINE,
    METIF,
    METELIF,
    METELSE,
    METENDIF
]

# Extra compiler stuff
LCBRACKET = '{'
RCBRACKET = '}'
LSBRACKET = '['
RSBRACKET = ']'
LBRACKET = '('
RBRACKET = ')'
ENDCOLUMN = ';'
COMMA = ','
EOF = 'endofFile'

LETTERS = string.ascii_letters
DIGITS = '0123456789'
LETGITS = LETTERS + DIGITS
FLOATMIN = 0.0000000000000001

# Error types
TESTERROR = 'TestError'
ILLEGALCHAR = 'IllegalChar'
EXPEXTEDCHAR = 'ExpectedChar'
PARSEERROR = 'ParseError'
SYNTAXERROR = 'SyntaxError'
DIVBYZERO = 'DivisionByZero'
PYTHON_EXCEPTION = 'Python Exception'
# ... (more in the future)


#####################
# - Lexer classes - #
#####################


class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, currChar=None):
        self.idx += 1
        self.col += 1

        if currChar == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


class Token:
    def __init__(self, type, value=None, start=None, end=None):
        self.type = type
        self.value = value
        if start:
            self.start = start.copy()
            self.end = start.copy()
            self.end.advance()
        if end:
            self.end = end

    def matches(self, type, value):
        return self.type == type and self.value == value

    def __repr__(self):
        if self.value:
            return f'[ {self.type}:{self.value} ]'
        return f'[ {self.type} ]'


class Error:
    def __init__(self, message, errorType, line, column, fileName):
        self.message = message
        self.errorType = errorType
        self.line = line
        self.column = column
        self.fileName = fileName

    def throw(self):
        print(
            f'{self.errorType} in {self.fileName} (line: {self.line}, {self.column}):\n\t{self.message}')


##################
# - The lexer - #
##################

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.currChar = None
        self.advance()

    def advance(self):
        self.pos.advance(self.currChar)
        self.currChar = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None

    def genTokens(self):
        tokens = []

        while self.currChar != None:
            if self.currChar in ' \t\n':                # [Space] or [Tab]
                self.advance()
            elif self.currChar in DIGITS:               # 0123456789
                token, error = self.genNum()
                if error:
                    return [], error
                tokens.append(token)
            elif self.currChar in LETTERS:              # abcdef...
                tokens.append(self.genIdentifier())
            elif self.currChar == LESS:                 # < or <=
                tokens.append(self.genLess())
            elif self.currChar == GREATER:              # > or >=
                tokens.append(self.genGreater())
            elif self.currChar == PLUS:                 # + or ++ or +=
                tokens.append(self.genPlus())
            elif self.currChar == MINUS:                # - or -- or -=
                tokens.append(self.genMinus())
            elif self.currChar == DIVIDE:               # / or // ... or /*...*/ or /=
                token = self.genDivide()
                if token:
                    tokens.append(token)
            elif self.currChar == MULTIPLY:             # * or *=
                tokens.append(self.genMultiply())
            elif self.currChar == METACODE:             # (metacode-expression)
                token, error = self.genMetaCode()
                if error:
                    return [], error
                tokens.append(token)
            elif self.currChar == QUOTE:                # "Hello World."
                tokens.append(self.genString())
            elif self.currChar == SQUOTE:               # 'a'
                token, error = self.genChar()
                if error:
                    return [], error
                tokens.append(token)
            elif self.currChar == BYTESTART:            # $0xFF
                token, error = self.genByte()
                if error:
                    return [], error
                tokens.append(token)
            elif self.currChar == ENDCOLUMN:            # ;
                tokens.append(Token(ENDCOLUMN, start=self.pos))
                self.advance()
            elif self.currChar == LCBRACKET:            # {
                tokens.append(Token(LCBRACKET, start=self.pos))
                self.advance()
            elif self.currChar == RCBRACKET:            # }
                tokens.append(Token(RCBRACKET, start=self.pos))
                self.advance()
            elif self.currChar == LSBRACKET:            # [
                tokens.append(Token(LSBRACKET, start=self.pos))
                self.advance()
            elif self.currChar == RSBRACKET:            # ]
                tokens.append(Token(RSBRACKET, start=self.pos))
                self.advance()
            elif self.currChar == LBRACKET:             # (
                tokens.append(Token(LBRACKET, start=self.pos))
                self.advance()
            elif self.currChar == RBRACKET:             # )
                tokens.append(Token(RBRACKET, start=self.pos))
                self.advance()
            elif self.currChar == POWER:                # ^
                tokens.append(Token(POWER, start=self.pos))
                self.advance()
            elif self.currChar == EQUALS:               # =
                tokens.append(Token(EQUALS, start=self.pos))
                self.advance()
            elif self.currChar == ISEQUALTO:            # ?
                tokens.append(Token(ISEQUALTO, start=self.pos))
                self.advance()
            elif self.currChar == NOT:                  # !
                tokens.append(Token(NOT, start=self.pos))
                self.advance()
            elif self.currChar == COMMA:                # ,
                tokens.append(Token(COMMA, start=self.pos))
                self.advance()
            elif self.currChar == DOT:                  # .
                tokens.append(Token(DOT, start=self.pos))
                self.advance()
            elif self.currChar == COLON:                # :
                tokens.append(Token(COLON, start=self.pos))
                self.advance()
            elif self.currChar == AND:                  # &
                tokens.append(Token(AND, start=self.pos))
                self.advance()
            elif self.currChar == OR:                   # |
                tokens.append(Token(OR, start=self.pos))
                self.advance()
            else:                                       # Error if nothing is true
                line = self.pos.ln
                column = self.pos.col
                self.advance()
                return [], Error(f'\'{self.currChar}\'', SYNTAXERROR,  line, column, self.pos.fn)

        # Appending an End-Of-File token.
        # Returning the list of all tokens with no error message.

        tokens.append(Token(EOF, start=self.pos))
        return tokens, None

    def genNum(self):
        num = ''
        dotCount = 0
        eCount = 0
        minusCount = 0
        start = self.pos.copy()

        while self.currChar != None and self.currChar in DIGITS + DOT + 'e-':
            if self.currChar == DOT:
                if dotCount == 1:
                    return None, Error("'.'", ILLEGALCHAR, self.pos.ln, self.pos.col, self.fn)
                dotCount += 1
                num += DOT
            elif self.currChar == 'e':
                if eCount == 1:
                    return None, Error("'ee' is not allowed inside a number!", ILLEGALCHAR, self.pos.ln, self.pos.col, self.fn)
                num += 'e'
                eCount += 1
                self.advance()

                if self.currChar == MINUS:
                    if minusCount == 1:
                        return None, Error("Two '-' is not allowed inside a number!", ILLEGALCHAR, self.pos.ln, self.pos.col, self.fn)
                    num += MINUS
                    minusCount += 1
                else:
                    return None, Error("Expected '-'", ILLEGALCHAR, self.pos.ln, self.pos.col, self.fn)
            elif self.currChar == MINUS:
                if minusCount == 1:
                    return None, Error("Two '-' is not allowed inside a number!", ILLEGALCHAR, self.pos.ln, self.pos.col, self.fn)
                else:
                    break
            else:
                num += self.currChar
            self.advance()

        if dotCount == 0 and eCount == 0:
            return Token(INT, int(num), start, self.pos), None
        else:
            Num = numpy.double(num)
            type = DBL if Num < FLOATMIN else FLT
            if type == DBL:
                return Token(DBL, numpy.double(num), start, self.pos), None
            if type == FLT:
                return Token(FLT, float(num), start, self.pos), None

    def genIdentifier(self):
        value = ''
        start = self.pos.copy()

        while self.currChar != None and self.currChar in LETGITS + "_":
            value += self.currChar
            self.advance()

        type = KEYWORD if value in KEYWORDS else IDENTIFIER
        type = VARTYPE if value in VARTYPES else type
        type = BOL if value in (TRUE, FALSE) else type
        return Token(type, value, start, self.pos)

    def genLess(self):
        type = LESS
        value = self.currChar
        start = self.pos.copy()

        self.advance()
        nextChar = self.currChar
        if nextChar == EQUALS:
            type = LESSEQUAL
            value += nextChar
            self.advance()
        return Token(type, value, start, self.pos)

    def genGreater(self):
        type = GREATER
        value = self.currChar
        start = self.pos.copy()

        self.advance()
        nextChar = self.currChar
        if nextChar == EQUALS:
            type = GREATEREQUAL
            value += nextChar
            self.advance()
        elif nextChar == GREATER:
            type = TOCODE
            value += nextChar
            self.advance()
        return Token(type, value, start, self.pos)

    def genPlus(self):
        type = PLUS
        value = self.currChar
        start = self.pos.copy()

        self.advance()
        nextChar = self.currChar
        if nextChar == EQUALS:
            type = PLUSEQUALS
            value += nextChar
            self.advance()
        elif nextChar == PLUS:
            type = PLUSPLUS
            value += nextChar
            self.advance()
        return Token(type, value, start, self.pos)

    def genMinus(self):
        type = MINUS
        value = self.currChar
        start = self.pos.copy()

        self.advance()
        nextChar = self.currChar
        if nextChar == EQUALS:
            type = MINUSEQUALS
            value += nextChar
            self.advance()
        elif nextChar == MINUS:
            type = MINUSMINUS
            value += nextChar
            self.advance()
        return Token(type, value, start, self.pos)

    def genDivide(self):
        type = DIVIDE
        value = self.currChar
        start = self.pos.copy()

        self.advance()
        nextChar = self.currChar
        if nextChar == EQUALS:
            type = DIVIDEEQUALS
            value += nextChar
            self.advance()
        elif nextChar == DIVIDE:
            type = COMMENT
            value += nextChar

            self.advance()
            while self.currChar != '\n':
                if self.currChar == None:
                    break
                self.advance()
            self.advance()
            return None
        elif nextChar == MULTIPLY:
            type = COMMENT
            value += nextChar

            self.advance()
            while self.currChar != None:
                if self.currChar == MULTIPLY:
                    self.advance()
                    if self.currChar == DIVIDE:
                        break
                self.advance()
            self.advance()
            return None

        return Token(type, value, start, self.pos)

    def genMultiply(self):
        type = MULTIPLY
        value = self.currChar
        start = self.pos.copy()

        self.advance()
        nextChar = self.currChar
        if nextChar == EQUALS:
            type = MULTIPLYEQUALS
            value += nextChar
            self.advance()
        return Token(type, value, start, self.pos)

    def genMetaCode(self):
        self.advance()
        value = ''
        start = self.pos.copy()

        while self.currChar != None and self.currChar in LETTERS:
            value += self.currChar
            self.advance()

        type = METAKEYWORD if value in METAKEYWORDS else None
        if type == None:
            return None, Error("Expected 'metif', 'define', ...", ILLEGALCHAR, self.pos.ln, self.pos.col, self.fn)
        return Token(type, value, start, self.pos), None

    def genString(self):
        self.advance()
        value = ''
        start = self.pos.copy()

        while self.currChar != QUOTE:
            value += self.currChar
            self.advance()

        self.advance()
        return Token(STR, value, start, self.pos)

    def genChar(self):
        self.advance()
        value = self.currChar
        start = self.pos.copy()

        self.advance()
        if self.currChar != SQUOTE:
            return None, Error('Expected \'', ILLEGALCHAR, self.pos.ln, self.pos.col, self.fn)
        self.advance()

        return Token(CHR, value, start, self.pos), None

    def genByte(self):
        self.advance()
        value = ''
        start = self.pos.copy()

        while self.currChar != None and self.currChar in LETGITS:
            value += self.currChar
            self.advance()

        type = BYT if all(
            c in 'xX' + string.hexdigits for c in value) else None
        if not type:
            return None, Error('Wrong byte format!', SYNTAXERROR, self.pos.ln, self.pos.col, self.fn)
        return Token(type, value, start, self.pos), None

######################
# - Parser classes - #
######################

# Normal nodes


class MasterScript:
    def __init__(self, libs):
        self.libs = libs

    def __repr__(self):
        return 'MASTERSCRIPT'


class Import:
    def __init__(self, lib):
        self.lib = lib

    def __repr__(self):
        return f'Import Node : [ {self.lib} ]'


# If there are no namespaces everything will be put into a 'virtual' namespace
# which contains every class etc. of the script!
# Variables of another script can only be accessed as long as they are public / not a constant / and as long
# as the script has the other script's library imported!
class Script:
    def __init__(self, name, imports, lib, namespaces, global_variables, global_classes, global_structs):
        self.name = name
        self.imports = imports
        self.lib = lib
        self.namespaces = namespaces
        self.global_variables = global_variables
        self.global_classes = global_classes
        self.global_structs = global_structs

    def __repr__(self):
        return f'Script Node : [ {self.name} | {self.imports} | {self.lib} | {self.namespaces} | {self.global_variables} | {self.global_classes} | {self.global_structs} ]'


class Lib:
    def __init__(self, scripts, name):
        self.scripts = scripts
        self.name = name

    def __repr__(self):
        return f'Lib Node : [ {self.name} | {self.scripts} ]'


# Cannot have variables


class Namespace:
    def __init__(self, name, classes, structs):
        self.name = name
        self.classes = classes
        self.structs = structs

    def __repr__(self):
        return f'Namespace Node : [ {self.name} | {self.classes} | {self.structs} ]'


class Using:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Using Node : [ {self.name} ]'


class Variable:
    def __init__(self, lib, namespace, classNode, public, static, const, type, name, value):
        self.lib = lib
        self.namespace = namespace
        self.classNode = classNode
        self.public = public
        self.static = static
        self.const = const
        self.type = type
        self.name = name
        self.value = value

        self.start = self.type.start
        self.end = self.value.end if self.value else self.name.end

    def __repr__(self):
        condition = 'static' if self.static else ''
        condition = 'const' if self.const else condition
        return f'Variable Node : [ {self.lib} | {self.namespace} | {self.classNode} | {self.public} | {condition} | {self.type} | {self.name} | {self.value} ]'


class VarAccess:
    def __init__(self, classNode, varName, start, end):
        self.classNode = classNode
        self.varName = varName

        self.start = start
        self.end = end

    def __repr__(self):
        return f'VarAccess Node : [ {self.classNode} | {self.varName} ]'


class List:
    def __init__(self, classNode, public, static, const, type, name, elements, start, end):
        self.classNode = classNode
        self.public = public
        self.static = static
        self.const = const
        self.type = type
        self.name = name
        self.elements = elements

        self.start = start
        self.end = end

    def __repr__(self):
        condition = 'static' if self.static != None else ''
        condition = 'const' if self.const != None else condition
        return f'List Node : [ {self.classNode} | {self.public} | {condition} | {self.type} | {self.name} | {self.elements} ]'


class Identifier:
    def __init__(self, type, name):
        self.type = type
        self.name = name

        self.start = self.name.start
        self.end = self.name.end

    def __repr__(self):
        return f'Idenfifier Node : [ {self.name} ]'


class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

        self.start = self.left.start
        self.end = self.right.end

    def __repr__(self):
        return f'Binary Op Node : [ {self.left} {self.op} {self.right} ]'


class UnaryNode:
    def __init__(self, op, node):
        self.op = op
        self.node = node

        self.start = self.op.start
        self.end = self.node.end

    def __repr__(self):
        return f'Unary Node : [ {self.op} {self.node} ]'


class If:
    def __init__(self, functionNode, variables, cases, elseCase):
        self.functionNode = functionNode
        self.variables = variables
        self.cases = cases
        self.elseCase = elseCase

        self.start = self.cases.start
        self.end = self.elseCase.end if self.elseCase else self.cases.end

    def __repr__(self):
        return f'If Node : [ {self.functionNode} | {self.variables} | {self.cases} | {self.elseCase} ]'


class For:
    def __init__(self, functionNode, variables, variable, condition, steps, body):
        self.functionNode = functionNode
        self.variables = variables
        self.variable = variable
        self.condition = condition
        self.steps = steps
        self.body = body

        self.start = self.variable.start
        self.end = self.body.end

    def __repr__(self):
        return f'For Node : [ {self.functionNode} | {self.variables} | {self.variable} | {self.condition} | {self.steps} | {self.body} ]'

# (Maybe)


class SimpleFor:
    pass


class While:
    def __init__(self, functionNode, variables, condition, body):
        self.functionNode = functionNode
        self.variables = variables
        self.condition = condition
        self.body = body

        self.start = self.condition.start
        self.end = self.body.end

    def __repr__(self):
        return f'While Node : [ {self.functionNode} | {self.variables} | {self.condition} | {self.body} ]'


# A struct has to have at least ONE constrctor!
class Struct:
    def __init__(self, script, namespace, variables, name, constructors):
        self.script = script
        self.namespace = namespace
        self.variables = variables
        self.name = name
        self.constructors = constructors

        self.start = self.name.start
        self.end = self.constructors[0].end

    def __repr__(self):
        return f'Class Node : [ {self.namespace} | {self.variables} | {self.name} | {self.constructors} ]'

# Doesn't have to have a cunstructor. Variables can be changeg by accessing the Class like this:
#
# SomeClass test = SomeClass();
# test.a = 1;
# Allways has to have private or public keyword!!!!


class Class:
    def __init__(self, script, namespace, externNameSpaces, variables, public, static, name, constructors, body):
        self.script = script
        self.namespace = namespace
        self.externNameSpaces = externNameSpaces
        self.variables = variables
        self.public = public
        self.static = static
        self.name = name
        self.constructors = constructors
        self.body = body

        self.start = self.name.start
        self.end = self.body.end

    def __repr__(self):
        return f'Class Node : [ {self.namespace} | {self.externNameSpaces} | {self.variables} | {self.public} | {self.static} | {self.name} | {self.constructors} | {self.body} ]'

# It can only have the returntype and arguments of the original function.
# The overriden function will only be overriden for the script the override function is being called


class Override:
    def __init__(self, classNode, functionNode, variables, returnType, name, args, body):
        self.classNode = classNode
        self.functionNode = functionNode
        self.variables = variables
        self.returnType = returnType
        self.name = name
        self.args = args
        self.body = body

        self.start = self.returnType.start
        self.end = self.body.end

    def __repr__(self):
        return f'Function Node : [ {self.classNode} | {self.functionNode} | {self.variables} | {self.returnType} | {self.name} | {self.args} | {self.body} ]'


class Function:
    def __init__(self, classNode, variables, constructor, public, static, protected, returnType, name, args, body):
        self.classNode = classNode
        self.variables = variables
        self.constructor = constructor
        self.public = public
        self.static = static
        self.protected = protected
        self.returnType = returnType
        self.name = name
        self.args = args
        self.body = body

        self.start = self.returnType.start
        self.end = self.body.end

    def __repr__(self):
        return f'Function Node : [ {self.classNode} | {self.variables} | {self.constructor} | {self.public} | {self.static} | {self.protected} | {self.returnType} | {self.name} | {self.args} | {self.body} ]'


class CallFunction:
    def __init__(self, classNode, name, args):
        self.classNode = classNode
        self.name = name
        self.args = args

        self.start = self.name.start
        self.end = self.args.end

    def __repr__(self):
        return f'Call-Function Node : [ {self.classNode} | {self.name} ({self.args}) ]'


class CallClass:
    def __init__(self, name, args):
        self.name = name
        self.args = args

        self.start = self.name.start
        self.end = self.args.end

    def __repr__(self):
        return f'Call-Class Node : [ {self.name} ({self.args}) ]'


class Return:
    def __init__(self, functionNode, returnTok):
        self.functionNode = functionNode
        self.returnType = returnTok.type
        self.returnValue = returnTok.value

        self.start = returnTok.start
        self.end = returnTok.end

    def __repr__(self):
        return f'Return Node : [ {self.functionNode} | {self.returnType} | {self.returnValue} ]'


class Continue:
    def __init__(self, loopNode, start, end):
        self.loopNode = loopNode

        self.start = start
        self.end = end

    def __repr__(self):
        return f'Continue Node : [ {self.loopNode} ]'


class Break:
    def __init__(self, loopNode, start, end):
        self.loopNode = loopNode

        self.start = start
        self.end = end

    def __repr__(self):
        return f'Break Node : [ {self.loopNode} ]'


class MetaCode:
    def __init__(self, type, identifier, metVarValue=None):
        self.type = type
        self.value = identifier.value
        self.metVarValue = metVarValue

        self.start = identifier.start
        self.end = identifier.end

    def __repr__(self):
        return f'MetaCode Node : [ {self.type} : {self.value} ]'

# Variable nodes


class Number:
    def __init__(self, type, value):
        self.type = type
        self.value = value

        self.start = self.value.start
        self.end = self.value.end

    def __repr__(self):
        return f'Number Node : [ {self.type} : {self.value} ]'


class String:
    def __init__(self, type, value):
        self.type = type
        self.value = value

        self.start = self.type.start
        self.end = self.value.end

    def __repr__(self):
        return f'String Node: [ {self.type} : {self.value} ]'


class Bool:
    def __init__(self, type, value):
        self.type = type
        self.value = value

        self.start = self.type.start
        self.end = self.value.end

    def __repr__(self):
        return f'Bool Node: [ {self.type} : {self.value} ]'


class Type:
    def __init__(self, type, value):
        self.type = type
        self.value = value

        self.start = self.type.start
        self.end = self.value.end

    def __repr__(self):
        return f'Type Node: [ {self.type} : {self.value} ]'


class Var:
    def __init__(self, type, value):
        self.type = type
        self.value = value

        self.start = self.type.start
        self.end = self.value.end

    def __repr__(self):
        return f'Var Node: [ {self.type} : {self.value} ]'


class Byte:
    def __init__(self, type, value):
        self.type = type
        self.value = value

        self.start = self.type.start
        self.end = self.value.end

    def __repr__(self):
        return f'Byte Node: [ {self.type} : {self.value} ]'


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.lastAdvCount = 0
        self.advanceCount = 0
        self.reverseCount = 0

    def registerAdvance(self):
        self.lastAdvCount = 1
        self.advanceCount += 1

    def register(self, res):
        self.lastAdvCount = res.advanceCount
        self.advanceCount += res.advanceCount
        if res.error:
            self.error = res.error
        return res.node

    def tryRegister(self, res):
        if res.error:
            self.reverseCount = res.advanceCount
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advanceCount == 0:
            self.error = error
        return self

##################
# - The parser - #
##################


masterscript = MasterScript([])
metacode = []


class Parser:
    def __init__(self, scriptName, tokens):
        self.tokens = tokens
        self.scriptName = scriptName
        self.idx = -1
        self.advance()

    def reverse(self, amount=1):
        self.idx -= amount
        self.updateTok()
        return self.currTok

    def updateTok(self):
        if self.idx >= 0 and self.idx < len(self.tokens):
            self.currTok = self.tokens[self.idx]

    def advance(self):
        self.idx += 1
        self.updateTok()
        return self.currTok

    def parse(self):
        res = self.lib()
        if not res.error and self.currTok.type != EOF:
            return res.failure(
                Error(
                    "Expected valid expression...", PARSEERROR,
                    self.currTok.start, self.currTok.end, self.scriptName))

        masterscript.libs.append(res.node)
        return res

    def lib(self):
        res = ParseResult()

        script = res.register(self.script())
        if res.error:
            return res

        return res.success(Lib(script, script.lib))

    def script(self):
        res = ParseResult()
        imports = []
        lib = None
        namespaces = []
        global_variables = []
        global_classes = []
        global_structs = []

        moreStatements = True
        while moreStatements:
            if self.currTok.type == METAKEYWORD:
                metaNode = res.register(self.metacode())
                if res.error:
                    return res

                if metaNode.type == LIB:
                    lib = metaNode
                else:
                    metacode.append(metaNode)
            elif self.currTok.type == KEYWORD:
                statements = res.register(self.expr())
                if res.error:
                    return res

                for node in statements:
                    if isinstance(node, MetaCode):
                        metacode.append(node)
                    elif isinstance(node, Namespace):
                        namespaces.append(node)
                    elif isinstance(node, Variable):
                        global_variables.append(node)
                    elif isinstance(node, Class):
                        global_classes.append(node)
                    elif isinstance(node, Struct):
                        global_structs.append(node)
            elif self.currTok.type == EOF:
                break

        # Final touch to metacode
        for node in metacode:
            if node.type == DEFINE:
                global_variables.append(
                    Variable(lib, None, None, True, False, True, node.value.type, node.value, node.metVarValue))

        return res.success(Script(self.scriptName, imports, lib, namespaces, global_variables))

    def metacode(self):
        res = ParseResult()
        node = None

        if self.currTok.value == LIB:
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == EQUALS:
                return res.failure(
                    Error(
                        "Expected '='.", SYNTAXERROR,
                        self.currTok.start, self.currTok.end, self.scriptName))

            res.registerAdvance()
            self.advance()

            if not self.currTok.type == STR:
                return res.failure(
                    Error(
                        "Expected string.", SYNTAXERROR,
                        self.currTok.start, self.currTok.end, self.scriptName))

            libName = self.currTok
            node = MetaCode(LIB, libName)
        elif self.currTok.value == DEFINE:
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == IDENTIFIER:
                return res.failure(
                    Error(
                        "Expected identifier.", SYNTAXERROR,
                        self.currTok.start, self.currTok.end, self.scriptName))

            name = self.currTok
            res.registerAdvance()
            self.advance()

            if not self.currTok.type in VARTYPES:
                return res.failure(
                    Error(
                        "Expected value.", SYNTAXERROR,
                        self.currTok.start, self.currTok.end, self.scriptName))

            value = self.currTok

            node = MetaCode(DEFINE, name, value)
        elif self.currTok.value == METIF:
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == IDENTIFIER:
                return res.failure(
                    Error(
                        "Expected identifier.", SYNTAXERROR,
                        self.currTok.start, self.currTok.end, self.scriptName))

            node = MetaCode(METIF, self.currTok)
        elif self.currTok.value == METELIF:
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == IDENTIFIER:
                return res.failure(
                    Error(
                        "Expected identifier.", SYNTAXERROR,
                        self.currTok.start, self.currTok.end, self.scriptName))

            node = MetaCode(METELIF, self.currTok)
        elif self.currTok.value == METELSE:
            node = MetaCode(METELIF, self.currTok)
        elif self.currTok.value == METENDIF:
            node = MetaCode(METENDIF, self.currTok)

        res.registerAdvance()
        self.advance()

        metacode.append(node)
        return res.success(node)
        # return res.success(node)

    def namespace(self):
        res = ParseResult()
        classes = []
        structs = []

        res.registerAdvance()
        self.advance()

        if not self.currTok.type == IDENTIFIER:
            return res.failure(
                Error(
                    "Expected identifier.", SYNTAXERROR,
                    self.currTok.start, self.currTok.end, self.scriptName))

        name = self.currTok
        res.registerAdvance()
        self.advance()

        if not self.currTok.type == LCBRACKET:
            return res.failure(
                Error(
                    "Expected '{'.", SYNTAXERROR,
                    self.currTok.start, self.currTok.end, self.scriptName))

        # TODO: When a new expression was found asign the name of the namespace!

        while True:
            res.registerAdvance()
            self.advance()

            expr = res.register(self.expr())
            if not expr:
                break
            if res.error:
                return res

            if isinstance(expr, Variable):
                return res.failure(
                    Error(
                        "Cannot define variables inside a namespace.", SYNTAXERROR,
                        self.currTok.start, self.currTok.end, self.scriptName))
            elif isinstance(expr, Class):
                expr.namespace = name
                classes.append(expr)
            elif isinstance(expr, Struct):
                expr.namespace = name
                structs.append(expr)

        res.registerAdvance()
        self.advance()

        if not self.currTok.type == RCBRACKET:
            return res.failure(
                Error(
                    "Expected '}'.", SYNTAXERROR,
                    self.currTok.start, self.currTok.end, self.scriptName))

        return res.success(Namespace(name, classes, structs))

    def ClassOrVarOrFunc(self):
        res = ParseResult()

        public = True if self.currTok.value == PUBLIC else False
        static = False
        const = False
        protected = False

        res.registerAdvance()
        self.advance()

        while self.currTok in (STATIC, CONST, PROTECTED):
            if self.currTok.value == STATIC:
                static = True
                res.registerAdvance()
                self.advance()
            elif self.currTok.value == CONST:
                const = True
                res.registerAdvance()
                self.advance()
            elif self.currTok.value == PROTECTED:
                protected = True
                res.registerAdvance()
                self.advance()

        if self.currTok.type == KEYWORD:
            if self.currTok.value == CLASS:
                node = res.register(self._class())
                if res.error:
                    return res

                node.public = public
                node.static = static
                return res.success(node)
            elif self.currTok.value in VARTYPES + VOID:
                node = res.register(self.function())
                if res.error:
                    return res

                node.public = public
                node.protected = protected
                node.static = static
                node.const = const
                return res.success(node)
        elif self.currTok.type in VARTYPES:
            node = res.register(self.defVar())
            if res.error:
                return res

            node.public = public
            node.static = static
            node.const = const
            return res.success(node)
        elif self.currTok.type == IDENTIFIER:
            pass  # Constructor or VarAccess or FuncCall

        return res.failure(
                Error(
                    "Expected valid class, variable or function...", PARSEERROR,
                    self.currTok.start, self.currTok.end, self.scriptName))
        

    def _class(self):
        res = ParseResult()

        functions = []
        variables = []
        constructors = []

        res.registerAdvance()
        self.advance()

        if not self.currTok.type == IDENTIFIER:
            return res.failure(
                Error(
                    "Expected indentifier.", SYNTAXERROR,
                    self.currTok.start, self.currTok.end, self.scriptName))

        name = self.currTok
        res.registerAdvance()
        self.advance()

        if not self.currTok.type == LCBRACKET:
            return res.failure(
                Error(
                    "Expected '{'", SYNTAXERROR,
                    self.currTok.start, self.currTok.end, self.scriptName))

        externNameSpaces = res.register(self.usings())

        while True:
            node = res.tryRegister(self.expr())
            if not node:
                self.reverse(res.reverseCount)
                break
            if res.error:
                return res

            node.classNode = name
            if isinstance(node, Class):
                return res.failure(
                    Error(
                        "It is not possible to define a class inside a class!", PARSEERROR,
                        self.currTok.start, self.currTok.end, self.scriptName))
            elif isinstance(node, Variable):
                variables.append(node)
            elif isinstance(node, Function):
                functions.append(node)

            res.registerAdvance()
            self.advance()

        if not self.currTok.type == RCBRACKET:
            return res.failure(
                Error(
                    "Expected '}'", SYNTAXERROR,
                    self.currTok.start, self.currTok.end, self.scriptName))

        return res.success(Class(self.scriptName, None, externNameSpaces, variables, False, False, name, constructors, functions))

    def usings(self):
        res = ParseResult()

        usings = []
        if self.currTok.value == USING:
            while True:

                if not self.currTok.value == USING:
                    break

                res.registerAdvance()
                self.advance()

                if not self.currTok.type == IDENTIFIER:
                    return res.failure(
                        Error(
                            "Expected indentifier.", SYNTAXERROR,
                            self.currTok.start, self.currTok.end, self.scriptName))

                name = self.currTok.value
                usings.append(Using(name))

                res.registerAdvance()
                self.advance()

        return res.success(usings)

    def Constructor(self):
        pass

    def function(self):
        res = ParseResult()

        args = []
        body = []
        variables = []

        returnType = self.currTok
        res.registerAdvance()
        self.advance()

        if not self.currTok.type == IDENTIFIER:
            return res.failure(
                Error(
                    "Expected identifier.", SYNTAXERROR,
                    self.currTok.start, self.currTok.end, self.scriptName))

        name = self.currTok
        res.registerAdvance()
        self.advance()

        if not self.currTok.type == LBRACKET:
            return res.failure(
                Error(
                    "Expected '('.", SYNTAXERROR,
                    self.currTok.start, self.currTok.end, self.scriptName))

        res.registerAdvance()
        self.advance()

        # Get parameters
        moreArgs = True
        while moreArgs:
            if not self.currTok.type == VARTYPE:
                return res.failure(
                    Error(
                        "Expected variable type.", SYNTAXERROR,
                        self.currTok.start, self.currTok.end, self.scriptName))

            type = self.currTok
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == IDENTIFIER:
                return res.failure(
                    Error(
                        "Expected identifier.", SYNTAXERROR,
                        self.currTok.start, self.currTok.end, self.scriptName))

            argName = self.currTok
            res.registerAdvance()
            self.advance()

            args.append(Variable(None, None, None, False,
                        False, True, type, argName, None))

            if self.currTok.type == RBRACKET:
                moreArgs = False
            res.registerAdvance()
            self.advance()

        if not self.currTok.type == LSBRACKET:
            return res.failure(
                Error(
                    "Expected '{'.", SYNTAXERROR,
                    self.currTok.start, self.currTok.end, self.scriptName))

        # Build Body
        while True:
            res.registerAdvance()
            self.advance()

            statement = res.tryRegister(self.statement())
            if not statement:
                self.reverse(res.reverseCount)
                break
            if res.error:
                return res

            if isinstance(statement, Return):
                statement.functionNode = name
                body.append(statement)
            elif isinstance(statement, Variable):
                if statement.static or statement.const:
                    return res.failure(
                        Error(
                            "'public', 'static' and 'const' are not allowed in a function.", SYNTAXERROR,
                            self.currTok.start, self.currTok.end, self.scriptName))
                else:
                    variables.append(statement)
            elif isinstance(statement, Class) or isinstance(statement, Function):
                return res.failure(
                    Error(
                        "Functions and classes cannot be defined inside a function.", SYNTAXERROR,
                        self.currTok.start, self.currTok.end, self.scriptName))
            elif isinstance(statement, If) or isinstance(statement, For) or isinstance(statement, While):
                statement.functionNode = name

        if not self.currTok.type == RCBRACKET:
            return res.failure(
                Error(
                    "Expected '}'.", SYNTAXERROR,
                    self.currTok.start, self.currTok.end, self.scriptName))

        return res.success(Function(None, variables, False, False, False, False, returnType, name, args, body))

    def statement(self):
        res = ParseResult()

        statement = None
        if self.currTok.value == WHILE:
            pass
        elif self.currTok.value == FOR:
            pass
        elif self.currTok.value == IF:
            pass
        elif self.currTok.value == RETURN:
            res.registerAdvance()
            self.advance()

            returnTok = res.register(self.expr())
            if res.error:
                return res

            res.registerAdvance()
            self.advance()
            if not self.currTok.type == ENDCOLUMN:
                return res.failure(
                    Error(
                        "Expected ';'.", SYNTAXERROR,
                        self.currTok.start, self.currTok.end, self.scriptName))

            statement = Return(None, returnTok)
        elif self.currTok.value == CONTINUE:
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == ENDCOLUMN:
                return res.failure(
                    Error(
                        "Expected ';'.", SYNTAXERROR,
                        self.currTok.start, self.currTok.end, self.scriptName))

            return res.success(Continue(None, self.currTok.start, self.currTok.end))
        elif self.currTok.value == BREAK:
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == ENDCOLUMN:
                return res.failure(
                    Error(
                        "Expected ';'.", SYNTAXERROR,
                        self.currTok.start, self.currTok.end, self.scriptName))

            return res.success(Break(None, self.currTok.start, self.currTok.end))
        elif self.currTok.type == IDENTIFIER:
            pass  # CallFunc or varaccess
        else:
            node = res.register(self.ClassOrVarOrFunc())
            if res.error:
                return res
            statement = node

        return res.success(statement)

    def defVar(self):
        res = ParseResult()

        type = self.currTok.value
        res.registerAdvance()
        self.advance()

        if not self.currTok.type == IDENTIFIER:
            return res.failure(
                Error(
                    "Expected identifier.", SYNTAXERROR,
                    self.currTok.start, self.currTok.end, self.scriptName))

        name = self.currTok.value
        res.registerAdvance()
        self.advance()

        if not self.currTok.type == EQUALS:
            return res.failure(
                Error(
                    "Expected '='.", SYNTAXERROR,
                    self.currTok.start, self.currTok.end, self.scriptName))

        value = res.register(self.expr())
        if res.error:
            return res

        res.registerAdvance()
        self.advance()

        if not self.currTok.type == ENDCOLUMN:
            return res.failure(
                Error(
                    "Expected ';'.", SYNTAXERROR,
                    self.currTok.start, self.currTok.end, self.scriptName))

        return res.success(Variable(None, None, None, False, False, False, type, name, value))

    def atom(self):
        res = ParseResult()
        tok = self.currTok

        if tok.type in (INT, FLT, DBL):
            res.registerAdvance()
            self.advance()
            return res.success(Number(tok.type, tok))
        elif tok.type == IDENTIFIER:
            res.registerAdvance()
            self.advance()
            return res.success(VarAccess(None, tok, tok.start, tok.end))
        elif tok.type == LBRACKET:
            res.registerAdvance()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.currTok.type == RBRACKET:
                res.registerAdvance()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(
                    Error(
                        "Expected ')'", SyntaxError,
                        self.currTok.start, self.currTok.end, self.scriptName))
        elif tok.type == KEYWORD:
            node = res.register(self.expr())
            if res.error:
                return res

            return res.success(node)

        return res.failure(
            Error(
                "Expected number, identifier, '+', '-' or '('", SyntaxError,
                self.currTok.start, self.currTok.end, self.scriptName))

    def power(self):
        return self.bin_op(self.atom, POWER, self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.currTok

        if tok.type in (PLUS, MINUS):
            res.registerAdvance()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryNode(tok, factor))

        return self.power()

    def term(self):
        return self.bin_op(self.factor, (MULTIPLY, DIVIDE))

    def expr(self):
        res = ParseResult()

        if self.currTok.type == KEYWORD:
            node = res.register(self.ClassOrVarOrFunc())
            if res.error:
                return res

            return res.success(node)
        elif self.currTok.value == NAMESPACE:
            node = res.register(self.namespace())
            if res.error:
                return res

            return res.success(node)
        elif self.currTok.value in (PUBLIC, PRIVATE, CLASS):
            node = res.register(self.ClassOrVarOrFunc())
            if res.error:
                return res

            return res.success(node)
        elif self.currTok.value == STRUCT:
            pass
        elif self.currTok.type == METAKEYWORD:
            metaNode = res.register(self.metacode())
            if res.error:
                return res

            return res.success(metaNode)

        node = res.register(self.bin_op(self.term, (PLUS, MINUS)))

        if res.error:
            return res.failure(
                Error(
                    "Expected variable, identifier, '+', '-' or '('", SyntaxError,
                    self.currTok.start, self.currTok.end, self.scriptName))

        return res.success(node)

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error:
            return res

        while self.currTok.type in ops:
            op_tok = self.currTok
            res.registerAdvance()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)


####################
# - Run Function - #
####################


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.genTokens()
    if error:
        return None, error

    parser = Parser(fn, tokens)
    ast = parser.parse()

    return ast.node, ast.error
