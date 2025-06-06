from typing import Dict, List, Optional
from ast_nodes import *
from enum import Enum

class MSILType(Enum):
    INT32 = "int32"
    BOOL = "bool"
    CHAR = "char"
    VOID = "void"

class CodeGenerator:
    def __init__(self):
        self.code: List[str] = []
        self.current_function = None
        self.label_counter = 0
        self.local_variables: Dict[str, int] = {}
        self.global_variables: Dict[str, str] = {}
        self.local_counter = 0
        self.indent_level = 0
        
    def get_new_label(self) -> str:
        """Генерирует новую метку"""
        self.label_counter += 1
        return f"IL_{self.label_counter:04d}"
    
    def emit(self, instruction: str):
        """Добавляет инструкцию в код с правильным отступом"""
        indent = "  " * self.indent_level
        self.code.append(f"{indent}{instruction}")
    
    def emit_label(self, label: str):
        """Добавляет метку"""
        self.code.append(f"{label}:")
    
    def get_msil_type(self, type_str: str) -> MSILType:
        """Преобразует тип из строки в MSIL тип"""
        type_map = {
            "int": MSILType.INT32,
            "bool": MSILType.BOOL,
            "char": MSILType.CHAR,
            "void": MSILType.VOID
        }
        return type_map.get(type_str, MSILType.INT32)
    
    def generate(self, node: AstNode) -> str:
        """Генерирует MSIL код для AST узла"""
        self.emit("// Generated MSIL code")
        self.emit(".assembly extern mscorlib {}")
        self.emit(".assembly generated_code {}")
        self.emit("")
        
        self.visit(node)
        
        return "\n".join(self.code)
    
    def visit(self, node):
        """Основной метод обхода AST"""
        if node is None:
            return
        if isinstance(node, (int, float, bool, str)):
            return
        if not isinstance(node, AstNode):
            return
            
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node: AstNode):
        """Общий метод обхода для неопределенных узлов"""
        for child in node.childs:
            self.visit(child)
    
    def visit_ExprListNode(self, node: ExprListNode):
        """Обработка списка выражений"""
        for child in node.childs:
            self.visit(child)
    
    def visit_FunctionNode(self, node: FunctionNode):
        """Генерация кода для функции"""
        self.current_function = node.name
        self.local_variables.clear()
        self.local_counter = 0
        
        # Определяем тип возвращаемого значения
        return_type = self.get_msil_type(node.return_type)
        
        # Генерируем заголовок функции
        params = []
        for i, param in enumerate(node.params):
            param_type = self.get_msil_type(param.type)
            params.append(f"{param_type.value} {param.name.name}")
        
        param_list = ", ".join(params) if params else ""
        
        if node.name == "main":
            self.emit(f".method static {return_type.value} main({param_list}) cil managed")
        else:
            self.emit(f".method static {return_type.value} {node.name}({param_list}) cil managed")
        
        self.emit("{")
        self.indent_level += 1
        
        # Добавляем параметры в локальные переменные
        for i, param in enumerate(node.params):
            self.local_variables[param.name.name] = i
        
        # Обрабатываем тело функции
        self.visit(node.body)
        
        # Если функция не заканчивается return, добавляем его
        if return_type == MSILType.VOID:
            self.emit("ret")
        
        self.indent_level -= 1
        self.emit("}")
        self.emit("")
    
    def visit_IdentificationNode(self, node: IdentificationNode):
        """Генерация кода для объявления переменной"""
        var_name = node.name.name
        var_type = self.get_msil_type(node.type_)
        
        if self.current_function is None:
            # Глобальная переменная
            self.emit(f".field static {var_type.value} {var_name}")
            self.global_variables[var_name] = var_type.value
            
            if node.value:
                # Инициализация глобальной переменной
                self.emit(f".method static void .cctor() cil managed")
                self.emit("{")
                self.indent_level += 1
                self.visit(node.value)
                self.emit(f"stsfld {var_type.value} generated_code::{var_name}")
                self.emit("ret")
                self.indent_level -= 1
                self.emit("}")
        else:
            # Локальная переменная
            self.local_variables[var_name] = self.local_counter
            self.emit(f".locals init ({var_type.value} V_{self.local_counter})")
            self.local_counter += 1
            
            if node.value:
                self.visit(node.value)
                self.emit(f"stloc V_{self.local_variables[var_name]}")
    
    def visit_AssignNode(self, node: AssignNode):
        """Генерация кода для присваивания"""
        if isinstance(node.var, IdentNode):
            var_name = node.var.name
            
            # Генерируем код для значения
            self.visit(node.val)
            
            if var_name in self.local_variables:
                # Локальная переменная
                self.emit(f"stloc V_{self.local_variables[var_name]}")
            elif var_name in self.global_variables:
                # Глобальная переменная
                var_type = self.global_variables[var_name]
                self.emit(f"stsfld {var_type} generated_code::{var_name}")
    
    def visit_IdentNode(self, node: IdentNode):
        """Генерация кода для использования переменной"""
        var_name = node.name
        
        if var_name in self.local_variables:
            # Локальная переменная
            self.emit(f"ldloc V_{self.local_variables[var_name]}")
        elif var_name in self.global_variables:
            # Глобальная переменная
            var_type = self.global_variables[var_name]
            self.emit(f"ldsfld {var_type} generated_code::{var_name}")
    
    def visit_NumNode(self, node: NumNode):
        """Генерация кода для числовой константы"""
        value = int(node.num)
        self.emit(f"ldc.i4 {value}")
    
    def visit_BoolValueNode(self, node: BoolValueNode):
        """Генерация кода для булевой константы"""
        value = 1 if node.name == "true" else 0
        self.emit(f"ldc.i4 {value}")
    
    def visit_CharNode(self, node: CharNode):
        """Генерация кода для символьной константы"""
        char_code = ord(node.value)
        self.emit(f"ldc.i4 {char_code}")
    
    def visit_BinOpNode(self, node: BinOpNode):
        """Генерация кода для бинарных операций"""
        # Генерируем код для левого операнда
        self.visit(node.arg1)
        
        # Генерируем код для правого операнда
        self.visit(node.arg2)
        
        # Генерируем операцию
        op_map = {
            '+': 'add',
            '-': 'sub',
            '*': 'mul',
            '/': 'div',
            '%': 'rem',
            '==': 'ceq',
            '>': 'cgt',
            '<': 'clt'
        }
        
        if node.op.value in op_map:
            self.emit(op_map[node.op.value])
        else:
            self.emit(f"// Unsupported operation: {node.op.value}")
    
    def visit_IfNode(self, node: IfNode):
        """Генерация кода для условного оператора"""
        else_label = self.get_new_label()
        end_label = self.get_new_label()
        
        # Генерируем условие
        self.visit(node.cond)
        
        # Переход, если условие ложно
        if node.else_:
            self.emit(f"brfalse {else_label}")
        else:
            self.emit(f"brfalse {end_label}")
        
        # Генерируем код для then блока
        self.visit(node.then_)
        
        if node.else_:
            self.emit(f"br {end_label}")
            self.emit_label(else_label)
            self.visit(node.else_)
        
        self.emit_label(end_label)
    
    def visit_WhileNode(self, node: WhileNode):
        """Генерация кода для цикла while"""
        start_label = self.get_new_label()
        end_label = self.get_new_label()
        
        self.emit_label(start_label)
        
        # Генерируем условие
        self.visit(node.cond)
        
        # Выход из цикла, если условие ложно
        self.emit(f"brfalse {end_label}")
        
        # Генерируем тело цикла
        self.visit(node.body)
        
        # Переход к началу цикла
        self.emit(f"br {start_label}")
        
        self.emit_label(end_label)
    
    def visit_ForNode(self, node: ForNode):
        """Генерация кода для цикла for"""
        start_label = self.get_new_label()
        end_label = self.get_new_label()
        
        # Инициализация
        self.visit(node.init)
        
        self.emit_label(start_label)
        
        # Проверка условия
        self.visit(node.cond)
        self.emit(f"brfalse {end_label}")
        
        # Тело цикла
        self.visit(node.body)
        
        # Шаг
        self.visit(node.step)
        
        # Переход к началу
        self.emit(f"br {start_label}")
        
        self.emit_label(end_label)
    
    def visit_ReturnNode(self, node: ReturnNode):
        """Генерация кода для возврата"""
        if node.expr:
            self.visit(node.expr)
        self.emit("ret")
    
    def visit_FunctionCallNode(self, node: FunctionCallNode):
        """Генерация кода для вызова функции"""
        # Генерируем аргументы
        for arg in node.args:
            self.visit(arg)
        
        # Вызов функции
        if node.name == "main":
            self.emit(f"call int32 generated_code::main()")
        else:
            # Определяем тип возвращаемого значения (упрощенно)
            self.emit(f"call int32 generated_code::{node.name}()") 