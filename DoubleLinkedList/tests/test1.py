import unittest
from src.DLlist import *

class Test_test1(unittest.TestCase):
    def test_A(self):
        l = DLlist()
        l.push_back(1)
        l.push_back(2)
        l.push_back(3)
        l.push_back(True)
        l.push_back('AAAA')

        assert l[2] == 3
    
    def test_B(self):
        l = DLlist()
        l.push_back(1)
        l.delete(0)

        assert len(l) == 0

    def test_C(self):
        l = DLlist()
        l.push_back(1)
        l.push_back(2)
        l.delete(0)

        assert len(l) == 1

    def test_D(self):
        l = DLlist()
        l.push_back(1)
        l.push_back(2)
        l.push_back(3)
        l.delete(0)

        assert len(l) == 2

    def test_E(self):
        l = DLlist()
        l.push_back(1)
        l.push_back(2)
        l.push_back(3)
        l.delete(2)

        assert len(l) == 2

    def test_F(self):
        l = DLlist()
        l.push_back(1)
        l.push_back(2)
        l.push_back(3)
        l.delete(1)

        assert len(l) == 2

    def test_G(self):
        l1 = DLlist()
        l1.push_back(1)
        l1.push_back(2)
        l1.push_back(3)

        l2 = DLlist()
        l2.push_back(2)
        l2.push_back(3)
        l2.push_back(4)

        assert l1 != l2

    def test_H(self):
        l1 = DLlist()
        l1.push_back(1)
        l1.push_back(2)
        l1.push_back(3)

        l2 = DLlist()
        l2.push_back(1)
        l2.push_back(2)
        l2.push_back(3)

        tmpdict = {l1 : 'AAAA', l2 : 'BBBB'}

        assert tmpdict[l1] == 'AAAA'
        assert tmpdict[l2] == 'BBBB'

    #def test_I(self):
    #    l1 = DLlist()
    #    l1.push_back(1)
    #    l1.push_back(2)
    #    l1.push_back(3)
    #    assert l1.pop(1) == 2
    #    assert len(l1) == 2

    def test_J(self):
        l1 = DLlist()
        l1.push_back(1)
        l1.push_back(2)
        l1.push_back(4)

        assert l1.front_insert(3, 2) == 4
        assert len(l1) == 4

    def test_K(self):
        l1 = DLlist()
        for i in range(0, 0x100):
            l1.push_back(str(i))
        
        assert len(l1) == 0x100

        for i in range(0x100-1, -1, -1):
            l1.delete(i)

        assert len(l1) == 0x0

if __name__ == '__main__':
    unittest.main()
