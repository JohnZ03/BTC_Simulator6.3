import time
from datetime import datetime
from simulator import Simulator
from json import dumps as dump_json
from nodeGenerator import NodeGenerator
from network import Network
from block import *
import json
import weakref




# Choose the appropriate index for the size and time configuration that you want
# Ex- If you want the block size to be 1MB and Block Generation Interval to be 10 min, [600,60] seconds, 
# then set i=0 and j=0 in the main function (line 164 & line 165)
# Ex- If you want the block size to be 16MB and Block Generation Interval to be 5 min, [300,30] seconds,
#then then set i=4 and j=1 in the main function (line 164 & line 165)

Size = [1000,2000,4000,8000,16000, 32000]; #in kB (index i)
Time = [ [600,60],[300,30],[180,18],[60,6],[10,1],[5,0.5],[3,0.3],[1,0.1]]; #in seconds ( index j)
config_file='configs/config.json';

def write_report(network,simulator, duration,t,s):
    print("rep")

    with open(f'output/nodes_{s/1000}MB_{t/60}min_paretn.json', 'w') as f:
        f.write(dump_json(network.data,indent=4))   

    with open(f'output/block_propogation_{s/1000}MB_{t/60}min_paretn.json', 'w') as f:
        f.write(dump_json(network.block_propagation,indent=4))

    with open(f'output/propagation/final_propagation_{s/1000}MB_{t/60}min_paretn.json', 'w') as f:
        f.write(dump_json(network.final_propagation_time,indent=4))


    with open(f'output/system/system_{s/1000}MB_{t/60}min_paretn.json', 'w') as f:
        f.write(dump_json(simulator.data,indent=4))
        
    with open(f'output/minerinfo_{s/1000}MB_{t/60}min_paretn.json', 'w') as f:
        f.write(dump_json(network.miner,indent=4))



def report_node(network, simulator, nodes_list, miner_list):
    for node in nodes_list:
        head = node.chain.head
        main_chain_list = node.chain.get_main_chain()
        
        key = f'{node.nid}_summary'
        network.data[key] = {
            'nid': node.nid,
            'region': node.region,
            'connections': list(node.neighbours.keys()),
            'hashrate': node.hashrate,
            'head_block_hash': f'{head.hash} #{head.height}',
            'number_of_total_known_blocks': len(node.known_blocks),
            'number_of_total_blocks_inchain': node.chain.block_counter,
            'number_of_blocks_on_main_chain': len(main_chain_list),
            'main_chain_list': main_chain_list
        }
        simulator.data['system summary'].update({
            'fork_rate':1-len(main_chain_list)/node.chain.block_counter})
    for miner in miner_list :
        key = f'{miner.nid}_summary'
        network.miner[key] = {
            'nid' : miner.nid,
            'hashrate': miner.hashrate,
            'block_reward':miner.block_reward,
            'blocks_genertated': list(miner.generated_block)
        }
        
def report_system_summary(simulator, nodes_list): 
    simulator.data['system summary']= {
                'start_simulation_time': datetime.utcfromtimestamp(
                    simulator.initial_time).strftime('%m-%d %H:%M:%S'),
                'end_simulation_time': datetime.utcfromtimestamp(
                   (simulator.initial_time + simulator.end_time)/1000).strftime('%m-%d %H:%M:%S'),
                'number_of_nodes': len(nodes_list),
                #'number_of_blocks': Block.nextBlockHash
                
            }

def run_model(duration,t,size,now=0):

    end = duration * 60 * 60 * 1000 #convert from h to ms
    nodes_list = []
    miner_list = []

    # Create the network
    network = Network(
        'Network 0.0',
        'configs/config.json',
        'configs/latency.json',
        'configs/throughput-rec.json',
        'configs/throughput-send.json',
        'configs/delays.json')

    node_distribution =  network.config[network.blockchain]["node_distribution"]
    total_nodes = network.config[network.blockchain]["number_of_nodes"]

    full_nodes = {
        'NORTH_AMERICA': {
            'how_many': int(total_nodes*node_distribution['NORTH_AMERICA']),
            'mega_hashrate_range': (0, 0)
        },
        'SOUTH_AMERICA': {
            'how_many': int(total_nodes*node_distribution['SOUTH_AMERICA']),
            'mega_hashrate_range': (0, 0)
        },
        'ASIA_PACIFIC': {
            'how_many': int(total_nodes*node_distribution[ 'ASIA_PACIFIC']),
            'mega_hashrate_range': (0, 0)
        },
        'JAPAN': {
            'how_many': int(total_nodes*node_distribution['JAPAN']),
            'mega_hashrate_range': (0, 0)
        },
        'AUSTRALIA': {
            'how_many': int(total_nodes*node_distribution['AUSTRALIA']),
            'mega_hashrate_range': (0, 0)
        },
        'EUROPE': {
            'how_many': int(total_nodes*node_distribution['EUROPE']),
            'mega_hashrate_range': (0, 0)
        }
    }

    miners = network.config[network.blockchain]["mining_pool"]

    node_generator = NodeGenerator(network)
    # Create all nodes
    nodes_list = node_generator.create_nodes(full_nodes)
    miner_list = node_generator.add_miner(miners)
    nodes_list.extend(miner_list)

    for node in nodes_list:
        node.connect(nodes_list) #

    s = Simulator(network, now, end)
    s.run()

    report_system_summary(s, nodes_list)
    report_node(network, s, nodes_list,miner_list)
    write_report(network,s,duration,t,size)
    
    for node in nodes_list:
        del node.chain
        del node
    del node_distribution
    del total_nodes
    del full_nodes
    del network
    del node_generator

    del miner_list
    del miners
    del s
         
    

if __name__ == '__main__':
    
    i=0; #
    j=4; #

    print(f'Simulation for Size - {Size[i]} Time - {Time[j][0]}')
    block_interval = "("+str(Time[j][0])+","+str(Time[j][1])+")"
    block_size = "("+str(Size[i])+",250)"
    with open(config_file,'r+') as f:
        data = json.load(f)
        data['bitcoin']['time_between_blocks_seconds']['parameters'] = block_interval
        data['bitcoin']["block_size_kB"]['parameters'] = block_size
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()     # remove remaining part
    hours = 100*Time[j][0]/3600
    b = time.time()
    run_model(hours,Time[j][0],Size[i],0)  
    e = time.time()
    print(f'{e-b}seconds')
    
    

 
    

