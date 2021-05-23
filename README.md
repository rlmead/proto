# MVP: Parsing a custom protocol format with Python

## Must have
- binary file parsing
- proper handling of file structure and encoding
- transaction calculation for required outputs
- proper output formatting:
```
total credit amount=0.00
total debit amount=0.00
autopays started=0
autopays ended=0
balance for user 2456938384156277127=0.00
```

## Should have
- graceful error handling for transaction logs that don't have the magic string in the header
- simple, clean design that will be straightforward to reviewers
- efficient code

## Could have

## Won't have
- input argument handling
- extensive error checks
