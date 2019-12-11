from dataclasses import dataclass
from bitarray import bitarray
from typing import *
import time

IS_DEBUG: bool = False

@dataclass
class Node:
    offset: int   # 
    length: int   #
    next_chr: bytes # next character

    def __str__(self):
        if (ord(self.next_chr) > 0x20 and ord(self.next_chr) < 0x7f) or (ord(self.next_chr) > 0x410 and ord(self.next_chr) < 0x44f):
            return f'[{self.offset}][{self.length}][{self.next_chr}]'
        return f'[{self.offset}][{self.length}][\\x{hex(ord(self.next_chr))[2:].zfill(2)}]'

@dataclass
class LZ77:
    search_buffer_size: int = 100
    proactive_buffer_size: int = 100

    @staticmethod
    def clamp(num, min_value, max_value):
        return max(min(num, max_value), min_value)

    def compress(self, msg: bytes) -> List[Node]:
        search_iterator = 0
        position = 0

        nodes = []

        while position < len(msg):
            search_buffer = msg[search_iterator:position]
            proactive = msg[position:position + min(self.search_buffer_size, len(msg) - position)]
            
            node = self.search(search_buffer, proactive)

            if IS_DEBUG:
                print(str(node))

            position = position + node.length + 1
            search_iterator = position - self.search_buffer_size

            nodes.append(node)
        
        return nodes

    def decompress(self, nodes: List[Node]) -> str:
        msg = ''
        for node in nodes:
            if node.length == 0 and node.offset == 0:
                try:
                    msg += chr(node.next_chr)
                except TypeError:
                    msg += node.next_chr
            else:
                if len(msg) - self.search_buffer_size < 0:
                    msg += msg[node.offset:node.offset + node.length]
                else:
                    msg += msg[node.offset + len(msg) - self.search_buffer_size:len(msg) - self.search_buffer_size + node.offset + node.length]
                try:
                    msg += chr(node.next_chr)
                except TypeError:
                    msg += node.next_chr
        return msg

    def search(self, search_buffer: bytes, proactive: bytes) -> Node:
        if len(search_buffer) == 0:
            return Node(0, 0, proactive[0])

        elif len(proactive) == 0:
            return Node(-1, -1, '')

        best_length = 0
        best_offset = 0 
        buf = search_buffer + proactive

        search_pointer = len(search_buffer)	

        for i in range(0, len(search_buffer)):
            length = 0
            while buf[i+length] == buf[search_pointer +length]:
                length = length + 1
                if search_pointer+length == len(buf):
                    length = length - 1
                    break
                if i+length >= search_pointer:
                    break	 
            if length > best_length:
                best_offset = i
                best_length = length

        return Node(best_offset, best_length, buf[search_pointer+best_length])

    def write(self, nodes: List[Node], fpath: str) -> None:
        with open(fpath, 'wb') as file:
            for node in nodes:
                file.write(str(node).encode())
        return None

def compare():
    with open('C:/Users/madrat/Desktop/data.bin', 'rb') as file:
        data = file.read()
        print(f'Data size: {len(data)}')

        lz77 = LZ77(64, 1024)
        start_time = time.time()
        compressed = lz77.compress(data)
        end_time = time.time()
        print(f'Data size compressed: {len(compressed) * 5}')
        print(f'Compression time (64, 1024): {end_time - start_time} seconds')
        

        lz77 = LZ77(512, 1024)
        start_time = time.time()
        compressed = lz77.compress(data)
        end_time = time.time()
        print(f'Data size compressed: {len(compressed) * 5}')
        print(f'Compression time (512, 1024): {end_time - start_time} seconds')

        lz77 = LZ77(2048, 1024)
        start_time = time.time()
        compressed = lz77.compress(data)
        end_time = time.time()
        print(f'Data size compressed: {len(compressed) * 5}')
        print(f'Compression time (2048, 1024): {end_time - start_time} seconds')

        lz77 = LZ77(2 ** 16, 1024)
        start_time = time.time()
        compressed = lz77.compress(data)
        end_time = time.time()
        print(f'Data size compressed: {len(compressed) * 5}')
        print(f'Compression time (2 ** 16, 1024): {end_time - start_time} seconds')

        # test big proactive
        lz77 = LZ77(64, 2 ** 8)
        start_time = time.time()
        compressed = lz77.compress(data)
        end_time = time.time()
        print(f'Data size compressed: {len(compressed) * 5}')
        print(f'Compression time (64, 2 ** 8): {end_time - start_time} seconds')

        lz77 = LZ77(512, 2 ** 8)
        start_time = time.time()
        compressed = lz77.compress(data)
        end_time = time.time()
        print(f'Data size compressed: {len(compressed) * 5}')
        print(f'Compression time (512, 2 ** 8): {end_time - start_time} seconds')

        lz77 = LZ77(2048, 2 ** 8)
        start_time = time.time()
        compressed = lz77.compress(data)
        end_time = time.time()
        print(f'Data size compressed: {len(compressed) * 5}')
        print(f'Compression time (2048, 2 ** 8): {end_time - start_time} seconds')

        lz77 = LZ77(2 ** 16, 2 ** 8)
        start_time = time.time()
        compressed = lz77.compress(data)
        end_time = time.time()
        print(f'Data size compressed: {len(compressed) * 5}')
        print(f'Compression time (2 ** 16, 2 ** 8): {end_time - start_time} seconds')

def main():
    lz77 = LZ77(5, 5)
    compressed = lz77.compress('клара у карла украла кораллы')
    lz77.write(compressed, 'C:/Users/madrat/Desktop/out.txt')
    decompressed = lz77.decompress(compressed)
    print(decompressed)

if __name__ == '__main__':
    compare()