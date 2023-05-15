from voter import Voter
import hashlib

voter_list = set()
voters = []

class add_voter():

    def __init__(self, Voter_id):
        self.key = hashlib.sha256(Voter_id.encode('utf-8')).hexdigest()
        self.voter = Voter(self.key)

    def disp(self):
        return self.voter.disp()

    def get_key(self):
        return self.voter.public_key

    def verify(self):
        if self.voter.amount == 0:
            return True
        else:
            return False

