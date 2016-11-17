## Overview:
	
You will design a program that simulates a voting machine. It will read a file containing
the votes that users cast, give each voter a receipt to provide accountability and tally the
votes for each candidate at the end.
The system you design will be modified to simulate a database with relatively high
failure rate. The database will corrupt information at a rate of approximately 1 fault per
1000 bits stored or retrieved.

## Functional Requirements:

1. The system will be provided with an input file containing a sequence of commands
to be processed in sequence.
2. The operators must be able to terminate the program prematurely.
3. When the program terminates (either from reaching the end of the input file or from
an early termination) the program must create a file containing the number of voters
processed and the number of votes received by each each candidate in each position.
4. The program must produce an output log containing the simulated “receipts” that
were given to voters.
5. The program must support a configuration command for passing configuration parameters
to the database subsystem.
6. The program must support a voter command to start the simulation for a voter.
7. The program must support a vote command to simulate the voter selecting a candidate
for a position.
8. The program must support a cast command to cast the votes that the voter specified.
9. The program must generate a unique vote record number to identify the votes cast
by a voter.
10. The program must support an inquire command to list the votes associated with a
specific vote record number.

## Non-Functional Requirements:

1. The system must have a MTTF<1,000,000 votes when the database system has a
failure rate of 1 corruption per 500 bits of data stored or retrieved.
2. If a candidate received k votes for an office but the system reports that the candidate
received n votes, this is counted as |n − k| failures.
3. If the system reports votes for an invalid candidate to a real office, this is counted as
1 fault regardless of the number of votes reported.
4. If the system reports votes for an invalid office, this is not considered a fault.
5. If an inquiry reports incorrect votes for a voter, this is a single fault no matter how
many errors there are or what kind they are.
6. The program must not keep any state information after processing any cast command.
7. The program must close the database subsystem before terminating
8. The program must be given the name of the input file when it starts.
9. The voter receipt log should be named source-votelog.txt, where source is
replaced with the main part of the input filename. For example, if the input filename
is smallinput.txt, the coter receipt log should be named smallinput-votelog.
txt.
10. The voter receipt log should use the same format as the command log, except that
the vote record number should be appended on the voter command.
11. The results file should be named source-results.txt, where source is replaced
with the main part of the input filename.
12. The results file should begin with a tally command containing the total number of
voters who cast votes.
13. The results file should contain tally commands for each office and candidate, in any
order.
14. If there has been a voter command that has not been followed by a cast command
when a new voter command comes in, the first voter has abandoned the booth and
the votes must not be counted.
15. Vote record numbers do not necessarily need to be really numbers, but may contain
other characters that do not interfere with parsing of the files.
16. The program may support extensions to allow receipts for abandoned voter sessions
and separately tallying the votes of abandoned sessions.
17. The program must be able to handle 1,000,000 voters.
18. The program must be able to handle 200 offices, with an average name length of 20
characters. The average number of offices voted per voter is 15.
19. The program must be able to handle 2000 candidates per office, with an average
name length of 25 characters.
20. Every voter will vote for each office at most once. The program is free to respond to
a violation of this rule in any way.
21. Input will contain only ordinary characters (US-ASCII). The program is free to
respond to a violation of this rule in any way.

## Commands

### Configuration command

The configuration command begins with the command CONF. The whole line that starts
with this command should be passed to the database subsystem without examining the rest
of the line

Example: `CONF cache-false-rate 0.00001`

### Voter command
The voter command contains only the command `VOTER`.

### Vote command
The vote command begins with the command `VOTE`, followed by the office and the selected
candidate, all separated by tab characters.

### Cast command
The cast command contains only the command `CAST`. It indicates that the user is ready
to cast the votes that were identified. The votes must not be added to the tallies for the
candidates until this command is received. When output in the vote receipt log, it is
followed by a tab and then the vote record number.
After this command is processed, the program is required to purge all of its variables,
except that it can keep the files and database subsystem open. This requirement is to ensure
that you do not cheat by circumventing the noisy database subsystem.

Example from the input file:

```
VOTER
VOTE Goveno r S i l l y Hen
VOTER
VOTE Goveno r Mickey Mouse
VOTE Mayor R o nal d Goose
CAST
```

Example from the vote receipt log:

```
VOTER
VOTE Goveno r Mickey Mouse
VOTE Mayor R o nal d Goose
CAST 8948298145031
```

### Inquiry command
The inquiry command contains the command `INQ`, followed by a tab and then the vote
record number. To process this command, the program should look up the votes cast for
the specified voter record number, and print a copy of the voter receipt on the voter receipt
log file.

Example from input file:
`INQ 8948298145031`

This should result in the following displayed in the vote receipt log:
```
VOTER
VOTE Goveno r Mickey Mouse
VOTE Mayor R o nal d Goose
CAST 8948298145031
```
