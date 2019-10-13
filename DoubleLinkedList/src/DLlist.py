# -*- coding: utf-8 -*-
# @Author: madrat
# @Date:   2019-10-09 19:41:34

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
    def __eq__(self, other):
        if isinstance(other, ListNode):
            return (self.data == other.data and
                    self.prev_node == other.prev_node and
                    self.next_node == other.next_node)
        return False

    def __repr__(self):
        return '<curr_node.data={:<8}> ' \
               '<type={:<20}> ' \
               '<curr_node={:<9}> ' \
               '<prev_node={:<9}> ' \
               '<next_node={:<9}>'.format((str(self.data)[:8] if len(str(self.data)) <= 8
                                           else str(self.data)[:5] + '...'), 
                                          str(type(self.data))[str(type(self.data)).find('\''):-1],
                                          'None' if self == None else hex(id(self)), 
                                          'None' if self.prev_node == None else hex(id(self.prev_node)), 
                                          'None' if self.next_node == None else hex(id(self.next_node)))

    def __str__(self):
        return str(self.data)

    def __init__(self, data=None, prev_node=None, next_node=None):
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

    def copy():
        return ListNode(self.data, self.prev_node, self.next_node)

class DLlist():
    # TODO add correct comaprison
    def __eq__(self, other):
        if isinstance(other, DLlist):
            return (len(other) == self.__length and
                    sum([True for i, j in zip(self, other) if i == j]) == self.__length)
        return False

    def __repr__(self):
        str_repr = ''
        idx = 0
        try:
            while self.next():
                str_repr += '[{:>2}] {}\n'.format(str(idx), repr(self.__current_node))
                idx += 1
        except StopIteration:
            pass
        return str_repr

    def __str__(self):
        return str([f'{i}' for i in self])
        # return str([f'{i}' if type(i) == str else i for i in self])

    # TODO make it work with negative indexes
    def __setitem__(self, key, value):
        self.__get(key).data = value

    # TODO make it work with negative indexes
    def __getitem__(self, key):
        if key < -self.__length or key >= self.__length:
            raise InvalidIndex(key)
        if key < 0:
            pass
        else:
            for idx in range(key + 1):
                current = self.next()
        
        self.__current_node = None
        return current.data

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def __len__(self):
        return self.__length

    def __init__(self, size=0, init_list=None):
        self.__current_node = None

        self.__length = 0
        self.__start_node = None
        self.__end_node   = None

        if size < 0:
            raise NegativeListLength
        elif size > 0:
            for i in range(size):
                self.push_back(None)
        elif init_list != None:
            # check if object is iterable
            try:
                tmp = iter(init_list)
            except TypeError:
                raise InvalidInitList
            else:
                for elem in init_list:
                    self.push_back(elem)

    def __len__(self):
        return self.__length

    def __hash__(self):
        return hash(str(self))

    def next(self):
        if self.__current_node == None:
            self.__current_node = self.__start_node
        else:
            if self.__current_node.next() != None:
                self.__current_node = self.__current_node.next()
            else:
                self.__current_node = None
                raise StopIteration()

        return self.__current_node

    # TODO make reverse iteration possible, e.g. accessing by negative index: [-1]
    def prev(self):
        if self.__current_node == None:
            self.__current_node = self.__end_node
        else:
            if self.__current_node.prev() != None:
                self.__current_node = self.__current_node.prev()
            else:
                self.__current_node = None
                raise StopIteration()

        return self.__current_node

    # returns a list node
    def __get(self, pos):
        if pos < 0 or pos >= self.__length:
            raise InvalidIndex(pos)
        for idx in range(pos + 1):
            current = self.next()

        self.__idx = 0
        self.__current_node = None
        return current

    # aka append in the end
    def push_back(self, data) -> int:
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
            +                    |                                  |
                                 +----------------------------------+
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
        |   +  new_node      = ListNode(data, None, self.start)
        |   |  self.start    = new_node
        |   |  self.end.prev = self.start
        |   |
        |   |     +--------------------------+ +--------------------------+
        +-> |     | self.start               | | self.end(old)            |  self.end (new)
            |    +v-----+------+------+     ++-v---+------+------+    +---+--+------+------+
            |    |      | Data | next |     | prev | Data |      |    |      | Data |      |
            |    | prev | AAAA | (old)|     | start| BBBB | end  |    | end  | CCCC | next |
            |    | None |      | end  |     |      |      | (new)|    |(old) |      | None |
            |    +------+------+--+---+     +---^---------+--+---+    +--^---+------+------+
            +                     |             |            |           |
                                  +-------------+            +-----------+
                '''
                new_node = ListNode(data, self.__end_node, None)
                self.__end_node.next_node = new_node
                self.__end_node = self.__end_node.next_node

        self.__length += 1
        return self.__length 

    # TODO push
    def push_front(self, data) -> int:
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
            +                                           |           |
                                                        +-----------+
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
            +                     |             |            |           |
                                  +-------------+            +-----------+
                '''
                new_node = ListNode(data, None, self.__start_node)
                self.__start_node.prev_node = new_node
                self.__start_node = self.__start_node.prev_node

        self.__length += 1
        return self.__length

    def front_insert(self, data, pos: int) -> int:
        if pos < 0 or pos >= self.__length:
            raise InvalidIndex(pos)

        curr_node = self.__get(pos)
        new_node =  ListNode(data, None, None)
        curr_node.front_link(new_node, self.__start_node, self.__end_node)
        self.__length += 1

        return self.__length

    # TODO after_insert
    def after_insert(self, data, pos: int) -> int:
        raise NotImplementedError()
        pass

    # deletes 1 element from dll
    def delete(self, pos: int) -> int:
        curr_node = self.__get(pos)

        curr_node.unlink(self.__start_node, self.__end_node)
        self.__length -= 1

        return self.__length

    # creates an independent copy of dll
    def copy(self):
        return DLlist(init_list=self)

def main():
    import timeit

    start = timeit.default_timer()
    print('Filling DoubleLinkedList with A, B, C, D, E, F, G')
    l = DLlist()
    l.push_back('A') # 0
    l.push_back('B') # 1
    l.push_back('C') # 2
    l.push_back('D') # 3
    l.push_back('E') # 4

    print(l)

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
    main()
