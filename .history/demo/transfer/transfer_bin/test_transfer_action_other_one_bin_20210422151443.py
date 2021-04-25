import pytest

class Test_transfer():
    
    def test_a(self):
        print('aaaa')

    def test_b(self):
        print('bbbb')

if __name__=='__main__':
    pytest.main('-s','test_transfer_action_other_one_bin.py')