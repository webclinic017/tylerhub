import pytest

class Test_transfer():
    
    def test_a(self):
        print('aaaa')

    @pytest.mark.skip(reason='跳过')
    def test_b(self):
        print('bbbb')

    def test_c(self):
        print('cccc')

if __name__=='__main__':
    pytest.main(['-s','test_transfer_action_other_one_bin.py'])