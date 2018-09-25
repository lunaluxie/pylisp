import math
import operator

Symbol      = str              
Number      = (int, float)
Atom        = (Symbol, Number) 
List        = list
Expression  = (Atom, List)     
Environment = dict

def tokenize(chars: str) -> list:
    """Convert a string of characters into a list of tokens
    
    Tokens table:
        Symbol = str              
        Number = (int, float)
        Atom   = (Symbol, Number) 
        List   = list
        Exp    = (Atom, List)     
        Env    = dict

    Args:
        chars (str): The characters to tokenize
    
    Returns:
        list: The tokens
    """
    return chars.replace('(',' ( ').replace(')', ' ) ').split()


def parse(program: str) -> Expression:
    """Parse program
    
    Args:
        program (str): Program to parse
    
    Returns:
        Expression
    """
    return read_from_tokens(tokenize(program))


def read_from_tokens(tokens: list) -> Expression:
    """Read an expression from tokens
    
    Args:
        tokens (list): The tokens to interpret
    
    Returns:
        Expression
    """
    if len(tokens) == 0:
        raise SyntaxError("unexpected EOF")
    
    token = tokens.pop(0)
    if token == '(':
        # Enter inner evaluation loop
        L = []
        while tokens[0] != ')': # end of loop condition
            L.append(read_from_tokens(tokens))
        tokens.pop(0)
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)


def atom(token: str) -> Atom:
    """Atomize token.

    Numbers become numbers, everything else symbols
    
    Args:
        token (str): The token to atomize
    
    Returns:
        Atom
    """
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)


def standard_environment() -> Environment:
    """An environment with standard procedures
    
    Returns:
        Environment
    """
    env = Environment()
    env.update(vars(math)) # sin, cos, sqrt, pi, ...
    env.update({
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '=': operator.eq,
        'abs': abs,
        'append': operator.add,
        'apply': lambda proc, args: proc(*args),
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        'cons':    lambda x,y: [x] + y,
        'eq?':     operator.is_, 
        'expt':    pow,
        'equal?':  operator.eq, 
        'length':  len, 
        'list':    lambda *x: List(x), 
        'list?':   lambda x: isinstance(x, List), 
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     operator.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, Number),  
		'print':   print,
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

global_env = standard_environment()

def eval(x: Expression, env:Environment=global_env) -> Expression:
    """Evaluate an expression in an environment
    
    Args:
        x (Expression): Expression to evaluate
        env (Environment, optional): Defaults to global_env.
    
    Returns:
        Expression: Answer
    """
    if isinstance(x, Symbol): # Variable
        return env[x]
    elif isinstance(x, Number): # Number
        return x
    elif x[0] == 'if': # Conditional
        _, test, conseq, alt = x
        exp = conseq if eval(test,env) else alt
        return eval(exp, env)
    elif x[0] == 'define': # Definition
        _, symbol, exp = x
        env[symbol] = eval(exp, env)
    else: # Procedure call
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)

def schemestr(exp:Expression) -> str:
    """Convert a Python object back into a Scheme-readable string.
    
    Args:
        exp (Expression): Expression to print
    
    Returns:
        str: Scheme-friendly string
    """

    if isinstance(exp, List):
        return '(' + ' '.join(map(schemestr, exp)) + ')' 
    else:
        return str(exp)

def run(program:str):
    return eval(parse(program))

def repl(prompt:str='pylisp> '):
    """A REPL implementation
        prompt (str, optional): Defaults to 'pylisp> '.
    """
    while True:
        val = eval(parse(input(prompt)))
        if val is not None:
            print(schemestr(val))


if __name__ == "__main__":
    repl()