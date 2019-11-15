from __future__ import annotations

import HuffmanCoding.src.exceptions
import collections
import heapq
import copy

from dataclasses import dataclass
from graphviz import Digraph

@dataclass
class HuffmanCoding:
    vis_queue: list = None
    sorted_queue: list = None
    hf_codes: dict = None
    default_freq_dict: dict = None

    def visualize(self, sq_init=None) -> Digraph:
        '''
        Creates graphviz.Digraph graph to visualize Huffman tree
        Parameters
        ----------
        sq_init: heapq-transformed list with frequences and letters in this format: 
            [[1, ['.']], [2, ['h']]] (each element is a list with 0 element = char frequency,
            and 1 element = actual char) (in sub-lists with chars can be more, than 1 elements)
        Returns
        -------
            digraph: Digraph
        Raises
        ------
            exceptions.NotInitializedError: if vis_queue variable is not initialized
        '''
        # create deepcopy of variable, because we will change it 
        if sq_init == None:
            if self.vis_queue == None:
                raise exceptions.NotInitializedError(f'The variable vis_queue is not initialized!')
            else:
                sq_init = copy.deepcopy(self.vis_queue)
        else:
            sq_init = copy.deepcopy(sq_init)

        digraph = Digraph()

        # if there is only one letter in message
        if len(sq_init) == 1:
            digraph.node(f"'{sq_init[0][1][0]}'", shape='circle')
        else:
            # create end nodes for all letters
            for node in sq_init:
                digraph.node(name=node[1][0], label=f"'{node[1][0]}'", shape='circle')
            # iterate over heap, while there is no more unused nodes
            while len(sq_init) > 1:
                min0 = heapq.heappop(sq_init) # extract char with smallest frequency
                min1 = heapq.heappop(sq_init) # extract char with smallest frequency

                # create new node
                new_node = [min0[0] + min1[0]] + [[min0[1][0] + min1[1][0]]]

                # create merged node 
                digraph.node(name=new_node[1][0], label='', shape='point')

                # connect merged node with 2 other
                digraph.edge(head_name=min0[1][0], tail_name=new_node[1][0], label='0')
                digraph.edge(head_name=min1[1][0], tail_name=new_node[1][0], label='1')

                # push resulting node to heapq
                heapq.heappush(sq_init, new_node)
        
        return digraph

    def normalize(self, msg: str) -> str:
        '''
        convert string to uppercase (in case we want to use dictionary with already
            known char frequences, and there are only upper-case letters)
        Parameters
        ----------
        msg: str
            just a string with message
        Returns
        -------
            upper-case string: str
        '''
        return msg.upper()

    def un_encode(self, msg: str) -> str:
        '''
        to visually show, that message now is different
        Parameters
        ----------
        msg: str
            huffman-coded message
        Returns
        -------
            encoded string: str
        '''
        data = [msg[i:i+8] for i in range(0, len(msg), 8)]

        tmp = ''
        for idx in range(0, len(data)):
            # ascii_printable
            if int(data[idx], 2) < 127 and int(data[idx], 2) > 31:
                tmp += chr(int(data[idx], 2))
            else:
                tmp += f'\\x{hex(int(data[idx], 2))[2:].rjust(2, "0")}'
        return tmp

    def decode(self, msg: str, freq: dict) -> str:
        '''
        Parameters
        ----------
            msg: str
                huffman-coded message
            freq: dict
                dict with all char codes and their symbol
        Returns
        -------
            decoded string: str
        '''

        out = ''
        cnt = 0

        while cnt != len(msg):
            for k, v in freq.items():
                if msg[cnt:cnt+len(v)] == v:
                    out += k
                    cnt += len(v)
                else:
                    continue
        return out

    def encode(self, msg: str) -> str:
        '''
        Parameters
        ----------
        msg: str
            input message
        Returns
        -------
            huffman encoded binary string: str
        '''
        # convert string to uppercase
        # msg = self.normalize(msg)

        if type(msg) == str: # we need to count frequences in message
            freq_dict = collections.Counter(msg)
        elif type(msg) == dict: # we already have dict with chars and frequences
            freq_dict = msg

        # if we want to use frequences from another dict
        if self.default_freq_dict != None:
            for k in freq_dict.keys():
                freq_dict[k] = self.default_freq_dict[k]
                
        # convert freq_dict to heapq
        self.sorted_queue = [[freq, [char, ""]] for char, freq in freq_dict.items()]
        heapq.heapify(self.sorted_queue)

        # initialize vis_queue var, to work with graphs
        self.vis_queue = copy.deepcopy(self.sorted_queue)

        # there is only one letter in message
        if len(self.sorted_queue) == 1:
            self.sorted_queue[0][1][1] = '0'
        else:
            # iterate over heap, while there is no more unused nodes
            while len(self.sorted_queue) > 1:
                min0 = heapq.heappop(self.sorted_queue) # extract char with smallest frequency
                min1 = heapq.heappop(self.sorted_queue) # extract char with smallest frequency

                # update code value for char in heap
                for pair in min0[1:]:
                    pair[1] = '0' + pair[1]
                for pair in min1[1:]:
                    pair[1] = '1' + pair[1]

                # merge two nodes
                heapq.heappush(self.sorted_queue, [min0[0] + min1[0]] + min0[1:] + min1[1:])

        # heap now is list
        self.sorted_queue = heapq.heappop(self.sorted_queue)[1:]

        # create dict from heap (key - char, value - huffman code)
        self.hf_codes = dict(self.sorted_queue)

        # convert to binary string
        return ''.join([self.hf_codes[char] for char in msg])

def main():
    hc = HuffmanCoding()

    strs_to_encode = ['AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 
                      'sacra ignis Inquisitionis devorabit vos', 
                      'Лорем ипсум долор сит амет, харум медиоцритатем еа дуо, нобис хомеро аудиам не дуо.', 
                      'FFFFFFFHHHDDDJJJJJJJJJQQQQQPEEEEEEELLLLLDDDS']
    str_to_encode  = strs_to_encode[2]

    encoded = hc.encode(str_to_encode)
    decoded = hc.decode(encoded, hc.hf_codes)
    
    print(f'Encoded:   "{encoded}"')
    print(f'UnEncoded: "{hc.un_encode(encoded)}"')
    print(f'Decoded:   "{decoded}"')
    print(f'HF_codes:  "{hc.hf_codes}"')

    print(f'str_to_encode == decoded: {str_to_encode == decoded}')

    hc.visualize().view(cleanup=True)

if __name__ == '__main__':
    main()