from ast_nodes import *

class ASTVisualizer:
    def __init__(self):
        self.level = 0
        self.output = []

    def visit(self, node):
        if node is None:
            return
        
        # Добавляем отступы в зависимости от уровня
        indent = "  " * self.level
        self.output.append(f"{indent}{str(node)}")
        
        # Увеличиваем уровень для дочерних узлов
        self.level += 1
        
        # Рекурсивно обходим все дочерние узлы
        for child in node.childs:
            self.visit(child)
            
        # Уменьшаем уровень после обработки дочерних узлов
        self.level -= 1

    def visualize(self, root):
        self.output = []
        self.level = 0
        self.visit(root)
        return "\n".join(self.output)

def print_ast(node, level=0):
    if node is None:
        return

    indent = "  " * level
    node_type = node.__class__.__name__

    if node_type == "ExprListNode":
        print(f"{indent}ExprList")
    elif node_type == "FunctionNode":
        print(f"{indent}Function: {node.name} (return type: {node.return_type})")
    elif node_type == "ReturnNode":
        print(f"{indent}Return")
    elif node_type == "IfNode":
        print(f"{indent}If")
    elif node_type == "ForNode":
        print(f"{indent}For")
    elif node_type == "WhileNode":
        print(f"{indent}While")
    elif node_type == "DoWhileNode":
        print(f"{indent}DoWhile")
    elif node_type == "AssignNode":
        print(f"{indent}Assign")
    elif node_type == "IdentificationNode":
        print(f"{indent}VarDecl: {node.name} (type: {node.type})")
    elif node_type == "BinOpNode":
        print(f"{indent}BinOp: {node.op.value}")
    elif node_type == "UnOpNode":
        print(f"{indent}UnOp: {node.op.value}")
    elif node_type == "NumNode":
        print(f"{indent}Number: {node.value}")
    elif node_type == "BoolValueNode":
        print(f"{indent}Boolean: {node.value}")
    elif node_type == "IdentNode":
        print(f"{indent}Identifier: {node.name}")
    elif node_type == "CharNode":
        print(f"{indent}Char: '{node.value}'")
    elif node_type == "StringNode":
        print(f"{indent}String: \"{node.value}\"")
    elif node_type == "InputNode":
        print(f"{indent}Input")
    elif node_type == "OutputNode":
        print(f"{indent}Output")
    elif node_type == "ArrayDeclarationNode":
        print(f"{indent}ArrayDecl: {node.name}[{node.size}] (type: {node.type})")
    elif node_type == "ArrayElementsNode":
        print(f"{indent}ArrayElements")
    elif node_type == "ArrayAccessNode":
        print(f"{indent}ArrayAccess")
    elif node_type == "IncrementDecrementNode":
        print(f"{indent}IncrementDecrement: {node.op}")
    elif node_type == "SystemFunctionNode":
        print(f"{indent}SystemFunction: {node.name}")
    else:
        print(f"{indent}Unknown node type: {node_type}")

    for child in node.children:
        print_ast(child, level + 1)

def print_ast(root):
    visualizer = ASTVisualizer()
    print(visualizer.visualize(root)) 