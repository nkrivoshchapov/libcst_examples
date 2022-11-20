import libcst as cst

CODE_FILE = 'test_codes/funcnames.py'


class NameCollector(cst.CSTVisitor):
    def __init__(self):
        self.functions = []
        self.classes = {}
        self.curclass = None
    
    def visit_ClassDef(self, node: cst.ClassDef):
        self.classes[node.name.value] = []
        self.curclass = node.name.value

    def leave_ClassDef(self, node: cst.ClassDef):
        self.curclass = None

    def visit_FunctionDef(self, node):
        if self.curclass is None:
            self.functions.append(node.name.value)
        else:
            self.classes[self.curclass].append(node.name.value)
    
    def print_stats(self):
        print("The class has {} functions and {} classes".format(len(self.functions), len(self.classes)))
        
        if len(self.functions) > 0:
            print("\nList of functions:")
            for fname in self.functions:
                print(fname)
        
        if len(self.classes) > 0:
            print("\nList of classes:")
            for class_name, methods in self.classes.items():
                print("-> " + class_name)
                for method in methods:
                    print("    " + method)
        

if __name__ == "__main__":
    module = cst.parse_module(open(CODE_FILE, 'r').read())
    visitor = NameCollector()
    module.visit(visitor)
    visitor.print_stats()
