import unittest
from DoubleLinkedList.src.DLlist import DLlist

class TestDefaultFunctionality(unittest.TestCase):
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
        l2.push_back(4)

        tmpdict = {l1 : 'AAAA', l2 : 'BBBB'}

        print(tmpdict[l1])
        print(tmpdict[l2])

        assert tmpdict[l1] == 'AAAA'
        assert tmpdict[l2] == 'BBBB'

    def test_I(self):
        l1 = DLlist()
        l1.push_back(1)
        l1.push_back(2)
        l1.push_back(3)

        l2 = DLlist()
        l2.push_back(1)
        l2.push_back(2)
        l2.push_back(3)

        assert l1 == l2

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

    def test_L(self):
        l1 = DLlist()
        l1.push_back(1)
        l1.push_back(2)
        l1.push_back(3)

        l2 = DLlist()
        l2.push_back(1)
        l2.push_back(2)
        l2.push_back(3)

        assert l1 == l2

    # Test init_list initialization
    def test_M(self):
        l1 = DLlist([1, 2, 3, 4])
        assert (l1[0] == 1 and
                l1[1] == 2 and
                l1[2] == 3 and
                l1[3] == 4)
    
    def test_N(self):
        l1 = DLlist(5)
        assert len(l1) == 5

    def test_O(self):
        l1 = DLlist()
        l1.push_back(1)
        l1.push_back(3)
        l1.push_back(2)

        l2 = DLlist()
        l2.push_back(1)
        l2.push_back(2)
        l2.push_back(3)

        tmpdict = {l1 : 'AAAA', l2 : 'BBBB'}

        print(tmpdict[l1])
        print(tmpdict[l2])

        assert tmpdict[l1] == 'AAAA'
        assert tmpdict[l2] == 'BBBB'

    def test_P(self):
        l1 = DLlist()
        l1.push_back(1)
        l1.push_back(2)

        l2 = l1
        l2.push_back(3)

        assert (len(l1) == 3 and
                len(l2) == 3 and
                id(l1) == id(l2))

    def test_Q(self):
        l1 = DLlist()
        l1.push_back(1)
        l1.push_back(2)

        l1[1] = 3

        assert l1[1] == 3

    def test_R(self):
        l1 = DLlist()
        l1.push_back(1)
        l1.push_back(2)

        l2 = l1.copy()
        l2.push_back(3)

        assert (len(l1) == 2 and
                len(l2) == 3 and
                id(l1) != id(l2) and
                l1 != l2)

    def test_S(self):
        l = DLlist()
        l.push_back(1)
        l.delete(0)
        l.push_back('A')
        l.push_back('B')
        l.push_back('C')
        l.push_back('D')

        assert (len(l) == 4 and
                l[0] == 'A' and
                l[1] == 'B' and
                l[2] == 'C' and
                l[3] == 'D')

    def test_T(self):
        l = DLlist()
        l.push_front('A')
        l.push_front('B')
        l.push_front('C')
        l.push_front('D')

        assert (len(l) == 4 and
                l[0] == 'D' and
                l[1] == 'C' and
                l[2] == 'B' and
                l[3] == 'A')

    def test_U(self):
        l = DLlist()
        l.push_front('A')
        l.push_front('B')
        l.push_front('C')
        l.push_front('D')

        assert (len(l) == 4 and
                l[-1] == 'A' and
                l[-2] == 'B' and
                l[-3] == 'C' and
                l[-4] == 'D')

    def test_V(self):
         pass

    def test_W(self):
         pass

    def test_X(self):
         pass

    def test_Y(self):
         pass

    def test_Z(self):
         pass

if __name__ == '__main__':
    unittest.main()
