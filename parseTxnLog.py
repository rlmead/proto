import sys
import struct

# define path to txnlog file
txnLogFile = './txnlog.dat'

# define user whose balance should be returned
user = 2456938384156277127

def main():
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
            # cycle through transaction records (note: this code is a bit wet/repetitive - wondering whether abstracting it with extra functions would be overengineering for this relatively simple task)
            if currentRecord == b'\x00':
                # read the remaining bytes in the record
                record = file.read(20)
                # parse the data from the record
                unixTimestamp, userId, dollarAmount = struct.unpack('! I Q d', record)
                # add record's amount in dollars to totalDebit
                totalDebit += dollarAmount
                # if record's user ID matches user, subtract record's amount in dollars from userBalance
                if userId == user:
                    userBalance -= dollarAmount
            elif currentRecord == b'\x01':
                # read the remaining bytes in the record
                record = file.read(20)
                # parse the data from the record
                unixTimestamp, userId, dollarAmount = struct.unpack('! I Q d', record)
                # add record's amount in dollars to totalCredit
                totalCredit += dollarAmount
                # if record's user ID matches user, add record's amount in dollars to userBalance
                if userId == user:
                    userBalance -= dollarAmount
            elif currentRecord == b'\x02':
                # increment the count of autopays started
                autopaysStarted += 1
                # read the remaining bytes in the record
                record = file.read(12)
                # parse the data from the record
                unixTimestamp, userId = struct.unpack('! I Q', record)
            elif currentRecord == b'\x03':
                # increment the count of autopays ended
                autopaysEnded += 1
                # read the remaining bytes in the record
                record = file.read(12)
                # parse the data from the record
                unixTimestamp, userId = struct.unpack('! I Q', record)
            # move on to the next record
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
