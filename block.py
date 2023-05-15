import hashlib
import time as t

def valid_noance(g_hash):
    if g_hash[:4] == "0000":
        return True
    else:
        return False
def cal_noance(pre_hash, c_hash):
    noance = 0
    guess = f'{pre_hash}{c_hash}{noance}'.encode()
    g_hash = hashlib.sha256(guess).hexdigest()

    while(not valid_noance(g_hash)):
        guess = f'{pre_hash}{c_hash}{noance}'.encode()
        g_hash = hashlib.sha256(guess).hexdigest()
        noance+=1
    return noance,g_hash


class Block():
    ind = 0
    b_hash = "k7a1u1n9d9a8l"

    def __init__(self, trns):
        self.index = Block.ind
        self.pre_hash = Block.b_hash
        self.noance, self.block_hash = cal_noance(self.pre_hash, trns)
        self.trans = trns
        Block.b_hash = self.block_hash
        Block.ind = Block.ind + 1

    def disp(self):
        print("index ", self.index)
        print("Previous hash ", self.pre_hash)
        print("noance ", self.noance)
        print("block hash ", self.block_hash)
        print("trans ", self.trans)


    def last_block_hash(self):
        return self.block_hash
