from __future__ import annotations

import collections
import typing
import heapq

from dataclasses import dataclass

@dataclass
class ListNode:
    left: ListNode
    right: ListNode
    value: typing.Any

@dataclass
class HuffmanCoding:
    heap: list = None
    hf_codes: dict = None
    default_freq_dict: dict = None

    def normalize(self, msg: str) -> str:
        return msg.upper()

    def decode(self, msg: str, freq: dict) -> str:
        '''
        params:
            msg: str
                huffman-coded message
            freq: dict
                dict with all char codes and their symbol 
        return: str
            decoded string
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
        msg: str
            input message
        return: str
            huffman encoded binary string
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
        self.heap = [[freq, [char, ""]] for char, freq in freq_dict.items()]
        heapq.heapify(self.heap)

        # iterate over heap, while there is no more unused nodes
        while len(self.heap) > 1:
            min0 = heapq.heappop(self.heap) # extract char with smallest frequency
            min1 = heapq.heappop(self.heap) # extract char with smallest frequency

            # update code value for char in heap
            for pair in min0[1:]:
                pair[1] = '0' + pair[1]
            for pair in min1[1:]:
                pair[1] = '1' + pair[1]

            # merge two nodes
            heapq.heappush(self.heap, [min0[0] + min1[0]] + min0[1:] + min1[1:])

        # heap now is list
        self.heap = heapq.heappop(self.heap)[1:]

        # create dict from heap (key - char, value - huffman code)
        self.hf_codes = dict(self.heap)

        # convert to binary string
        return ''.join([self.hf_codes[char] for char in msg])

def main():
    hc = HuffmanCoding()

    str_to_encode = 'Ларионов-Тришкин Теодор Арсений'

    encoded = hc.encode(str_to_encode)
    decoded = hc.decode(encoded, hc.hf_codes)
    
    print(f'Encoded: {encoded}')
    print(f'Decoded: {decoded}')

    print(f'str_to_encode == decoded: {str_to_encode == decoded}')

if __name__ == '__main__':
    main()