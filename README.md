# Block Explorer

In order to to run the collector.py use the following command:

python3 collector.py #par1 #par2 #par3 

while the parameters are:
  - par1 is number Of the Block that youwant to stat from.
  - par2 is number Of the Block that you want to End at  Or "end" to run till last block available.
  - par3 w for getting blocks from witness or d to get from directory .
 
#### Example
```sh
$ python3 collector.py 234324 end
```
### Configuration file
In order to choose between write the information from the internet to the DB or to csv file we are using the configuration file ("configuration.yml") it appears as the following format:
```sh
Output:
DB:
     Type: 'csv' or 'MySQL' 
```
### Log file
In order to know what is the last Block number that we red from the witness look at the log file at path: ./logs/logFile.log
