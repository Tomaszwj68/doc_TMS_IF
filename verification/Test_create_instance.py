import unittest
import sys
import os
# dodaje sciezke do path, by moc zaimportowac potrzebne wlasne pliki
sys.path.append('/home/tomek/Py_projects/CIS_COS')

from body import create_instance


class TestCreateInstance(unittest.TestCase):
    def test_prev_version_has_low_number(self):
        # sprawdzam poprawnosc wprowadzenia numerow wersji
        self.assertEqual(create_instance(12, 13), "Poprzednia wersja nie może mieć wyższego numeru niż obecna!")

    def test_versions_only_float(self):
        # sprawdzenie poprawnego podania numeru wersji
        self.assertEqual(create_instance(12.0, AA), "Numer wersji może być tylko liczbą.")

    def test_prepare_doc_for_correct_version(self):
        # sprawdzenie czy generuje sie poprawna instancja
        self.assertIsInstance(Doc_in.rider, CsvReader)

    def test_exceptions(self):
        # sprawdzam komunikat w przypadku braku dokumentu pdf lub csv
        with self.assertRaises(OSError):
            os.rename(r'IN_CIS_COS.csv', r'__IN_CIS_COS.csv')


if __name__ == '__main__':
    unittest.main()
