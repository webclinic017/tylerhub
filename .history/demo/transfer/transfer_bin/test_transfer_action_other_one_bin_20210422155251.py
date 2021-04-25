import pytest

class Test_transfer():
    
    def test_a(self):
        print('aaaa')

    #@pytest.mark.skip(reason='跳过')
    def test_b(self):
        if 1<2:
            pytest.skip('跳过')
        else:
            print('bbbb')

    def test_c(self):
        print('cccc')

    # def setup(self):
    #     if 3>2:
    #         return True
    #     else:
    #         return False
    
    #@pytest.mark.skipif(condition=setup,reason='3>2 跳過')
    def test_d(self):
        print('dddd')

if __name__=='__main__':
    pytest.main(['-v','test_transfer_action_other_one_bin.py'])