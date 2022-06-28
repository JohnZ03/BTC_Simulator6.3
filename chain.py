import random
import itertools
import time
from db import *
from block import Block
from consensus import *


class Chain:
    """Defines a base chain model that needs to be extended according to blockchain protocol
    being simulated"""
    def __init__(self, node):
        self.node = node
        self.db = BaseDB()
        self.current_height = 0
        self.block_counter = 0
        

        # Init the chain with the Genesis block
        if Block.genesis == None:
            genesis = Block(0, None, self.node, 0, 0)
            Block.set_genesis(genesis)

        self.genesis = Block.genesis
        node.known_blocks.add(self.genesis.hash)
       
       
        #keep track blocks at each height: if there is more than one
        #block at a height, then there is a fork

        self.db.put(self.current_height,[self.genesis])
        self.db.put(f'{self.genesis.hash}', self.genesis)
        self.block_counter += 1

        self.head = self.genesis
        self.parent_queue = {}

    def get_main_chain(self):
        cur = self.head
        chain_list = []
        while cur.height > 0:
            chain_list.append(f'{cur.hash}')
            cur = self.get_parent(cur)
        chain_list.append(f'{cur.hash}')
        return chain_list



    def get_parent(self, block):
        """Genesis Block do not have parent"""
        if block.height == 0:
            return None
        return self.get_block(block.parentHash)

    def get_block(self, bhash):
        """Gets the block with a given block hash"""
        try:
            return self.db.get(f'{bhash}')
        except BaseException:
            return None
            

    def get_block_by_height(self, height):
        """Gets the block on main chain
        with the given block number"""
        cur = self.head
        if height > cur.height:
            return None
        while height < cur.height:
            # print(cur.height)
            cur = self.get_parent(cur)
        return cur


    def get_block_hash_by_height(self, height):
        """Gets the hash of the block on main chain
        with the given block number"""
        try:
            return self.get_block_by_height(height).hash
        except BaseException:
            return None

    def add_child(self, child):
        """Add a record allowing you to later look up the provided block's
        parent hash and see that it is one of its children"""
        try:
             children = self.db.get(f'children of {child.parentHash}')
        except BaseException:
             self.db.put(f'children of {child.parentHash}',[child.hash])
             return
        children.append(child.hash)
        self.db.put(f'children of {child.parentHash}',children)

    def get_child_hashs(self, h):
        """Get the hashes of all known children of a given block"""
        try:
            data = self.db.get(f'childs of {h}')
        except BaseException:
            return []
        return data

    def get_children(self, block):
        """Get the children of a block"""
        return [self.get_block(h) for h in self.get_child_hashes(block.hash)]

    def add_block(self, block):
        """Call upon receiving new a block"""
        # Double check the block is not in the chain
        key = f'{block.hash}'
        if key in self.db:
            return 
            
        # The block being added to a fork
        pkey = f'{block.parentHash}'#parent hash
        if pkey in self.db:
            self.db.put(key,block)
            self.add_child(block)
            self.block_counter += 1
        
            # Add the block to the chain accoridng to consensus algorthm

            longest_chain(block, self)
            #heaviest_chain(block, self)

            # Process blocks that are received and were waiting for this block
            if block.hash in self.parent_queue:
                for blk in self.parent_queue[block.hash]:
                    self.add_block(blk)
                    del self.parent_queue[block.hash]
            return True
        
        # Block has no parent yet
        else:
            if block.parentHash not in self.parent_queue:
                self.parent_queue[block.parentHash] = []
            self.parent_queue[block.parentHash].append(block)
            # print(
            #     f'{self.node.nid}: \
            #     Got block #{block.height} ({block.hash}) \
            #     with prevhash {block.parentHash}, \
            #     parent not found. Delaying for now')
            return False

      
       

    def __contains__(self, block):
        try:
            o = self.get_block_hash_by_height(block.height)
            assert o == block.hash
            return True
        except Exception as e:
            return False

    def get_block_hashes_from_hash(self, block_hash, max_num):
        """Get blockhashes starting from a hash and going backwards"""
        block = self.get_block(block_hash)
        if block is None:
            return []
        hashes = []
        hashes.append(block.hash)
        for i in range(max_num - 1):  # We already have one block added to the hashes list
            block = self.get_block(block.parentHash)
            if block is None:
                break
            hashes.append(block.hash)
            if block.height == 0:
                break
        return hashes
