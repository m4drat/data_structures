from src.DLlist import DLlist

def main():
    l = DLlist([1, 2, 3, 4])
    print(f'Contents of l:\n{l.__repr__()}')

if __name__ == '__main__':
    main()