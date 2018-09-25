# py-lisp

A simple python lisp interpreter that implements a subset of the lisp language.

Since type-annotations have been used, the implementation only supports python 3.

## Usage

Standard mode: 
```Python
from lisp import run

program = "(print (max 1 5))"

run(program)
```

REPL mode: 
```
python3 lisp.py
```

## Implemented Standard Operations
```python
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
```