# define path to txnlog file
# txnLogFile = './txnlog.dat'

# define user whose balance should be returned
# user = '2456938384156277127'

# define variables that will be returned
# totalDebit = 0.0
# totalCredit = 0.0
# autopaysStarted = 0
# autopaysEnded = 0
# userBalance = 0.0

# parse binary file txnLogFile
    # read the first 9 bytes - these will be the header if the txnLogFile is the proper format
    # validate magic string "MPS7" in header - if the first 4 bytes don't match the magic string:
            # exit gracefully
    # define a variable for cycling through the transaction records - currentRecord = next byte
    # while currentRecord:
        # cycle through transaction records (note: this code is a bit wet/repetitive, but i think abstracting it with extra functions would be overengineering for this relatively simple task)
        # determine transaction type from value of currentRecord
            # if 0x00: debit
                # read the next 20 bytes - the rest of the record
                # parse record's user ID and amount in dollars
                # add record's amount in dollars to totalDebit
                # if record's user ID matches user:
                    # subtract record's amount in dollars from userBalance
            # if 0x01: credit
                # read the next 20 bytes - the rest of the record
                # parse record's user ID and amount in dollars
                # add record's amount in dollars to totalDebit
                # if record's user ID matches user:
                    # subtract record's amount in dollars from userBalance
            # if 0x02: startAutopay
                # autopaysStarted += 1
                # read the next 12 bytes - the rest of the record (but do nothing else with them)
            # if 0x03: endAutopay
                # autopaysEnded += 1
                # read the next 12 bytes - the rest of the record (but do nothing else with them)
        # currentRecord = next byte

# return the required information
# print("total credit amount="+str(round(totalCredit,2)))
# print("total debit amount="+str(round(totalDebit,2)))
# print("autopays started="+str(autopaysStarted))
# print("autopays ended="+str(autopaysEnded))
# print("balance for user 2456938384156277127="+str(round(userBalance,2)))
