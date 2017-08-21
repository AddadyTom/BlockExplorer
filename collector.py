import os.path
import sys
import json
from pprint import pprint
from peerplays import PeerPlays
from peerplays.block import Block


def interpetringJson(data1):
    print("in11111111111111111111")
    pprint(len(data1["transactions"]))
#    ls2 =json.dumps(data1["transactions"])
    print("sssssssssssssssssssssssSSS")
    pprint((data1["transactions"][0]["operations"][0][1]["from"])) 



#arg[1] is index of start block
#arg[2] is index of last block 
#arg[3] is from where to get the blocks

if (len(sys.argv) != 4):
    print ("The program should get the folowing arguments: number of block to start, number to end (end means infinity), w for witness or d from directory")
    sys.exit()


#reading the blocks from witness 
if sys.argv[3] == "witness" or sys.argv[3] == "w":
    ServerNode = PeerPlays(
                node="wss://api.ppy.blckchnd.com/ws",
                    debug=True
                    #           nobroadcast=True,
                    #               bundle=True,
                    )

    startBlockIndex = int(sys.argv[1])
    if (sys.argv[2] == "end"):
        endBlockIndex = sys.maxint
    else:
        endBlockIndex = int(sys.argv[2])
    while(startBlockIndex <= endBlockIndex) :
        ls =json.dumps(Block(startBlockIndex,peerplays_instance=ServerNode))
        ls1 = json.loads(ls);
        if len(ls1["transactions"]) != 0:
            #print ((ls1["transactions"]));
            with open('transactions/'+ str(startBlockIndex) +'.json', 'w') as outfile:
                json.dump(ls1, outfile)
            interpetringJson(ls1)
        with open('logs/logFile.log', "a") as logfile:
            logfile.write("Block number "+str(startBlockIndex)+" from witness\n")
        print ("Block number "+str(startBlockIndex)+" from witness\n")
        startBlockIndex+=1


else:
    startBlockIndex = int(sys.argv[1])
    if (sys.argv[2] == "end"):
        endBlockIndex = sys.maxint
    else:
        endBlockIndex = int(sys.argv[2])
    while(startBlockIndex <= endBlockIndex) :
        if os.path.isfile('transactions/'+ str(startBlockIndex) +'.json'):
            data=""
            with open('transactions/'+ str(startBlockIndex) +'.json') as data_file:    
                  data = json.load(data_file)
                  pprint(data)
            interpetringJson(data)
        with open('logs/logFile.log', "a") as logfile:
                logfile.write("Block number "+str(startBlockIndex)+" from directory\n")
        print ("Block number "+str(startBlockIndex)+" from witness\n")
        startBlockIndex+=1
with open('logs/logFile.log', "a") as logfile:
    logfile.write("end of running :)\n")




