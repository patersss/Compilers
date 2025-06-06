from typing import Dict, List, Set, Optional
from ast_nodes import *
from dataclasses import dataclass
from enum import Enum

class VariableType(Enum):
    INT = "int"
    BOOL = "bool"
    CHAR = "char"
    STRING = "string"
    ARRAY = "array"

@dataclass
class Variable:
    name: str
    type: VariableType
    is_initialized: bool = False
    scope_level: int = 0
    is_global: bool = False

class Scope:
    def __init__(self, parent: Optional['Scope'] = None):
        self.variables: Dict[str, Variable] = {}
        self.parent = parent
        self.level = 0 if parent is None else parent.level + 1

    def add_variable(self, var: Variable) -> bool:
        if var.name in self.variables:
            return False
        var.scope_level = self.level
        self.variables[var.name] = var
        return True

    def get_variable(self, name: str) -> Optional[Variable]:
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get_variable(name)
        return None

class SemanticError(Exception):
    def __init__(self, message: str, line: int = None):
        self.message = message
        self.line = line
        super().__init__(f"Семантическая ошибка: {message}" + (f" в строке {line}" if line else ""))

class SemanticAnalyzer:
    def __init__(self):
        self.current_scope = Scope()
        self.errors: List[SemanticError] = []
        self.in_loop = False
        self.in_function = False
        self.known_system_identifiers = {
            "cout", "cin", "endl", "abs",
            "printf", "scanf", "main",
            "true", "false", "NULL"
        }

    def analyze(self, node: AstNode) -> List[SemanticError]:
        try:
            self.visit(node)
        except Exception as e:
            self.errors.append(SemanticError(f"Ошибка при анализе: {str(e)}"))
        return self.errors

    def visit(self, node):
        try:
            # Если это строка-идентификатор, проверяем её существование
            if isinstance(node, str):
                if node not in self.known_system_identifiers:
                    # Это может быть идентификатор переменной, проверим его наличие
                    var = self.current_scope.get_variable(node)
                    if not var:
                        self.errors.append(SemanticError(f"Использование необъявленного идентификатора: {node}"))
                return
            # Если это число, char, bool, просто пропускаем
            if isinstance(node, (int, float, bool)):
                return
            # Если это None, пропускаем
            if node is None:
                return
            # Если это не AstNode, пропускаем
            if not isinstance(node, AstNode):
                return
            method_name = f'visit_{node.__class__.__name__}'
            visitor = getattr(self, method_name, self.generic_visit)
            visitor(node)
        except Exception as e:
            self.errors.append(SemanticError(f"Ошибка при обработке узла: {str(e)}"))

    def generic_visit(self, node: AstNode):
        for child in node.childs:
            if isinstance(child, AstNode):
                self.visit(child)

    def visit_ProgramNode(self, node: ProgramNode):
        self.visit(node.main_function)

    def visit_MainFunctionNode(self, node: MainFunctionNode):
        old_scope = self.current_scope
        self.current_scope = Scope(old_scope)
        old_in_function = self.in_function
        self.in_function = True
        self.visit(node.body)
        self.current_scope = old_scope
        self.in_function = old_in_function

    def visit_FunctionNode(self, node: FunctionNode):
        old_scope = self.current_scope
        self.current_scope = Scope(old_scope)
        old_in_function = self.in_function
        self.in_function = True
        
        # Обработка параметров функции
        for param in node.params:
            if not isinstance(param, ParameterNode):
                self.errors.append(SemanticError("Некорректный узел параметра функции"))
                continue
                
            if not isinstance(param.name, IdentNode):
                self.errors.append(SemanticError("Некорректный идентификатор в параметре функции"))
                continue
                
            var = Variable(param.name.name, self._get_type_from_string(param.type))
            if not self.current_scope.add_variable(var):
                self.errors.append(SemanticError(f"Дублирование параметра функции: {param.name.name}"))
        
        self.visit(node.body)
        self.current_scope = old_scope
        self.in_function = old_in_function

    def visit_IdentificationNode(self, node: IdentificationNode):
        if not isinstance(node.name, IdentNode):
            self.errors.append(SemanticError("Некорректный идентификатор в объявлении переменной"))
            return
        var_name = node.name.name
        var_type = self._get_type_from_string(node.type_)
        var = Variable(var_name, var_type, is_global=not self.in_function)
        if not self.current_scope.add_variable(var):
            self.errors.append(SemanticError(f"Переменная {var_name} уже объявлена в текущей области видимости"))
        if node.value and isinstance(node.value, AstNode):
            self.visit(node.value)

    def visit_ForNode(self, node: ForNode):
        old_scope = self.current_scope
        self.current_scope = Scope(old_scope)
        old_in_loop = self.in_loop
        self.in_loop = True
        self.visit(node.init)
        self.visit(node.cond)
        self.visit(node.step)
        self.visit(node.body)
        self.current_scope = old_scope
        self.in_loop = old_in_loop

    def visit_WhileNode(self, node: WhileNode):
        old_scope = self.current_scope
        self.current_scope = Scope(old_scope)
        old_in_loop = self.in_loop
        self.in_loop = True
        self.visit(node.cond)
        self.visit(node.body)
        self.current_scope = old_scope
        self.in_loop = old_in_loop

    def visit_DoWhileNode(self, node: DoWhileNode):
        old_scope = self.current_scope
        self.current_scope = Scope(old_scope)
        old_in_loop = self.in_loop
        self.in_loop = True
        self.visit(node.body)
        self.visit(node.cond)
        self.current_scope = old_scope
        self.in_loop = old_in_loop

    def visit_IdentNode(self, node: IdentNode):
        if not hasattr(node, 'name'):
            self.errors.append(SemanticError("Некорректный идентификатор"))
            return
        var = self.current_scope.get_variable(node.name)
        if not var and node.name not in self.known_system_identifiers:
            self.errors.append(SemanticError(f"Использование необъявленной переменной: {node.name}"))
        elif self.in_loop and var and var.scope_level > self.current_scope.level:
            self.errors.append(SemanticError(f"Попытка доступа к переменной {node.name} из цикла вне её области видимости"))

    def visit_AssignNode(self, node: AssignNode):
        if isinstance(node.var, IdentNode):
            var = self.current_scope.get_variable(node.var.name)
            if not var:
                self.errors.append(SemanticError(f"Присваивание необъявленной переменной: {node.var.name}"))
            elif self.in_loop and var.scope_level > self.current_scope.level:
                self.errors.append(SemanticError(f"Попытка присваивания переменной {node.var.name} из цикла вне её области видимости"))
        self.visit(node.val)

    def visit_FunctionCallNode(self, node: FunctionCallNode):
        for arg in node.args:
            self.visit(arg)

    def visit_ExprListNode(self, node: ExprListNode):
        for expr in node.exprs:
            self.visit(expr)

    def visit_ArrayAccessNode(self, node: ArrayAccessNode):
        self.visit(node.index)

    def visit_ArrayDeclarationNode(self, node: ArrayDeclarationNode):
        if not isinstance(node.name, IdentNode):
            self.errors.append(SemanticError("Некорректный идентификатор в объявлении массива"))
            return
        name = node.name.name
        var = Variable(name, self._get_type_from_string(node.type), is_global=not self.in_function)
        if not self.current_scope.add_variable(var):
            self.errors.append(SemanticError(f"Массив {name} уже объявлен в текущей области видимости"))
        if node.init:
            self.visit(node.init)

    def visit_SystemFunctionNode(self, node: SystemFunctionNode):
        self.visit(node.arg)

    def visit_IncrementDecrementNode(self, node: IncrementDecrementNode):
        self.visit(node.ident)

    def visit_ReturnNode(self, node: ReturnNode):
        if not self.in_function:
            self.errors.append(SemanticError("Оператор return вне функции"))
        if node.expr:
            self.visit(node.expr)

    def _get_type_from_string(self, type_str: str) -> VariableType:
        type_map = {
            "int": VariableType.INT,
            "bool": VariableType.BOOL,
            "char": VariableType.CHAR,
            "string": VariableType.STRING
        }
        return type_map.get(type_str, VariableType.INT) 