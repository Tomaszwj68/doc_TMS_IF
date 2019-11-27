import unittest
import sys
# dodaje sciezke do path, by moc zaimportowac potrzebne wlasne pliki
sys.path.append('/home/tomek/Py_projects/CIS_COS')

from body import test_decision


class TestUserDecision(unittest.TestCase):
    def test_input_only_number_in_range(self):
        # przypadek pozytywny, daje dowolna liczbe z zakresu
        self.assertEqual(test_decision('2'), str(2))
        # wartosci brzegowe. Daje 0 i 4. Dodatkowo sprawdzam co w przypadku liczby ujemnej.
        self.assertEqual(test_decision('0'), str("Podano liczbę spoza zakresu!"))
        self.assertEqual(test_decision('4'), str("Podano liczbę spoza zakresu!"))
        self.assertEqual(test_decision('-1'), str("Podano literę zamiast liczby!"))

    def test_string_not_allowed(self):
        # niedopuszczam liter ani ciagow znakow
        self.assertEqual(test_decision('a'), str("Podano literę zamiast liczby!"))
        self.assertEqual(test_decision('topinambur'), str("Podano literę zamiast liczby!"))


if __name__ == '__main__':
    unittest.main()
