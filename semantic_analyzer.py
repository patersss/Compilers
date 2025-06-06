from typing import Dict, List, Set, Optional
from ast_nodes import *
from dataclasses import dataclass
from enum import Enum

class VariableType(Enum):
    INT = "int"
    CHAR = "char"
    BOOL = "bool"
    ARRAY = "array"
    VOID = "void"

@dataclass
class Variable:
    name: str
    type: VariableType
    is_initialized: bool = False
    scope_level: int = 0
    is_global: bool = False
    array_type: Optional[VariableType] = None  # Тип элементов массива
    array_size: Optional[int] = None  # Размер массива

class Scope:
    def __init__(self, parent: Optional['Scope'] = None):
        self.variables: Dict[str, Variable] = {}
        self.parent = parent
        self.level = 0 if parent is None else parent.level + 1
        self.is_block_scope = False  # Флаг для блоков if, while и т.д.

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

    def is_variable_accessible(self, name: str) -> bool:
        """Проверяет, доступна ли переменная в текущей области видимости"""
        var = self.get_variable(name)
        if not var:
            return False
        # Если переменная объявлена в блоке (if, while и т.д.), 
        # то она доступна только внутри этого блока
        if var.scope_level > self.level:
            return False
        return True

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
        self.current_function = None
        self.known_system_identifiers = {
            "cout", "cin", "endl", "abs",
            "printf", "scanf", "main",
            "true", "false", "NULL"
        }
        self.functions: Dict[str, dict] = {}
        
        # Словарь допустимых приведений типов
        self.type_conversions = {
            VariableType.CHAR: {VariableType.INT},  # char можно привести к int
            VariableType.INT: {VariableType.BOOL},  # int можно привести к bool для условий
        }
        
        # Определяем допустимые операции для типов
        self.binary_operations = {
            '+': {
                (VariableType.INT, VariableType.INT): VariableType.INT,
                (VariableType.CHAR, VariableType.INT): VariableType.INT,
                (VariableType.INT, VariableType.CHAR): VariableType.INT,
                (VariableType.CHAR, VariableType.CHAR): VariableType.INT,
            },
            '-': {
                (VariableType.INT, VariableType.INT): VariableType.INT,
                (VariableType.CHAR, VariableType.INT): VariableType.INT,
                (VariableType.INT, VariableType.CHAR): VariableType.INT,
                (VariableType.CHAR, VariableType.CHAR): VariableType.INT,
            },
            '*': {
                (VariableType.INT, VariableType.INT): VariableType.INT,
                (VariableType.INT, VariableType.CHAR): VariableType.INT,
                (VariableType.CHAR, VariableType.INT): VariableType.INT,
            },
            '/': {
                (VariableType.INT, VariableType.INT): VariableType.INT,
                (VariableType.INT, VariableType.CHAR): VariableType.INT,
                (VariableType.CHAR, VariableType.INT): VariableType.INT,
            },
            '%': {
                (VariableType.INT, VariableType.INT): VariableType.INT,
                (VariableType.INT, VariableType.CHAR): VariableType.INT,
                (VariableType.CHAR, VariableType.INT): VariableType.INT,
            },
            '==': {
                (VariableType.INT, VariableType.INT): VariableType.BOOL,
                (VariableType.CHAR, VariableType.CHAR): VariableType.BOOL,
                (VariableType.BOOL, VariableType.BOOL): VariableType.BOOL,
            },
            '!=': {
                (VariableType.INT, VariableType.INT): VariableType.BOOL,
                (VariableType.CHAR, VariableType.CHAR): VariableType.BOOL,
                (VariableType.BOOL, VariableType.BOOL): VariableType.BOOL,
            },
            '<': {
                (VariableType.INT, VariableType.INT): VariableType.BOOL,
                (VariableType.CHAR, VariableType.CHAR): VariableType.BOOL,
            },
            '>': {
                (VariableType.INT, VariableType.INT): VariableType.BOOL,
                (VariableType.CHAR, VariableType.CHAR): VariableType.BOOL,
            },
            '<=': {
                (VariableType.INT, VariableType.INT): VariableType.BOOL,
                (VariableType.CHAR, VariableType.CHAR): VariableType.BOOL,
            },
            '>=': {
                (VariableType.INT, VariableType.INT): VariableType.BOOL,
                (VariableType.CHAR, VariableType.CHAR): VariableType.BOOL,
            },
            '&&': {
                (VariableType.BOOL, VariableType.BOOL): VariableType.BOOL,
            },
            '||': {
                (VariableType.BOOL, VariableType.BOOL): VariableType.BOOL,
            }
        }

    def analyze(self, node: AstNode) -> List[SemanticError]:
        try:
            # Сначала собираем все функции, если это ExprListNode
            if isinstance(node, ExprListNode):
                # Первый проход - собираем все функции
                for child in node.childs:
                    if isinstance(child, FunctionNode):
                        self.collect_function(child)
                
                # Второй проход - анализируем семантику
                for child in node.childs:
                    self.visit(child)
            else:
                self.visit(node)
        except Exception as e:
            self.errors.append(SemanticError(f"Ошибка при анализе: {str(e)}"))
        return self.errors

    def collect_function(self, node: FunctionNode):
        """Собирает информацию о функции без анализа её тела"""
        self.functions[node.name] = {
            'return_type': node.return_type,
            'params': [(p.type, p.name.name) for p in node.params],
        }

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
            self.errors.append(SemanticError(f"Ошибка при обработке узла {node.__class__.__name__}: {str(e)}"))

    def generic_visit(self, node: AstNode):
        for child in node.childs:
            if isinstance(child, AstNode):
                self.visit(child)

    def visit_ProgramNode(self, node: ProgramNode):
        # Сначала собираем все функции
        for child in node.childs:
            if isinstance(child, FunctionNode):
                self.visit(child)
        # Затем проверяем main
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
        # Сохраняем текущую область видимости
        old_scope = self.current_scope
        self.current_scope = Scope(old_scope)
        
        # Сохраняем информацию о текущей функции
        old_function = self.current_function
        self.current_function = {
            'name': node.name,
            'return_type': node.return_type,
            'params': [(p.type, p.name.name) for p in node.params]
        }
        
        # Добавляем функцию в таблицу функций
        self.functions[node.name] = {
            'return_type': node.return_type,
            'params': [(p.type, p.name.name) for p in node.params],
            'scope': self.current_scope
        }
        
        # Обрабатываем параметры
        for param in node.params:
            var = Variable(param.name.name, self._get_type_from_string(param.type))
            self.current_scope.add_variable(var)
        
        # Обрабатываем тело функции
        old_in_function = self.in_function
        self.in_function = True
        self.visit(node.body)
        self.in_function = old_in_function
        
        # Восстанавливаем область видимости и информацию о функции
        self.current_scope = old_scope
        self.current_function = old_function

    def visit_IdentificationNode(self, node: IdentificationNode):
        if not isinstance(node.name, IdentNode):
            self.errors.append(SemanticError("Некорректный идентификатор в объявлении переменной"))
            return

        var_name = node.name.name
        var_type = self._get_type_from_string(node.type_)
        
        # Проверяем инициализацию
        if node.value:
            value_type = self._get_expression_type(node.value)
            if value_type and value_type != var_type:
                self.errors.append(SemanticError(
                    f"Несоответствие типов при инициализации: переменная типа {var_type.value}, "
                    f"значение типа {value_type.value}"
                ))
            # Посещаем значение только один раз здесь
            self.visit(node.value)
        
        var = Variable(var_name, var_type, is_global=not self.in_function)
        if not self.current_scope.add_variable(var):
            self.errors.append(SemanticError(f"Переменная {var_name} уже объявлена в текущей области видимости"))

    def visit_ForNode(self, node: ForNode):
        old_scope = self.current_scope
        self.current_scope = Scope(old_scope)
        self.current_scope.is_block_scope = True
        
        self.visit(node.init)
        
        cond_type = self._get_expression_type(node.cond)
        if cond_type and cond_type != VariableType.BOOL:
            # Проверяем возможность приведения к bool только для int
            if not self._can_convert_type(cond_type, VariableType.BOOL):
                self.errors.append(SemanticError(
                    f"Условие в for должно быть типа bool, получен тип {cond_type.value}"
                ))
        
        old_in_loop = self.in_loop
        self.in_loop = True
        
        self.visit(node.cond)
        self.visit(node.step)
        self.visit(node.body)
        
        self.in_loop = old_in_loop
        self.current_scope = old_scope

    def visit_WhileNode(self, node: WhileNode):
        cond_type = self._get_expression_type(node.cond)
        if cond_type and cond_type != VariableType.BOOL:
            # Проверяем возможность приведения к bool только для int
            if not self._can_convert_type(cond_type, VariableType.BOOL):
                self.errors.append(SemanticError(
                    f"Условие в while должно быть типа bool, получен тип {cond_type.value}"
                ))
        
        old_scope = self.current_scope
        self.current_scope = Scope(old_scope)
        self.current_scope.is_block_scope = True
        
        old_in_loop = self.in_loop
        self.in_loop = True
        
        self.visit(node.cond)
        self.visit(node.body)
        
        self.in_loop = old_in_loop
        self.current_scope = old_scope

    def visit_IfNode(self, node: IfNode):
        cond_type = self._get_expression_type(node.cond)
        if cond_type and cond_type != VariableType.BOOL:
            # Проверяем возможность приведения к bool только для int
            if not self._can_convert_type(cond_type, VariableType.BOOL):
                self.errors.append(SemanticError(
                    f"Условие в if должно быть типа bool, получен тип {cond_type.value}"
                ))
        
        old_scope = self.current_scope
        self.current_scope = Scope(old_scope)
        self.current_scope.is_block_scope = True
        
        self.visit(node.cond)
        self.visit(node.then_)
        if node.else_:
            self.visit(node.else_)
        
        self.current_scope = old_scope

    def visit_AssignNode(self, node: AssignNode):
        if isinstance(node.var, IdentNode):
            var = self.current_scope.get_variable(node.var.name)
            if not var:
                self.errors.append(SemanticError(f"Присваивание необъявленной переменной: {node.var.name}"))
            elif not self.current_scope.is_variable_accessible(node.var.name):
                self.errors.append(SemanticError(f"Попытка доступа к переменной {node.var.name} вне её области видимости"))
            else:
                # Проверяем тип присваиваемого значения
                value_type = self._get_expression_type(node.val)
                if value_type:
                    if var.type == VariableType.ARRAY:
                        self.errors.append(SemanticError(f"Невозможно присвоить значение массиву {node.var.name}"))
                    elif not self._can_convert_type(value_type, var.type):
                        self.errors.append(SemanticError(
                            f"Несоответствие типов при присваивании: переменная типа {var.type.value}, "
                            f"значение типа {value_type.value} (нет допустимого приведения типов)"
                        ))
        elif isinstance(node.var, ArrayAccessNode):
            array_var = self.current_scope.get_variable(node.var.array.name)
            if not array_var or array_var.type != VariableType.ARRAY:
                self.errors.append(SemanticError(f"Некорректный доступ к массиву: {node.var.array.name}"))
                return
                
            value_type = self._get_expression_type(node.val)
            if value_type and not self._can_convert_type(value_type, array_var.array_type):
                self.errors.append(SemanticError(
                    f"Несоответствие типов при присваивании элементу массива: "
                    f"ожидался {array_var.array_type.value}, получен {value_type.value} (нет допустимого приведения типов)"
                ))
        
        self.visit(node.val)
        if isinstance(node.var, ArrayAccessNode):
            self.visit(node.var)

    def visit_IdentNode(self, node: IdentNode):
        if not hasattr(node, 'name'):
            self.errors.append(SemanticError("Некорректный идентификатор"))
            return
        if node.name not in self.known_system_identifiers:
            var = self.current_scope.get_variable(node.name)
            if not var:
                self.errors.append(SemanticError(f"Использование необъявленной переменной: {node.name}"))
            elif not self.current_scope.is_variable_accessible(node.name):
                self.errors.append(SemanticError(f"Попытка доступа к переменной {node.name} вне её области видимости (переменная объявлена в блоке if/while/for)"))

    def visit_FunctionCallNode(self, node: FunctionCallNode):
        if node.name not in self.functions:
            self.errors.append(SemanticError(f"Вызов несуществующей функции: {node.name}"))
            return

        func = self.functions[node.name]
        
        # Проверяем количество аргументов
        if len(node.args) != len(func['params']):
            self.errors.append(SemanticError(
                f"Неверное количество аргументов при вызове функции {node.name}. "
                f"Ожидалось {len(func['params'])}, получено {len(node.args)}"
            ))
            return

        # Проверяем типы аргументов
        for i, (arg, param) in enumerate(zip(node.args, func['params'])):
            arg_type = self._get_expression_type(arg)
            param_type = self._get_type_from_string(param[0])
            
            # Проверяем строгое соответствие типов - без автоматических приведений для аргументов функций
            if arg_type and arg_type != param_type:
                self.errors.append(SemanticError(
                    f"Несоответствие типов аргумента в функции {node.name}: "
                    f"аргумент {i+1} ({param[1]}) ожидал тип {param_type.value}, "
                    f"получен тип {arg_type.value}"
                ))
            self.visit(arg)

    def visit_ExprListNode(self, node: ExprListNode):
        for child in node.childs:
            self.visit(child)

    def visit_ArrayAccessNode(self, node: ArrayAccessNode):
        var = self.current_scope.get_variable(node.array.name)
        if not var:
            self.errors.append(SemanticError(f"Использование необъявленного массива: {node.array.name}"))
            return
            
        if var.type != VariableType.ARRAY:
            self.errors.append(SemanticError(f"{node.array.name} не является массивом"))
            return
            
        # Проверяем индекс
        index_type = self._get_expression_type(node.index)
        if index_type != VariableType.INT:
            self.errors.append(SemanticError(
                f"Индекс массива должен быть типа int, получен тип {index_type.value}"
            ))
            return
            
        # Проверяем выход за границы массива
        if var.array_size and isinstance(node.index, int):
            if node.index < 0 or node.index >= var.array_size:
                self.errors.append(SemanticError(f"Выход за границы массива {node.array.name}"))
        
        self.visit(node.index)

    def visit_ArrayDeclarationNode(self, node: ArrayDeclarationNode):
        if not isinstance(node.name, IdentNode):
            self.errors.append(SemanticError("Некорректный идентификатор в объявлении массива"))
            return
            
        name = node.name.name
        array_type = self._get_type_from_string(node.type)
        
        # Проверяем размер массива
        size = None
        if node.size:
            if isinstance(node.size, int):
                size = node.size
            else:
                size_type = self._get_expression_type(node.size)
                if size_type != VariableType.INT:
                    self.errors.append(SemanticError("Размер массива должен быть типа int"))
                    return
        
        var = Variable(name, VariableType.ARRAY, is_global=not self.in_function)
        var.array_type = array_type
        var.array_size = size
        
        if not self.current_scope.add_variable(var):
            self.errors.append(SemanticError(f"Массив {name} уже объявлен в текущей области видимости"))
        
        # Проверяем инициализацию массива
        if node.init:
            if not isinstance(node.init, ArrayElementsNode):
                self.errors.append(SemanticError("Некорректная инициализация массива"))
                return
                
            if size and len(node.init.childs) > size:
                self.errors.append(SemanticError(f"Превышен размер массива {name}"))
                return
                
            for init_value in node.init.childs:
                init_type = self._get_expression_type(init_value)
                if init_type != array_type:
                    self.errors.append(SemanticError(
                        f"Несоответствие типов при инициализации массива {name}: "
                        f"ожидался {array_type.value}, получен {init_type.value}"
                    ))

    def visit_ArrayElementsNode(self, node: ArrayElementsNode):
        for child in node.childs:
            self.visit(child)

    def visit_SystemFunctionNode(self, node: SystemFunctionNode):
        self.visit(node.arg)

    def visit_IncrementDecrementNode(self, node: IncrementDecrementNode):
        self.visit(node.ident)

    def visit_ReturnNode(self, node: ReturnNode):
        if not self.in_function:
            self.errors.append(SemanticError("Оператор return вне функции"))
            return
            
        if node.expr:
            return_type = self._get_expression_type(node.expr)
            if self.current_function and return_type:
                expected_type = self._get_type_from_string(self.current_function['return_type'])
                if not self._can_convert_type(return_type, expected_type):
                    self.errors.append(SemanticError(
                        f"Несоответствие типа возвращаемого значения в функции {self.current_function['name']}: "
                        f"ожидался тип {expected_type.value}, получен тип {return_type.value}"
                    ))
            self.visit(node.expr)

    def _get_type_from_string(self, type_str: str) -> VariableType:
        type_map = {
            "int": VariableType.INT,
            "char": VariableType.CHAR,
            "bool": VariableType.BOOL,
            "void": VariableType.VOID
        }
        return type_map.get(type_str, VariableType.INT)

    def _can_convert_type(self, from_type: VariableType, to_type: VariableType) -> bool:
        """Проверяет, можно ли привести один тип к другому"""
        if from_type == to_type:
            return True
        # Проверяем, есть ли в словаре преобразований запись для исходного типа
        if from_type in self.type_conversions:
            return to_type in self.type_conversions[from_type]
        return False

    def _get_expression_type(self, node) -> Optional[VariableType]:
        if isinstance(node, NumNode):
            return VariableType.INT
        elif isinstance(node, BoolValueNode):
            return VariableType.BOOL
        elif isinstance(node, CharNode):
            return VariableType.CHAR
        elif isinstance(node, IdentNode):
            var = self.current_scope.get_variable(node.name)
            return var.type if var else None
        elif isinstance(node, BinOpNode):
            left_type = self._get_expression_type(node.arg1)
            right_type = self._get_expression_type(node.arg2)
            if left_type and right_type:
                op_types = self.binary_operations.get(node.op.value, {})
                # Проверяем прямое соответствие типов
                if (left_type, right_type) in op_types:
                    return op_types[(left_type, right_type)]
                # Проверяем возможность приведения типов
                for (t1, t2), result_type in op_types.items():
                    if (self._can_convert_type(left_type, t1) and 
                        self._can_convert_type(right_type, t2)):
                        return result_type
                # Если операция не найдена, проверяем обратный порядок типов
                if (right_type, left_type) in op_types:
                    return op_types[(right_type, left_type)]
                for (t1, t2), result_type in op_types.items():
                    if (self._can_convert_type(right_type, t1) and 
                        self._can_convert_type(left_type, t2)):
                        return result_type
        return None

    def visit_BinOpNode(self, node: BinOpNode):
        left_type = self._get_expression_type(node.arg1)
        right_type = self._get_expression_type(node.arg2)
        
        if not left_type or not right_type:
            self.errors.append(SemanticError("Неизвестный тип в бинарной операции"))
            return
            
        op_types = self.binary_operations.get(node.op.value, {})
        
        # Для операций сравнения проверяем строгое соответствие типов
        if node.op.value in ['==', '!=', '<', '>', '<=', '>=']:
            # Проверяем, есть ли допустимая операция сравнения для этих типов
            if (left_type, right_type) not in op_types:
                self.errors.append(SemanticError(
                    f"Недопустимое сравнение типов {left_type.value} и {right_type.value}"
                ))
            self.visit(node.arg1)
            self.visit(node.arg2)
            return
            
        # Для арифметических операций
        operation_found = False
        
        # Проверяем прямое соответствие типов
        if (left_type, right_type) in op_types:
            operation_found = True
        
        if not operation_found:
            self.errors.append(SemanticError(
                f"Недопустимая операция {node.op.value} для типов {left_type.value} и {right_type.value}"
            ))
        
        self.visit(node.arg1)
        self.visit(node.arg2) 