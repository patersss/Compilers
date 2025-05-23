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
        self.output.append(f"{indent}{node.__class__.__name__}")
        
        # Увеличиваем уровень для дочерних узлов
        self.level += 1
        
        # Рекурсивно обходим все дочерние узлы
        for child in node.children:
            self.visit(child)
            
        # Уменьшаем уровень после обработки дочерних узлов
        self.level -= 1

    def visualize(self, root):
        self.output = []
        self.level = 0
        self.visit(root)
        return "\n".join(self.output)

def print_ast(root):
    visualizer = ASTVisualizer()
    print(visualizer.visualize(root)) 