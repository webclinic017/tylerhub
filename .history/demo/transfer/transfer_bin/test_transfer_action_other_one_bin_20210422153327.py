import pytest

class Test_transfer():
    
    def test_a(self):
        print('aaaa')

    @pytest.mark.skip(reason='跳过')
    def test_b(self):
        print('bbbb')

    def test_c(self):
        print('cccc')

    def isok(self):
        if 3>2:
            return True
        else:
            return False
    
    @pytest.mark.skipif(condition=isok,reason='')
    def test_d(self):
        print('dddd')

if __name__=='__main__':
    pytest.main(['-r','test_transfer_action_other_one_bin.py'])