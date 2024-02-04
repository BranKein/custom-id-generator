class Node:
    def __init__(self):
        self.x = None
        self.y = None
        self.value = 0
        self.is_root = False
        self.parent_node: Node = None
        self.left_child: Node = None
        self.right_child: Node = None
        self.is_leaf = False

    def get_level(self, cnt=1):
        if self.is_root:
            return cnt
        else:
            cnt += 1
            cnt = self.parent_node.get_level(cnt)
            return cnt

    def set_left_child(self, node):
        self.left_child = node
        node.parent_node = self

    def set_right_child(self, node):
        self.right_child = node
        node.parent_node = self


class Tree:
    def __init__(self, root: Node):
        assert root.is_root, 'node should be specified as root'
        self.__root = root

    def get_root(self):
        return self.__root

    def get_length_of_branch(self, node: Node, cnt=1):
        if node.parent_node is None:
            return cnt
        else:
            cnt += 1
            return self.get_length_of_branch(node.parent_node, cnt)

    def get_depth(self, remove_leaf=False):
        all_nodes = self.traverse_in_order()
        if remove_leaf:
            depth = max([self.get_length_of_branch(node) for node in all_nodes if not node.is_leaf])
        else:
            depth = max([self.get_length_of_branch(node) for node in all_nodes])
        return depth

    def traverse_in_order(self, node: Node = None):
        if node is None:
            node = self.__root
        res = []
        if node.left_child is not None:
            res = res + self.traverse_in_order(node.left_child)
        res.append(node)
        if node.right_child is not None:
            res = res + self.traverse_in_order(node.right_child)
        return res

    def get_right_most_node(self, node: Node = None, level=None):
        if node is None:
            node = self.__root
        if level is None:
            return [nd for nd in self.traverse_in_order(node)][-1]
        else:
            return [nd for nd in self.traverse_in_order(node) if nd.get_level() == level][-1]

    def get_left_most_node(self, node: Node = None, level=None):
        if node is None:
            node = self.__root
        if level is None:
            return [nd for nd in self.traverse_in_order(node)][0]
        else:
            return [nd for nd in self.traverse_in_order(node) if nd.get_level() == level][0]

    def get_distance_between_subtrees(self):
        self.__root.left_child.parent_node = None
        self.__root.right_child.parent_node = None
        self.__root.left_child.is_root = True
        self.__root.right_child.is_root = True
        left_subtree = Tree(self.__root.left_child)
        right_subtree = Tree(self.__root.right_child)
        if left_subtree.get_depth() == right_subtree.get_depth():
            level = right_subtree.get_depth()
        elif left_subtree.get_depth() > right_subtree.get_depth():
            level = right_subtree.get_depth()
        else:
            level = left_subtree.get_depth()

        lrmn = left_subtree.get_right_most_node(level=level)
        rlmn = right_subtree.get_left_most_node(level=level)
        x_diff = rlmn.x - lrmn.x

        self.__root.left_child.parent_node = self.__root
        self.__root.right_child.parent_node = self.__root
        self.__root.left_child.is_root = False
        self.__root.right_child.is_root = False
        return x_diff

    def move_tree(self, shift=1):
        for nd in self.traverse_in_order():
            nd.x = nd.x + shift


class BMinusTree:
    def __init__(self):
        return


__all__ = ['Node', 'Tree']
