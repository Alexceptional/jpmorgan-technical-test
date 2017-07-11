# JP Morgan - Technical Test
### Daily Trade Reporting Engine

Written in Python (v3.4.3) using PyCharm v5.0.5.
---

## Assignment Overview
This is a coding assignment as part of the JP Morgan application process. The objective of this task is to produce a trade report, with specified output, based on source data containing trade instructions.

### Data
Some sample data was provided, as below:

Entity|Buy/Sell|AgreedFx|Currency|InstructionDate|SettlementDate|Units|Price per unit
------|--------|--------|--------|---------------|--------------|-----|--------------
foo|B|0.50|SGP|01 Jan 2016|02 Jan 2016|200|100.25
bar|S|0.22|AED|05 Jan 2016|07 Jan 2016|450|150.5

### Instruction Rules
Some rules apply to the trade instructions:

* A work week starts Monday and ends Friday, unless the currency of the trade is AED or SAR, where the work week starts Sunday and ends Thursday. No other holidays to be taken into account.
* A trade can only be settled on a working day.
* If an instructed settlement date falls on a weekend, then the settlement date should be changed to the next working day.
* USD amount of a trade = Price per unit * Units * Agreed Fx

### Report
The objective of this assignment is to produce a report detailing the following:

* Amount in USD settled incoming everyday
* Amount in USD settled outgoing everyday
* Ranking of entities based on incoming and outgoing amount.

## My Approach
I chose to implement this task in a object-oriented manor, with a class defined for a trade instrcution, and a class defined for the report. This would allow for the objects to be extended; for example the report class could be extended to add extra report types and formats.

My source data is loaded from a CSV file, containing ten rows of non-specific, fictitious sample data. This data is then used to initialse a list of trade instruction objects. This list can then be used to initialise the report class to produce the desired report formats.

### Project Structure
The source code for the project is located in the 'report.py' file. I chose to add all code (apart from the tests) to a single source file due to the simplicity of the project. The sample data file is located at data/source_data.csv. 

### Tests
The Python unit tests are located in the tests directory and are in tow files: file_tests.py for the file import test and report_tests.py for the 'Instruction' class tests. I chose not to build unit tests for the 'Report' class due to the nature of its functionality.

## Dependencies
No non-standard dependencies (ses datetime, tempfile, csv and unittest modules.)
