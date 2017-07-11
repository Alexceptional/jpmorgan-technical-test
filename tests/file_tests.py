import unittest

from report import import_data
from tempfile import TemporaryFile


class TestImportData(unittest.TestCase):

    def test_import_data(self):

        """
        Test CSV file import. Expected dictionaries vs sample imput,

        """

        test_csv_data = (
            "test1,B,0.5,SGP,01-Jan-16,02-Jan-16,200,100.50\n"
            "test2,S,0.25,AED,02-Feb-16,03-Mar-16,300,250.25\n"
        )

        expected_response = [
            {'entity': 'test1', 'buy_sell': 'B', 'agreed_fx': '0.5', 'currency': 'SGP',
             'instr_date': '01-Jan-16', 'settle_date': '02-Jan-16', 'units': '200', 'ppu': '100.50',
             },
            {'entity': 'test2', 'buy_sell': 'S', 'agreed_fx': '0.25', 'currency': 'AED',
             'instr_date': '02-Feb-16', 'settle_date': '03-Mar-16', 'units': '300', 'ppu': '250.25',
             },
        ]

        # Create temporary file to handle sample data:

        with TemporaryFile('w+') as f:
            f.write(test_csv_data)
            f.seek(0)

            response = import_data(f)

        self.assertCountEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
