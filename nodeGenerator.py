import random
from node import *

class NodeGenerator:
    """ Responsible to create the nodes used during the simulation.
    Depending on the blockchain being simulated, 
        node factory will create nodes according to the node model. 
    The user can specify the location, 
        number of miners and non-miners,
        and the range of hash rate for the miner nodes. 
    When nodes are created, 
        it is chosen a random hash rate from the range inputed. 
    The location of each node needs to be recognised by the simulator, 
        meaning that it needs to be existing input parameters 
        about latency and throughput.
    """

    def __init__(self, network):
        self.network = network

    def create_nodes(self, full_nodes):
        # Unique ID for each node
        # Create the full nodes
        nodes_list = []
        for node_location, _nodes in full_nodes.items():
            for i in range(_nodes['how_many']):
                new = Node( self.network,
                            node_location,
                            0,
                            chain=None
                            # processingTime,#NC
                            )
                nodes_list.append(new)
        print(f'NodeGenerator: Created {len(nodes_list)} full nodes')
        return nodes_list
        
    def add_miner(self, miners):
        # Unique ID for each node
        # Create the miners nodes
        miners_list = []
        for name, info in miners.items():    
            hashrate= info["mega_hashrate"]
            miner_location = info["region"]

            new = Node( self.network,
                        miner_location,
                        hashrate,
                        info=name
                        )
            miners_list.append(new)
                

        print(f'NodeGenerator: Created {len(miners_list)} miners')
        return miners_list

    # def create_bitcoin_nodes(self, miners, non_miners):
    #     node_id = 0  # Unique ID for each node
    #     # Create the miners nodes
    #     miners_list = []
    #     for miner_location, _miners in miners.items():
    #         for i in range(_miners['how_many']):
    #             node_id += 1
    #             node_address = f'{miner_location.lower()}-{node_id}'
    #             mega_hashrate_range = make_tuple(
    #                 _miners['mega_hashrate_range'])
    #             # Choose a random value on MH/s range and convert to H/s
    #             hashrate = randint(
    #                 mega_hashrate_range[0], mega_hashrate_range[1])*10**6
    #             new = BTCNode(self._world.env,
    #                           self._network,
    #                           miner_location,
    #                           node_address,
    #                           hashrate,
    #                           True)
    #             miners_list.append(new)
    #     # Create the non-miners nodes
    #     non_miners_list = []
    #     for miner_location, _miners in non_miners.items():
    #         for i in range(_miners['how_many']):
    #             node_id += 1
    #             node_address = f'{miner_location.lower()}-{node_id}'
    #             new = BTCNode(self._world.env,
    #                           self._network,
    #                           miner_location,
    #                           node_address)
    #             non_miners_list.append(new)
    #     # Fully connect all the nodes
    #     nodes_list = miners_list + non_miners_list
    #     print(f'NodeFactory: Created {len(nodes_list)} bitcoin nodes')
    #     return nodes_list

    # def create_ethereum_nodes(self, miners, non_miners):
    #     node_id = 0  # Unique ID for each node
    #     # Create the miners nodes
    #     miners_list = []
    #     for miner_location, _miners in miners.items():
    #         for i in range(_miners['how_many']):
    #             node_id += 1
    #             node_address = f'{miner_location.lower()}-{node_id}'
    #             mega_hashrate_range = make_tuple(
    #                 _miners['mega_hashrate_range'])
    #             # Choose a random value on MH/s range and convert to H/s
    #             hashrate = randint(
    #                 mega_hashrate_range[0], mega_hashrate_range[1])*10**6
    #             new = ETHNode(self._world.env,
    #                           self._network,
    #                           miner_location,
    #                           node_address,
    #                           hashrate,
    #                           True)
    #             miners_list.append(new)
    #     # Create the non-miners nodes
    #     non_miners_list = []
    #     for miner_location, _miners in non_miners.items():
    #         for i in range(_miners['how_many']):
    #             node_id += 1
    #             node_address = f'{miner_location.lower()}-{node_id}'
    #             new = ETHNode(self._world.env,
    #                           self._network,
    #                           miner_location,
    #                           node_address,
    #                           False)
    #             non_miners_list.append(new)
    #     # Fully connect all the nodes
    #     nodes_list = miners_list + non_miners_list
    #     print(f'NodeFactory: Created {len(nodes_list)} ethereum nodes')
    #     return nodes_list

    def _check_location(self, miners):
        nodes_location = list(miners.keys())
        for location in nodes_location:
            if location not in self._world.locations:
                raise RuntimeError(
                    f'There are not measurements for the location {location}. \
                    Only available locations: {self.network.locations()}')

