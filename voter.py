import time as t
import hashlib


class Voter():
    def __init__(self, key):
        self.public_key = key
        self.T = str(t.time())
        self.private_key = hashlib.sha256((key + self.T).encode('utf-8')).hexdigest()
        self.amount = 1
        self.chain = {}

    def trans_vote(self):
        self.amount = 0

    def disp(self):
        self.di = {}
        self.di[self.public_key] = [self.private_key , self.amount]
        return self.di


    def return_amt(self):
        return self.amount
