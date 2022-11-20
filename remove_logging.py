import libcst as cst
import libcst.matchers as m

CODE_FILE = 'test_codes/logging.py'


class LogTransformer(m.MatcherDecoratableTransformer):
    def __init__(self):
        super().__init__()
        self.deleted = []
    
    @m.call_if_inside(m.Expr(
        value=m.Call(
            func=m.Attribute(
                             value=m.Name(value='logger'), 
                             attr=(m.Name('info') | m.Name('debug'))
                            )
        )
    ))
    def leave_Expr(self, original_node, updated_node):
        self.deleted.append(original_node)
        return cst.RemoveFromParent()

    def print_stats(self, module):
        print("----------------------------")
        print("Deleted items:")
        for node in self.deleted:
            print(module.code_for_node(node))


if __name__ == "__main__":
    module = cst.parse_module(open(CODE_FILE, 'r').read())
    transform = LogTransformer()
    res = module.visit(transform)
    print("New code:\n" + res.code)
    transform.print_stats(res)
