from pprint import pprint
from peerplays import PeerPlays
from peerplays.block import Block

ServerNode = PeerPlays(
        #node="wss://ppy.proxyhosts.info/wss",
            node="wss://api.ppy.blckchnd.com/ws",
                debug=True
                #           nobroadcast=True,
                #               bundle=True,
                )

#pprint(testnet.Block(1))
pprint(Block(2139354,peerplays_instance=ServerNode))


