import collections
import binarytree
import heapq

from dataclasses import dataclass

@dataclass
class HuffmanCoding:
    heap: list = None
    default_freq_dict: dict = None

    def normalize(self, msg: str):
        return msg.upper()

    def decode(self):
        pass

    def encode(self, msg: str):
        # convert string to uppercase
        msg = self.normalize(msg)

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

        while len(self.heap) > 1:
            min0 = heapq.heappop(self.heap) # extract char with smallest frequency
            min1 = heapq.heappop(self.heap) # extract char with smallest frequency

            for pair in min0[1:]:
                pair[1] = '0' + pair[1]
            for pair in min1[1:]:
                pair[1] = '1' + pair[1]

            heapq.heappush(self.heap, [min0[0] + min1[0]] + min0[1:] + min1[1:])

        self.heap = sorted(heapq.heappop(self.heap)[1:], key=lambda p: (len(p[-1]), p))

        return ''.join([dict(self.heap)[char] for char in msg])

def main():
    pass

if __name__ == '__main__':
    main()