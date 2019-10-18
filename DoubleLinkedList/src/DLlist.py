# -*- coding: utf-8 -*-
# @Author: madrat
# @Date:   2019-10-09 19:41:34

from __future__ import annotations # to support Forward-annotations
import typing

class NegativeListLength(Exception):
    def __init__(self):
        Exception.__init__(self, 'Trying to initialize double linked list with negative length!')

class InvalidInitList(Exception):
    def __init__(self):
        Exception.__init__(self, 'Trying to initialize double linked list with incorrect init_list!')

class InvalidIndex(Exception):
    def __init__(self, msg):
        Exception.__init__(self, f'Trying to access element at impossible index: {msg}')

class ListNode():
    data: typing.Any
    prev_node: ListNode
    next_node: ListNode

    def __init__(self, data=None, prev_node=None, next_node=None):
        self.data      = data
        self.prev_node = prev_node
        self.next_node = next_node

    def __eq__(self, other):
        if isinstance(other, ListNode):
            return self.data == other.data
        return False

    def __repr__(self) -> str:
        return '<curr_node.data={:<8}> ' \
               '<type={:<20}> ' \
               '<curr_node={:<9}> ' \
               '<prev_node={:<9}> ' \
               '<next_node={:<9}>'.format((str(self.data)[:8] if len(str(self.data)) <= 8
                                           else str(self.data)[:5] + '...'), 
                                           self.data.__class__.__name__,
                                          'None' if self == None else hex(id(self)), 
                                          'None' if self.prev_node == None else hex(id(self.prev_node)), 
                                          'None' if self.next_node == None else hex(id(self.next_node)))

    def __str__(self) -> str:
        return f'<{self.__class__.__name__} object at {hex(id(self))}>'

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        return self.next_node

    def prev(self):
        return self.prev_node

    def copy(self) -> ListNode:
        return ListNode(self.data, self.prev_node, self.next_node)

    def clear_node(self):
        self.data = None
        self.prev_node = None
        self.next_node = None


