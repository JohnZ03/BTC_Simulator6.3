from node import *
from datetime import datetime

class Block:
    nextBlockHash = 0 #simulating block hash 
    genesis = None
    def __init__(self, height, parentHash, miner, timestampe, size):
        self.height = height #height = -1 if block is orphaned, 0 if is genesis block
        self.parentHash = parentHash
        self.miner = miner
        self.timestamp = timestampe
        self.size = size 
        self.hash = Block.nextBlockHash
        Block.nextBlockHash += 1
    
    def set_genesis(genesis):
        Block.genesis = genesis
        
    def orphanBlock(self):
        self.height = -1

    def isOrphan(self):
        return self.height == -1

    def __repr__(self):
        """Returns a unambiguous representation of the block header"""
        return f'<{self.__class__.__name__}(#{self.hash} height{self.height})>'

    def __str__(self):
        """Returns a readable representation of the block"""
        timestamp = datetime.utcfromtimestamp(
            self.timestamp).strftime('%m-%d %H:%M:%S')
        return f'<{self.__class__.__name__}(#{self.hash} \
        prevhash:{self.parentHash[:8]} \
        timestamp:{timestamp} \
        height:{self.height} miner:{self.miner})>'

    def __eq__(self, other):
        """Two blocks are equal iff they have the same hash."""
        return isinstance(other, self.__class__) and self.hash == other.hash

    def __ne__(self, other):
        return not self.__eq__(other)







