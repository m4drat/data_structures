# -*- coding: utf-8 -*-
# @Author: madrat
# @Date:   2019-10-09 19:41:34

class NegativeListLength(Exception):
    def __init__(self):
        Exception.__init__(self, 'Trying to initialize list with negative length!')

class InvalidIndex(Exception):
    def __init__(self, msg):
        Exception.__init__(self, f'Trying to access element at impossible index: {msg}')

class ListNode():
    def __repr__(self):
        return f'<data={self.data}> <prev_node={self.prev_node}> <next_node={self.next_node}>'

    def __str__(self):
        return str(self.data)

    def __init__(self, data, prev_node=None, next_node=None):
        self.data      = data
        self.prev_node = prev_node
        self.next_node = next_node

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        return self.next_node

    def prev(self):
        return self.prev_node

    def unlink(self):
        '''
        Unlink Node from specific location
        Algorithm:
            - previous_node.next_node = curr_node.next_node
            - next_node.prev_node     = curr_node.prev_node
        '''

        p_node = self.prev_node
        n_node = self.next_node

        if p_node != None:
            p_node.next_node = n_node
        else:
            # 'delete' start_node 
            self.data = n_node.data
            self.prev_node = None
            self.next_node = n_node.next_node
            self.next_node.prev_node = self
            
        if n_node != None:
            n_node.prev_node = p_node
        else:
            # 'delete' end_node
            self.data = p_node.data
            self.next_node = None
            self.prev_node = p_node.prev_node
            self.prev_node.next_node = self

        if p_node != None and n_node != None:
            self.prev_node = None
            self.next_node = None
            self.data = None

    def front_link(self, new_node):
        '''
        Head insert
        Algorithm:
            - create new_node (Z)
            - set new_node (Z) p_node=None
            - set new_node (Z) n_node=previous_node (A)
            - set previous_node (A) p_node=new_node (Z)

        A. p_node=None, n_node=B
        B. p_node=A,    n_node=C
        C. p_node=B,    n_node=None
            ==> (Z.p_node=None, Z.n_node=A, A.p_node=Z)
        Z. p_node=None, n_node=A
        A. p_node=Z,    n_node=B
        B. p_node=A,    n_node=C
        C. p_node=B,    n_node=None
        
        OR 

        Middle insert
        Algorithm:
            - create new_node
            - set new_node(Z) p_node=previous_node(A)
            - set new_node(Z) n_node=next_node(B)
            - set previous_node(A) n_node=new_node(Z)
            - set next_node(B) p_node=new_node(Z)

        A. p_node=None, n_node=B
        B. p_node=A,    n_node=C
        C. p_node=B,    n_node=None
            ==> (A.n_node=Z, Z.p_node=A, Z.n_node=B, B.p_node=Z)
        A. p_node=None, n_node=Z
        Z. p_node=A,    n_node=B
        B. p_node=Z,    n_node=C
        C. p_node=B,    n_node=None

        OR

        Tail insert
        Algorithm:
            - 
        '''

        new_node.next_node = self
        new_node.prev_node = self.prev_node
        
        # tail insert
        if self.next_node != None:
            self.next_node.prev_node = new_node
        else:
            self.next_node = None
            self.prev_node.next_node = new_node
            self.prev_node = new_node
            return None

        # head insert
        if self.prev_node != None:
            self.prev_node.next_node = new_node
        else:
            # self == start_node, so we must copy all its content and create new node
            old_head = ListNode(self.data, self, self.next_node)
            self.next_node.prev_node = old_head
            self.next_node = old_head
            self.prev_node = None
            self.data = new_node.data
            return None

    # TODO back link
    def back_link(self, new_node):
        pass

