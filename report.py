"""
=====================================================================

  JP Morgan Trade Report Test Exercise -- Main Code
  - - - - - - - - - - - - - - - - - - - - - - - - -

  Main code of the project is in this file. Code is ran from __main__
  function (bottom of file).

  AUTHOR:           Alexander N Scott
  LAST UPDATED:     11/07/2017

=====================================================================
"""


import datetime
import csv


def import_data(file):

    """
    Imports instruction data from a .csv file, at the specified filepath

    :param file: file
        File object, to be read by the CSV reader
    :return: list
        A list of dictionaries, per row in the file, with the keys specified in the headers list
        below

    """

    headers = [
        'entity', 'buy_sell', 'agreed_fx', 'currency', 'instr_date', 'settle_date', 'units', 'ppu',
    ]

    # Create CSV reader object, using header schema defined to generate dictionary
    csv_reader = csv.DictReader(file, headers)

    # Create list of dictionaries from reader
    data_rows = [file_row for file_row in csv_reader]

    return data_rows

#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Instruction:

    """
    Class "Instruction"
    - - - - - - - - - -

    This object stores an instance of a trade instruction. Class is initialised by a dictionary from
    the CSV file (or other data source).

    """

    # Define currencies following the Sunday-Thursday working week
    ST_WEEK = (
        'AED', 'SAR',
    )

    def __init__(self, input_data):

        """
        :param input_data: dictionary
            Input dictionary consisting of a data row; dict keys are identical to the variable
            names of the instruction fields

        :return: None
        """

        try:
            self.entity = input_data['entity']
            self.buy_sell = input_data['buy_sell']
            self.agreed_fx = float(input_data['agreed_fx'])
            self.currency = input_data['currency']
            self.instr_date = datetime.datetime.strptime(input_data['instr_date'], '%d-%b-%y')
            self.settle_date = datetime.datetime.strptime(input_data['settle_date'], '%d-%b-%y')
            self.units = int(input_data['units'])
            self.ppu = float(input_data['ppu'])

        except ValueError as err:
            raise RuntimeError('Error: incorrect data type/format: {}'.format(str(err)))

        except KeyError as err:
            raise RuntimeError('Error: field {} not found!'.format(str(err)))

        self.date_today = datetime.datetime.now()

    def get_trade_amount(self):

        """
        Calculates the trade value, based on an instruction sent by an entity

        :return: float
            Trade value, in USD
        """

        trade_amt = self.ppu * self.units * self.agreed_fx

        return trade_amt

    def get_settle_date(self):

        """
        Calculate the actual settlement date; if the specified date falls on a weekend/non-working
        day then the next working day is specified

        :return: datetimne
            Returns the settlement date
        """

        weekday = self.settle_date.weekday()
        offset = 0

        if self.currency in self.ST_WEEK and weekday in (4, 5):
            offset = 6 - weekday

        elif weekday in (5, 6):
            offset = 7 - weekday

        # Shift date to next working day if required:

        if offset:
            return self.settle_date + datetime.timedelta(days=offset)

        return self.settle_date

#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Report:

    """
     This class is intialised with an array (list) of instructions, and generates reports based
     on this data.

     Add methods or extend class to add futher report formats

    """

    def __init__(self, instructions):

        """
        Initialise class with two lists of trade instructions; incoming (sell) and outgoing (buy)

        :param instructions: list
            Trade instruction objects, in a list
        """

        self.outgoing = []
        self.incoming = []

        for instruction in instructions:
            if instruction.buy_sell == 'B':
                self.outgoing.append(instruction)

            elif instruction.buy_sell == 'S':
                self.incoming.append(instruction)

    def print_incoming_outgoing(self):

        """
        Compile a list of buy and sell trades, grouped by date, and print to screen. Values are
        displayed in dollars and rounded to two decimal places.
        """

        print('SELL TOTALS:')

        for record in self._get_incoming_outgoing(self.incoming):
            print(record['date'].strftime('%d/%m/%Y').ljust(15), '${0:.2f}'.format(record['value']))

        print('\nBUY TOTALS:')

        for record in self._get_incoming_outgoing(self.outgoing):
            print(record['date'].strftime('%d/%m/%Y').ljust(15), '${0:.2f}'.format(record['value']))

    def print_entity_ranks(self):

        """
        Compile a list of trade entities and their total trade values, split into buy and sell transactions,
        and ordered with highest value ranked first. Values are displayed in dollars and rounded to two
        decimal places.
        """

        print('SELL RANKING:')

        for record in self._get_entity_ranks(self.incoming):
            print('{}'.format(record['entity']).ljust(15), '${0:.2f}'.format(record['value']))

        print('\nBUY RANKING:')

        for record in self._get_entity_ranks(self.outgoing):
            print('{}'.format(record['entity']).ljust(15), '${0:.2f}'.format(record['value']))

    @staticmethod
    def _get_incoming_outgoing(insructions):

        """
        Compile list of total trade figures, per date

        :param insructions: list
            list of instructions

        :return: list
            sorted list of dicts: {'date': trade_date, 'value': date_total }

        """

        data_format = {}

        for trade in insructions:

            date = trade.get_settle_date()
            value = trade.get_trade_amount()

            if data_format.get(date):
                data_format[date] += value

            else:
                data_format[date] = value

        data_list = [{'date': date, 'value': value} for date, value in data_format.items()]

        return sorted(data_list, key=lambda k: k['date'])

    @staticmethod
    def _get_entity_ranks(insructions):

        """
        Compile list of total trade figures, per entity, sorted highest to lowest

        :param insructions: list
            list of instructions

        :return: list
            sorted list of dicts: {'entity': entity, 'value': entity_total }

        """

        data_format = {}

        for trade in insructions:

            entity = trade.entity
            value = trade.get_trade_amount()

            if data_format.get(entity):
                data_format[entity] += value

            else:
                data_format[entity] = value

        data_list = [{'entity': entity, 'value': value} for entity, value in data_format.items()]

        return sorted(data_list, key=lambda k: k['value'], reverse=True)

#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


if __name__ == '__main__':

    # Import sample data from file
    with open('data/source_data.csv', 'r') as source_file:
        raw_data = import_data(source_file)

    # Build list of instruction objects
    trade_array = []

    for row in raw_data:
        trade_array.append(Instruction(row))

    # Create new report object based on list of trade instrcutions
    report = Report(trade_array)

    # Print report details:

    print('\n== BUY/SELL SUMMARY ===================\n')

    report.print_incoming_outgoing()

    print('\n== ENTITY RANKING =====================\n')

    report.print_entity_ranks()
