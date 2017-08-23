import yaml
import os.path
import sys
import json
import csv
from pprint import pprint
from peerplays import PeerPlays
from peerplays.block import Block


def interpetringJson(data1):
    pprint(len(data1["transactions"]))
    pprint((data1["transactions"][0]["operations"][0][1]["from"])) 


"""
arg[1] is index of start block
arg[2] is index of last block 
arg[3] is from where to get the blocks
"""
if (len(sys.argv) != 4):
    print ("The program should get the folowing arguments: number of block to start, number to end (end means infinity), w for witness or d from directory")
    sys.exit()


with open("configuration.yml", 'r') as ymlfile:
      cfg = yaml.load(ymlfile)
kindOfOutPut = cfg["Output"]

#reading the blocks from witness 
if sys.argv[3] == "witness" or sys.argv[3] == "w":
    ServerNode = PeerPlays(
                node="wss://api.ppy.blckchnd.com/ws",
                    debug=True
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
            data = None
            jsonToBeWrriten = {}
            with open('transactions/'+ str(startBlockIndex) +'.json') as data_file:    
                  data = json.load(data_file)
                  pprint(data)
            i = 0 
            for trans in data["transactions"]:
                foo = None
                valuesList = [startBlockIndex]
                for param in cfg["Mapping"]:
                    exec("jsonToBeWrriten[param]"+ " = data['transactions'][i]" + cfg["Mapping"][param])
                    valuesList.append(jsonToBeWrriten[param])
                jsonToBeWrriten["blockNumber"] = startBlockIndex 
                #valuesList.append(jsonToBeWrriten["blockNumber"])
                """
                writing to csv
                """
                with open('csvFirst.csv','a') as f:
                        writer=csv.writer(f)
                       # writer.writerow([])
                        pprint (valuesList)
                        writer.writerow(valuesList)
                pprint (jsonToBeWrriten[param])
                i += 1
            pprint (jsonToBeWrriten)

        with open('logs/logFile.log', "a") as logfile:
            logfile.write("Block number "+str(startBlockIndex)+" from directory\n")
        print ("Block number "+str(startBlockIndex)+" from directory\n")

        startBlockIndex+=1
with open('logs/logFile.log', "a") as logfile:
    logfile.write("end of running :)\n")




