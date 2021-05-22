import sys
import struct
from enum import Enum

# define path to txnlog file
txnLogFile = './txnlog.dat'

# define user whose balance should be returned
user = 2456938384156277127

# define variables that will be returned
totalDebit = 0.0
totalCredit = 0.0
autopaysStarted = 0
autopaysEnded = 0
userBalance = 0.0

# function to handle transaction data
def handleTransaction(recordType,parsedData):
    global user
    global totalDebit
    global totalCredit
    global autopaysStarted
    global autopaysEnded
    global userBalance
    if recordType == b'\x00':
        # get and use the data from the record
        unixTimestamp, userId, dollarAmount = parsedData
        totalDebit += dollarAmount
        if userId == user:
            userBalance -= dollarAmount
    elif recordType == b'\x01':
        # get and use the data from the record
        unixTimestamp, userId, dollarAmount = parsedData
        totalCredit += dollarAmount
        if userId == user:
            userBalance -= dollarAmount
    elif recordType == b'\x02':
        # get the data from the record (currently unused)
        unixTimestamp, userId = parsedData
        # increment the count of autopays started
        autopaysStarted += 1
    elif recordType == b'\x03':
        # get the data from the record (currently unused)
        unixTimestamp, userId = parsedData
        # increment the count of autopays ended
        autopaysEnded += 1

# main function to parse transaction log
def main():
    # read binary file
    with open(txnLogFile, 'rb') as file:
        # check for properly-formatted header
        header = file.read(9)
        magicString, version, numRecordsTotal = struct.unpack('! 4s c I', header)
        # validate that first 4 bytes in header are "MPS7"
        if magicString != b'MPS7':
            sys.exit("ERROR: ./txnlog.dat is not the correct format.")
        # define a couple variables for cycling through the transaction records
        currentRecord = file.read(1)
        numRecordsRead = 0
        # cycle through transaction records
        while currentRecord:
            if currentRecord in [b'\x00', b'\x01']:
                # parse the 20 remaining bytes in debit/credit records
                handleTransaction(currentRecord, struct.unpack('! I Q d', file.read(20)))
            elif currentRecord in [b'\x02', b'\x03']:
                # parse the 12 remaining bytes in autopay start/end records
                handleTransaction(currentRecord, struct.unpack('! I Q', file.read(12)))
            currentRecord = file.read(1)

    file.close()

    # return the required information in the required format
    print("total credit amount="+str('{:.2f}'.format(round(totalCredit,2))))
    print("total debit amount="+str('{:.2f}'.format(round(totalDebit,2))))
    print("autopays started="+str(autopaysStarted))
    print("autopays ended="+str(autopaysEnded))
    print("balance for user "+str(user)+"="+str('{:.2f}'.format(round(userBalance,2))))

if __name__ == "__main__":
    main()
