import yaml
import os.path
import sys
import json
import csv
import pymysql.cursors
from pprint import pprint
from peerplays import PeerPlays
from peerplays.block import Block
from peerplays.exceptions import BlockDoesNotExistsException
import time

""" This function is geting data to write to the DB
and map of the connection details.
the function writes the data in the DB.
"""
def writeTransToMySql(data,connectionDetails):
    connection = pymysql.connect(host=connectionDetails["host"],
            user=connectionDetails["user"],
            password=connectionDetails["password"],
            db=connectionDetails["db"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)
    i = 0
	#goes over the block transactions and inserting them
    for trans in data["transactions"]:
                dateTime = data['transactions'][i]['expiration']
                #writing all transactions any way
                valuesList = [startBlockIndex]
                for param in cfg["Mapping"]["all_transaction"]:
                        exec("jsonToBeWrriten[param]"+ " = data['transactions'][i]" + cfg["Mapping"]["all_transaction"][param])
                        valuesList.append(ops[int(jsonToBeWrriten['Operations'])])
                jsonToBeWrriten["blockNumber"] = startBlockIndex 
            
                #writing to data base
                try:
                    with connection.cursor() as cursor:
                    # Create a new record
                        sql= "INSERT INTO `all_transaction` (`Operations`, `blockNumber`, `time`) VALUES (%s, %s, %s)"
                        cursor.execute(sql, (ops[int(jsonToBeWrriten['Operations'])],startBlockIndex,dateTime))
                        print ("i trien in mysql insertion to all_tracsion done %d" % (i))
                    connection.commit()
                finally:
                    print ("inserted to 'all_transactions");
					#connection.close()
               
                



                #now writing the rest of the transaction that is not "all transactions"(account creat for example)
                if ops[int(jsonToBeWrriten['Operations'])] in cfg["Mapping"]:
                    sql= "INSERT INTO `"+ ops[int(jsonToBeWrriten['Operations'])] + '` (`blockNumber`, `time'
                    valuesList = [startBlockIndex,dateTime]
                    titleList = ["BlockNumber", "DateAndTime"]
                    toAppend = "%s, %s"
                    for param in cfg["Mapping"][ops[int(jsonToBeWrriten['Operations'])]]:
                        sql += '`, `' +  param
                        toAppend += ", %s"
                        titleList.append(param)
                        exec("valuesList.append("+ "data['transactions'][i]" + cfg["Mapping"][ops[int(jsonToBeWrriten['Operations'])]][param]+")")
                    sql += '`) VALUES (' + toAppend + ')'
#                    print ("sql we will use for spesific:")      // oppetunity to check the sql.
#                    print (sql)
                    try:
                        with connection.cursor() as cursor:
                            # Create a new record
                            str1 = "'" + "','".join(map(str, valuesList)) + "'"
#                            print ("list of values we will use:") // oppertunity to check the values.
#                            print (valuesList)
                          #  print (str1)
                            #sys.exit()
                            cursor.execute(sql,(valuesList))
                            print ("insertion in mysql spesific done")
                        connection.commit()
                    finally:
                        print("inserted to DB");
						#connection.close()


                    """ 
                    #checks if need to write a new file or to append 
                    if (int(jsonToBeWrriten['Operations']) in alreadyWas):
                            with open("logs/" + ops[int(jsonToBeWrriten['Operations'])] + ".csv",'a') as f:
                                writer=csv.writer(f)
                                pprint (valuesList)
                                writer.writerow(valuesList)
                    else :
                        with open("logs/" + ops[int(jsonToBeWrriten['Operations'])] + ".csv",'w') as f:
                            writer=csv.writer(f)
                            pprint (valuesList)
                            writer.writerow(titleList)   
                            writer.writerow(valuesList)  
 
                    alreadyWas.append(int(jsonToBeWrriten['Operations']))
                    """
                i+=1
    connection.close()
    
""" This function is geting data to write to csv file
the function writes the data in the csv file.
"""

def writeTransToCsv(data):
    i = 0 
    for trans in data["transactions"]:
                dateTime = data['transactions'][i]['expiration']
                #writing all transactions any way
                valuesList = [startBlockIndex]
                for param in cfg["Mapping"]["all_transaction"]:
                    exec("jsonToBeWrriten[param]"+ " = data['transactions'][i]" + cfg["Mapping"]["all_transaction"][param])
                    valuesList.append(ops[int(jsonToBeWrriten['Operations'])])
                jsonToBeWrriten["blockNumber"] = startBlockIndex 
                #valuesList.append(jsonToBeWrriten["blockNumber"])
                """
                writing to csv
                """
                with open('logs/all_transaction.csv','a') as f:
                        writer=csv.writer(f)
                        pprint (valuesList)
                        writer.writerow(valuesList)
                pprint (jsonToBeWrriten[param])
                #now writing the rest of the transaction that is not "all transactions"(account creat for example)
                if ops[int(jsonToBeWrriten['Operations'])] in cfg["Mapping"]:
                    valuesList = [startBlockIndex,dateTime]
                    titleList = ["BlockNumber", "DateAndTime"]
                    for param in cfg["Mapping"][ops[int(jsonToBeWrriten['Operations'])]]:
                        titleList.append(param)
                        exec("valuesList.append("+ "data['transactions'][i]" + cfg["Mapping"][ops[int(jsonToBeWrriten['Operations'])]][param]+")")
                    #checks if need to write a new file or to append 
                    if (int(jsonToBeWrriten['Operations']) in alreadyWas):
                            with open("logs/" + ops[int(jsonToBeWrriten['Operations'])] + ".csv",'a') as f:
                                writer=csv.writer(f)
                                pprint (valuesList)
                                writer.writerow(valuesList)
                    else :
                        with open("logs/" + ops[int(jsonToBeWrriten['Operations'])] + ".csv",'w') as f:
                            writer=csv.writer(f)
                            pprint (valuesList)
                            writer.writerow(titleList)   
                            writer.writerow(valuesList)  
 
                    alreadyWas.append(int(jsonToBeWrriten['Operations']))
                i+=1

"""
ops is an arrey of possible operations.
"""

ops = [
        "transfer",  # 0
        "limit_order_create",
        "limit_order_cancel",
        "call_order_update",
        "fill_order",
        "account_create", # 5
        "account_update",
        "account_whitelist",
        "account_upgrade",
        "account_transfer",
        "asset_create", 
        "asset_update",
        "asset_update_bitasset",
        "asset_update_feed_producers",
        "asset_issue",
        "asset_reserve",
        "asset_fund_fee_pool",
        "asset_settle",
        "asset_global_settle",
        "asset_publish_feed",
        "witness_create",
        "witness_update",
        "proposal_create",
        "proposal_update",
        "proposal_delete",
        "withdraw_permission_create",
        "withdraw_permission_update",
        "withdraw_permission_claim",
        "withdraw_permission_delete",
        "committee_member_create",
        "committee_member_update",
        "committee_member_update_global_parameters",
        "vesting_balance_create",
        "vesting_balance_withdraw",
        "worker_create",
        "custom",
        "assert",
        "balance_claim",
        "override_transfer",
        "transfer_to_blind",
        "blind_transfer",
        "transfer_from_blind",
        "asset_settle_cancel",
        "asset_claim_fees",
        "fba_distribute",
        "asset_update_dividend"
        "asset_dividend_distribution",
        "sport_create",
        "sport_update",
        "event_group_create",
        "event_group_update",
        "event_create",
        "event_update",
        "betting_market_rules_create",
        "betting_market_rules_update",
        "betting_market_group_create",
        "betting_market_create",
        "bet_place",
        "betting_market_group_resolve",
        "betting_market_group_resolved",
        "betting_market_group_freeze",
        "betting_market_group_cancel_unmatched_bets",
        "bet_matched",
        "bet_cancel",
        "bet_canceled",
        "tournament_create",
        "tournament_join",
        "game_move",
        "tournament_payout",
        "tournament_leave",
    ]


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
kindOfOutPut = cfg["Output"]["DB"]["Type"]#csv or mysql
runUntilTheEnd = False
#reading the blocks from witness 
if sys.argv[3] == "witness" or sys.argv[3] == "w":
    ServerNode = PeerPlays(
                node="wss://api.ppy.blckchnd.com/ws",
                    debug=True
                    )

    alreadyWas = []
    startBlockIndex = int(sys.argv[1])
    if (sys.argv[2] == "end"):
       # endBlockIndex = sys.maxint
       runUntilTheEnd = True
    else:
        endBlockIndex = int(sys.argv[2])
    while(startBlockIndex <= endBlockIndex or runUntilTheEnd) :
        try:
            ls =json.dumps(Block(startBlockIndex,peerplays_instance=ServerNode))
            ls1 = json.loads(ls)
        except BlockDoesNotExistsException:
            print ("sleeping 10 seconds")
            time.sleep( 10 )
            continue

        if len(ls1["transactions"]) != 0:
            jsonToBeWrriten = {}
            if (kindOfOutPut == "csv"):
                writeTransToCsv(ls1)
            else:
                writeTransToMySql(ls1,cfg["Output"]["DB"])


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
    titleList = ["BlockNumber", "Operations"]
#    writerAll = None
    alreadyWas = []
    with open('logs/all_transaction.csv','w') as f:
        writerAll=csv.writer(f)
        writerAll.writerow(titleList)   
    while(startBlockIndex <= endBlockIndex) :
        if os.path.isfile('transactions/'+ str(startBlockIndex) +'.json'):    
            data = None
            jsonToBeWrriten = {}
            with open('transactions/'+ str(startBlockIndex) +'.json') as data_file:    
                  data = json.load(data_file)
                  pprint(data)
            if (kindOfOutPut == "csv"):
                writeTransToCsv(data)
            else:
                writeTransToMySql(data,cfg["Output"]["DB"])
        with open('logs/logFile.log', "a") as logfile:
            logfile.write("Block number "+str(startBlockIndex)+" from directory\n")
        print ("Block number "+str(startBlockIndex)+" from directory\n")
        startBlockIndex+=1
with open('logs/logFile.log', "a") as logfile:
    logfile.write("end of running :)\n")
