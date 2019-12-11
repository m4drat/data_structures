from __future__ import annotations

from dataclasses import field, dataclass
from node import Node
from typing import *

IS_DEBUG: bool = True

class AdaptiveHuffman():
    def __init__(self):

        # esc - node
        self.ESC: Node = Node(symbol = 'ESC')
        
        # reference to root node
        self.root: Node = self.ESC
        
        # actual nodes
        self.tree: List[Node] = [] # field(default_factory=list)

        # nodes with already seen symbols
        self.table: List[Union[Node, None]] = [None] * 2 ** 16 # field(default_factory=lambda: [None for i in range(256)]) 

    def swap_node(self, node1, node2):
        '''Swap 2 given nodes
        '''
        node_1_idx, node_2_idx = self.tree.index(node1), self.tree.index(node2)

        # swap nodes
        self.tree[node_1_idx], self.tree[node_2_idx] = self.tree[node_2_idx], self.tree[node_1_idx]

        tmp_parent = node1.parent
        node1.parent = node2.parent
        node2.parent = tmp_parent

        if node1.parent.left is node2:
            node1.parent.left = node1
        else:
            node1.parent.right = node1

        if node2.parent.left is node1:
            node2.parent.left = node2
        else:
            node2.parent.right = node2

    def get_code(self, char, node, code=''):
        '''Get code for char
        '''
        if node.left is None and node.right is None:
            return code if node.symbol == char else ''
        else:
            temp = ''
            if node.left is not None:
                temp = self.get_code(char, node.left, code + '0')
            if not temp and node.right is not None:
                temp = self.get_code(char, node.right, code + '1')
            return temp

    def find_largest_node(self, weight):
        '''Find node with biggest weight
        '''
        for n in reversed(self.tree):
            if n.weight == weight:
                return n

    def insert(self, char):
        node = self.table[ord(char)]

        if node is None:
            spawn = Node(symbol=char, weight=1)
            internal = Node(symbol='', weight=1, parent=self.ESC.parent, left=self.ESC, right=spawn)
            spawn.parent = internal
            self.ESC.parent = internal

            if internal.parent is not None:
                internal.parent.left = internal
            else:
                self.root = internal

            self.tree.insert(0, internal)
            self.tree.insert(0, spawn)

            self.table[ord(char)] = spawn
            node = internal.parent

        while node is not None:
            largest = self.find_largest_node(node.weight)

            if (node is not largest and node is not largest.parent and
                largest is not node.parent):
                self.swap_node(node, largest)

            node.weight = node.weight + 1
            node = node.parent

    def encode(self, msg):
        out = ''

        for char in msg:
            # if we already have this symbol
            if self.table[ord(char)]:
                out += self.get_code(char, self.root) + '_'
                if IS_DEBUG:
                    print(f'New Code: {self.get_code(char, self.root)}:{char}')
            else:
                out += self.get_code('ESC', self.root) + '_'
                out += bin(ord(char))[2:].zfill(8) + '_'
                if IS_DEBUG:
                    print(f'New Code: {self.get_code("ESC", self.root) + bin(ord(char))[2:].zfill(8)}:{char}')

            self.insert(char)

        return out

    def decode(self, text):
        result = ''

        to_char = lambda char: chr(int(char, 2))
        
        text = text.replace('_', '')

        symbol = to_char(text[:8])
        result += symbol
        self.insert(symbol)
        node = self.root

        i = 8
        while i < len(text):
            node = node.left if text[i] == '0' else node.right
            symbol = node.symbol

            if symbol:
                if symbol == 'ESC':
                    symbol = to_char(text[i+1:i+9])
                    i += 8

                result += symbol
                self.insert(symbol)
                node = self.root

            i += 1

        return result
    
def main():
    result = AdaptiveHuffman().encode(input('Write message to encode: '))
    print(result)

    result = AdaptiveHuffman().decode(result)
    print(result)


if __name__ == '__main__':
    main()