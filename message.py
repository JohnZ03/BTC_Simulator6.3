from utils import kB_to_MB

class Message:  
    """Defines a model for the network messages of the Bitcoin blockchain.
    For each message its calculated the size, taking into account measurements from the live and public network.
    """

    def __init__(self, sender, ty, blocks):
        self.sender = sender
        self.blocks = blocks

        message_size = self.sender.network.config['bitcoin']['message_size_kB']

        if ty == "blocks":
            self.id = "blocks"
            total_block_size = 0
            for block in self.blocks:
                total_block_size = message_size['header'] + \
                                block.size + \
                                message_size['block_base']
            self.size = kB_to_MB(float(total_block_size))
        else:  
            #Used to retrieve the content of a specific type (e.g. block or transaction).
            if ty == "get_data":
                self.id = "get_data"
            #Allows a node to advertise its knowledge of one or more transactions or blocks
            elif ty == "inv":
                self.id = "inv"
            num_items = len(blocks)
            message_size = message_size['header']+ num_items * message_size['inv_vector']
            self.size = kB_to_MB(message_size)
           