class DLlist():
    def __repr__(self):
        str_repr = ''
        for idx in range(self.__length):
            str_repr += repr(self.next(True)) + '\n'
        
        self.__idx = 0
        self.__current_node = None
        
        return str_repr

    def __str__(self):
        res = '['
        for idx in range(self.__length):
            if type(self[idx]) == str:
                res += "'" + self[idx] + "'"
            elif type(self[idx]) == int:
                res += str(self[idx])
            elif type(self[idx]) == bool:
                res += str(self[idx])
            else:
                res += str(self[idx])

            if idx + 1 != self.__length:
                res += ', '

        res += ']'
        return res

    # returns listNode.data
    def __getitem__(self, key):
        if key < 0 or key >= self.__length:
            raise InvalidIndex(key)
        for idx in range(key + 1):
            current = self.next()

        self.__idx = 0
        self.__current_node = None
        return current

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def __len__(self):
        return self.__length

    def __init__(self):
        self.__idx    = 0
        self.__current_node = None

        self.__length = 0
        self.__start_node = None
        self.__end_node   = None

    def __len__(self):
        return self.__length

    # TODO hash realisation
    def __hash__(self):
        return hash(str(self))

    def next(self, get_list_node=False):
        if self.__idx < self.__length:
            if self.__idx == 0:
                self.__current_node = self.__start_node
            else:
                self.__current_node = next(self.__current_node)

            self.__idx += 1
            if get_list_node:
                return self.__current_node
            elif self.__current_node != None:
                return self.__current_node.data
            else:
                return None
        else:
            self.__current_node = None
            self.__idx = 0
            raise StopIteration()

    # TODO make reverse iteration possible, e.g. accessing by negative index: [-1]
    def prev(self, get_list_nodes=False):
        pass

    # returns a list node
    def __get(self, pos):
        if pos < 0 or pos >= self.__length:
            raise InvalidIndex(pos)
        for idx in range(pos + 1):
            current = self.next(True)

        self.__idx = 0
        self.__current_node = None
        return current

    # aka append in the end
    def push_back(self, data) -> int:
        if self.__start_node == None:
            self.__start_node = ListNode(data)
        elif self.__end_node == None:
            self.__end_node = ListNode(data, self.__start_node, None)
            self.__start_node.next_node = self.__end_node
        else:
            new_node = ListNode(data, self.__end_node, None)
            self.__end_node.next_node = new_node
            self.__end_node = new_node

        self.__length += 1
        return self.__length 

    # TODO push
    def push(self, data) -> int:
        pass

    def front_insert(self, data, pos: int) -> int:
        if pos < 0 or pos >= self.__length:
            raise InvalidIndex(pos)

        curr_node = self.__get(pos)
        new_node =  ListNode(data, None, None)
        curr_node.front_link(new_node)
        self.__length += 1

        return self.__length

    # TODO after_insert
    def after_insert(self, new_node) -> int:
        pass

    #def pop(self, pos: int):
    #    curr_node = self.__get(pos)
    #    curr_node.unlink()
    #    self.__length -= 1
    #    return curr_node.data

    def delete(self, pos: int):
        curr_node = self.__get(pos)

        curr_node.unlink()
        self.__length -= 1

        return self.__length

def main():
    print('Filling DoubleLinkedList with B, C, D, E, F')
    l = DLlist()
    l.push_back('A') # 0
    l.push_back('B') # 0
    l.push_back('C') # 1
    l.push_back('D') # 2
    l.push_back('E') # 3
    l.push_back('G') # 4
    # l.append('F') # 5

    lstdata = ', '.join([data for data in l])
    print(f'List data: {lstdata}')
    print(f'Double-linked list length: {len(l)}')
    #print(f'Element at idx[2]: {l[2]}')

    #print(f'Before deleting element at idx 2')
    #lstdata = ', '.join([data for data in l])
    #print(f'List data: {lstdata}')

    l.delete(0)
    lstdata = ', '.join([data for data in l])
    print(f'List data after deleting 0 element: {lstdata}')

    #l.insert('Z', 2)
    #lstdata = ', '.join([data for data in l])
    #print(f'List data after inserting \'Z\' at 2 index: {lstdata}')

    #print(f'Popped element from 0 position: {l.pop(2)}')
    #lstdata = ', '.join([data for data in l])
    #print(f'List data: {lstdata}')

    l.front_insert('A', 0)
    lstdata = ', '.join([data for data in l])
    print(f'List data after inserting \'A\' at 0 index: {lstdata}')

    l.front_insert('F', len(l)-1)
    lstdata = ', '.join([data for data in l])
    print(f'List data after inserting \'F\' at {len(l)-2} index: {lstdata}')

    l.delete(len(l)-1)
    lstdata = ', '.join([data for data in l])
    print(f'List data after deleting {len(l)} element: {lstdata}')

    #l.insert('Y', l.length-1)
    #lstdata = ', '.join([data for data in l])
    #print(f'List data after inserting \'Y\' at {l.length-1} index: {lstdata}')

    #l.delete(l.length - 1)
    #lstdata = ', '.join([data for data in l])
    #print(f'List data: {lstdata}')


if __name__ == '__main__':
    main()
