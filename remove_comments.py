import libcst as cst

CODE = '''
def func(a):
    return 1

def funcY(a):
    """Comment""" ## <- It is parsed as a BasicString, so it is technically not a comment
    return 1

def funcX(a): # stupid comment
    return 1
    
# some = useless(code)

##func(funcX(2))

'''

class CommentTransformer(cst.CSTTransformer):
    def __init__(self):
        self.changes = {'old': [], 'new': []}
        self.deleted = []
    
    def leave_Comment(self, original_node, updated_node):
        if original_node.value.startswith('##'):
            newcomment = original_node.value[1:]
            self.changes['old'].append(original_node.value)
            self.changes['new'].append(newcomment)
            return updated_node.with_changes(value=newcomment)
        elif original_node.value.startswith('#'):
            self.deleted.append(original_node.value)
            return cst.RemoveFromParent()
        # else:
            # print()
            # return updated_node
    
    def print_stats(self):
        print("----------------------------")
        if len(self.changes['old']) > 0:
            print("\nChanges:")
            for old, new in zip(self.changes['old'], self.changes['new']):
                print(f"{old} -> {new}")
        if len(self.deleted) > 0:
            print("\nDeletions:")
            for line in self.deleted:
                print(line)
                
if __name__ == "__main__":
    module = cst.parse_module(CODE)
    transform = CommentTransformer()
    res = module.visit(transform)
    print("New code:\n" + res.code)
    transform.print_stats()