class DLlist():
    __current_node: ListNode
    __length: int
    __start_node: ListNode
    __end_node: ListNode

    def __init__(self, initializer=None):
        self.__current_node = None

        self.__length = 0
        self.__start_node = None
        self.__end_node   = None

        
        if initializer == None:
            pass
        elif isinstance(initializer, int):
            # initialize by size
            if initializer < 0:
                raise NegativeListLength
            elif initializer > 0:
                for i in range(initializer):
                    self.push_back(None)
        else:
            # check if object is iterable
            try:
                tmp = iter(initializer)
            except TypeError:
                raise InvalidInitList
            else:
                for elem in initializer:
                    self.push_back(elem)

    def __eq__(self, other):
        if isinstance(other, DLlist):
            return (len(other) == self.__length and
                    sum([True for i, j in zip(self, other) if i == j]) == self.__length)
        return False

    def __repr__(self) -> str:
        try:
            str_repr = ''
            idx = 0
            while self.next():
                str_repr += '[{:>2}] {}\n'.format(str(idx), repr(self.__current_node))
                idx += 1
        except StopIteration:
            pass
        finally:
            return str_repr

    def __str__(self) -> str:
        return str([f'{i}' for i in self])
        # return str([f'{i.to_str()}' for i in self])
        # return str([f'{i}' if type(i) == str else i for i in self])

    # TODO make it work with negative indexes
    def __setitem__(self, key: int, value: typing.Any) -> None:
        self.__get(key).data = value

        return None

    # TODO make it work with slices
    def __getitem__(self, given) -> typing.Any:
        if isinstance(given, slice):
            raise NotImplementedError
        elif isinstance(given, int):
            if given < 0 and given >= -self.__length:
                given += self.__length
            elif given < -self.__length or given >= self.__length:
                raise InvalidIndex(given)
            for idx in range(given + 1):
                current = self.next()
        
        self.__current_node = None
        return current.data

    # returns a list node
    def __get(self, pos: int) -> ListNode:
        if isinstance(pos, slice):
            raise NotImplementedError
        elif isinstance(pos, int):
            if pos < 0 and pos >= -self.__length:
                pos += self.__length
            elif pos < -self.__length or pos >= self.__length:
                raise InvalidIndex(pos)
            for idx in range(pos + 1):
                current = self.next()
        
        self.__current_node = None
        return current

    # FIXME
    def __iter__(self):
        return self

    def __next__(self):
        return self.next().data

    def __len__(self):
        return self.__length

    def __hash__(self):
        return hash(str(self))

    def next(self) -> ListNode:
        if self.__current_node == None:
            self.__current_node = self.__start_node
        else:
            if self.__current_node.next() != None:
                self.__current_node = self.__current_node.next()
            else:
                self.__current_node = None
                raise StopIteration()

        return self.__current_node

    def prev(self) -> ListNode:
        if self.__current_node == None:
            self.__current_node = self.__end_node
        else:
            if self.__current_node.prev() != None:
                self.__current_node = self.__current_node.prev()
            else:
                self.__current_node = None
                raise StopIteration()

        return self.__current_node

    # aka append in the end
    def push_back(self, data: typing.Any) -> int:
        if self.__start_node == None and self.__end_node == None:
            # Base case. List isn't initialized
            '''
            1.
        +-+    self.start = None
        |      self.end   = None
        |
        |   2.
        |
        |   +  new_node   = ListNode(data, None, None)
        |   |  self.start = new_node
        |   |  self.end   = self.start
        |   |  # self.end is self.start
        |   |
        +-> |        self.start  <-------->   self.end
            |  +------+------+- ----+  +------+------+------+
            |  |      | Data |      |  |      | Data |      |
            |  | prev | AAAA | next |  | prev | AAAA | next |
            |  | None |      | None |  | None |      | None |
            +  +------+------+------+  +------+------+------+
            '''
            new_node = ListNode(data) # prev and next = None
            self.__start_node = new_node
            self.__end_node = self.__start_node

            # Just to be sure (i dont like python...)
            assert self.__end_node is self.__start_node, '1. WTF? end != start'
        else:
            if self.__start_node != None and self.__end_node is self.__start_node:
                # Second case (right after base), make self.__start_node and self.__end_node independent
                '''
            1.
        +-+    self.start == self.end
        |
        |   2.
        |
        |   +  new_node      = ListNode(data, self.end, None)
        |   |  self.end      = new_node
        |   |  self.end.prev = self.start
        |   |
        |   |     +------------------------------------------------+
        +-> |     |  self.start           self.end(deleted)        |  self.end
            |  +--v---+------+------+  +------+------+------+    +---+--+------+------+
            |  |      | Data |      |  |      | Data |      |    |      | Data |      |
            |  | prev | AAAA | next |  | prev | BBBB | end  |    | start| BBBB | next |
            |  | None |      | end  |  | None |      |      |    |      |      | None |
            |  +------+------+------+  +------+------+------+    +--^---+------+------+
            |                    |                                  |
            +                    +----------------------------------+
                '''
                new_node = ListNode(data, self.__end_node, None)
                self.__end_node = new_node
                self.__start_node.next_node = self.__end_node

                assert self.__end_node is not self.__start_node, '2. WTF? end == start'
            else:
                # Third general case
                '''
            1.
        +-+    self.start = node_1 (points to self.end)
        |      self.end   = node_2 (points to self.start)
        |   2.
        |
        |   +  new_node      = ListNode(data, self.end, None)
        |   |  self.end.next = new_node  
        |   |  self.end      = self.end.next
        |   |  
        |   |
        |   |     +--------------------------+ +--------------------------+
        +-> |     | self.start               | | self.end(old)            |  self.end (new)
            |    +v-----+------+------+     ++-v---+------+------+    +---+--+------+------+
            |    |      | Data | next |     | prev | Data |      |    |      | Data |      |
            |    | prev | AAAA | (old)|     | start| BBBB | end  |    | end  | CCCC | next |
            |    | None |      | end  |     |      |      | (new)|    |(old) |      | None |
            |    +------+------+--+---+     +---^---------+--+---+    +--^---+------+------+
            |                     |             |            |           |
            +                     +-------------+            +-----------+
                '''
                new_node = ListNode(data, self.__end_node, None)
                self.__end_node.next_node = new_node
                self.__end_node = self.__end_node.next_node

        self.__length += 1
        return self.__length 

    def push_front(self, data: typing.Any) -> int:
        if self.__start_node == None and self.__end_node == None:
            # Base case. List isn't initialized
            '''
            1.
        +-+    self.start = None
        |      self.end   = None
        |
        |   2.
        |
        |   +  new_node   = ListNode(data, None, None)
        |   |  self.start = new_node
        |   |  self.end   = self.start
        |   |  # self.end is self.start
        |   |
        +-> |        self.start  <-------->   self.end
            |  +------+------+- ----+  +------+------+------+
            |  |      | Data |      |  |      | Data |      |
            |  | prev | AAAA | next |  | prev | AAAA | next |
            |  | None |      | None |  | None |      | None |
            +  +------+------+------+  +------+------+------+
            '''
            new_node = ListNode(data) # prev and next = None
            self.__start_node = new_node
            self.__end_node = self.__start_node

            # Just to be sure (i dont like python...)
            assert self.__end_node is self.__start_node, '1. WTF? end != start'
        else:
            if self.__start_node != None and self.__end_node is self.__start_node:
                # Second case (right after base), make self.__start_node and self.__end_node independent
                '''
            1.
        +-+    self.start == self.end
        |
        |   2.
        |
        |   +  new_node      = ListNode(data, None, self.end)
        |   |  self.start    = new_node
        |   |  self.end.prev = self.start
        |   |
        |   |                           +--------------------------+
        +-> |   self.start (deleted)    | self.start(new_node)     |  self.end
            |  +------+------+- ----+  +v-----+------+------+    +---+--+------+------+
            |  |      | Data |      |  |      | Data |      |    |      | Data |      |
            |  | prev | AAAA | next |  | prev | BBBB | end  |    | start| AAAA | next |
            |  | None |      | None |  | None |      |      |    |      |      | None |
            |  +------+------+------+  +------+------+--+---+    +--^---+------+------+
            |                                           |           |
            +                                           +-----------+
                '''
                new_node = ListNode(data, None, self.__end_node)
                self.__start_node = new_node
                self.__end_node.prev_node = self.__start_node

                assert self.__end_node is not self.__start_node, '2. WTF? end == start'
            else:
                # Third general case
                '''
            1.
        +-+    self.start = node_1 (points to self.end)
        |      self.end   = node_2 (points to self.start)
        |   2.
        |
        |   +  new_node      = ListNode(data, None, self.start)
        |   |  self.start    = new_node
        |   |  self.end.prev = self.start
        |   |
        |   |     +--------------------------+ +--------------------------+
        +-> |     | self.start(new)          | |self.start(old)           |  self.end
            |    +v-----+------+------+     ++-v---+------+------+    +---+--+------+------+
            |    |      | Data | next |     | prev | Data |      |    |      | Data |      |
            |    | prev | CCCC |  old |     | new  | BBBB | end  |    | start| AAAA | next |
            |    | None |      | start|     | start|      |      |    |      |      | None |
            |    +------+------+--+---+     +---^---------+--+---+    +--^---+------+------+
            |                     |             |            |           |
            +                     +-------------+            +-----------+
                '''
                new_node = ListNode(data, None, self.__start_node)
                self.__start_node.prev_node = new_node
                self.__start_node = self.__start_node.prev_node

        self.__length += 1
        return self.__length

    # TODO insert before given element
    def front_insert(self, data: typing.Any, pos: int) -> int:
        raise NotImplementedError()
        return self.__length

    # TODO insert after given element
    def rear_insert(self, data: typing.Any, pos: int) -> int:
        raise NotImplementedError()
        return self.__length

    # TODO node deletion
    def delete(self, pos: int) -> int:
        raise NotImplementedError()
        return self.__length

    # creates an independent copy of dll
    def copy(self) -> DLlist:
        return DLlist(self)

    # Todo 'clear' implementation
    def clear(self) -> None:
        raise NotImplementedError

        self.__current_node = None
        try:
            while self.next():
                curr = self.__current_node 
                self.__current_node = self.__current_node.next_node 
                self.__current_node.clear_node()
        except StopIteration:
            pass

        self.__current_node = None
        self.__length = 0

        return None

