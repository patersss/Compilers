from ast_nodes import *

def print_ast(node, prefix="", is_last=True):
    """
    Рекурсивно выводит AST с линиями для связи узлов
    """
    if node is None:
        return

    # Определяем символы для отображения связей
    connector = "└── " if is_last else "├── "
    line = "    " if is_last else "│   "
    
    # Выводим текущий узел с его типом и значением
    node_type = node.__class__.__name__
    node_str = str(node)
    
    if node_type == "ExprListNode":
        print(f"{prefix}{connector}ExprList")
    elif node_type == "FunctionNode":
        print(f"{prefix}{connector}Function: {node.name} (return type: {node.return_type})")
    elif node_type == "ReturnNode":
        print(f"{prefix}{connector}Return")
    elif node_type == "IfNode":
        print(f"{prefix}{connector}If")
    elif node_type == "ForNode":
        print(f"{prefix}{connector}For")
    elif node_type == "WhileNode":
        print(f"{prefix}{connector}While")
    elif node_type == "DoWhileNode":
        print(f"{prefix}{connector}DoWhile")
    elif node_type == "AssignNode":
        print(f"{prefix}{connector}Assign")
    elif node_type == "IdentificationNode":
        print(f"{prefix}{connector}VarDecl: {node.name} (type: {node.type_})")
    elif node_type == "BinOpNode":
        print(f"{prefix}{connector}BinOp: {node.op.value}")
    elif node_type == "UnOpNode":
        print(f"{prefix}{connector}UnOp: {node.op.value}")
    elif node_type == "NumNode":
        print(f"{prefix}{connector}Number: {node.num}")
    elif node_type == "BoolValueNode":
        print(f"{prefix}{connector}Boolean: {node.name}")
    elif node_type == "IdentNode":
        print(f"{prefix}{connector}Identifier: {node.name}")
    elif node_type == "CharNode":
        print(f"{prefix}{connector}Char: '{node.value}'")
    elif node_type == "StringNode":
        print(f"{prefix}{connector}String: \"{node.value}\"")
    elif node_type == "InputNode":
        print(f"{prefix}{connector}Input")
    elif node_type == "OutputNode":
        print(f"{prefix}{connector}Output")
    elif node_type == "ArrayDeclarationNode":
        print(f"{prefix}{connector}ArrayDecl: {node.name}[{node.size}] (type: {node.type})")
    elif node_type == "ArrayElementsNode":
        print(f"{prefix}{connector}ArrayElements")
    elif node_type == "ArrayAccessNode":
        print(f"{prefix}{connector}ArrayAccess")
    elif node_type == "IncrementDecrementNode":
        print(f"{prefix}{connector}IncrementDecrement: {node.op}")
    elif node_type == "SystemFunctionNode":
        print(f"{prefix}{connector}SystemFunction: {node.func_name}")
    else:
        print(f"{prefix}{connector}{node_str}")
    
    # Получаем дочерние узлы
    children = node.childs if hasattr(node, 'childs') else []
    
    # Рекурсивно выводим дочерние узлы
    for i, child in enumerate(children):
        is_last_child = i == len(children) - 1
        print_ast(child, prefix + line, is_last_child)

def visualize_ast(node):
    """
    Запускает визуализацию AST
    """
    print("\nАбстрактное синтаксическое дерево:")
    print("=" * 50)
    print_ast(node)
    print("=" * 50) 