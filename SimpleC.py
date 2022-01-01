##############################################################################################
# This is the compiler for SimpleC\n\t\tdevelopment start: 18.12.2021\n\t\trelease date: ?   #
##############################################################################################
#                                                                                            #
# - SimpleC is mixture of many C-like programming languages                                  #
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
FUNCTION = 'function'
STRUCT = 'struct'
CONSTRUCTOR = 'constructor'
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
    FUNCTION,
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
    THIS,
    USING,
    NAMESPACE
]

PREDEFINED = [
    NULL,
    FALSE,
    TRUE
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

# Extra types
BON = 'binopnode'
UNN = 'unarynode'
VAC = 'varaccess'
DOA = 'dotaccess'
AGA = 'argaccess'
FUNCTYPES = [
    VOID,
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
            return f'\n\t{self.type}:{self.value}'
        return f'\n\t{self.type}'


class Error:
    def __init__(self, message, errorType, position, fileName):
        self.message = message
        self.errorType = errorType
        self.position = position
        self.fileName = fileName

    def throw(self):
        print(
            f'{self.errorType} in {self.fileName} (line: {self.position.ln}, {self.position.col}):\n\t\t{self.message}')


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
            elif self.currChar == MODULUS:              # %
                tokens.append(Token(MODULUS, start=self.pos))
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
                self.advance()
                return [], Error(f'Illegal character : \'{self.currChar}\'', SYNTAXERROR,  self.pos, self.pos.fn)

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
        return f'MASTERSCRIPT : {self.libs}'


class Import:
    def __init__(self, lib):
        self.lib = lib

    def __repr__(self):
        return f'Import Node : \n\t\tLibrary Name > {self.lib} '

# Variables of another script can only be accessed as long as they are public / not a constant / and as long
# as the script has the other script's library imported!


class Script:
    def __init__(self, name, imports, lib, metacode, namespaces, global_variables, global_classes, global_structs):
        self.name = name
        self.imports = imports
        self.lib = lib
        self.metacode = metacode
        self.namespaces = namespaces
        self.global_variables = global_variables
        self.global_classes = global_classes
        self.global_structs = global_structs

    def __repr__(self):
        return f'\nScript Node : \n\t[\n\n\t\tScript name > {self.name}\n\t\tImports > {self.imports}\n\t\tLibrary name > {self.lib}\n\t\tNamespaces > {self.namespaces}\n\t\tGlobal variables > {self.global_variables}\n\t\tGlobal classes > {self.global_classes}\n\t\tGlobal structs > {self.global_structs}\n\n\t]'


class Lib:
    def __init__(self, scripts, name):
        self.scripts = scripts
        self.name = name

    def __repr__(self):
        return f'Lib Node : \n[\n\n\t\tLibrary\'s name > {self.name}\n\t\tSpripts > {self.scripts}\n\n]'


class Namespace:
    def __init__(self, script, lib, name, childSpaces, classes, structs):
        self.script = script
        self.lib = lib
        self.name = name
        self.parentSpace = None
        self.childSpaces = childSpaces
        self.classes = classes
        self.structs = structs

    def __repr__(self):
        return f'\n\tNamespace Node : \n\t\tScript > {self.script}\n\t\tLibrary > {self.lib}\n\t\tParent namespace > {self.parentSpace}\n\t\tName > {self.name}\n\t\tChild namespaces > {self.childSpaces}\n\t\tClasses > {self.classes}\n\t\tStructs > {self.structs}'


class Using:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'\n\tUsing Node : \n\t\tNamespace > {self.name}'


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

        if self.value and not isinstance(self.value, str):
            if not isinstance(self.value, DotAccess) and not isinstance(self.value, ArgAccess):
                self.start = self.value.start
                self.end = self.value.end if self.value else self.name.end
        elif not isinstance(self.name, str):
            self.start = self.name.start
            self.end = self.name.end
        else:
            self.start = None
            self.end = None

    def __repr__(self):
        condition = 'static' if self.static else ''
        condition = 'const' if self.const else condition
        return f'\n\tVariable Node : \n\t\tLibrary > {self.lib}\n\t\tNamespace > {self.namespace}\n\t\tClass > {self.classNode}\n\t\tPublic > {self.public}\n\t\tStatic/Const > {condition}\n\t\tType > {self.type}\n\t\tName > {self.name}\n\t\tValue > {self.value}'


class ReasignVar:
    def __init__(self, name, op, value):
        self.name = name
        self.op = op
        self.value = value

    def __repr__(self):
        return f'\n\tReasignVar Node : \n\t\nVariable > {self.name} \n\t\t{self.op} \n\t\t{self.value}'


class VarAccess:
    def __init__(self, classNode, varName, start, end):
        self.classNode = classNode
        self.varName = varName

        self.start = start
        self.end = end

    def __repr__(self):
        return f'\n\tVarAccess Node : \n\t\tClass > {self.classNode}\n\t\tVariable name > {self.varName}'

    def getType(self):
        return VAC


class DotAccess:
    def __init__(self, parent, var, node):
        self.parent = parent
        self.var = var
        self.node = node

    def __repr__(self):
        if self.var:
            return f'\n\tDotAccess Node : \n\t\tParent > {self.parent}\n\t\tVariable > {self.var}'
        elif self.node:
            return f'\n\tDotAccess Node : \n\t\tParent > {self.parent}\n\t\tNode > {self.node}'

    def getType(self):
        return DOA


class ArgAccess:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f'\n\t ArgAccess Node : \n\t\tName > {self.name} ({self.args})'

    def getType(self):
        return AGA


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
        return f'\n\tList Node : \n\t\tClass > {self.classNode}\n\t\tPublic > {self.public}\n\t\tStatic/Const > {condition}\n\t\tType > {self.type}\n\t\tName > {self.name}\n\t\tElements > {self.elements}'

    def getType(self):
        return self.type


class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

        self.start = self.left.start
        self.end = self.right.end

    def __repr__(self):
        return f'\n\tBinary Op Node : \n\t\tLeft node > {self.left}\n\t\tOperator > {self.op}\n\t\tRight node > {self.right}'

    def getType(self):
        return BON


class UnaryNode:
    def __init__(self, op, node):
        self.op = op
        self.node = node

        self.start = self.op.start
        self.end = self.node.end

    def __repr__(self):
        return f'\n\tUnary Node : \n\t\tOperator > {self.op}\n\t\tNode > {self.node}'

    def getType(self):
        return UNN


class If:
    def __init__(self, functionNode, condition, variables, body, cases, elseCase):
        self.functionNode = functionNode
        self.condition = condition
        self.variables = variables
        self.body = body
        self.cases = cases
        self.elseCase = elseCase

        if self.condition:
            self.start = self.condition.start
            self.end = self.condition.end

    def __repr__(self):
        return f'\n\tIf Node : \n\t\tFunction name > {self.functionNode}\n\t\tCondition > {self.condition}\n\t\tVariables > {self.variables}\n\t\tBody > {self.body}\n\t\tCases > {self.cases}\n\t\tElse case > {self.elseCase}'


class For:
    def __init__(self, functionNode, variables, variable, condition, steps, body):
        self.functionNode = functionNode
        self.variables = variables
        self.variable = variable
        self.condition = condition
        self.steps = steps
        self.body = body

        self.start = self.variable.start
        self.end = self.variable.end

    def __repr__(self):
        return f'\n\tFor Node : \n\t\tFunction name > {self.functionNode}\n\t\tVariables > {self.variables}\n\t\tStep variable > {self.variable}\n\t\tCondition > {self.condition}\n\t\tStep count > {self.steps}\n\t\tBody > {self.body}'


class SimpleFor:
    # (Maybe)
    pass


class While:
    def __init__(self, functionNode, variables, condition, body, do):
        self.functionNode = functionNode
        self.variables = variables
        self.condition = condition
        self.body = body
        self.do = do

        self.start = self.condition.start
        self.end = self.condition.end

    def __repr__(self):
        return f'\n\tWhile Node : \n\t\tFunction name > {self.functionNode}\n\t\tVariables > {self.variables}\n\t\tCondition > {self.condition}\n\t\tBody > {self.body} \n\t\tExecute first > {self.do}'


class Struct:
    def __init__(self, script, lib, namespace, externNameSpaces, variables, name, constructors):
        self.script = script
        self.lib = lib
        self.namespace = namespace
        self.externNameSpaces = externNameSpaces
        self.variables = variables
        self.name = name
        self.constructors = constructors

        self.start = self.name.start
        self.end = self.constructors[0].end

    def __repr__(self):
        return f'\n\tStruct Node : \n\t\tScript name > {self.script}\n\t\tLibrary name > {self.lib}\n\t\tNamespace name > {self.namespace}\n\t\tUsing namespaces > {self.externNameSpaces}\n\t\tVariables > {self.variables}\n\t\tName > {self.name}\n\t\tConstructors > {self.constructors}'


class Class:
    def __init__(self, script, lib, namespace, externNameSpaces, variables, public, static, name, constructors, body):
        self.script = script
        self.lib = lib
        self.namespace = namespace
        self.externNameSpaces = externNameSpaces
        self.variables = variables
        self.public = public
        self.static = static
        self.name = name
        self.constructors = constructors
        self.body = body

        self.start = self.name.start
        self.end = self.name.end

    def __repr__(self):
        return f'\n\tClass Node : \n\t\tScript name > {self.script}\n\t\tLibrary name > {self.lib}\n\t\tNamespace name > {self.namespace}\n\t\tUsing namespaces > {self.externNameSpaces}\n\t\tVariables > {self.variables}\n\t\tPublic > {self.public}\n\t\tStatic > {self.static}\n\t\tName > {self.name}\n\t\tConstructors > {self.constructors}\n\t\tBody > {self.body}'

# It can only have the returntype and arguments of the original function.
# The overriden function will only be overriden for the script the override function is being called


class OverrideFunction:
    def __init__(self, _class, function, variables, args, body):
        self._class = _class
        self.function = function
        self.variables = variables
        self.args = args
        self.body = body

    def __repr__(self):
        return f'\n\tOverride Node : \n\t\tClass name > {self._class}\n\t\tFunction to override > {self.function}\n\t\tVariables > {self.variables}\n\t\tParameters > {self.args}\n\t\tBody > {self.body}'


class OverrideOperation:
    # Maybe
    pass


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

        if not isinstance(self.returnType, str):
            self.start = self.returnType.start if self.returnType else None
        else:
            self.start = None
        self.end = None

    def __repr__(self):
        return f'\n\tFunction Node : \n\t\tClass name > {self.classNode}\n\t\tVariables > {self.variables}\n\t\tIs constructor? > {self.constructor}\n\t\tPublic > {self.public}\n\t\tStatic > {self.static}\n\t\tProtected > {self.protected}\n\t\tReturn type > {self.returnType}\n\t\tName > {self.name}\n\t\tParameters > {self.args}\n\t\tBody > {self.body}'


class Return:
    def __init__(self, functionNode, returnTok):
        self.functionNode = functionNode
        self.returnType = returnTok.getType() if returnTok else VOID
        self.returnValue = returnTok if returnTok else VOID

        self.start = returnTok.start if returnTok else None
        self.end = returnTok.end if returnTok else None

    def __repr__(self):
        return f'\n\tReturn Node : \n\t\tFunction name > {self.functionNode}\n\t\tReturn type > {self.returnType}\n\t\tReturn value > {self.returnValue}'


class Continue:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return f'\n\t<Continue Node>'


class Break:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return f'\n\t<Break Node>'


class MetaCode:
    def __init__(self, type, identifier, metVarValue=None):
        self.type = type
        self.value = identifier.value
        self.metVarValue = metVarValue

        self.start = identifier.start
        self.end = identifier.end

    def __repr__(self):
        return f'\nMetaCode Node : \n\tType > {self.type} : Value > {self.value}'

# Variable nodes


class Number:
    def __init__(self, type, value):
        self.type = type
        self.value = value

        self.start = self.value.start
        self.end = self.value.end

    def __repr__(self):
        return f'\n\tNumber Node : \n\t\tType > {self.type} : Value > {self.value}'

    def getType(self):
        return self.type


class String:
    def __init__(self, type, value):
        self.type = type
        self.value = value

        self.start = self.value.start
        self.end = self.value.end

    def __repr__(self):
        return f'\n\tString Node: \n\t\tType > {self.type} : Value > {self.value}'

    def getType(self):
        return self.type


class Bool:
    def __init__(self, type, value):
        self.type = type
        self.value = value

        self.start = self.value.start
        self.end = self.value.end

    def __repr__(self):
        return f'\n\tBool Node: \n\t\tType > {self.type} : Value > {self.value}'

    def getType(self):
        return self.type


class Type:
    def __init__(self, type, value):
        self.type = type
        self.value = value

        self.start = self.value.start
        self.end = self.value.end

    def __repr__(self):
        return f'\n\tType Node: \n\t\tType > {self.type} : Value > {self.value}'

    def getType(self):
        return self.type


class Var:
    def __init__(self, type, value):
        self.type = type
        self.value = value

        self.start = self.value.start
        self.end = self.value.end

    def __repr__(self):
        return f'\n\tVar Node: \n\t\tType > {self.type} : Value > {self.value}'

    def getType(self):
        return self.type


class Byte:
    def __init__(self, type, value):
        self.type = type
        self.value = value

        self.start = self.value.start
        self.end = self.value.end

    def __repr__(self):
        return f'\n\tByte Node: \n\t\tType > {self.type} : Value > {self.value}'

    def getType(self):
        return self.type


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
            print('\n This error can be ignored: \n')
            res.error.throw()
            print('\n')
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


masterscript = None
metacode = None


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
                    self.currTok.start, self.scriptName))

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
                metaNode = res.register(self.metacode(False))
                if res.error:
                    return res

                if metaNode.type == LIB:
                    lib = metaNode
                else:
                    metacode.append(metaNode)
            elif self.currTok.type == KEYWORD:
                node = res.register(self.expr())
                if res.error:
                    return res

                if isinstance(node, MetaCode):
                    metacode.append(node)
                elif isinstance(node, Namespace):
                    node.lib = lib
                    namespaces.append(node)
                elif isinstance(node, Variable):
                    node.lib = lib
                    global_variables.append(node)
                elif isinstance(node, Class):
                    node.lib = lib
                    global_classes.append(node)
                elif isinstance(node, Struct):
                    node.lib = lib
                    global_structs.append(node)
            elif self.currTok.type == EOF:
                break
            else:
                return res.failure(
                    Error(
                        "No valid expression found.", PARSEERROR,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()
            if self.currTok.type == EOF:
                moreStatements = False

        # Final touch to metacode
        for node in metacode:
            if node.type == DEFINE:
                global_variables.append(
                    Variable(lib, None, None, True, False, True, DEFINE, node.value, node.metVarValue))

        return res.success(Script(self.scriptName, imports, lib, metacode, namespaces, global_variables, global_classes, global_structs))

    def metacode(self, append):
        res = ParseResult()
        node = None

        if self.currTok.value == LIB:
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == EQUALS:
                return res.failure(
                    Error(
                        "Expected '='.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()

            if not self.currTok.type == STR:
                return res.failure(
                    Error(
                        "Expected string.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            libName = self.currTok
            node = MetaCode(LIB, libName)
        elif self.currTok.value == DEFINE:
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == IDENTIFIER:
                return res.failure(
                    Error(
                        "Expected identifier.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            name = self.currTok
            res.registerAdvance()
            self.advance()

            value = res.register(self.atom())
            if res.error or isinstance(value, MetaCode) or isinstance(value, Class) or isinstance(value, Function) or isinstance(value, Struct):
                return res.failure(
                    Error(
                        "Expected valid metavalue.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))
            self.reverse()

            node = MetaCode(DEFINE, name, value)
        elif self.currTok.value == METIF:
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == IDENTIFIER:
                return res.failure(
                    Error(
                        "Expected identifier.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            node = MetaCode(METIF, self.currTok)
        elif self.currTok.value == METELIF:
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == IDENTIFIER:
                return res.failure(
                    Error(
                        "Expected identifier.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            node = MetaCode(METELIF, self.currTok)
        elif self.currTok.value == METELSE:
            node = MetaCode(METELIF, self.currTok)
        elif self.currTok.value == METENDIF:
            node = MetaCode(METENDIF, self.currTok)

        if append:
            metacode.append(node)
        return res.success(node)

    def namespace(self):
        res = ParseResult()
        classes = []
        structs = []
        childSpaces = []

        res.registerAdvance()
        self.advance()

        if not self.currTok.type == IDENTIFIER:
            return res.failure(
                Error(
                    "Expected identifier.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        name = self.currTok
        res.registerAdvance()
        self.advance()

        if not self.currTok.type == LCBRACKET:
            return res.failure(
                Error(
                    "Expected '{'.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        while True:
            res.registerAdvance()
            self.advance()

            expr = res.tryRegister(self.expr())
            if not expr:
                self.reverse(res.reverseCount)
                break
            if res.error:
                return res

            if isinstance(expr, Variable):
                return res.failure(
                    Error(
                        "Cannot define variables inside a namespace.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))
            elif isinstance(expr, Class):
                expr.namespace = name
                classes.append(expr)
            elif isinstance(expr, Struct):
                expr.namespace = name
                structs.append(expr)
            elif isinstance(expr, Namespace):
                expr.parentSpace = name
                childSpaces.append(expr)

        if not self.currTok.type == RCBRACKET:
            return res.failure(
                Error(
                    "Expected '}'.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        return res.success(Namespace(self.scriptName, None, name, childSpaces, classes, structs))

    def ClassOrVarOrFunc(self):
        res = ParseResult()

        public = True if self.currTok.value == PUBLIC else False
        static = False
        const = False
        protected = False

        res.registerAdvance()
        self.advance()

        while self.currTok.value in (STATIC, CONST, PROTECTED):
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
            elif self.currTok.value == FUNCTION:
                res.registerAdvance()
                self.advance()

                if self.currTok.value in FUNCTYPES:
                    node = res.register(self.function())
                    if res.error:
                        return res

                    node.public = public
                    node.protected = protected
                    node.static = static
                    node.const = const
                    return res.success(node)
                else:
                    return res.failure(
                        Error(
                            "Expected valid function type!", SYNTAXERROR,
                            self.currTok.start, self.scriptName))
        elif self.currTok.type in VARTYPE:
            node = res.register(self.defVar())
            if res.error:
                return res

            node.public = public
            node.static = static
            node.const = const
            return res.success(node)
        elif self.currTok.type == IDENTIFIER:
            node = res.register(self.accessPointOrIdentifier())
            if not node:
                node = res.register(self.atom())
                if res.error:
                    return res
                return res.success(node)

            if isinstance(node, Variable):
                node.public = public
                node.static = static
                node.const = const
            return res.success(node)

        return res.failure(
            Error(
                "Expected valid class, variable or function...", PARSEERROR,
                self.currTok.start, self.scriptName))

    def struct(self):
        res = ParseResult()
        variables = []
        constructors = []

        res.registerAdvance()
        self.advance()

        if not self.currTok.type == IDENTIFIER:
            return res.failure(
                Error(
                    "Expected indentifier.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        name = self.currTok
        res.registerAdvance()
        self.advance()

        if not self.currTok.type == LCBRACKET:
            return res.failure(
                Error(
                    "Expected '{'", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        res.registerAdvance()
        self.advance()
        externNameSpaces = res.register(self.usings())

        while True:
            node = res.tryRegister(self.expr())
            if not node:
                self.reverse(res.reverseCount)
                break
            if res.error:
                return res

            node.classNode = name
            if isinstance(node, Class) or isinstance(node, Struct):
                return res.failure(
                    Error(
                        "It is not possible to define a class or struct inside a struct!", PARSEERROR,
                        self.currTok.start, self.scriptName))
            elif isinstance(node, Variable):
                node.public = True
                if node.static:
                    return res.failure(
                        Error(
                            "A variable cannot be static inside a struct.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))
                variables.append(node)
            elif isinstance(node, Function):
                if node.constructor:
                    constructors.append(node)
                else:
                    return res.failure(
                        Error(
                            "It is not possible to define a function inside a struct!", PARSEERROR,
                            self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()

        if not self.currTok.type == RCBRACKET:
            return res.failure(
                Error(
                    "Expected '}'", SYNTAXERROR,
                    self.currTok.start, self.scriptName))
        if len(constructors) == 0:
            return res.failure(
                Error(
                    "Expected at least one constructor!", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        return res.success(Struct(self.scriptName, None, None, externNameSpaces, variables, name, constructors))

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
                    self.currTok.start, self.scriptName))

        name = self.currTok
        res.registerAdvance()
        self.advance()

        if not self.currTok.type == LCBRACKET:
            return res.failure(
                Error(
                    "Expected '{'", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        res.registerAdvance()
        self.advance()
        externNameSpaces = res.register(self.usings())

        while True:
            node = res.tryRegister(self.expr())
            if not node:
                self.reverse(res.reverseCount)
                break
            if res.error:
                return res

            node.classNode = name
            if isinstance(node, Class) or isinstance(node, Struct):
                return res.failure(
                    Error(
                        "It is not possible to define a class or struct inside a class!", PARSEERROR,
                        self.currTok.start, self.scriptName))
            elif isinstance(node, Variable):
                variables.append(node)
            elif isinstance(node, Function) or isinstance(node, OverrideFunction):
                functions.append(node)

            res.registerAdvance()
            self.advance()

        if not self.currTok.type == RCBRACKET:
            return res.failure(
                Error(
                    "Expected '}'", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        return res.success(Class(self.scriptName, None, None, externNameSpaces, variables, False, False, name, constructors, functions))

    def usings(self):
        res = ParseResult()

        usings = []
        while True:
            if not self.currTok.value == USING:
                break

            res.registerAdvance()
            self.advance()

            name = res.register(self.statement())
            usings.append(Using(name))

            if not self.currTok.type == ENDCOLUMN:
                return res.failure(
                    Error(
                        "Expected ';'.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()

        return res.success(usings)

    def constructor(self):
        res = ParseResult()

        args = []
        body = []
        variables = []

        if not self.currTok.type == IDENTIFIER:
            return res.failure(
                Error(
                    "Expected identifier.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        name = self.currTok
        res.registerAdvance()
        self.advance()

        if not self.currTok.type == LBRACKET:
            return res.failure(
                Error(
                    "Expected '('.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        res.registerAdvance()
        self.advance()

        # Get parameters
        while True:
            if self.currTok.type == RBRACKET:
                res.registerAdvance()
                self.advance()
                break
            if not self.currTok.type == VARTYPE:
                return res.failure(
                    Error(
                        "Expected variable type.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            type = self.currTok
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == IDENTIFIER:
                return res.failure(
                    Error(
                        "Expected identifier.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            argName = self.currTok
            res.registerAdvance()
            self.advance()

            args.append(Variable(None, None, None, False,
                        False, True, type, argName, None))

            if self.currTok.type == RBRACKET:
                res.registerAdvance()
                self.advance()
                break
            if not self.currTok.type == COMMA:
                return res.failure(
                    Error(
                        "Expected ','.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()

        # Alternativ variable setup
        if self.currTok.type == COLON:
            while True:
                res.registerAdvance()
                self.advance()

                if not self.currTok.type == IDENTIFIER:
                    return res.failure(
                        Error(
                            "Expected identifier.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))

                varName = self.currTok.value
                res.registerAdvance()
                self.advance()

                if not self.currTok.type == LBRACKET:
                    return res.failure(
                        Error(
                            "Expected '('.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))

                res.registerAdvance()
                self.advance()

                if not self.currTok.type == IDENTIFIER:
                    return res.failure(
                        Error(
                            "Expected identifier.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))

                valueVarName = self.currTok.value
                res.registerAdvance()
                self.advance()

                type = None
                for i in args:
                    if i.name.value == valueVarName:
                        type = i.type
                        break
                if not type:
                    return res.failure(
                        Error(
                            f"Parameter with the name '{valueVarName}' does not exist.", PARSEERROR,
                            self.currTok.start, self.scriptName))

                if not self.currTok.type == RBRACKET:
                    return res.failure(
                        Error(
                            "Expected ')'.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))

                body.append(Variable(None, None, None, False, False,
                            False, type, varName, valueVarName))
                res.registerAdvance()
                self.advance()

                if not self.currTok.type == COMMA:
                    break

        if not self.currTok.type == LCBRACKET:
            return res.failure(
                Error(
                    "Expected '{'.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

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

            if isinstance(statement, Variable):
                statement.public = False
                if statement.static or statement.const:
                    return res.failure(
                        Error(
                            "'public', 'static' and 'const' are not allowed in a function.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))
                else:
                    variables.append(statement)
            elif isinstance(statement, Class) or isinstance(statement, Struct) or isinstance(statement, Function):
                return res.failure(
                    Error(
                        "Functions, classes and structs cannot be defined inside a constructor.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))
            elif isinstance(statement, Break) or isinstance(statement, Continue) or isinstance(statement, Return):
                return res.failure(
                    Error(
                        "Break points, continues and returns cannot be defined inside a constructor.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))
            elif isinstance(statement, If) or isinstance(statement, For) or isinstance(statement, While):
                statement.functionNode = name
                body.append(statement)

        if not self.currTok.type == RCBRACKET:
            return res.failure(
                Error(
                    "Expected '}'.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        return res.success(Function(None, variables, True, False, False, False, CONSTRUCTOR, None, args, body))

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
                    self.currTok.start, self.scriptName))

        name = self.currTok
        res.registerAdvance()
        self.advance()

        if not self.currTok.type == LBRACKET:
            return res.failure(
                Error(
                    "Expected '('.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        res.registerAdvance()
        self.advance()

        # Get parameters
        while True:
            if self.currTok.type == RBRACKET:
                res.registerAdvance()
                self.advance()
                break
            if not self.currTok.type == VARTYPE:
                return res.failure(
                    Error(
                        "Expected variable type.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            type = self.currTok
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == IDENTIFIER:
                return res.failure(
                    Error(
                        "Expected identifier.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            argName = self.currTok
            res.registerAdvance()
            self.advance()

            args.append(Variable(None, None, None, False,
                        False, True, type, argName, None))

            if self.currTok.type == RBRACKET:
                res.registerAdvance()
                self.advance()
                break
            if not self.currTok.type == COMMA:
                return res.failure(
                    Error(
                        "Expected ','.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()

        if not self.currTok.type == LCBRACKET:
            return res.failure(
                Error(
                    "Expected '{'.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

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
                statement.public = False
                if statement.static or statement.const:
                    return res.failure(
                        Error(
                            "'public', 'static' and 'const' are not allowed in a function.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))
                else:
                    variables.append(statement)
            elif isinstance(statement, Class) or isinstance(statement, Struct) or isinstance(statement, Function):
                return res.failure(
                    Error(
                        "Functions, classes and structs cannot be defined inside a function.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))
            elif isinstance(statement, Break) or isinstance(statement, Continue):
                return res.failure(
                    Error(
                        "Break points and continues cannot be defined inside a function.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))
            elif isinstance(statement, If) or isinstance(statement, For) or isinstance(statement, While):
                statement.functionNode = name
                body.append(statement)
            else:
                body.append(statement)

        if not self.currTok.type == RCBRACKET:
            return res.failure(
                Error(
                    "Expected '}'.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        return res.success(Function(None, variables, False, False, False, False, returnType, name, args, body))

    def overrideFunc(self):
        res = ParseResult()
        
        args = []
        body = []
        variables = []
        
        res.registerAdvance()
        self.advance()
        
        if not self.currTok.type == IDENTIFIER:
            return res.failure(
                Error(
                    "Expected class name.", SyntaxError,
                    self.currTok.start, self.scriptName))

        className = self.currTok.value
        res.registerAdvance()
        self.advance()
        
        if not self.currTok.type == COLON:
            return res.failure(
                Error(
                    "Expected ':'.", SyntaxError,
                    self.currTok.start, self.scriptName))
        
        res.registerAdvance()
        self.advance()
        
        if not self.currTok.type == COLON:
            return res.failure(
                Error(
                    "Expected '::'.", SyntaxError,
                    self.currTok.start, self.scriptName))
        
        res.registerAdvance()
        self.advance()
        
        if not self.currTok.type == IDENTIFIER:
            return res.failure(
                Error(
                    "Expected class name.", SyntaxError,
                    self.currTok.start, self.scriptName))
        
        funcName = self.currTok.value
        res.registerAdvance()
        self.advance()
        
        if not self.currTok.type == LBRACKET:
            return res.failure(
                Error(
                    "Expected class '('.", SyntaxError,
                    self.currTok.start, self.scriptName))
        
        res.registerAdvance()
        self.advance()
        
        # Get parameters
        while True:
            if self.currTok.type == RBRACKET:
                res.registerAdvance()
                self.advance()
                break
            if not self.currTok.type == VARTYPE:
                return res.failure(
                    Error(
                        "Expected variable type.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            type = self.currTok
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == IDENTIFIER:
                return res.failure(
                    Error(
                        "Expected identifier.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            argName = self.currTok
            res.registerAdvance()
            self.advance()

            args.append(Variable(None, None, None, False,
                        False, True, type, argName, None))

            if self.currTok.type == RBRACKET:
                res.registerAdvance()
                self.advance()
                break
            if not self.currTok.type == COMMA:
                return res.failure(
                    Error(
                        "Expected ','.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()
        
        if not self.currTok.type == LCBRACKET:
            return res.failure(
                Error(
                    "Expected '{'.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

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
                statement.functionNode = funcName
                body.append(statement)
            elif isinstance(statement, Variable):
                statement.public = False
                if statement.static or statement.const:
                    return res.failure(
                        Error(
                            "'public', 'static' and 'const' are not allowed in a function.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))
                else:
                    variables.append(statement)
            elif isinstance(statement, Class) or isinstance(statement, Struct) or isinstance(statement, Function):
                return res.failure(
                    Error(
                        "Functions, classes and structs cannot be defined inside a function.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))
            elif isinstance(statement, Break) or isinstance(statement, Continue):
                return res.failure(
                    Error(
                        "Break points and continues cannot be defined inside a function.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))
            elif isinstance(statement, If) or isinstance(statement, For) or isinstance(statement, While):
                statement.functionNode = funcName
                body.append(statement)
            else:
                body.append(statement)

        if not self.currTok.type == RCBRACKET:
            return res.failure(
                Error(
                    "Expected '}'.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        return res.success(OverrideFunction(className, funcName, variables, args, body))
        
    def statement(self):
        res = ParseResult()

        statement = None
        if self.currTok.value in (WHILE, DO):
            statement = res.register(self._while())
            if res.error:
                return res
        elif self.currTok.value == FOR:
            statement = res.register(self._for())
            if res.error:
                return res
        elif self.currTok.value == IF:
            statement = res.register(self.ifelifelse(IF))
            if res.error:
                return res
        elif self.currTok.value == RETURN:
            res.registerAdvance()
            self.advance()

            returnTok = res.tryRegister(self.expr())
            if not returnTok:
                self.reverse(res.reverseCount)
            if res.error:
                return res

            if not self.currTok.type == ENDCOLUMN:
                return res.failure(
                    Error(
                        "Expected ';'.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            statement = Return(None, returnTok)
        elif self.currTok.value == CONTINUE:
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == ENDCOLUMN:
                return res.failure(
                    Error(
                        "Expected ';'.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            return res.success(Continue(self.currTok.start, self.currTok.end))
        elif self.currTok.value == BREAK:
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == ENDCOLUMN:
                return res.failure(
                    Error(
                        "Expected ';'.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            return res.success(Break(self.currTok.start, self.currTok.end))
        elif self.currTok.type == IDENTIFIER or self.currTok.type == KEYWORD and self.currTok.value == THIS:
            statement = res.tryRegister(self.accessPointOrIdentifier())
            if not statement:
                statement = res.register(self.atom())
                if res.error:
                    return res
        elif self.currTok.value in VARTYPES:
            statement = res.register(self.defVar())
            if res.error:
                return res

        return res.success(statement)

    def _while(self):
        res = ParseResult()

        variables = []
        body = []
        do = False

        if self.currTok.value == WHILE:
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == LBRACKET:
                return res.failure(
                    Error(
                        "Expected '('", SyntaxError,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()
            condition = res.register(self.expr())
            if res.error:
                return res

            if not self.currTok.type == RBRACKET:
                return res.failure(
                    Error(
                        "Expected ')'", SyntaxError,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()

            if not self.currTok.type == LCBRACKET:
                statement = res.register(self.statement())
                if res.error:
                    return res

                if isinstance(statement, Variable):
                    variables.append(statement)
                else:
                    body.append(statement)
                return res.success(While(None, variables, condition, body, do))

            while True:
                res.registerAdvance()
                self.advance()

                statement = res.tryRegister(self.statement())
                if not statement:
                    self.reverse(res.reverseCount)
                    break
                if res.error:
                    return res

                if isinstance(statement, Variable):
                    variables.append(statement)
                else:
                    body.append(statement)

            if not self.currTok.type == RCBRACKET:
                return res.failure(
                    Error(
                        "Expected '}'", SyntaxError,
                        self.currTok.start, self.scriptName))
        else:
            if not self.currTok.value == DO:
                return res.failure(
                    Error(
                        "Expected do { ... }.", SyntaxError,
                        self.currTok.start, self.scriptName))

            do = True
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == LCBRACKET:
                return res.failure(
                    Error(
                        "Expected '{'", SyntaxError,
                        self.currTok.start, self.scriptName))

            while True:
                res.registerAdvance()
                self.advance()

                statement = res.tryRegister(self.statement())
                if not statement:
                    self.reverse(res.reverseCount)
                    break
                if res.error:
                    return res

                if isinstance(statement, Variable):
                    variables.append(statement)
                else:
                    body.append(statement)

            if not self.currTok.type == RCBRACKET:
                return res.failure(
                    Error(
                        "Expected '}'", SyntaxError,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()

            if not self.currTok.value == WHILE:
                return res.failure(
                    Error(
                        "Expected while (...).", SyntaxError,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()

            if not self.currTok.type == LBRACKET:
                return res.failure(
                    Error(
                        "Expected '('", SyntaxError,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()
            condition = res.register(self.expr())
            if res.error:
                return res

            if not self.currTok.type == RBRACKET:
                return res.failure(
                    Error(
                        "Expected ')'", SyntaxError,
                        self.currTok.start, self.scriptName))

        return res.success(While(None, variables, condition, body, do))

    def _for(self):
        res = ParseResult()

        variables = []
        body = []

        res.registerAdvance()
        self.advance()

        if not self.currTok.type == LBRACKET:
            return res.failure(
                Error(
                    "Expected '('.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        res.registerAdvance()
        self.advance()

        variable = res.register(self.defVar())
        if res.error:
            return res
        if not variable.value:
            return res.failure(
                Error(
                    "Expected value.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        res.registerAdvance()
        self.advance()
        condition = res.register(self.expr())

        if res.error:
            return res
        if not self.currTok.type == ENDCOLUMN:
            return res.failure(
                Error(
                    "Expected ';'.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        res.registerAdvance()
        self.advance()

        steps = res.register(self.expr())
        if res.error:
            return res

        res.registerAdvance()
        self.advance()

        if not self.currTok.type == RBRACKET:
            return res.failure(
                Error(
                    "Expected ')'.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        res.registerAdvance()
        self.advance()

        if not self.currTok.type == LCBRACKET:
            statement = res.register(self.statement())
            if res.error:
                return res

            if isinstance(statement, Variable):
                variables.append(statement)
            else:
                body.append(statement)
            return res.success(For(None, variables, variable, condition, steps, body))

        while True:
            res.registerAdvance()
            self.advance()

            statement = res.tryRegister(self.statement())
            if not statement:
                self.reverse(res.reverseCount)
                break
            if res.error:
                return res

            if isinstance(statement, Variable):
                variables.append(statement)
            else:
                body.append(statement)

        if not self.currTok.type == RCBRACKET:
            return res.failure(
                Error(
                    "Expected '}'.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        return res.success(For(None, variables, variable, condition, steps, body))

    def ifelifelse(self, ifType):
        res = ParseResult()

        condition = None
        variables = []
        body = []
        cases = []
        elseCase = None

        if ifType == IF:
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == LBRACKET:
                return res.failure(
                    Error(
                        "Expected '('.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()

            condition = res.register(self.expr())
            if res.error:
                return res

            if not self.currTok.type == RBRACKET:
                return res.failure(
                    Error(
                        "Expected ')'.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()

            if not self.currTok.type == LCBRACKET:
                statement = res.register(self.statement())
                if res.error:
                    return res

                if isinstance(statement, Variable):
                    variables.append(statement)
                elif isinstance(statement, Break) or isinstance(statement, Continue):
                    return res.failure(
                        Error(
                            "Break points and continues cannot be defined inside an if-statement.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))
                else:
                    body.append(statement)
            else:
                while True:
                    res.registerAdvance()
                    self.advance()

                    statement = res.tryRegister(self.statement())
                    if not statement:
                        self.reverse(res.reverseCount)
                        break
                    if res.error:
                        return res

                    if isinstance(statement, Variable):
                        variables.append(statement)
                    elif isinstance(statement, Break) or isinstance(statement, Continue):
                        return res.failure(
                            Error(
                                "Break points and continues cannot be defined inside an if-statement.", SYNTAXERROR,
                                self.currTok.start, self.scriptName))
                    else:
                        body.append(statement)

                if not self.currTok.type == RCBRACKET:
                    return res.failure(
                        Error(
                            "Expected '}'.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()

            if not self.currTok.value == ELIF:
                if not self.currTok.value == ELSE:
                    self.reverse()
                    return res.success(If(None, condition, variables, body, cases, elseCase))
                else:
                    elseCase = res.register(self.ifelifelse(ELSE))
                    if res.error:
                        return res

                    return res.success(If(None, condition, variables, body, cases, elseCase))
            else:
                while True:
                    _elif = res.register(self.ifelifelse(ELIF))
                    if res.error:
                        return res

                    cases.append(_elif)
                    res.registerAdvance()
                    self.advance()

                    if self.currTok.value == ELIF:
                        continue
                    elif self.currTok.value == ELSE:
                        elseCase = res.register(self.ifelifelse(ELSE))
                        if res.error:
                            return res

                        return res.success(If(None, condition, variables, body, cases, elseCase))
                    else:
                        self.reverse()
                        return res.success(If(None, condition, variables, body, cases, elseCase))
        elif ifType == ELIF:
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == LBRACKET:
                return res.failure(
                    Error(
                        "Expected '('.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()

            condition = res.register(self.expr())
            if res.error:
                return res

            if not self.currTok.type == RBRACKET:
                return res.failure(
                    Error(
                        "Expected ')'.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()

            if not self.currTok.type == LCBRACKET:
                statement = res.register(self.statement())
                if res.error:
                    return res

                if isinstance(statement, Variable):
                    variables.append(statement)
                elif isinstance(statement, Break) or isinstance(statement, Continue):
                    return res.failure(
                        Error(
                            "Break points and continues cannot be defined inside an if-statement.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))
                else:
                    body.append(statement)
            else:
                while True:
                    res.registerAdvance()
                    self.advance()

                    statement = res.tryRegister(self.statement())
                    if not statement:
                        self.reverse(res.reverseCount)
                        break
                    if res.error:
                        return res

                    if isinstance(statement, Variable):
                        variables.append(statement)
                    elif isinstance(statement, Break) or isinstance(statement, Continue):
                        return res.failure(
                            Error(
                                "Break points and continues cannot be defined inside an if-statement.", SYNTAXERROR,
                                self.currTok.start, self.scriptName))
                    else:
                        body.append(statement)

                if not self.currTok.type == RCBRACKET:
                    return res.failure(
                        Error(
                            "Expected '}'.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))
        elif ifType == ELSE:
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == LCBRACKET:
                statement = res.register(self.statement())
                if res.error:
                    return res

                if isinstance(statement, Variable):
                    variables.append(statement)
                elif isinstance(statement, Break) or isinstance(statement, Continue):
                    return res.failure(
                        Error(
                            "Break points and continues cannot be defined inside an if-statement.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))
                else:
                    body.append(statement)
            else:
                while True:
                    res.registerAdvance()
                    self.advance()

                    statement = res.tryRegister(self.statement())
                    if not statement:
                        self.reverse(res.reverseCount)
                        break
                    if res.error:
                        break

                    if isinstance(statement, Variable):
                        variables.append(statement)
                    elif isinstance(statement, Break) or isinstance(statement, Continue):
                        return res.failure(
                            Error(
                                "Break points and continues cannot be defined inside an if-statement.", SYNTAXERROR,
                                self.currTok.start, self.scriptName))
                    else:
                        body.append(statement)

                if not self.currTok.type == RCBRACKET:
                    return res.failure(
                        Error(
                            "Expected '}'.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))

        return res.success(If(None, condition, variables, body, None, None))

    def accessPointOrIdentifier(self):
        res = ParseResult()

        currTok = self.currTok

        res.registerAdvance()
        self.advance()

        if self.currTok.type in (EQUALS, PLUSPLUS, MINUSMINUS, PLUSEQUALS, MINUSEQUALS, DIVIDEEQUALS, MULTIPLYEQUALS):
            if self.currTok.type in (PLUSPLUS, MINUSMINUS):
                op_tok = self.currTok
                res.registerAdvance()
                self.advance()

                if not self.currTok.type == ENDCOLUMN:
                    return res.failure(
                        Error(
                            "Expected ';'.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))

                return res.success(ReasignVar(currTok.value, op_tok, Number(INT, Token(INT, "1", self.currTok.start, self.currTok.end))))
            op_tok = self.currTok

            res.registerAdvance()
            self.advance()

            right = res.register(self.expr())
            if res.error:
                return res

            if not self.currTok.type == ENDCOLUMN:
                return res.failure(
                    Error(
                        "Expected ';'.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            return res.success(ReasignVar(currTok.value, op_tok, right))
        if self.currTok.type == ENDCOLUMN:
            return res.success(VarAccess(None, currTok.value, currTok.start, currTok.end))

        if self.currTok.type == IDENTIFIER:
            varName = self.currTok.value
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == EQUALS:
                return res.failure(
                    Error(
                        "Expected '='.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()
            value = res.register(self.statement())
            if res.error:
                return res

            if isinstance(value, ArgAccess):
                res.registerAdvance()
                self.advance()

                if not self.currTok.type == ENDCOLUMN:
                    return res.failure(
                        Error(
                            "Expected ';'.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))

            return res.success(Variable(None, None, None, False, False, False, currTok, varName, value))
        elif self.currTok.type == LBRACKET:
            res.registerAdvance()
            self.advance()

            args = []

            if self.currTok.type == RBRACKET:
                return res.success(ArgAccess(currTok.value, args))

            while True:
                argExpr = res.register(self.expr())
                if res.error:
                    return res

                args.append(argExpr)

                if self.currTok.type == RBRACKET:
                    break
                if not self.currTok.type == COMMA:
                    return res.failure(
                        Error(
                            "Expected identifier.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))

                res.registerAdvance()
                self.advance()

            return res.success(ArgAccess(currTok.value, args))
        elif self.currTok.type == DOT:
            res.registerAdvance()
            self.advance()

            expr = res.register(self.statement())
            if res.error:
                return res

            if isinstance(expr, VarAccess):
                return res.success(DotAccess(currTok, expr, None))
            elif isinstance(expr, ArgAccess):
                res.registerAdvance()
                self.advance()
                if not self.currTok.type == ENDCOLUMN:
                    return res.failure(
                        Error(
                            "Expected ';'.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))

                return res.success(DotAccess(currTok, None, expr))
            elif isinstance(expr, DotAccess):
                return res.success(DotAccess(currTok, None, expr))
            elif isinstance(expr, ReasignVar):
                return res.success(DotAccess(currTok, None, expr))

        return res.failure(
            Error(
                "Expected valid access point.", SYNTAXERROR,
                self.currTok.start, self.scriptName))

    def defVar(self):
        res = ParseResult()

        type = self.currTok.value
        res.registerAdvance()
        self.advance()

        if not self.currTok.type == IDENTIFIER:
            return res.failure(
                Error(
                    "Expected identifier.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        name = self.currTok.value
        res.registerAdvance()
        self.advance()

        if not self.currTok.type == EQUALS:
            if not self.currTok.type == ENDCOLUMN:
                return res.failure(
                    Error(
                        "Expected ';'.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            return res.success(Variable(None, None, None, False, False, False, type, name, None))

        res.registerAdvance()
        self.advance()

        value = res.register(self.expr())
        if res.error:
            return res

        if not self.currTok.type == ENDCOLUMN:
            return res.failure(
                Error(
                    "Expected ';'.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        return res.success(Variable(None, None, None, False, False, False, type, name, value))

    def atom(self):
        res = ParseResult()
        tok = self.currTok

        if tok.type in (INT, FLT, DBL):
            res.registerAdvance()
            self.advance()
            return res.success(Number(tok.type, tok))
        elif tok.type == STR:
            res.registerAdvance()
            self.advance()
            return res.success(String(tok.type, tok))
        elif tok.type == CHR:
            res.registerAdvance()
            self.advance()
            return res.success(String(tok.type, tok))
        elif tok.type == BOL:
            res.registerAdvance()
            self.advance()
            return res.success(Bool(tok.type, tok))
        elif tok.type == BYT:
            res.registerAdvance()
            self.advance()
            return res.success(Byte(tok.type, tok))
        elif tok.type == TYP:
            res.registerAdvance()
            self.advance()
            return res.success(Type(tok.type, tok))
        elif tok.type == IDENTIFIER or tok.value in PREDEFINED:
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
                        self.currTok.start, self.scriptName))
        elif tok.type == KEYWORD:
            node = res.register(self.expr())
            if res.error:
                return res

            return res.success(node)

        return res.failure(
            Error(
                "Expected number, identifier, '+', '-' or '('", SyntaxError,
                self.currTok.start, self.scriptName))

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
        return self.bin_op(self.factor, (MULTIPLY, DIVIDE, MODULUS))

    def arith_expr(self):
        return self.bin_op(self.term, (PLUS, MINUS, PLUSPLUS, MINUSMINUS))

    def comp_expr(self):
        res = ParseResult()

        if self.currTok.type == NOT:
            op_tok = self.currTok
            res.registerAdvance()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryNode(op_tok, node))

        node = res.register(self.bin_op(
            self.arith_expr, (ISEQUALTO, NOT, LESS, GREATER, LESSEQUAL, GREATEREQUAL)))
        if res.error:
            return res

        return res.success(node)

    def expr(self):
        res = ParseResult()

        if self.currTok.value == NAMESPACE:
            node = res.register(self.namespace())
            if res.error:
                return res

            return res.success(node)
        elif self.currTok.value == STRUCT:
            node = res.register(self.struct())
            if res.error:
                return res

            return res.success(node)
        elif self.currTok.value == CONSTRUCTOR:
            node = res.register(self.constructor())
            if res.error:
                return res

            return res.success(node)
        elif self.currTok.value == OVERRIDE:
            node = res.register(self.overrideFunc())
            if res.error:
                return res
            
            return res.success(node)
        elif self.currTok.type == KEYWORD:
            node = res.register(self.ClassOrVarOrFunc())
            if res.error:
                return res

            return res.success(node)
        elif self.currTok.type == METAKEYWORD:
            metaNode = res.register(self.metacode(True))
            if res.error:
                return res

            return res.success(metaNode)
        elif self.currTok.type == VARTYPE:
            node = res.register(self.defVar())
            if res.error:
                return res
            return res.success(node)

        node = res.register(self.bin_op(self.comp_expr, (AND, OR)))

        if res.error:
            return res

        return res.success(node)

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if isinstance(left, BinOpNode):
            if left.op.type in (PLUSPLUS, MINUSMINUS):
                return res.success(left)
        if res.error:
            return res

        if not isinstance(left, BinOpNode) and self.currTok.type in (PLUSPLUS, MINUSMINUS):
            op_tok = self.currTok
            return res.success(BinOpNode(left, op_tok, Number(INT, Token(INT, "1", self.currTok.start, self.currTok.end))))

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
    # Reset data
    global masterscript, metacode
    masterscript = MasterScript([])
    metacode = []

    # Lexing
    lexer = Lexer(fn, text)
    tokens, error = lexer.genTokens()
    if error:
        return None, error

    # Parsing
    parser = Parser(fn, tokens)
    ast = parser.parse()

    return ast.node, ast.error


# TODOs :
#
# - Lists
