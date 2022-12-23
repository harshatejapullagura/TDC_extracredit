#complete binary tree insertionfr
from create import create_cluster 
from delete import delete_cluster
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Harsha\\Desktop\\osfinal\\osfinal\\application_default_credentials.json" #env setting up to connect the gcp account
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.key = key

class BinarySearchTree(object):
    pre_order = 'PREORDER'
    in_order = 'INORDER'
    post_order = 'POSTORDER'

    def __init__(self, root=None):
        self.root = root

    def get_root(self):
        return self.root

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self.utility_insert(self.root, key)

    def utility_insert(self, this_node, key):
        if this_node.key > key:
            if this_node.left is None:
                this_node.left = Node(key)
            else:
                self.utility_insert(this_node.left, key)
        else:
            if this_node.right is None:
                this_node.right = Node(key)
            else:
                self.utility_insert(this_node.right, key)

    def print(self, traversal_type='INORDER'):
        if traversal_type.upper() == self.in_order:
            print('\nInorder Traversal :>')
            self.inorder(self.root)
        elif traversal_type.upper() == self.pre_order:
            print('\nPreorder Traversal :>')
            self.preorder(self.root)
        elif traversal_type.upper() == self.post_order:
            print('\nPostorder Traversal :>')
            self.postorder(self.root)

    def inorder(self, this_node):
        if this_node:
            self.inorder(this_node.left)
            print(this_node.key, ', ', end='')
            self.inorder(this_node.right)

    def preorder(self, this_node):
        if this_node:
            print(this_node.key, ', ', end='')
            self.preorder(this_node.left)
            self.preorder(this_node.right)

    def postorder(self, this_node):
        if this_node:
            self.postorder(this_node.left)
            self.postorder(this_node.right)
            print(this_node.key, ', ', end='')

    def max_depth(self, this_node):
        '''
         calculate number of node from root to max depth
        :param this_node: root node
        :return: height of tree (root node has height 1):
        '''
        if this_node is None:
            return 0
        left_subtree = self.max_depth(this_node.left)
        right_subtree = self.max_depth(this_node.right)

        return max(left_subtree, right_subtree)+1

    def print_all_leaf_node(self, this_node):
        '''
         print all leaf Node
        :param this_node: this_node
        :return: print values at leave node
        '''
        if this_node.left:
            self.print_all_leaf_node(this_node.left)
        if this_node.right:
            self.print_all_leaf_node(this_node.right)
        if this_node.right is None and this_node.left is None:
            print(this_node.key, ', ', end='')

    @staticmethod
    def search(self, this_node, key):
        if this_node is None:
            print('Key (',key , ')is Not Found !')
            return False
        elif this_node.key == key:
            print('Key (=', key, ') Found :) ')
            return True
        elif key < this_node.key:
            self.search(this_node.left, key)
        else:
            self.search(this_node.right, key)

    def level_order_traversal(self, queue):
        '''
        input root node as a list
        print 'level order traversal '
        :return: None
        '''
        queue_new = []
        data = []
        print()
        if not queue:
            return
        else:
            for node in queue:
                #print('<-->', node.key, end='')
                data.append(node.key)
                if node.left is not None:
                    queue_new.append(node.left)
                if node.right is not None:
                    queue_new.append(node.right)
            print(' <> '.join([str(x) for x in data]))
        self.level_order_traversal(queue_new)

    def level_order_without_recursion(self):
        queue = [self.root]
        data = []

        while queue:
            node = queue.pop(0)
            data.append(str(node.key))
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        print(' level order Traversal without recursion :')
        print(' <> '.join(data))

    def find_inorder_succesor(self, this_node):
        ptr = this_node

        while ptr.left is not None:
            ptr = ptr.left
        return ptr

    def delete_node(self, this_node, key):
        if this_node is None:
            return this_node
        if key < this_node.key:
            this_node.left = self.delete_node(this_node.left, key)
        elif key > this_node.key:
            this_node.right = self.delete_node(this_node.right, key)
        else:
            # case 1 : delete node with no child or only one child node
            if this_node.left is None:
                temp = this_node.right
                this_node = None
                return temp
            elif this_node.right is None:
                temp = this_node.left
                this_node = None
                return temp

            # case 2 : Have 2 child node: then assign this node to its inorder successor
            temp = self.find_inorder_succesor(this_node.right)

            this_node.key = temp.key
            this_node.right = self.delete_node(this_node.right, temp.key)
        return this_node

    def delete_tree(self, this_node):
        if this_node:
            self.delete_tree(this_node.left)
            self.delete_tree(this_node.right)
            this_node = None


if __name__ == '__main__':
    print('Complete Binary TREE')
    project_id = "graphite-willow-363021" #project Initilization and project setup 
    location = "us-west2" #project zone
    cluster_name = "cluster-node-" 
    bst = BinarySearchTree() #Tree construction 
    bst.insert(3)
    bst.insert(1)
    bst.insert(2)
    bst.level_order_traversal([bst.get_root()])
    print("Creating Cluster")
    bst.print() #printing the tree
    bst.delete_node(bst.get_root(), 2) 
    print("Creating Cluster")
    create_cluster(project_id , location, cluster_name+"3") # create cluster function invocation to create a cluster 3 on kubernutes engine.
    print("Creating Cluster")
    create_cluster(project_id , location, cluster_name+"2") # create cluster function invocation to create a cluster 2 on kubernutes engine.
    print("Creating Cluster")
    delete_cluster(project_id ,location, cluster_name+"1") # node deletion  function invocation to delete a cluster 2 on kubernutes engine.
    bst.print(traversal_type='preorder') #printinh the preorder
    bst.level_order_traversal([bst.get_root()])
