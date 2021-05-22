import sys
import struct

txnLogFile = './txnlog.dat'

user = 2456938384156277127

# define variables to track data that will be returned
totalDebit = 0.0
totalCredit = 0.0
autopaysStarted = 0
autopaysEnded = 0
userBalance = 0.0

# define function to handle transaction data
def handleTransaction(recordType,parsedData):
    global totalDebit
    global totalCredit
    global autopaysStarted
    global autopaysEnded
    global userBalance
    if recordType == 0:
        # get and use the data from the record
        unixTimestamp, userId, dollarAmount = parsedData
        totalDebit += dollarAmount
        if userId == user:
            userBalance -= dollarAmount
    elif recordType == 1:
        # get and use the data from the record
        unixTimestamp, userId, dollarAmount = parsedData
        totalCredit += dollarAmount
        if userId == user:
            userBalance -= dollarAmount
    elif recordType == 2:
        # get the data from the record (currently unused)
        unixTimestamp, userId = parsedData
        # increment the count of autopays started
        autopaysStarted += 1
    elif recordType == 3:
        # get the data from the record (currently unused)
        unixTimestamp, userId = parsedData
        # increment the count of autopays ended
        autopaysEnded += 1

# define main function to parse transaction log
def main():
    # read binary file
    with open(txnLogFile, 'rb') as file:
        # get file header - should be the first 9 bytes
        header = file.read(9)
        magicString, version, numRecordsTotal = struct.unpack('! 4s c I', header)
        # validate that first 4 bytes in header are "MPS7"
        if magicString != b'MPS7':
            sys.exit("ERROR: ./txnlog.dat is not the correct format.")
        # cycle through transaction records
        nextRecord = file.read(1)
        numRecordsRead = 0
        while nextRecord and numRecordsRead < numRecordsTotal:
            currentRecord = struct.unpack('B', nextRecord)[0]
            if currentRecord in [0, 1]:
                # parse the 20 remaining bytes in debit/credit records
                handleTransaction(currentRecord, struct.unpack('! I Q d', file.read(20)))
                numRecordsRead += 1
            elif currentRecord in [2, 3]:
                # parse the 12 remaining bytes in autopay start/end records
                handleTransaction(currentRecord, struct.unpack('! I Q', file.read(12)))
                numRecordsRead += 1
            nextRecord = file.read(1)

    file.close()

    # return the required information in the required format
    print("total credit amount="+str('{:.2f}'.format(round(totalCredit,2))))
    print("total debit amount="+str('{:.2f}'.format(round(totalDebit,2))))
    print("autopays started="+str(autopaysStarted))
    print("autopays ended="+str(autopaysEnded))
    print("balance for user "+str(user)+"="+str('{:.2f}'.format(round(userBalance,2))))

# run main function
if __name__ == "__main__":
    main()
