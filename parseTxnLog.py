import sys
import struct

# Define global variables
hardcodedLogFile = './txnlog.dat'

hardcodedUser = 2456938384156277127

totalCredit = 0.0
totalDebit = 0.0
autopaysStarted = 0
autopaysEnded = 0
userBalance = 0.0

# Define function to use transaction data
def handleTransaction(recordType,parsedData,user):
    global totalDebit
    global totalCredit
    global autopaysStarted
    global autopaysEnded
    global userBalance
    if recordType == 0:
        userId, dollarAmount = parsedData[1], parsedData[2]
        totalDebit += dollarAmount
        if userId == user:
            userBalance -= dollarAmount
    elif recordType == 1:
        userId, dollarAmount = parsedData[1], parsedData[2]
        totalCredit += dollarAmount
        if userId == user:
            userBalance += dollarAmount
    elif recordType == 2:
        autopaysStarted += 1
    elif recordType == 3:
        autopaysEnded += 1

# Define main function to parse log file
def main(logFile,userId):
    with open(logFile, 'rb') as file:
        header = struct.unpack('! 4s c I', file.read(9))
        magicString, numRecordsTotal = header[0], header[2]
        if magicString != b'MPS7':
            sys.exit("ERROR: ./txnlog.dat is not the correct format.")
        nextRecord = file.read(1)
        numRecordsRead = 0
        while nextRecord and numRecordsRead < numRecordsTotal:
            currentRecord = struct.unpack('B', nextRecord)[0]
            if currentRecord in [0, 1]:
                handleTransaction(currentRecord, struct.unpack('! I Q d', file.read(20)), userId)
                numRecordsRead += 1
            elif currentRecord in [2, 3]:
                handleTransaction(currentRecord, struct.unpack('! I Q', file.read(12)), userId)
                numRecordsRead += 1
            nextRecord = file.read(1)
    file.close()

    # Return required data
    print("total credit amount="+str('{:.2f}'.format(round(totalCredit,2))))
    print("total debit amount="+str('{:.2f}'.format(round(totalDebit,2))))
    print("autopays started="+str(autopaysStarted))
    print("autopays ended="+str(autopaysEnded))
    print("balance for user "+str(userId)+"="+str('{:.2f}'.format(round(userBalance,2))))

if __name__ == "__main__":
    main(hardcodedLogFile, hardcodedUser)
