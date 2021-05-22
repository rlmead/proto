import sys
import struct

# define path to txnlog file
txnLogFile = './txnlog.dat'

# define user whose balance should be returned
user = 2456938384156277127

# define variables to track data that will be returned
totalDebit = 0.0
totalCredit = 0.0
autopaysStarted = 0
autopaysEnded = 0
userBalance = 0.0

# map record enumerations to human-readable names
recordTypes = {
    '0': 'debit',
    '1': 'credit',
    '2': 'startAutopay',
    '3': 'endAutopay'
}

# define function to handle transaction data
def handleTransaction(recordType,parsedData):
    global user
    global totalDebit
    global totalCredit
    global autopaysStarted
    global autopaysEnded
    global userBalance
    if recordType == 'debit':
        # get and use the data from the record
        unixTimestamp, userId, dollarAmount = parsedData
        totalDebit += dollarAmount
        if userId == user:
            userBalance -= dollarAmount
    elif recordType == 'credit':
        # get and use the data from the record
        unixTimestamp, userId, dollarAmount = parsedData
        totalCredit += dollarAmount
        if userId == user:
            userBalance -= dollarAmount
    elif recordType == 'startAutopay':
        # get the data from the record (currently unused)
        unixTimestamp, userId = parsedData
        # increment the count of autopays started
        autopaysStarted += 1
    elif recordType == 'endAutopay':
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
        while nextRecord:
            currentRecord = str(struct.unpack('B', nextRecord)[0])
            if currentRecord in recordTypes:
                currentRecordType = recordTypes[currentRecord]
                if currentRecordType in ['debit', 'credit']:
                    # parse the 20 remaining bytes in debit/credit records
                    handleTransaction(currentRecordType, struct.unpack('! I Q d', file.read(20)))
                elif currentRecordType in ['startAutopay', 'endAutopay']:
                    # parse the 12 remaining bytes in autopay start/end records
                    handleTransaction(currentRecordType, struct.unpack('! I Q', file.read(12)))
                numRecordsRead += 1
            nextRecord = file.read(1)

    file.close()

    # return the required information in the required format
    print("total credit amount="+str('{:.2f}'.format(round(totalCredit,2))))
    print("total debit amount="+str('{:.2f}'.format(round(totalDebit,2))))
    print("autopays started="+str(autopaysStarted))
    print("autopays ended="+str(autopaysEnded))
    print("balance for user "+str(user)+"="+str('{:.2f}'.format(round(userBalance,2))))

if __name__ == "__main__":
    main()
