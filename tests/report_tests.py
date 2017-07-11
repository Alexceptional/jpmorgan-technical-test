import unittest

from report import Instruction
import datetime


class TestInstruction(unittest.TestCase):

    # Default data:
    data = {
        'entity': 'test',
        'buy_sell': 'B',
        'agreed_fx': 1.5,
        'currency': 'GBP',
        'instr_date': '01-Jan-17',
        'settle_date': '02-Jan-17',
        'units': 100,
        'ppu': 200.50,
    }

    def test_get_trade_amount(self):

        """
        Test output of trade amount calculation

        """

        instruction = Instruction(self.data)

        self.assertEqual(instruction.get_trade_amount(), 30075.0)

    def test_get_settle_date(self):

        """
        Test the settle date calculation: standard working week, within working days

        """

        data = self.data.copy()
        data['settle_date'] = '14-Jul-17'

        instruction = Instruction(data)

        self.assertEqual(instruction.get_settle_date(), datetime.datetime(2017, 7, 14))

    def test_get_settle_date_weekend(self):

        """
        Test the settle date calculation: standard working week, outwith working days

        """

        data = self.data.copy()
        data['settle_date'] = '16-Jul-17'

        instruction = Instruction(data)

        self.assertEqual(instruction.get_settle_date(), datetime.datetime(2017, 7, 17))

    def test_get_settle_date_nonstd(self):

        """
        Test the settle date calculation: alternative working week, outwith working days

        """

        data = self.data.copy()
        data['settle_date'] = '14-Jul-17'
        data['currency'] = 'AED'

        instruction = Instruction(data)

        self.assertEqual(instruction.get_settle_date(), datetime.datetime(2017, 7, 16))


if __name__ == '__main__':
    unittest.main()
