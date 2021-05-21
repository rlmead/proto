import sys
import struct

# define path to txnlog file
txnLogFile = './txnlog.dat'

# define user whose balance should be returned
user = '2456938384156277127'

# define variables that will be returned
totalDebit = 0.0
totalCredit = 0.0
autopaysStarted = 0
autopaysEnded = 0
userBalance = 0.0

# parse binary file txnLogFile
with open(txnLogFile, 'rb') as file:
    # read the first 9 bytes - these will be the header if the txnLogFile is the proper format
    header = file.read(9)
    magicString, version, numRecords = struct.unpack('! 4s c I', header)
    # validate magic string "MPS7" in header
    if magicString != b'MPS7':
        sys.exit("ERROR: ./txnlog.dat is not the correct format.")
    # define a couple variables for cycling through the transaction records
    currentRecord = file.read(1)
    count = 0
    # cycle through transaction records
    while currentRecord:
        # cycle through transaction records (note: this code is a bit wet/repetitive, but i think abstracting it with extra functions would be overengineering for this relatively simple task)
        if currentRecord == b'\x00':
            # read the remaining bytes in the record
            record = file.read(20)
            # parse record's user ID and amount in dollars
            # add record's amount in dollars to totalDebit
            # if record's user ID matches user:
                # subtract record's amount in dollars from userBalance
        elif currentRecord == b'\x01':
            # read the remaining bytes in the record
            record = file.read(20)
            # parse record's user ID and amount in dollars
            # add record's amount in dollars to totalCredit
            # if record's user ID matches user:
                # add record's amount in dollars to userBalance
        elif currentRecord == b'\x02':
            # increment the count of autopays started
            autopaysStarted += 1
            # read the remaining bytes in the record
            record = file.read(12)
        elif currentRecord == b'\x03':
            # increment the count of autopays ended
            autopaysEnded += 1
            # read the remaining bytes in the record
            record = file.read(12)
        # move on to the next record
        currentRecord = file.read(1)

file.close()

# return the required information in the required format
print("total credit amount="+str('{:.2f}'.format(round(totalCredit,2))))
print("total debit amount="+str('{:.2f}'.format(round(totalDebit,2))))
print("autopays started="+str(autopaysStarted))
print("autopays ended="+str(autopaysEnded))
print("balance for user 2456938384156277127="+str('{:.2f}'.format(round(userBalance,2))))
