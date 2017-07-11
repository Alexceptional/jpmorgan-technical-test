# JP Morgan - Technical Test
### Daily Trade Reporting Engine
--

## Overview
This is a coding assignment as part of the JP Morgan application process. The objective of this task is to produce a trade report, with specified output, based on source data containing trade instructions.

### Data
Some sample data was provided, as below:

Entity|Buy/Sell|AgreedFx|Currency|InstructionDate|SettlementDate|Units|Price per unit
foo|B|0.50SGP|01 Jan 2016|02 Jan 2016|200|100.25

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

These are based on sample source data containing 
