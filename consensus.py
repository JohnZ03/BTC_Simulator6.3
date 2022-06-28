from utils import *
""" Different consensus algorithms"""


def validate_block(network, block=None):
    """ Simulates the block validation.
        For now, it only applies a delay in simulation, 
        corresponding to previous measurements
    """
    delay = round(get_random_values(
        network.delays['block_validation'])[0], 4)
    return delay

def longest_chain(block, chain):
    if block.height > chain.head.height:
        chain.head = block
        chain.db.put(block.height, [block])
        # print(
        # f'{chain.node.nid}: \
        # # Adding block #{block.height} ({block.hash}) to the head')
    else:
        l = chain.db.get(block.height)
        l.append(block)
        chain.db.put(block.height,l)
        # print(
        # f'{chain.node.nid}: \
        # # Adding block #{block.height} ({block.hash}) to a fork')

def heaviest_chain(block, chain):
    # Just add to current head
    if block.parentHash == chain.head.hash:
        chain.head = block
        chain.db.put(block.height, [block])
        # print(
        # f'{chain.node.nid}: \
        # # Adding block #{block.height} ({block.hash}) to the head')
    else:
        try:
            l = chain.db.get(block.height)        
        except Exception as e:
            l = []
        l.append(block)
        chain.db.put(block.height,l)

        # Recalculate main chain from genesis block
        pre = chain.head.hash
        cur = chain.genesis
        next_main_chain_block = get_heaviest_child(cur,chain)
        while next_main_chain_block != None:
            cur = next_main_chain_block
            next_main_chain_block = get_heaviest_child(cur,chain)
            chain.head = cur
        # print(f'{chain.node.nid}: \
        # # change head from block {pre} to \
        # block {cur.hash}')


def count_weight(block,chain):
    """Find weight of the subtree rooted at block."""
    weight = 1
    try:
        children_hash = chain.db.get(f'children of {block.hash}')
    except Exception as e:
        return weight

    for ch in children_hash:    
        child = chain.db.get(f'{ch}')
        weight += count_weight(child,chain)
    return weight

def get_heaviest_child(block,chain):
    """ Find the heaviest child of the block."""
    try:
        children_hash = chain.db.get(f'children of {block.hash}')
    except Exception as e:
        return None

    heaviest = None
    max_weight = 0    
    for ch in children_hash:    
        child = chain.db.get(f'{ch}')
        weight = count_weight(child,chain)
        if weight > max_weight:
            max_weight = weight
            heaviest = child
    return heaviest





