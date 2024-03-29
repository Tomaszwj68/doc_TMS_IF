# -*- coding:UTF-8

from csvrider import CsvRider
import os
from PyPDF2 import PdfFileMerger, PdfFileReader

# konfiguracje dokumentow

config_full = ['Tytulowa.pdf', 'Spis_tresci.pdf', 'IF_in.pdf', 'IF_out.pdf', 'IF_compare_out.pdf',
               'IF_compare_in.pdf']


def merge(conf):
    merger = PdfFileMerger()
    for file in conf:
        merger.append(PdfFileReader(file), 'rb')
    merger.write('CIS-COS.pdf')
    exit()


# decision = 0


def test_decision(local_decision):
    # akceptowalne tylko liczby z okreslonego przedzialu
    if local_decision.isdigit():
        if float(local_decision) in [1, 2, 3]:
            return local_decision
        else:
            print("Podano liczbę spoza zakresu!")
            return "Podano liczbę spoza zakresu!"
    else:
        print("Podano literę zamiast liczby!")
        return "Podano literę zamiast liczby!"


def create_instance(ver,prev):
    ver = input("Podaj numer wersji (np. 13.0):")
    prev = input("Podaj numer poprzedniej wersji (np. 14.0):")
    if all(ver.isdigit(), prev.isdigit()):
        if float(prev) <= float(ver):
            print ("Poprzednia wersja nie może mieć wyższego numeru niż obecna!")
            return "Poprzednia wersja nie może mieć wyższego numeru niż obecna!"


if __name__ == '__main__':


    # Wybor przez usera co bedzie generowane. Zaimplementowane narazie jedynie polowicznie 1.
    print("CIS-COS Generator ver. 1.0\n")
    print("""1 - Generacja pelnego opisu interfejsu CIS-COS\n
            2 - Porownanie dwoch wersji CIS-COS (nie zaimplementowane)\n
            3 - XML z logika dla MDC (nie zaimplementowane)""")
    decision = input("Wybierz opcje (podaj numer):")
    test_decision(decision)


    if float(decision) == 1:
        try:
            ver = input("Podaj numer wersji (np. 13.0):")
            prev = input("Podaj numer poprzedniej wersji (np. 14.0):")
            assert (float(prev) <= float(ver)), "Numer poprzedniej wersji nie moze byc wiekszy niz obecnej!"
            # przywoluje klase i obrabiam wejscia do systemu, narazie nie dziala porownanie wejsc
            Doc_in = CsvRider(ver, prev, 'IN_CIS_COS.csv')
            Doc_in.rider()
            # przywuluje klase na wyjscia z systemu
            Doc_out = CsvRider(ver, prev, 'OUT_CIS_COS.csv')
            Doc_out.rider()
            Doc_out.compare(ver, prev)
            del Doc_in
            del Doc_out
            merge(config_full)

        except OSError:
            print("Dokument CIS-COS zablokowany - nie mozna wygenerowac nowego.\n Zamknij otwarty dokument pdf lub "
                  "sprawdz nazwy plikow CSV i pdf.")
        except KeyboardInterrupt:
            print("Generacja przerwana przez uzytkownika")
    #    except:
     #       print("Nieznany rodzaj bledu.")
    else:
        print("Opcja narazie nie zaimplementowana.")