def test():
    import timeit

    start = timeit.default_timer()
    print('Filling DoubleLinkedList with A, B, C, D, E')
    l = DLlist()
    l.push_back('A') # 0
    l.push_back('B') # 1
    l.push_back('C') # 2
    l.push_back('D') # 3
    l.push_back('E') # 4

    print(l)

    for node in l:
        for node2 in l:
            print(node, node2)

    l.clear()

    exit()

    # print(l[1:4])

    #lstdata = ', '.join([data.data for data in l])
    #print(f'List data: {lstdata}')
    #print(f'Double-linked list length: {len(l)}')
    ##print(f'Element at idx[2]: {l[2]}')

    ##print(f'Before deleting element at idx 2')
    ##lstdata = ', '.join([data for data in l])
    ##print(f'List data: {lstdata}')

    #l.delete(0)
    #lstdata = ', '.join([data for data in l])
    #print(f'List data after deleting 0 element: {lstdata}')

    ##l.insert('Z', 2)
    ##lstdata = ', '.join([data for data in l])
    ##print(f'List data after inserting \'Z\' at 2 index: {lstdata}')

    ##print(f'Popped element from 0 position: {l.pop(2)}')
    ##lstdata = ', '.join([data for data in l])
    ##print(f'List data: {lstdata}')

    #l.front_insert('A', 0)
    #lstdata = ', '.join([data for data in l])
    #print(f'List data after inserting \'A\' at 0 index: {lstdata}')

    #l.front_insert('F', len(l)-1)
    #lstdata = ', '.join([data for data in l])
    #print(f'List data after inserting \'F\' at {len(l)-2} index: {lstdata}')

    #l.delete(len(l)-1)
    #lstdata = ', '.join([data for data in l])
    #print(f'List data after deleting {len(l)} element: {lstdata}')

    ##l.insert('Y', l.length-1)
    ##lstdata = ', '.join([data for data in l])
    ##print(f'List data after inserting \'Y\' at {l.length-1} index: {lstdata}')

    ##l.delete(l.length - 1)
    ##lstdata = ', '.join([data for data in l])
    ##print(f'List data: {lstdata}')
    #l = DLlist()
    #l.push_back('A')
    #l.push_back('B')
    #l.push_back('C')
    #l.push_back('D')
    #print(l)

    stop = timeit.default_timer()

    print(f'Execution time: {stop-start:.6f} s')

if __name__ == '__main__':
    test()
