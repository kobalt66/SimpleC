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

import string
import os
import numpy
import random


#############################
# - Keywords / Operations - #
#############################

# Variable types
OBJ = 'obj' # [object]
VAR = 'var' # [variable]
BYT = 'byt' # [byte]
CHR = 'chr' # [character]
STR = 'str' # [string]
INT = 'int' # [integer]
FLT = 'flt' # [floating point]
DBL = 'dbl' # [double]
BOL = 'bol' # [boolean]
TYP = 'typ' # [type]
LST = 'lst' # [array]

VARTYPE = 'VARIABLE'
TYPEOF = 'typeof'
VARTYPES = [
    VAR,
    BYT,
    CHR,
    STR,
    INT,
    FLT,
    DBL,
    BOL,
    TYP,
    LST,
    OBJ
]
TYPEOFS = [
    'BYT',
    'CHR',
    'STR',
    'INT',
    'FLT',
    'DBL',
    'BOL',
    'TYP',
    'LST'
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
LENGHTOF = 'lenghtof'
NULL = 'null'
FALSE = 'false'
TRUE = 'true'
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
    LENGHTOF,
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
IMPORT = 'import'

METAKEYWORD = 'METAKEYWORD'
METAKEYWORDS = [
    LIB,
    IMPORT,
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
EQEQ = '=='
EOF = 'endofFile'

LETTERS = string.ascii_letters
DIGITS = '0123456789'
LETGITS = LETTERS + DIGITS
FLOATMIN = 0.0000000000000001

outputdir = ""
librarydir = "Libraries"
fileType = ".sc"
usedLibs = []

# Extra types
BON = 'binopnode'
UNN = 'unarynode'
VAC = 'varaccess'
DOA = 'dotaccess'
LIA = 'listaccess'
AGA = 'argaccess'
FUNCTYPES = [
    VOID,
    OBJ,
    BYT,
    CHR,
    STR,
    INT,
    FLT,
    DBL,
    BOL,
    TYP,
    LST
]


# Error types
TESTERROR = 'TestError'
ILLEGALCHAR = 'IllegalChar'
EXPEXTEDCHAR = 'ExpectedChar'
PARSEERROR = 'ParseError'
SYNTAXERROR = 'SyntaxError'
COMP2PYERROR = 'copmile2python < Error >'
COMP2CSHARPERROR = 'compile2csharp < Error >'
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
                tokens.append(Token(ENDCOLUMN, ENDCOLUMN, start=self.pos))
                self.advance()
            elif self.currChar == LCBRACKET:            # {
                tokens.append(Token(LCBRACKET, LCBRACKET, start=self.pos))
                self.advance()
            elif self.currChar == RCBRACKET:            # }
                tokens.append(Token(RCBRACKET, RCBRACKET, start=self.pos))
                self.advance()
            elif self.currChar == LSBRACKET:            # [
                tokens.append(Token(LSBRACKET, LSBRACKET, start=self.pos))
                self.advance()
            elif self.currChar == RSBRACKET:            # ]
                tokens.append(Token(RSBRACKET, RSBRACKET, start=self.pos))
                self.advance()
            elif self.currChar == LBRACKET:             # (
                tokens.append(Token(LBRACKET, LBRACKET, start=self.pos))
                self.advance()
            elif self.currChar == RBRACKET:             # )
                tokens.append(Token(RBRACKET, RBRACKET, start=self.pos))
                self.advance()
            elif self.currChar == POWER:                # ^
                tokens.append(Token(POWER, POWER, start=self.pos))
                self.advance()
            elif self.currChar == EQUALS:               # =
                tokens.append(Token(EQUALS, EQUALS, start=self.pos))
                self.advance()
            elif self.currChar == ISEQUALTO:            # ?
                tokens.append(Token(ISEQUALTO, ISEQUALTO, start=self.pos))
                self.advance()
            elif self.currChar == NOT:                  # !
                tokens.append(Token(NOT, NOT, start=self.pos))
                self.advance()
            elif self.currChar == MODULUS:              # %
                tokens.append(Token(MODULUS, MODULUS, start=self.pos))
                self.advance()
            elif self.currChar == COMMA:                # ,
                tokens.append(Token(COMMA, COMMA, start=self.pos))
                self.advance()
            elif self.currChar == DOT:                  # .
                tokens.append(Token(DOT, DOT, start=self.pos))
                self.advance()
            elif self.currChar == COLON:                # :
                tokens.append(Token(COLON, COLON, start=self.pos))
                self.advance()
            elif self.currChar == AND:                  # &
                tokens.append(Token(AND, AND, start=self.pos))
                self.advance()
            elif self.currChar == OR:                   # |
                tokens.append(Token(OR, OR, start=self.pos))
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
        type = TYPEOF if value in TYPEOFS else type
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
            return None, Error("Expected 'metif', 'define', ...", ILLEGALCHAR, self.pos, self.fn)
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
        self.name = name if name else 'libDEFAULTlib'

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


class TypeOf:
    def __init__(self, type):
        self.value = type.value
        self.type = type.type
        
        self.start = type.start
        self.end = type.end

    def getType(self):
        return TYPEOF


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
        return f'\n\tReasignVar Node : \n\t\tVariable > {self.name} \n\t\t{self.op} \n\t\t{self.value}'


class AccessPoint:
    def __init__(self):
        self.type = 'accesspoint'


class VarAccess(AccessPoint):
    def __init__(self, classNode, varName, start, end):
        self.classNode = classNode
        self.varName = varName

        self.start = start
        self.end = end

    def __repr__(self):
        return f'\n\tVarAccess Node : \n\t\tClass > {self.classNode}\n\t\tVariable name > {self.varName}'

    def getType(self):
        return VAC


class DotAccess(AccessPoint):
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


class ArgAccess(AccessPoint):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f'\n\tArgAccess Node : \n\t\tName > {self.name} ({self.args})'

    def getType(self):
        return AGA


class ListAccess(AccessPoint):
    def __init__(self, name, elementIdx, start, end):
        self.name = name
        self.elementIdx = elementIdx

        self.start = start
        self.end = end

    def __repr__(self):
        return f'\n\tListAccess Node: \n\t\tList name > {self.name}\n\t\tIndex > {self.elementIdx}'

    def getType(self):
        return LIA


class List:
    def __init__(self, lib, namespace, classNode, public, static, const, type, name, elements, start, end):
        self.lib = lib
        self.namespace = namespace
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
        return f'\n\tList Node : \n\t\tLib > {self.lib}\n\t\tNamespace > {self.namespace}\n\t\tClass > {self.classNode}\n\t\tPublic > {self.public}\n\t\tStatic/Const > {condition}\n\t\tType > {self.type}\n\t\tName > {self.name}\n\t\tElements > {self.elements}'

    def getType(self):
        return self.type


class ListSpace:
    def __init__(self, length, elements, listType):
        self.length = length
        self.elements = elements
        self.listType = listType

    def __repr__(self):
        return f'\n\tListSpace Node: \n\t\tLength > {self.length}\n\t\tElements > {self.elements}'


class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

        if not isinstance(self.left, AccessPoint):
            self.start = self.left.start
            self.end = self.left.end
        else:
            self.start = Position(0, 0, 0, '', '')
            self.end = Position(0, 0, 0, '', '')

    def __repr__(self):
        return f'\n\tBinary Op Node : \n\t\tLeft node > {self.left}\n\t\tOperator > {self.op}\n\t\tRight node > {self.right}'

    def getType(self):
        return BON


class UnaryNode:
    def __init__(self, op, node):
        self.op = op
        self.node = node

        self.start = self.op.start
        self.end = self.op.end

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

        if self.condition and not isinstance(self.condition, AccessPoint):
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
    def __init__(self, functionNode, returnTok, start, end):
        self.functionNode = functionNode
        self.returnType = returnTok.getType() if returnTok else VOID
        self.returnValue = returnTok if returnTok else VOID

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


class Lst:
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
            print('\n Side Error: \n')
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
        global metacode
        metacode = []
        
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

        scripts = []
        name = None

        script = res.register(self.script())
        if res.error:
            return res

        name = script.lib
        scripts.append(script)

        return res.success(Lib(scripts, name))

    def script(self):
        res = ParseResult()
        imports = []
        lib = 'libDEFAULTlib'
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
                    lib = metaNode.value
                elif metaNode.type == IMPORT:
                    imports.append(metaNode)
                    if not metaNode.value in usedLibs:
                        usedLibs.append(metaNode.value)
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
                elif isinstance(node, Variable) or isinstance(node, List):
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
        elif self.currTok.value == IMPORT:
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == LESS:
                return res.failure(
                    Error(
                        "Expected '<'.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()

            if not self.currTok.type == IDENTIFIER:
                return res.failure(
                    Error(
                        "Expected identifier.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            libName = self.currTok
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == GREATER:
                return res.failure(
                    Error(
                        "Expected '>'.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            node = MetaCode(IMPORT, libName)
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

        if self.currTok.value in (PUBLIC, PRIVATE):
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
            node = res.register(self.expr())

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
            elif isinstance(node, Variable) or isinstance(node, List):
                variables.append(node)
            elif isinstance(node, Function):
                if node.constructor:
                    constructors.append(node)
                else:
                    functions.append(node)
            elif isinstance(node, OverrideFunction):
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
            if not isinstance(name, AccessPoint):
                return res.failure(
                    Error(
                        "Expected nested namespace name or a single namespace name.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))
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
                if not self.currTok.type == IDENTIFIER:
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

                body.append(ReasignVar(varName, Token(
                    EQUALS, EQUALS), valueVarName))
                res.registerAdvance()
                self.advance()

                if not self.currTok.type == COMMA:
                    break

        if not self.currTok.type == LCBRACKET:
            self.reverse()
            return res.success(Function(None, variables, True, False, False, False, CONSTRUCTOR, None, args, body))

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
                    body.append(statement)
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
            else:
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
                if not self.currTok.type == IDENTIFIER:
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
            elif isinstance(statement, Variable) or isinstance(statement, List):
                statement.public = False
                if statement.static or statement.const:
                    return res.failure(
                        Error(
                            "'public', 'static' and 'const' are not allowed in a function.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))
                else:
                    body.append(statement)
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

            statement = Return(
                None, returnTok, self.currTok.start, self.currTok.end)
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
        elif self.currTok.type == IDENTIFIER:
            statement = res.register(self.expr())
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

                # if isinstance(statement, Variable):
                #     variables.append(statement)
                # else:
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

                # if isinstance(statement, Variable):
                #     variables.append(statement)
                # else:
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

                # if isinstance(statement, Variable):
                #     variables.append(statement)
                # else:
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

            # if isinstance(statement, Variable):
            #     variables.append(statement)
            # else:
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

            # if isinstance(statement, Variable):
            #     variables.append(statement)
            # else:
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

                # if isinstance(statement, Variable):
                #     variables.append(statement)
                if isinstance(statement, Break) or isinstance(statement, Continue):
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

                    # if isinstance(statement, Variable):
                    #    variables.append(statement)
                    if isinstance(statement, Break) or isinstance(statement, Continue):
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

                # if isinstance(statement, Variable):
                #     variables.append(statement)
                if isinstance(statement, Break) or isinstance(statement, Continue):
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

                    # if isinstance(statement, Variable):
                    #     variables.append(statement)
                    if isinstance(statement, Break) or isinstance(statement, Continue):
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

                # if isinstance(statement, Variable):
                #     variables.append(statement)
                if isinstance(statement, Break) or isinstance(statement, Continue):
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

                    # if isinstance(statement, Variable):
                    #     variables.append(statement)
                    if isinstance(statement, Break) or isinstance(statement, Continue):
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
            value = res.register(self.atom())
            if res.error:
                return res

            if isinstance(value, ArgAccess):
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

                if self.currTok.type == ENDCOLUMN:
                    self.reverse()
                if self.currTok.type == RBRACKET:
                    break
                if not self.currTok.type == COMMA:
                    return res.failure(
                        Error(
                            "Expected ','.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))

                res.registerAdvance()
                self.advance()

            return res.success(ArgAccess(currTok.value, args))
        elif self.currTok.type == LSBRACKET:
            res.registerAdvance()
            self.advance()

            if not self.currTok.type in (INT, IDENTIFIER):
                return res.failure(
                    Error(
                        "Expected integer or identifier.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            idx = self.currTok
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == RSBRACKET:
                return res.failure(
                    Error(
                        "Expected ']'.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            left = ListAccess(currTok.value, idx,
                              self.currTok.start, self.currTok.end)

            self.advance()
            if self.currTok.type == DOT:
                res.registerAdvance()

                res.registerAdvance()
                self.advance()
                expr = res.register(self.atom())
                if res.error:
                    return res

                if isinstance(expr, VarAccess):
                    return res.success(DotAccess(left, expr, None))
                elif isinstance(expr, ArgAccess):
                    return res.success(DotAccess(left, None, expr))
                elif isinstance(expr, DotAccess):
                    return res.success(DotAccess(left, None, expr))
                elif isinstance(expr, ListAccess):
                    return res.success(DotAccess(left, expr, None))
                elif isinstance(expr, ReasignVar):
                    return res.success(DotAccess(left, None, expr))
            elif self.currTok.type == EQUALS:
                res.registerAdvance()

                res.registerAdvance()
                self.advance()
                value = res.register(self.expr())
                if res.error:
                    return res

                if isinstance(value, ArgAccess):
                    if not self.currTok.type == ENDCOLUMN:
                        return res.failure(
                            Error(
                                "Expected ';'.", SYNTAXERROR,
                                self.currTok.start, self.scriptName))

                if not self.currTok.type == ENDCOLUMN:
                    return res.failure(
                        Error(
                            "Expected ';'.", SYNTAXERROR,
                            self.currTok.start, self.scriptName))

                return res.success(ReasignVar(left, Token(EQUALS, EQUALS), value))
            else:
                self.reverse()

            return res.success(left)
        elif self.currTok.type == DOT:
            res.registerAdvance()
            self.advance()

            expr = res.register(self.atom())
            if res.error:
                return res

            if isinstance(expr, VarAccess):
                return res.success(DotAccess(currTok, expr, None))
            elif isinstance(expr, ArgAccess):
                return res.success(DotAccess(currTok, None, expr))
            elif isinstance(expr, DotAccess):
                return res.success(DotAccess(currTok, None, expr))
            elif isinstance(expr, ListAccess):
                return res.success(DotAccess(currTok, expr, None))
            elif isinstance(expr, ReasignVar):
                return res.success(DotAccess(currTok, None, expr))

        # If it's just an identifier
        self.reverse()
        return res.success(VarAccess(None, currTok.value, currTok.start, currTok.end))

    def defVar(self):
        res = ParseResult()

        type = self.currTok.value
        res.registerAdvance()
        self.advance()

        if type == LST:
            if not self.currTok.type == LSBRACKET:
                return res.failure(
                    Error(
                        "Expected '['.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))
                
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == RSBRACKET:
                return res.failure(
                    Error(
                        "Expected ']'.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

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
                return res.failure(
                    Error(
                        "Expected '='.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()

            value = res.register(self.listElements())
            if res.error:
                return res
                        
            return res.success(List(None, None, None, False, False, False, value.listType, name, value, self.currTok.start, self.currTok.end))

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

    def listElements(self):
        res = ParseResult()

        listType = LST
        if self.currTok.type == VARTYPE:
            listType = self.currTok.value
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == LSBRACKET:
                return res.failure(
                    Error(
                        "Expected '['.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()

            if not self.currTok.type == INT:
                return res.failure(
                    Error(
                        "Expected integer.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            length = int(self.currTok.value)
            res.registerAdvance()
            self.advance()

            if not self.currTok.type == RSBRACKET:
                return res.failure(
                    Error(
                        "Expected '['.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            res.registerAdvance()
            self.advance()

            if not self.currTok.type == ENDCOLUMN:
                return res.failure(
                    Error(
                        "Expected ';'.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))

            return res.success(ListSpace(length, None, listType))

        if not self.currTok.type == LCBRACKET:
            return res.failure(
                Error(
                    "Expected '{'.", SYNTAXERROR,
                    self.currTok.start, self.scriptName))

        elements = []
        while True:
            res.registerAdvance()
            self.advance()

            element = res.tryRegister(self.expr())

            self.advance()
            if self.currTok.type in (COMMA, RCBRACKET):
                res.registerAdvance()
            else:
                self.reverse()

            if not element:
                self.reverse(res.reverseCount)
                break
            if res.error:
                return res

            elements.append(element)
            listType = element.type.value if isinstance(element, Variable) else listType
            listType = element.name if isinstance(element, ArgAccess) else listType
            
            if self.currTok.type == COMMA:
                continue

            if not self.currTok.type == RCBRACKET:
                return None, res.failure(
                    Error(
                        "Expected '}'.", SYNTAXERROR,
                        self.currTok.start, self.scriptName))
            else:
                break

        return res.success(ListSpace(len(elements), elements, listType))

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
            return res.success(Lst(tok.type, tok))
        elif tok.type == LST:
            res.registerAdvance()
            self.advance()
            return res.success(Type(tok.type, tok))
        elif tok.type == TYPEOF:
            res.registerAdvance()
            self.advance()
            return res.success(TypeOf(tok))
        elif tok.type == IDENTIFIER or tok.value in PREDEFINED:
            res.registerAdvance()
            self.advance()

            if self.currTok.type in (EQUALS, PLUSPLUS, MINUSMINUS, PLUSEQUALS, MINUSEQUALS, DIVIDEEQUALS, MULTIPLYEQUALS):
                self.reverse()
                left = VarAccess(None, self.currTok.value,
                                 self.currTok.start, self.currTok.end)

                res.registerAdvance()
                self.advance()

                if self.currTok.type in (PLUSPLUS, MINUSMINUS):
                    op_tok = self.currTok

                    res.registerAdvance()
                    self.advance()

                    if not self.currTok.type == ENDCOLUMN:
                        return res.failure(
                            Error(
                                "Expected ';'.", SYNTAXERROR,
                                self.currTok.start, self.scriptName))

                    return res.success(ReasignVar(left, op_tok, Number(INT, Token(INT, "1", self.currTok.start, self.currTok.end))))
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

                return res.success(ReasignVar(left, op_tok, right))
            if self.currTok.type in (DOT, IDENTIFIER, LBRACKET, LSBRACKET):
                self.reverse()

                value = res.register(self.accessPointOrIdentifier())
                if res.error:
                    return res

                self.advance()

                if not self.currTok.type == ENDCOLUMN:
                    self.reverse()
                else:
                    res.registerAdvance()

                return res.success(value)

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
            self.arith_expr, (EQUALS, ISEQUALTO, NOT, TOCODE, LESS, GREATER, LESSEQUAL, GREATEREQUAL)))
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


def ParseScripts(projectdir):
    files = os.listdir(projectdir)
    print(files)
    
    for file in files:
        name, extension = os.path.splitext(file)
        if not extension == fileType:
            continue
        
        script, error = openFile(projectdir, name)
        if error:
            return error
    
        lexer = Lexer(name, script)
        tokens, error = lexer.genTokens()
        if error:
            return error

        # Parsing
        parser = Parser(name, tokens)
        ast = parser.parse()
        if ast.error:
            return ast.error

    return None

def ParseExternLibraries():
    files = os.listdir(librarydir)
    
    for file in files:
        name, extension = os.path.splitext(file)
        if not extension == fileType:
            continue
        
        if not name in usedLibs:
            continue
        
        script, error = openFile(librarydir, name)
        if error:
            return error
    
        lexer = Lexer(name, script)
        tokens, error = lexer.genTokens()
        if error:
            return error

        # Parsing
        parser = Parser(name, tokens)
        ast = parser.parse()
        if ast.error:
            return ast.error

    return None

####################
# - The compiler - #
####################


# - The output file will allways be called "output.py"                                                                                  (check)
# - The compiler gets the data of the masterscript so it has access to all the data inside the SimpleC project                          (check)
# - It will start running through all that data (script by script)
# - When comiling, the compiler will first check for any old "output.py" file and reset it                                              (check)
# - Everything will be loaded into one file                                                                                             (check)
# - First all the necessary stuff like classes are going to be pasted into the script
# - Then all scripts with their namespaces, classes, structs and constants will be loaded below
# - In the mean while the compiler will check for the correctness of the script
# - In the end a main function will be generated containing all necessary instructions to run the script
# - The final step would be to call that main function at the end of the script
# - Then the compiler returns to "main.py" (basically all the compiling errors)
# - The program stops
# - Now in the custom code editor the code will receive a callback to give the user access to the start button
# - If the script is compiled the code editor will look for any errors it received from the compiler and mark them in the scripts
# - When pressing the start button the script will be started and the output of that script will be displayed in the console

class compPath:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def compare(self, name):
        return self.name == name


class compile2python:
    def __init__(self, masterscript, outputdir, projectdir):
        self.outputdir = outputdir
        self.projectdir = projectdir

        # compiler stuff
        self.ms = masterscript
        self.defaultLib = 'libDEFAULTlib'
        self.noneStr = 'None'
        self.outputFile = f'{self.outputdir}output.py'

        self.pathData = []

        self.namespaceNames = []
        self.classNames = []
        self.structNames = []
        self.varNames = []

        self.basicData = [
            "VAR = 'var'",
            "BYT = 'byt'",
            "CHR = 'chr'",
            "STR = 'str'",
            "INT = 'int'",
            "FLT = 'flt'",
            "DBL = 'dbl'",
            "BOL = 'bol'",
            "TYP = 'typ'",
            ' ',
            'class InvalidAccess(Exception):\n\tpass',
            ' ',
            'class arg:\n\tdef __init__(self, name, type):\n\t\tself.arg = Var(False, False, True, type, name)\n\t\tself.name = name\n\t\tself.type = type',
            ' ',
            'class Var:\n\tdef __init__(self, public, static, const, type, name, value=None):\n\t\tself.public = public\n\t\tself.static = static\n\t\tself.const = const\n\t\tself.type = type\n\n\t\tself.name = name\n\t\tself.valType = None\n\t\tself.value = None if not value else value\n\n\tdef getType(self):\n\t\treturn self.type\n\n\tdef equals(self, value):\n\t\tif self.const and self.value: raise SyntaxError(f\'{self.name} is a constant!\')\n\t\tif self.compareType(value):\n\t\t\tself.value = value.value\n\n\tdef compareType(self, value):\n\t\tif not isinstance(value, Var):\n\t\t\tif not self.getType() == VAR:\n\t\t\t\tif self.getType() == INT and not isinstance(value, int) or self.getType() == FLT and not isinstance(value, float) or self.getType() == DBL and not isinstance(value, float) or self.getType() == BOL and not isinstance(value, bool) or self.getType() == BYT and not isinstance(value, int) or self.getType() == STR and not isinstance(value, str) or self.getType() == CHR and (not isinstance(value, str) or len(value) > 1):\n\t\t\t\t\traise SyntaxError(f\'{self.name}: cannot convert a {type(value)} into {self.getType()}!\')\n\t\t\treturn True\n\t\telse:\n\t\t\tif not self.getType() == Var:\n\t\t\t\tif not self.getType() == value.getType():\n\t\t\t\t\traise SyntaxError(f\'{self.name}: cannot convert a {type(value.value)} into {self.getType()}!\')\n\t\t\treturn True',
            ' ',
            "SCRIPT = 'script'",
            "LIB = 'library'",
            "SPACE = 'namespace'",
            "CLASS = 'class'",
            "STRUCT = 'struct'"
        ]

        # Setup output.py
        if os.path.exists(self.outputFile):
            f = open(self.outputFile, 'w')
            f.write('# This is the compiled script of your project.\n\n')
            f.close()
        else:
            f = open(self.outputFile, 'x')
            f.close()

    def genHexCode(self):
        return '{0:032x}'.format(random.randrange(16**32))

    def getPath(self, name):
        for path in self.pathData:
            if path.compare(name):
                return path.path
        return 'self'

    def write(self, data, print=False):
        f = open(self.outputFile, 'a')
        f.write(data)
        f.close()

        # Open and read the file after the appending
        if print:
            f = open(self.outputFile, 'r')
            print(f.read())
            f.close()

    def compile(self):
        # Write all the basic data into the script
        for data in self.basicData:
            self.write(data)
            self.write('\n')
        self.write('\n' + '#' * 200)

        # Start with libs
        for lib in self.ms.libs:
            mPath = lib.name
            self.pathData.append(compPath(lib.name, lib.name))

            self.write('\n\n')
            self.write(
                f'class {lib.name}:\n\tdef __init__(self):\n\t\tself.type = LIB')

            # Generate all script classes
            for script in lib.scripts:
                error = self.genScript(script, mPath)
                if error:
                    return error
            self.write('\n\n')

        print('Successfully compiled the project!')
        return None

    def checkPaths(self):
        f = open(self.outputFile, 'r')
        oldScript = f.read()
        f.close()

        # Check for @!VM!@ and replaces it with the right path
        idx = 0
        newScript = ''
        while idx < len(oldScript):
            currChar = oldScript[idx]
            if currChar == '@':
                following = oldScript[idx + 1:idx + 6]
                if following == '!VM!@':
                    name = ''
                    idx += 7
                    while True:
                        currChar = oldScript[idx]
                        if currChar in LETGITS + '_':
                            name += currChar
                            idx += 1
                        else:
                            break
                    newScript += self.getPath(name)
            else:
                newScript += oldScript[idx]
                idx += 1

        # Set up new script
        f = open(self.outputFile, 'w')
        f.write(newScript)
        f.close()

    def genScript(self, script, parentPath):
        mPath = f'{parentPath}.{script.name}'
        self.pathData.append(compPath(script.name, mPath))

        self.write(
            f'\n\n\tclass {script.name}:\n\t\tdef __init__(self):\n\t\t\tself.type = SCRIPT\n\t\t\tself.imports = [')

        # imports
        for imp in script.imports:
            self.write(f'\n\t\t\t\t\'{imp.value}\',')
        self.write('\n\t\t\t]\n')

        # lib
        self.write(
            f'\t\t\tself.lib = \'{script.lib if script.lib else self.defaultLib}\'')

        # global_variables
        for var in script.global_variables:
            if not var.name in self.varNames:
                self.varNames.append(var.name)
                error = self.genVariable(var, 3, mPath)
                if error:
                    return error
            else:
                return Error(f'You cannot use {var.name} twice.', COMP2PYERROR,
                             Position(-1, -1, -1, '', ''), '<comiler>')

        # namespaces
        for namespace in script.namespaces:
            if not namespace.name.value in self.namespaceNames:
                self.namespaceNames.append(namespace.name.value)
                error = self.genNamespace(namespace, 2, mPath)
                if error:
                    return error
            else:
                return Error(f'You cannot use {namespace.name.value} twice.', COMP2PYERROR,
                             Position(-1, -1, -1, '', ''), '<comiler>')

        # classes
        for _class in script.global_classes:
            if not _class.name.value in self.classNames:
                self.classNames.append(_class.name.value)
                error = self.genClass(_class, 2, mPath)
                if error:
                    return error
            else:
                return Error(f'You cannot use {_class.name.value} twice.', COMP2PYERROR,
                             Position(-1, -1, -1, '', ''), '<comiler>')

        # structs
        for struct in script.global_structs:
            if not struct.name.value in self.structNames:
                self.structNames.append(struct.name.value)
                error = self.genStruct(struct, 2, mPath)
                if error:
                    return error
            else:
                return Error(f'You cannot use {struct.name.value} twice.', COMP2PYERROR,
                             Position(-1, -1, -1, '', ''), '<comiler>')

        # getVar function
        self.write(f'\n\n\t\tdef getVar(self, var):\n\t\t\tcheck = hasattr(self, var)\n\t\t\tif check:\n\t\t\t\tmember = getattr(self, var)\n\t\t\t\tif isinstance(member, Var):\n\t\t\t\t\tif not member.public and not member.static:\n\t\t\t\t\t\traise InvalidAccess(f\'' +
                   '{var}' + f' is not accessable.\')\t\n\t\t\t\telse:\n\t\t\t\t\treturn member\n\t\t\telse:\n\t\t\t\traise AttributeError(f\'' + '{var}' + ' does not exist inside {self.__class__.__name__}.\')')

        return None

    def genNamespace(self, namespace, tabs, parentPath):
        tab = '\t'
        mPath = f'{parentPath}.{namespace.name.value}'
        self.pathData.append(compPath(namespace.name.value, mPath))

        self.write(
            f'\n\n{tab * tabs}class {namespace.name.value}:\n{tab * tabs}\tdef __init__(self):\n{tab * tabs}\t\tself.type = SPACE')

        # parent namespace
        self.write(f'\n{tab * tabs}\t\tself.parentSpace = {parentPath}()')

        # name
        self.write(f'\n{tab * tabs}\t\tself.name = \'{namespace.name.value}\'')

        # child namespaces
        for childNamespace in namespace.childSpaces:
            if not childNamespace.name.value in self.namespaceNames:
                self.namespaceNames.append(childNamespace.name.value)
                error = self.genNamespace(childNamespace, tabs + 1, mPath)
                if error:
                    return error
            else:
                return Error(f'You cannot use {childNamespace.name} twice.', COMP2PYERROR,
                             Position(-1, -1, -1, '', ''), '<comiler>')

        # classes
        for _class in namespace.classes:
            if not _class.name.value in self.classNames:
                self.classNames.append(_class.name.value)
                error = self.genClass(_class, tabs + 1, mPath)
                if error:
                    return error
            else:
                return Error(f'You cannot use {_class.name.value} twice.', COMP2PYERROR,
                             Position(-1, -1, -1, '', ''), '<comiler>')

        # structs
        for struct in namespace.structs:
            if not struct.name.value in self.structNames:
                self.structNames.append(struct.name.value)
                error = self.genStruct(struct, tabs + 1, mPath)
                if error:
                    return error
            else:
                return Error(f'You cannot use {struct.name.value} twice.', COMP2PYERROR,
                             Position(-1, -1, -1, '', ''), '<comiler>')

        return None

    def genClass(self, _class, tabs, parentPath):
        tab = '\t'
        mPath = f'{parentPath}.{_class.name.value}'
        self.pathData.append(compPath(_class.name.value, mPath))

        # keep track of all the used names
        varNames = []
        funcNames = []

        self.write(
            f'\n\n{tab * tabs}class {_class.name.value}:\n{tab * tabs}\tdef __init__(self, *args):\n{tab * tabs}\t\tself.type = CLASS')

        # using
        for using in _class.externNameSpaces:
            error = self.genUsing(using, tabs + 2)
            if error:
                return error
        self.write('\n')

        # variables
        for var in _class.variables:
            if not var.name in varNames:
                self.varNames.append(var.name)
                error = self.genVariable(var, 5, mPath)
                if error:
                    return error
            else:
                return Error(f'You cannot use {var.name} twice.', COMP2PYERROR,
                             Position(-1, -1, -1, '', ''), '<comiler>')

        # constructors

        # getVar function
        self.write(f'\n\n{tab * tabs}\tdef getVar(self, var):\n{tab * tabs}\t\tcheck = hasattr(self, var)\n{tab * tabs}\t\tif check:\n{tab * tabs}\t\t\tmember = getattr(self, var)\n{tab * tabs}\t\t\tif isinstance(member, Var):\n{tab * tabs}\t\t\t\tif not member.public and not member.static:\n{tab * tabs}\t\t\t\t\traise InvalidAccess(f\'' +
                   '{var}' + f' is not accessable.\')\n{tab * tabs}\t\t\t\telse:\n{tab * tabs}\t\t\t\t\treturn member\n{tab * tabs}\t\telse:\n{tab * tabs}\t\t\traise AttributeError(f\'' + '{var}' + ' does not exist inside {self.__class__.__name__}.\')')

        return None

    # make a pool for all the static members of a class/struct and a function to get a variable
    def genStruct(self, struct, tabs, parentPath):
        tab = '\t'
        mPath = f'{parentPath}.{struct.name.value}'
        self.pathData.append(compPath(struct.name.value, mPath))

        # keep track of all the used names
        varNames = []

        self.write(
            f'\n\n{tab * tabs}class {struct.name.value}:\n{tab * tabs}\tdef __init__(self, *args):\n{tab * tabs}\t\tself.type = STRUCT')

        # parent
        self.write(f'\n{tab * tabs}\t\tself.parent = {parentPath}()')

        # using
        for using in struct.externNameSpaces:
            error = self.genUsing(using, tabs + 2)
            if error:
                return error
        self.write('\n')

        # variables
        for var in struct.variables:
            if not var.name in varNames:
                self.varNames.append(var.name)
                error = self.genVariable(var, 5, mPath)
                if error:
                    return error
            else:
                return Error(f'You cannot use {var.name} twice.', COMP2PYERROR,
                             Position(-1, -1, -1, '', ''), '<comiler>')

        # constructors
        count = 0
        for const in struct.constructors:
            count += 1
            error = self.genConstructor(const, count, 5, mPath)
            if error:
                return error

        # getVar function
        self.write(f'\n\n{tab * tabs}\tdef getVar(self, var):\n{tab * tabs}\t\tcheck = hasattr(self, var)\n{tab * tabs}\t\tif check:\n{tab * tabs}\t\t\tmember = getattr(self, var)\n{tab * tabs}\t\t\tif isinstance(member, Var):\n{tab * tabs}\t\t\t\tif not member.public and not member.static:\n{tab * tabs}\t\t\t\t\traise InvalidAccess(f\'' +
                   '{var}' + f' is not accessable.\')\n{tab * tabs}\t\t\t\telse:\n{tab * tabs}\t\t\t\t\treturn member\n{tab * tabs}\t\telse:\n{tab * tabs}\t\t\traise AttributeError(f\'' + '{var}' + ' does not exist inside {self.__class__.__name__}.\')')

        return None

    def genUsing(self, using, tabs):
        tab = '\t'

        if isinstance(using.name, VarAccess):
            self.write(
                f'\n{tab * tabs}self.{using.name.varName.value.capitalize()} = @!VM!@.{using.name.varName.value}()')
        elif isinstance(using.name, DotAccess):
            dotAccess, lastNamespace = self.genDotaccess(using.name, True)
            self.write(
                f'\n{tab * tabs}self.{lastNamespace.capitalize()} = @!VM!@{dotAccess}()')
        else:
            return Error(f'You can only use a varaccess point inside a using expression.', COMP2PYERROR,
                         Position(-1, -1, -1, '', ''), '<comiler>')

        return None

    def genArgs(self, var):
        value = ''

        for arg in var.args:
            if isinstance(arg, VarAccess):
                value += f'@!VM!@.{arg.varName.value},'
            elif isinstance(arg, DotAccess):
                value += '@!VM!@'
                currAccess = arg
                while isinstance(currAccess, DotAccess) and currAccess.parent.value:
                    value += '.'
                    value += currAccess.parent.value
                    if currAccess.node:
                        currAccess = currAccess.node
                    else:
                        currAccess = currAccess.var.varName.value
                value += '.'
                value += currAccess
                value += ','
            else:
                if isinstance(arg, String):
                    value += f'\'{arg.value.value}\','
                elif isinstance(arg, Bool):
                    value += f'{str(arg.value.value).capitalize()},'
                else:
                    value += f'{arg.value.value},'
        return value

    def genDotaccess(self, var, returnLast=False):
        value = ''

        currAccess = var
        while isinstance(currAccess, DotAccess) and currAccess.parent.value:
            value += '.'
            value += currAccess.parent.value
            if currAccess.node:
                currAccess = currAccess.node
                if isinstance(currAccess, ArgAccess):
                    argAccess = self.genArgaccess(currAccess)
                    value += '.' + argAccess
                    return value
            else:
                currAccess = currAccess.var.varName.value
        value += '.'
        value += currAccess

        if returnLast:
            return value, currAccess
        return value

    def genConstructor(self, const, num, tabs, parentPath):
        tab = '\t'

        # keep track of all the used names
        varNames = []

        # generate args
        self.write('\n')
        argNames = []
        for arg in const.args:
            argCode = 'p_' + self.genHexCode()
            argNames.append(argCode)
            self.write(
                f'\n{tab * tabs}{argCode} = arg(\'{arg.name.value}\', \'{arg.type.value}\')')

        # generating arg list
        list = f'argList{num}'
        listStr = f'\n{tab * tabs}{list} = ['
        for argName in argNames:
            listStr += argName + ','
        listStr += ']'
        self.write(listStr)

        # generate constructor function
        self.write(
            f'\n{tab * tabs}if True == [{list}[x].arg.compareType(args[x]) for x in range(len(list))]:')

        if len(const.variables) > 0 or len(const.body) > 0:
            # variables
            for var in const.variables:
                if not var.name in varNames:
                    self.varNames.append(var.name)
                    error = self.genVariable(var, 6, None)
                    if error:
                        return error
                else:
                    return Error(f'You cannot use {var.name} twice.', COMP2PYERROR,
                                 Position(-1, -1, -1, '', ''), '<comiler>')

            # body
            for part in const.body:
                error = self.genBodyParts(part, 6)
                if error:
                    return error
        else:
            self.write(f'\n{tab * tabs}\tpass')

        return None

    def function(self, func, parentPath):
        pass

    def genBodyParts(self, part, tabs):
        tab = '\t'

        if isinstance(part, DotAccess):
            self.write(f'\n{tab * tabs}@!VM!@.{self.genDotaccess(part)})')
            return None
        elif isinstance(part, ArgAccess):
            self.write(
                f'\n{tab * tabs}@!VM!@.{part.name}({self.genArgs(part)})')
            return None
        elif isinstance(part, BinOpNode):
            self.genBinOp(part.left, part.op, part.right)

        return Error(f'Unknown instruction: couldn\'t compile the instruction properly.', COMP2PYERROR,
                     Position(-1, -1, -1, '', ''), '<comiler>')

    def genBinOp(self, left, op, right):
        tab = '\t'

    def genVariable(self, var, tabs, parentPath):
        tab = '\t'
        if parentPath:
            mPath = f'{parentPath}().getVar(\'{var.name}\')'
            self.pathData.append(compPath(var.name, mPath))

        if isinstance(var.value, AccessPoint):
            if isinstance(var.value, ArgAccess):
                # setting up variable
                self.write(
                    f'\n{tab * tabs}self.{var.name} = Var({var.public}, {var.static}, {var.const}, \'{var.type.value if not isinstance(var.type, str) else var.type}\', \'{var.name}\')')

                # defining variable
                self.write(
                    f'\n{tab * tabs}self.{var.name}.equals(@!VM!@.{var.value.name}({self.genArgs(var.value)}))')
            elif isinstance(var.value, DotAccess):
                # setting up variable
                self.write(
                    f'\n{tab * tabs}self.{var.name} = Var({var.public}, {var.static}, {var.const}, \'{var.type.value if not isinstance(var.type, str) else var.type}\', \'{var.name}\')')

                # defining variable
                self.write(
                    f'\n{tab * tabs}self.{var.name}.equals(@!VM!@{self.genDotaccess(var.value)})')
            elif isinstance(var.value, ListAccess):
                pass
            elif isinstance(var.value, VarAccess):
                # setting up variable
                self.write(
                    f'\n{tab * tabs}self.{var.name} = Var({var.public}, {var.static}, {var.const}, \'{var.type.value if not isinstance(var.type, str) else var.type}\', \'{var.name}\')')

                # defining variable
                self.write(
                    f'\n{tab * tabs}self.{var.name}.equals(@!VM!@.{var.value.varName.value})')
        else:
            # setting up variable
            self.write(
                f'\n{tab * tabs}self.{var.name} = Var({var.public}, {var.static}, {var.const}, \'{var.type.value if not isinstance(var.type, str) else var.type}\', \'{var.name}\')')

            # defining variable
            if var.value:
                if isinstance(var.value, String):
                    self.write(
                        f'\n{tab * tabs}self.{var.name}.equals(\'{var.value.value.value}\')')
                elif isinstance(var.value, Bool):
                    self.write(
                        f'\n{tab * tabs}self.{var.name}.equals({str(var.value.value.value).capitalize()})')
                else:
                    self.write(
                        f'\n{tab * tabs}self.{var.name}.equals({var.value.value.value})')
        return None

################################################################################################################################################################################

class constant:
    def __init__(self, script, accessibility, name, type, value):
        self.script = script
        self.accessibility = accessibility
        self.name = name
        self.type = type
        self.value = value

class compile2Csharp:
    def __init__(self, masterscript, outputdir, projectdir):
        self.outputdir = outputdir
        self.projectdir = projectdir

        # compiler stuff
        self.ms = masterscript
        self.defaultLib = 'libDEFAULTlib'
        self.noneStr = 'None'
        self.outputFile = f'{self.outputdir}output.cs'

        # keeping track of names
        self.currScript = ''
        self.usings = []
        self.classes = []
        self.structs = []
        self.constants = []

        self.basicData = [
            'using System;',
            'using System.Collections;',
            'using System.Collections.Generic;',
        ]

        # Setup output.py
        if os.path.exists(self.outputFile):
            f = open(self.outputFile, 'w')
            f.write('// This is the compiled script of your project.\n\n')
            f.close()
        else:
            f = open(self.outputFile, 'x')
            f.close()

    def write(self, data, print=False):
        f = open(self.outputFile, 'a')
        f.write(data)
        f.close()

        # Open and read the file after the appending
        if print:
            f = open(self.outputFile, 'r')
            print(f.read())
            f.close()

    def isAccessingClass(self, varName):
        for using in self.usings:
            if varName in using:
                return True
        return False
    
    def genUsing(self, using):
        if isinstance(using.name, VarAccess):
            self.usings.append(using.name.varName.value)
            self.write(
                f'\nusing {using.name.varName.value};')
        elif isinstance(using.name, DotAccess):
            dotAccess = self.genDotaccess(using.name)
            self.usings.append(dotAccess)
            self.write(
                f'\nusing {dotAccess};')
        else:
            return Error(f'You can only use a varaccess point inside a using expression.', COMP2CSHARPERROR,
                         Position(-1, -1, -1, '', ''), '<comiler>')

        return None

    def genString(self, var):
        return f'"{var.value.value}"' if len(var.value.value) > 1 else f'\'{var.value.value}\''

    def genNumber(self, var):
        res = str(var.value.value)
        res += 'f' if var.type == FLT else ''
        return res

    def genArgs(self, var):
        value = ''

        currIdx = 0
        maxIdx = len(var.args)
        for arg in var.args:
            currIdx += 1
            if isinstance(arg, VarAccess):
                value += f'{self.genVarAccess(arg)}'
            elif isinstance(arg, DotAccess):
                currAccess = arg
                while isinstance(currAccess, DotAccess) and currAccess.parent.value:
                    value += '.'
                    value += currAccess.parent.value
                    if currAccess.node:
                        currAccess = currAccess.node
                    else:
                        currAccess = currAccess.var.varName.value
                value += '.'
                value += currAccess
            else:
                if isinstance(arg, String):
                    value += f'\'{arg.value.value}\''
                elif isinstance(arg, Bool):
                    value += f'{str(arg.value.value)}'
                elif isinstance(arg, BinOpNode):
                    value += f'{self.genOperationPart(arg)}'
                elif isinstance(arg, UnaryNode):
                    value += f'{self.genOperationPart(arg)}'
                else:
                    value += f'{arg.value.value}'

            if currIdx < maxIdx:
                value += ', '

        return value

    def genArgAccess(self, access):
        Var = access.name
        value = 'new ' if Var in self.classes or Var in self.structs else ''
        value = Var if not Var in self.classes and not Var in self.structs or self.isAccessingClass(Var) else f'new {Var}.{Var}'
        res = f'{value}('

        currIdx = 0
        maxIdx = len(access.args)
        for param in access.args:
            if isinstance(param, Number):
                res += self.genNumber(param)
            elif isinstance(param, String):
                res += self.genString(param)
            elif isinstance(param, VarAccess):
                res += self.genVarAccess(param)
            elif isinstance(param, DotAccess):
                res += self.genDotaccess(param)
            elif isinstance(param, BinOpNode):
                res += self.genBinOp(param.left, param.op, param.right)
            else:
                res += param.value.value

            currIdx += 1
            if currIdx < maxIdx:
                res += ', '

        res += ')'
        return res

    def genDotaccess(self, var):
        value = ''

        currIdx = 0
        currAccess = var 
        while isinstance(currAccess, DotAccess) and currAccess.parent.value:
            value += '.' if currIdx > 0 else ''
            currIdx += 1

            value += currAccess.parent.value
            if currAccess.node:
                currAccess = currAccess.node
                if isinstance(currAccess, ArgAccess):
                    argAccess = self.genArgAccess(currAccess)
                    value += '.' + argAccess
                    return value
            else:
                currAccess = currAccess.var.varName.value
        value += '.'
        
        if isinstance(currAccess, ReasignVar):
            value += f'{currAccess.name.varName} {currAccess.op.value} {self.genOperationPart(currAccess.value)}'
            return value
        
        value += currAccess

        return value

    def genListAccess(self, var):
        return f'{var.name}[{var.elementIdx.value}]'

    def genVarAccess(self, var):
        value = var.varName.value
        for const in self.constants:
            if const.accessibility:
                if const.name == value:
                    return f'___Global___.{const.script.lib}_{value}'
            if not const.accessibility:
                if const.name == value and const.script.name == self.currScript:
                    return f'___Global___.{const.script.lib}_{const.script.name}_{value}'
        
        value = value if not value in self.classes and not value in self.structs or self.isAccessingClass(value) else f'{value}.{value}'
        return value 

    def genUnaryOp(self, op, node):
        return f'{op.value}{self.genOperationPart(node)}'

    def genBinOp(self, left, op, right):
        opValue = op.value if not op.value == ISEQUALTO else EQEQ
        
        if op.value == TOCODE:
            return f'({self.genOperationPart(right)} as {self.genOperationPart(left)})'    
        return f'{self.genOperationPart(left)} {opValue} {self.genOperationPart(right)}'

    def genTypeOf(self, type):
        return f'{self.convertTypeof2String(type.value)}'

    def genReasign(self, name, op, value):
        if op.value == PLUSPLUS:
            return f'{name}++'
        elif op.value == MINUSMINUS:
            return f'{name}--'
        return f'{name} {op.value} {self.genOperationPart(value)}'

    def genReturn(self, _return):
        if _return.returnValue == VOID:
            self.write('\nreturn;')
        else:
            self.write(f'\nreturn {self.genOperationPart(_return.returnValue)};')

    def genContinue(self):
        self.write('\ncontinue;')

    def genBreak(self):
        self.write('\nbreak;')
    
    def genForLoop(self, loop):
        self.write(f'\nfor ({self.genVariable(loop.variable, True, True)} {self.genOperationPart(loop.condition)}; {self.genReasign(loop.steps.name.varName, loop.steps.op, loop.steps.value)})' + '\n{\n')
        
        # body
        for part in loop.body:
            error = self.genBodyParts(part)
            if error:
                return error
        
        self.write('\n}')
        return None
    
    def genWhileLoop(self, loop):
        if loop.do:
            self.write('\ndo \n{\n')
        else:
            self.write(f'\nwhile ({self.genOperationPart(loop.condition)})' + '\n{\n')
            
        # body
        for part in loop.body:
            error = self.genBodyParts(part)
            if error:
                return error
        
        if loop.do:
            self.write('\n}' + f' while ({self.genOperationPart(loop.condition)});')
        else:
            self.write('\n}')
            
        return None
        
    def genIf(self, If):
        self.write(f'\nif ({self.genOperationPart(If.condition)})' + '\n{\n')
        
        # body
        for part in If.body:
            error = self.genBodyParts(part)
            if error:
                return error
        
        self.write('\n}')
        
        for _elif in If.cases:
            self.write(f'\nelse if ({self.genOperationPart(_elif.condition)})' + '\n{\n')

            # body
            for part in _elif.body:
                error = self.genBodyParts(part)
                if error:
                    return error
            
            self.write('\n}')
            
        if If.elseCase:
            self.write('\nelse\n{\n')

            # body
            for part in If.elseCase.body:
                error = self.genBodyParts(part)
                if error:
                    return error
            
            self.write('\n}')
            
        return None
    
    def genOperationPart(self, part):
        res = ''

        if isinstance(part, DotAccess):
            res = self.genDotaccess(part)
        elif isinstance(part, ArgAccess):
            res = self.genArgAccess(part)
        elif isinstance(part, ListAccess):
            res = self.genListAccess(part)
        elif isinstance(part, VarAccess):
            res = self.genVarAccess(part)
        elif isinstance(part, Number):
            res = self.genNumber(part)
        elif isinstance(part, String):
            res = self.genString(part)
        elif isinstance(part, BinOpNode):
            res = f'({self.genBinOp(part.left, part.op, part.right)})'
        elif isinstance(part, UnaryNode):
            res = self.genUnaryOp(part.op, part.node)
        elif isinstance(part, str):
            res = part
        elif isinstance(part, TypeOf):
            res = self.genTypeOf(part)
        else:
            res = part.value.value

        return res

    def convertType2String(self, type):
        if type == BYT:
            return 'byte'
        elif type == FLT:
            return 'float'
        elif type == INT:
            return 'int'
        elif type == DBL:
            return 'double'
        elif type == BOL:
            return 'bool'
        elif type == STR:
            return 'string'
        elif type == CHR:
            return 'char'
        elif type == TYP:
            return 'Type'
        elif type == VAR:
            return 'var'
        elif type == OBJ:
            return 'object'
        elif type == LST:
            return 'Array'
        elif type == VOID:
            return 'void'
        elif isinstance(type, str):
            return type + '.' + type if not self.isAccessingClass(type) else type
        else:
            return type.value + '.' + type.value if not self.isAccessingClass(type.value) else type.value 

    def convertTypeof2String(self, type):
        if type == 'BYT':
            return 'byte'
        elif type == 'CHR':
            return 'char'
        elif type == 'STR':
            return 'string'
        elif type == 'INT':
            return 'int'
        elif type == 'FLT':
            return 'float'
        elif type == 'DBL':
            return 'double'
        elif type == 'BOL':
            return 'bool'
        elif type == 'TYP':
            return 'Type'
        elif type == 'LST':
            return 'Array'

    def genBodyParts(self, part):
        if isinstance(part, DotAccess):
            self.write(f'\n{self.genDotaccess(part)};')
            return None
        elif isinstance(part, ArgAccess):
            self.write(f'\n{part.name}({self.genArgs(part)});')
            return None
        elif isinstance(part, BinOpNode):
            self.write(f'\n{self.genBinOp(part.left, part.op, part.right)};')
            return None
        elif isinstance(part, ReasignVar):
            if isinstance(part.name, str):
                self.write(
                    f'\n{self.genReasign(part.name, part.op, part.value)};')
            elif isinstance(part.name, ListAccess):
                 self.write(
                    f'\n{self.genReasign(self.genOperationPart(part.name), part.op, part.value)};')
            else:
                self.write(
                    f'\n{self.genReasign(part.name.varName, part.op, part.value)};')
            return None
        elif isinstance(part, Variable) or isinstance(part, List):
            self.genVariable(part, True)
            return None
        elif isinstance(part, Function):
            error = self.genFunc(part)
            if error:
                error
            return None
        elif isinstance(part, Return):
            self.genReturn(part)
            return None
        elif isinstance(part, Break):
            self.genBreak()
            return None
        elif isinstance(part, Continue):
            self.genContinue()
            return None
        elif isinstance(part, For):
            error = self.genForLoop(part)
            if error:
                error
            return None
        elif isinstance(part, While):
            self.genWhileLoop(part)
            return None
        elif isinstance(part, If):
            self.genIf(part)
            return None
        
        return Error(f'Unknown instruction: couldn\'t compile the instruction properly.', COMP2CSHARPERROR,
                     Position(-1, -1, -1, '', ''), '<comiler>')

    def compile(self):
        # Write all the basic data into the script
        for data in self.basicData:
            self.write(data)
            self.write('\n')
        self.write('\n' + '/' * 200)

        # Start with libs
        for lib in self.ms.libs:
            self.write('\n\n')
            self.write(
                f'namespace {lib.name} ' + '\n{\n')

            # Generate all script classes
            for script in lib.scripts:
                self.currScript = script.name
                error = self.genScript(script)
                if error:
                    return error
            self.write('\n}\n')

        # Generating the global class
        self.write(f'\npublic static class ___Global___' + '\n{\n')
        for const in self.constants:
            tokens = const.script.lib
            tokens += '_' + const.script.name if not const.accessibility else ''
            self.write(f'\npublic static {const.type} {tokens}_{const.name} = {const.value};')
        self.write('\n}')
        
        print('Successfully compiled the project!')
        return None

    def genScript(self, script):
        self.write(f'namespace {script.name}' + '\n{\n')

        # Give necessary information to the compiler
        for _class in script.global_classes:
            if (_class.name.value in self.classes):
                return Error(f'({self.currScript}) You\'re not allowed to define two classes with the same name [{_class.name.value}].', COMP2CSHARPERROR,
                         Position(-1, -1, -1, '', ''), '<comiler>')
            self.classes.append(_class.name.value)
            
        for struct in script.global_structs:
            if (struct.name.value in self.structs):
                return Error(f'({self.currScript}) You\'re not allowed to define two structs with the same name [{struct.name.value}].', COMP2CSHARPERROR,
                         Position(-1, -1, -1, '', ''), '<comiler>')
            self.structs.append(struct.name.value)

        # imports
        for imp in script.imports:
            self.write(f'\nusing {imp.value};')

        # global_variables
        for var in script.global_variables:
            self.genGlobalVar(script, var)

        # namespaces
        for namespace in script.namespaces:
            error = self.genNamespace(namespace)
            if error:
                return error

        # classes
        for _class in script.global_classes:
            error = self.genClass(_class)
            if error:
                return error

        # structs
        for struct in script.global_structs:
            error = self.genStruct(struct)
            if error:
                return error

        self.write('\n}')
        return None

    def genNamespace(self, namespace):
        self.write(f'\nnamespace {namespace.name.value}' + '\n{\n')

        # Give necessary information to the compiler
        for _class in namespace.classes:
            if (_class.name.value in self.classes):
                return Error(f'({self.currScript}) You\'re not allowed to define two classes with the same name [{_class.name.value}].', COMP2CSHARPERROR,
                         Position(-1, -1, -1, '', ''), '<comiler>')
            self.classes.append(_class.name.value)
            
        for struct in namespace.structs:
            if (struct.name.value in self.structs):
                return Error(f'({self.currScript}) You\'re not allowed to define two structs with the same name [{struct.name.value}].', COMP2CSHARPERROR,
                         Position(-1, -1, -1, '', ''), '<comiler>')
            self.structs.append(struct.name.value)

        
        # child namespaces
        for childNamespace in namespace.childSpaces:
            error = self.genNamespace(childNamespace)
            if error:
                return error

        # classes
        for _class in namespace.classes:
            error = self.genClass(_class)
            if error:
                return error

        # structs
        for struct in namespace.structs:
            error = self.genStruct(struct)
            if error:
                return error

        self.write('\n}')
        return None

    def genClass(self, _class):
        attributes = ''
        attributes += 'public ' if _class.public else 'private '
        attributes += 'static ' if _class.static else ''
        self.write(f'\nnamespace {_class.name.value}' + '\n{\n')

        # using
        self.usings = []
        for using in _class.externNameSpaces:
            error = self.genUsing(using)
            if error:
                return error
        self.write('\n')

        self.write(f'\n{attributes}class {_class.name.value}' + '\n{\n')

        # variables
        for var in _class.variables:
            error = self.genVariable(var)
            if error:
                return error

        # constructors
        for constructor in _class.constructors:
            error = self.genConstructor(constructor, _class)
            if error:
                return error

        # body
        for part in _class.body:
            error = self.genBodyParts(part)
            if error:
                return error

        self.write('\n}')
        self.write('\n}')
        return None

    def genStruct(self, struct):
        self.write(f'\nnamespace {struct.name.value}' + '\n{\n')

        # using
        for using in struct.externNameSpaces:
            error = self.genUsing(using)
            if error:
                return error
        self.write('\n')

        self.write(f'\npublic struct {struct.name.value}' + '\n{\n')

        # variables
        for var in struct.variables:
            error = self.genVariable(var)
            if error:
                return error

        # constructors
        for constructor in struct.constructors:
            error = self.genConstructor(constructor, struct)
            if error:
                return error

        self.write('\n}')
        self.write('\n}')
        return None

    def genConstructor(self, constructor, parent):
        self.write(f'\npublic {parent.name.value}(')

        currIdx = 0
        maxIdx = len(constructor.args)
        for arg in constructor.args:
            type = self.convertType2String(arg.type.value)
            self.write(f'{type} {arg.name.value}')

            currIdx += 1
            if currIdx < maxIdx:
                self.write(', ')
        self.write(')\n{\n')

        # body
        for part in constructor.body:
            error = self.genBodyParts(part)
            if error:
                return error

        self.write('\n}')
        return None

    def genFunc(self, func):
        attributes = ''
        attributes += 'public ' if func.public else 'private '
        attributes += 'static ' if func.static else ''
        #attributes += 'protected ' if func.protected else ''
        self.write(f'\n{attributes}{self.convertType2String(func.returnType.value)} {func.name.value}(')

        if func.name.value == 'Main':
            self.write('string[] args)\n{\n')
        else:
            currIdx = 0
            maxIdx = len(func.args)
            for arg in func.args:
                type = self.convertType2String(arg.type.value)
                self.write(f'{type} {arg.name.value}')

                currIdx += 1
                if currIdx < maxIdx:
                    self.write(', ')
            self.write(')\n{\n')

        # body
        for part in func.body:
            error = self.genBodyParts(part)
            if error:
                return error

        self.write('\n}')
        return None

    def getVarType(self, var):
        return self.convertType2String(var.value.type)
    
    def getVarValue(self, var):
        value = var.value.value.value
        if var.value.type == FLT:
            return str(value) + 'f'
        elif isinstance(value, str):
            return f'"{value}"' if len(value) > 1 else f"'{value}'"
        else:
            return var.value.value.value

    def genVariable(self, var, inBody=False, _return=False):
        # Setup variable
        attributes = ''
        attributes += 'public ' if var.public and not inBody else ''
        attributes += 'private ' if not var.public and not inBody else ''
        attributes += 'static ' if var.static else ''
        attributes += 'const ' if var.const else ''
        if isinstance(var, List):
            self.write(
                f'\n{attributes}{self.convertType2String(var.type)}[] {var.name}')

            if isinstance(var.elements, ListSpace):
                if not var.elements.elements == None:
                    self.write(' = {')

                    currIdx = 0
                    maxIdx = len(var.elements.elements)
                    for e in var.elements.elements:
                        currIdx += 1

                        self.write(f' {self.genOperationPart(e)}')
                        if currIdx < maxIdx:
                            self.write(',')

                    self.write(' };')
                else:
                    self.write(f' = new {var.type}[{var.elements.length}];')
            else:
                print('Other list value type! Unexpected!!!!')

            return None
        
        variable = f'{attributes}{self.convertType2String(var.type)} {var.name}'

        if isinstance(var.value, AccessPoint):
            if isinstance(var.value, ArgAccess):
                Var = var.value.name
                res = 'new ' if Var in self.classes or Var in self.structs else ''
                res += Var if not Var in self.classes and not Var in self.structs or self.isAccessingClass(Var) else f'{Var}.{Var}'
                variable += f' = {res}({self.genArgs(var.value)});';
            elif isinstance(var.value, DotAccess):
                variable += f' = {self.genDotaccess(var.value)};'
            elif isinstance(var.value, ListAccess):
                variable += f' = {self.genListAccess(var.value)};'
            elif isinstance(var.value, VarAccess):
                variable += f' = {self.genVarAccess(var.value)};'
        else:
            if var.value:
                if isinstance(var.value, String):
                    variable += f' = {self.genString(var.value)};'
                elif isinstance(var.value, Number):
                    variable += f' = {self.genNumber(var.value)};'
                elif isinstance(var.value, str):
                    variable += f' = {var.value};'
                elif isinstance(var.value, BinOpNode):
                    variable += f' = {self.genOperationPart(var.value)};'
                elif isinstance(var.value, UnaryNode):
                    variable += f' = {self.genOperationPart(var.value)};'
                else:
                    variable += f' = {var.value.value.value};'
            else:
                variable += ';'

        if _return:
            return variable
        else:
            self.write('\n' + variable)
            
        return None

    def genGlobalVar(self, script, var):
        name = var.name
        type = self.getVarType(var)
        value = self.getVarValue(var)
        
        self.constants.append(constant(script, var.public, name, type, value))
        
####################
# - Run Function - #
####################


def openFile(projectdir, fn):
    try:
        with open(f'{projectdir}/{fn}{fileType}', "r") as f:
            script = f.read()
            f.close()
            return script, None
    except Exception as e:
        return None, Error(e, PYTHON_EXCEPTION, Position(0, -1, -1, fn, ""), fn)


def run(projectdir):
    # Reset data
    global masterscript, metacode, usedLibs, outputdir
    masterscript = MasterScript([])
    usedLibs = []

    # Parsing the project
    error = ParseScripts(projectdir)
    if error:
        return error
    error = ParseExternLibraries()
    if error:
        return error

    # Compiling the project
    compiler = compile2Csharp(masterscript, outputdir, projectdir)
    error = compiler.compile()
    if error:
        return error

    return None


# TODOs (compile2python):
#
# - make sure the libraries of all scripts get compined if they have the same name!
# - constructors
# - lists
# - make new 'pathfinding' algorithm
# - currently everything is allways accassable!
# - refactor the dotproduct > make a 'getVar()' function that return the requested varaible if possible (checks for the variables existance, static "state" and so on...)
# - metacode
#

# TODOs (compile2csharp):
#
# - OverrideFunction
# - Metacode
# - Cannot have private classes
# - Import is kind of broken? Importing another lib will not give access to it.
#

