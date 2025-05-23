from abc import ABC, abstractmethod
from typing import Callable, Tuple, List
from enum import Enum


class AstNode(ABC):
    @property
    def childs(self) -> Tuple['AstNode', ...]:
        return ()

    def add_child(self, *ch):
        self.childs += ch

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    def tree(self) -> [str, ...]:
        res = [str(self)]
        childs = self.childs
        for i, child in enumerate(childs):
            ch0, ch = '├', '│'
            if i == len(childs) - 1:
                ch0, ch = '└', ' '
            res.extend(((ch0 if j == 0 else ch) + ' ' + s for j, s in enumerate(child.tree)))
        return res

    def visit(self, func: Callable[['AstNode'], None]) -> None:
        func(self)
        for child in self.childs:
            child.visit(func)

    def __getitem__(self, index):
        return self.childs[index] if index < len(self.childs) else None


class ValueNode(AstNode):
    pass


class NumNode(ValueNode):
    def __init__(self, num: float):
        super().__init__()
        self.num = float(num)

    def __str__(self) -> str:
        return str(self.num)


class IdentNode(ValueNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = str(name)

    def __str__(self) -> str:
        return str(self.name)


class BoolValueNode(ValueNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = str(name)

    def __str__(self) -> str:
        return str(self.name)


class BinOp(Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    MOD = '%'
    GT = '>'
    LT = '<'
    GE = '>='
    LE = '<='
    EQUALS = '=='
    NOTQUALS = '!='
    AND = '&&'
    OR = '||'


class BinOpNode(ValueNode):
    def __init__(self, op: BinOp, arg1: ValueNode, arg2: ValueNode):
        super().__init__()
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2

    @property
    def childs(self) -> Tuple[ValueNode, ValueNode]:
        return self.arg1, self.arg2

    def __str__(self) -> str:
        return str(self.op.value)


class UnOp(Enum):
    SUB = '-'
    NOT = '!'


class UnOpNode(ValueNode):
    def __init__(self, op: UnOp, arg: ValueNode):
        super().__init__()
        self.op = op
        self.arg = arg

    @property
    def childs(self) -> Tuple[ValueNode]:
        return self.arg,

    def __str__(self) -> str:
        return str(self.op.value)


class ExprListNode(AstNode):
    def __init__(self, *exprs: AstNode):
        super().__init__()
        self.exprs = exprs

    @property
    def childs(self) -> Tuple[AstNode]:
        return self.exprs

    def add_child(self, ch):
        self.exprs = self.exprs + (ch,)

    def __str__(self) -> str:
        return '...'


class AssignNode(ValueNode):
    def __init__(self, var: IdentNode, val: ValueNode):
        super().__init__()
        self.var = var
        self.val = val

    @property
    def childs(self) -> Tuple[IdentNode, ValueNode]:
        return self.var, self.val

    def __str__(self) -> str:
        return '='


class OutputNode(AstNode):
    def __init__(self, arg: ValueNode):
        super().__init__()
        self.args = [arg] if arg is not None else []

    def add_child(self, ch):
        if ch is not None:
            self.args.insert(0, ch)

    @property
    def childs(self) -> tuple:
        return tuple(self.args)

    def __str__(self) -> str:
        return 'cout'


class InputNode(AstNode):
    def __init__(self, var: IdentNode):
        self.var = var

    @property
    def childs(self) -> Tuple[IdentNode]:
        return self.var,

    def __str__(self) -> str:
        return 'cin'


class IfNode(AstNode):
    def __init__(self, cond: ValueNode, then_: AstNode, else_: AstNode = None):
        self.cond = cond
        self.then_ = then_
        self.else_ = else_

    @property
    def childs(self) -> Tuple[ValueNode]:
        res = [self.cond, self.then_]
        if self.else_:
            res.append(self.else_)
        return tuple(res)

    def __str__(self) -> str:
        return 'if'


class ForNode(AstNode):
    def __init__(self, init: AstNode, cond: ValueNode, step: AstNode, body: AstNode):
        self.init = init
        self.cond = cond
        self.step = step
        self.body = body

    @property
    def childs(self) -> Tuple[ValueNode]:
        return self.init, self.cond, self.step, self.body

    def __str__(self) -> str:
        return 'for'


class WhileNode(AstNode):
    def __init__(self, cond: ValueNode, body: AstNode):
        self.cond = cond
        self.body = body

    @property
    def childs(self) -> Tuple[ValueNode]:
        return self.cond, self.body

    def __str__(self) -> str:
        return 'while'


class DoWhileNode(AstNode):
    def __init__(self, body: AstNode, cond: ValueNode):
        self.body = body
        self.cond = cond

    @property
    def childs(self) -> Tuple[ValueNode]:
        return self.body, self.cond

    def __str__(self) -> str:
        return 'do while'


class IdentificationNode(AstNode):
    def __init__(self, type_: str, name: ValueNode, value: ValueNode = None):
        self.type_ = type_
        self.name = name
        self.value = value

    @property
    def childs(self) -> Tuple[ValueNode]:
        res = [self.name]
        if self.value:
            res.append(self.value)
        return tuple(res)

    def __str__(self) -> str:
        return str(self.type_)


class ArrayElementsNode(AstNode):
    def __init__(self):
        super().__init__()
        self.elements = []

    def add_child(self, child):
        if child is not None:
            self.elements.append(child)

    @property
    def childs(self):
        return tuple(self.elements)

    def __str__(self):
        return "ArrayElements"


class ArrayDeclarationNode(AstNode):
    def __init__(self, type_name, name, size, init=None):
        super().__init__()
        self.type = type_name
        self.name = name
        self.size = size
        self.init = init

    @property
    def childs(self):
        if self.init:
            return (self.init,)
        return ()

    def __str__(self):
        return f"Array[{self.type}][{self.size}]"


class ArrayAccessNode(AstNode):
    def __init__(self, array_name, index):
        super().__init__()
        self.array_name = array_name
        self.index = index

    @property
    def childs(self):
        return (self.index,)

    def __str__(self):
        return f"ArrayAccess[{self.array_name}]"


class SystemFunctionNode(ValueNode):
    def __init__(self, func_name, arg):
        super().__init__()
        self.func_name = func_name
        self.arg = arg

    @property
    def childs(self):
        return (self.arg,)

    def __str__(self):
        return f"system_function {self.func_name}"


class ProgramNode(AstNode):
    def __init__(self, includes: List['IncludeNode'], using_stmt: 'UsingNode', main_function: 'MainFunctionNode'):
        super().__init__()
        self.includes = includes
        self.using_stmt = using_stmt
        self.main_function = main_function

    @property
    def childs(self) -> Tuple['AstNode', ...]:
        return tuple(self.includes) + (self.using_stmt, self.main_function)

    def __str__(self) -> str:
        return "Program"


class IncludeNode(AstNode):
    def __init__(self, header: str):
        super().__init__()
        self.header = header

    def __str__(self) -> str:
        return f"#include <{self.header}>"


class UsingNode(AstNode):
    def __str__(self) -> str:
        return "using namespace std"


class MainFunctionNode(AstNode):
    def __init__(self, body: 'ExprListNode'):
        super().__init__()
        self.body = body

    @property
    def childs(self) -> Tuple['AstNode', ...]:
        return (self.body,)

    def __str__(self) -> str:
        return "main"


class StringNode(ValueNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return f'"{self.value}"'


class CharNode(ValueNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return f"'{self.value}'"


class IncrementDecrementNode(AstNode):
    def __init__(self, ident, op):
        super().__init__()
        self.ident = ident
        self.op = op

    @property
    def childs(self):
        return (self.ident,)

    def __str__(self):
        return self.op


class ReturnNode(AstNode):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    @property
    def childs(self):
        return (self.expr,)

    def __str__(self):
        return "return"


class FunctionCallNode(ValueNode):
    def __init__(self, name, args):
        super().__init__()
        self.name = name
        self.args = args

    @property
    def childs(self):
        return tuple(self.args)

    def __str__(self):
        return f"call {self.name}"


class ParameterNode(AstNode):
    def __init__(self, type_name, name):
        super().__init__()
        self.type = type_name
        self.name = name

    @property
    def childs(self):
        return ()

    def __str__(self):
        return f"{self.type} {self.name}"


class FunctionNode(AstNode):
    def __init__(self, return_type, name, params, body):
        super().__init__()
        self.return_type = return_type
        self.name = name
        self.params = params
        self.body = body

    @property
    def childs(self):
        return tuple(self.params) + (self.body,)

    def __str__(self):
        return f"function {self.name}"


class ParserError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
