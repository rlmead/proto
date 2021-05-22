import sys
import struct

txnLogFile = './txnlog.dat'

user = 2456938384156277127

totalCredit = 0.0
totalDebit = 0.0
autopaysStarted = 0
autopaysEnded = 0
userBalance = 0.0

def handleTransaction(recordType,parsedData):
    global totalDebit
    global totalCredit
    global autopaysStarted
    global autopaysEnded
    global userBalance
    if recordType == 0:
        totalDebit += parsedData[2]
        if parsedData[1] == user:
            userBalance -= parsedData[2]
    elif recordType == 1:
        totalCredit += parsedData[2]
        if parsedData[1] == user:
            userBalance += parsedData[2]
    elif recordType == 2:
        autopaysStarted += 1
    elif recordType == 3:
        autopaysEnded += 1

def main():
    with open(txnLogFile, 'rb') as file:
        header = file.read(9)
        magicString, version, numRecordsTotal = struct.unpack('! 4s c I', header)
        if magicString != b'MPS7':
            sys.exit("ERROR: ./txnlog.dat is not the correct format.")
        nextRecord = file.read(1)
        numRecordsRead = 0
        while nextRecord and numRecordsRead < numRecordsTotal:
            currentRecord = struct.unpack('B', nextRecord)[0]
            if currentRecord in [0, 1]:
                handleTransaction(currentRecord, struct.unpack('! I Q d', file.read(20)))
                numRecordsRead += 1
            elif currentRecord in [2, 3]:
                handleTransaction(currentRecord, struct.unpack('! I Q', file.read(12)))
                numRecordsRead += 1
            nextRecord = file.read(1)
    file.close()

    print("total credit amount="+str('{:.2f}'.format(round(totalCredit,2))))
    print("total debit amount="+str('{:.2f}'.format(round(totalDebit,2))))
    print("autopays started="+str(autopaysStarted))
    print("autopays ended="+str(autopaysEnded))
    print("balance for user "+str(user)+"="+str('{:.2f}'.format(round(userBalance,2))))

if __name__ == "__main__":
    main()
