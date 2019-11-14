from src.HuffmanCoding import HuffmanCoding

def main():
    hc = HuffmanCoding()
    print(f"{hc.encode('JFFEEQPPDDPSSMPZXXC')}")
    print(f"{hc.heap}")

if __name__ == '__main__':
    main()