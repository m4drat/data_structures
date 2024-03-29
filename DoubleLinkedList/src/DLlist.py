# -*- coding: utf-8 -*-
# @Author: madrat
# @Date:   2019-10-09 19:41:34

from __future__ import annotations # to support Forward-annotations
import typing
import gc

class ListIsEmpty(Exception):
    def __init__(self):
        Exception.__init__(self, 'Cannot insert node, because List is empty!')

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
               '<type={:<10}> ' \
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

    def __iter__(self) -> ListNode:
        return self

    def __next__(self) -> ListNode:
        return self.next()

    def next(self) -> ListNode:
        '''returns next node, that references in current

        Returns
        -------
            ListNode or None
        '''
        return self.next_node

    def prev(self) -> ListNode:
        '''returns previous node, that references in current
        Returns
        -------
            ListNode or None
        '''
        return self.prev_node

    def copy(self) -> ListNode:
        '''Copies current node

        Returns
        -------
            independent ListNode
        '''
        return ListNode(self.data, self.prev_node, self.next_node)

    def clear_node(self) -> None:
        '''Clears current node, by setting all its pointers to None
        
        Returns
        -------
            None
        '''
        self.data = None
        self.prev_node = None
        self.next_node = None

        return None

class DLlist():
    __current_node: ListNode
    __length: int
    __start_node: ListNode
    __end_node: ListNode

    def __init__(self, initializer=None, current_node=None):
        self.__current_node = current_node

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

    def __eq__(self, other) -> bool:
        if isinstance(other, DLlist):
            return (len(other) == self.__length and
                    sum([True for i, j in zip(self, other) if i == j]) == self.__length)
        return False

    def __repr__(self) -> str:
        try:
            str_repr = ''
            idx = 0
            while self.next():
                str_repr += '[{idx:>{align}}] {node}\n'.format(idx=str(idx), align=len(str(self.__length)), node=repr(self.__current_node))
                idx += 1
        except StopIteration:
            pass
        finally:
            return str_repr

    def __str__(self) -> str:
        return str([f'{i}' for i in self])

    # TODO make it work with negative indexes
    def __setitem__(self, key: int, value: typing.Any) -> None:
        self.__get(key).data = value
        return None

    # TODO make it work with slices + refactor
    def __getitem__(self, given: int) -> typing.Any:
        if isinstance(given, slice):
            raise NotImplementedError
        elif isinstance(given, int):
            if given < 0 and given >= -self.__length:
                given += self.__length
            elif self.__length == 0:
                raise ListIsEmpty()
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
            elif self.__length == 0:
                raise ListIsEmpty()
            elif pos < -self.__length or pos >= self.__length:
                raise InvalidIndex(pos)
            for idx in range(pos + 1):
                current = self.next()
        
        self.__current_node = None
        return current

    # FIXME make it work with nested loops
    def __iter__(self) -> DLlist:
        return DLlist(self, self.__current_node)

    # TODO refactor!
    def __next__(self) -> typing.Any:
        return self.next().data

    def __len__(self) -> int:
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
        '''append new ListNode in the end, with node.data = data
        
        Parameters
        ----------
        data: can be any type

        Returns
        -------
            list length : int 
        '''
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
        '''insert new ListNode at the beginning
        
        Parameters
        ----------
            data: can be any type

        Returns
        -------
            list length : int 
        '''
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

    def front_insert(self, data: typing.Any, pos: int) -> int:
        '''insert new node, with node.data = data before given node (by index)
        
        Parameters
        ----------
            data: can be any type
            pos: int (index, before which element you want to insert new node)

        Returns
        -------
            list length : int 
        '''

        node = self.__get(pos)

        # First node in the list
        if self.__start_node != None and self.__end_node is self.__start_node:
            new_node = ListNode(data, None, self.__end_node)
            self.__start_node = new_node
            self.__end_node.prev_node = self.__start_node
        # node is head
        elif node is self.__start_node:
            new_node = ListNode(data, None, self.__start_node)
            node.prev_node = new_node
            self.__start_node = new_node
        # node is tail
        elif node is self.__end_node:
            new_node = ListNode(data, node.prev_node, node)
            node.prev_node.next_node = new_node
            node.prev_node = new_node
        else:
            new_node = ListNode(data, node.prev_node, node)
            node.prev_node.next_node = new_node

        self.__length += 1

        return self.__length

    def rear_insert(self, data: typing.Any, pos: int) -> int:
        '''insert new node, with node.data = data after given node (by index)
        
        Parameters
        ----------
            data: can be any type
            pos: int (index, after which element you want to insert new node)

        Returns
        -------
            list length : int 
        '''
        
        node = self.__get(pos)

        # First node in the list
        if self.__start_node != None and self.__end_node is self.__start_node:
            new_node = ListNode(data, self.__start_node, None)
            self.__end_node = new_node
            self.__start_node.next_node = self.__end_node
        # node is head
        elif node is self.__start_node:
            new_node = ListNode(data, node, node.next_node)
            node.next_node.prev_node = new_node
            node.next_node = new_node
        # node is tail
        elif node is self.__end_node:
            new_node = ListNode(data, self.__end_node, None)
            node.next_node = new_node
            self.__end_node = new_node
        else:
            new_node = ListNode(data, node, node.next_node)
            node.next_node.prev_node = new_node
            node.next_node = new_node

        self.__length += 1

        return self.__length

    def delete(self, pos: int) -> int:
        '''delete one element from list
        
        Parameters
        ----------
            pos: int (index, where you want to delete node)

        Returns
        -------
            list length : int 
        '''
        node = self.__get(pos)

        # First node in the list
        if self.__start_node != None and self.__end_node is self.__start_node:
            self.__start_node = None
            self.__end_node = None
        # node is head
        elif node is self.__start_node:
            self.__start_node.next_node.prev_node = None
            self.__start_node = self.__start_node.next_node
        # node is tail
        elif node is self.__end_node:
            self.__end_node.prev_node.next_node = None
            self.__end_node = self.__end_node.prev_node
        else:
            node.prev_node.next_node = node.next_node
            node.next_node.prev_node = node.prev_node

        self.__length -= 1

        gb = gc.collect()
        if __debug__:
            print(f'Objects collected by gc: {gb}')

        return self.__length

    # creates an independent copy of dll
    def copy(self) -> DLlist:
        '''create independent copy of current list

        Returns
        -------
            DLlist
        '''
        return DLlist(self)

    # TODO
    def find(self, needle) -> typing.Any:
        '''search for needle in DLlist

        Parameters
        ----------
            needle: any data type you need

        Returns
        -------
            index, where needle is found or None
        '''
        raise NotImplementedError()

    def clear(self) -> None:
        '''clear memory currently occupied by list (delete all pointers in each node)
        
        Returns
        -------
            None
        '''
        self.__start_node = None
        self.__end_node = None

        self.__current_node = None
        self.__length = 0

        gb = gc.collect()
        if __debug__:
            print(f'Objects collected by gc: {gb}')

        return None

def test():
    import timeit

    start = timeit.default_timer()
    print(' Filling DoubleLinkedList with A, B, C, D, E')
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

    stop = timeit.default_timer()

    print(f'Execution time: {stop-start:.6f} s')

if __name__ == '__main__':
    test()
