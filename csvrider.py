# -*- coding:UTF-8

import csv
import sys
from fpdf import *
import xml.etree.ElementTree as xml
from table_config import *


class CsvRider:

    def __init__(self, version, previous, csv_input):
        self.version = version
        self.previous = previous
        self.csv_input = csv_input

    def __del__(self):
        print('Instancja zniszczona')

    def rider(self):
        with open(self.csv_input, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            pdf = FPDF()
            pdf.add_font('DejaVu', '',
                         '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
            pdf.add_page(orientation='L')
            # robie standardowa tabelke naglowkowa
            pdf.set_font("DejaVu", size=8)
            pdf.cell(40, 10, txt="XXX", border=1, align='C')
            pdf.cell(100, 10, txt="IF CIS-COS", border=1, align='C')
            pdf.cell(40, 10, txt="Korekta: 0", border=1, align='C')
            pdf.cell(40, 10, txt="Strona: x", border=1, align='C')
            pdf.ln(20)

            pdf.set_font("DejaVu", size=12)
            if self.csv_input.startswith('OUT'):
                pdf.cell(200, 10, txt="Komunikaty wysylane przez system zaleznosciowy", ln=1, align="C")
                pdf_name = 'IF_out.pdf'
            elif self.csv_input.startswith('IN'):
                pdf.cell(200, 10, txt="Komunikaty odbierane przez system zaleznosciowy", ln=1, align="C")
                pdf_name = 'IF_in.pdf'
            else:
                print('Nie można znaleźć pliku csv')
                sys.exit()
            pdf.ln(10)

            # skladam w jedno jaka to wersja T2C
            pdf.set_font("DejaVu", size=10)
            tools = "Tools2Config_PKP_L2-{}".format(self.version)
            pdf.cell(150, 8, txt=tools, ln=1, align='C')
            pdf.ln(10)
            # ustalenie wielkosci komorek, daje naglowki...
            pdf.set_fill_color(169, 169, 169)
            # szerokosc wrzucam z łapy. Traktuje to jako dwa rzedy
            # przy Znaczenie po prostu inne obramowanie by nie bylo widac
            pdf.set_font("DejaVu", size=10)
            pdf.cell(18, 8, txt="Zdarzenie", border=1, fill=True, align='C')
            pdf.cell(28, 8, txt="Polecenie", border=1, fill=True, align='C')
            pdf.cell(100, 8, txt="Znaczenie", border='LT', fill=True, align='C')
            pdf.cell(26, 8, txt="Argument", border=1, fill=True, align='C')
            pdf.cell(44, 8, txt="Własności", border=1, fill=True, ln=1, align='C')
            pdf.cell(18, 8, txt="DEC", border=1, fill=True, align='C')
            pdf.cell(12, 8, txt="Typ", border=1, fill=True, align='C')
            pdf.cell(16, 8, txt="Ident", border=1, fill=True, align='C')
            pdf.cell(100, 8, txt=" ", border='BL', fill=True, align='C')
            pdf.cell(12, 8, txt="Liczba", border=1, fill=True, align='C')
            pdf.cell(14, 8, txt="Obiekt", border=1, fill=True, align='C')
            pdf.cell(20, 8, txt="PRETEST", border=1, fill=True, align='C')
            pdf.cell(12, 8, txt="PRIO", border=1, fill=True, align='C')
            pdf.cell(12, 8, txt="NVS", border=1, fill=True, ln=1, align='C')

            for row in csv_reader:
                pdf.set_font("DejaVu", size=8)
                print(row)
                if line_count != 0:
                    if float(self.version) < float(row[0]):
                        line_count += 1
                if line_count == 0:
                    line_count += 1
                    continue
                m = 0
                lista = [n for n in range(1, 10, 1)]
                for elems in lista:
                    pdf.cell(conf_out[m], 8, txt=str(elems), border=1)
                    m += 1
                    if m == 9: m = 0
                pdf.ln(8)
            pdf.output(pdf_name)
            pdf.close()
        csv_file.close()

    def compare(self, previous, current):
        current = self.version
        previous = self.previous
        # csv_to_compare = ['IN_CIS_COS.csv', 'OUT_CIS_COS.csv']
        csv_to_compare = ['OUT_CIS_COS.csv']
        for n in csv_to_compare:
            with open(n, mode='r') as csv_file:
                dict_reader = csv.DictReader(csv_file, delimiter=';')
                pdf = FPDF()
                pdf.add_font('Arial Unicode MS', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
                pdf.add_page()
                # robie standardowa tabelke naglowkowa
                pdf.set_font("Arial Unicode MS", size=8)
                pdf.cell(30, 10, txt="XXX", border=1, align='C')
                pdf.cell(80, 10, txt="IF CIS-COS", border=1, align='C')
                pdf.cell(30, 10, txt="Korekta: 0", border=1, align='C')
                pdf.cell(30, 10, txt="Strona: x", border=1, align='C')
                pdf.ln(20)

                pdf.set_font("Arial", size=10)
                pdf.cell(100, 10, txt="8. Zmiany w komunikatach w porownaniu do poprzedniej wersji.", ln=1, align="R")
                if n.startswith('OUT'):
                    pdf.cell(200, 10, txt="Komunikaty wysylane przez system zaleznosciowy", ln=1, align="C")
                    pdf_name = 'IF_compare_out.pdf'
                    # tworze wiersz z headerem
                    headers = dict_reader.fieldnames
                    comp_header = []
                    comp_header.append(headers[6])
                    comp_header.append(headers[10])
                    comp_header.append(headers[12])
                    comp_header.append(headers[1])
                    comp_header.append(headers[13])
                    comp_header.append(headers[14])
                    for i in comp_header:
                        pdf.set_font("Arial Unicode MS", size=8)
                        pdf.cell(20, 10, txt=i, border=1)
                    pdf.ln(10)
                    line_count = 0
                    for row in dict_reader:
                        if row['validFrom']:
                            value = row['validFrom']
                            # dodaje tylko te, ktore doszly, nie drukuje wczesniej istniejacych
                            # pomijam to, co doszlo w pozniejszych wersjach
                            if float(value) < float(previous) or float(value) > float(current):
                                pass
                            else:
                                pdf.set_font("Arial Unicode MS", size=8)
                                pdf.cell(20, 10, txt=row['Obiekt'], border=1)
                                pdf.cell(20, 10, txt=row['Variable'], border=1)
                                pdf.cell(20, 10, txt=row['Value'], border=1)
                                pdf.cell(20, 10, txt=row['Dec'], border=1)
                                pdf.cell(20, 10, txt=row['HEX'], border=1)
                                pdf.cell(20, 10, txt=row['Comment'], border=1)
                                pdf.ln(10)

                        else:
                            pass
                elif n.startswith('IN'):
                    pdf.cell(200, 10, txt="Komunikaty odbierane przez system zaleznosciowy", ln=1, align="C")
                    pdf_name = 'IF_compare_in.pdf'
                    # tworze wiersz z headerem
                    headers = dict_reader.fieldnames
                    comp_header = []
                    comp_header.append(headers[6])
                    comp_header.append(headers[10])
                    comp_header.append(headers[12])
                    comp_header.append(headers[1])
                    comp_header.append(headers[13])
                    comp_header.append(headers[14])
                    for i in comp_header:
                        pdf.set_font("Arial Unicode MS", size=8)
                        pdf.cell(20, 10, txt=i, border=1)
                    pdf.ln(10)
                    line_count = 0
                    for row in dict_reader:
                        if row['validFrom']:
                            value = row['validFrom']
                            # dodaje tylko te, ktore doszly, nie drukuje wczesniej istniejacych
                            # pomijam to, co doszlo w pozniejszych wersjach
                            if float(value) < float(previous) or float(value) > float(current):
                                pass
                            else:
                                pdf.set_font("Arial Unicode MS", size=8)
                                pdf.cell(20, 10, txt=row['Obiekt'], border=1)
                                pdf.cell(20, 10, txt=row['Variable'], border=1)
                                pdf.cell(20, 10, txt=row['Value'], border=1)
                                pdf.cell(20, 10, txt=row['Dec'], border=1)
                                pdf.cell(20, 10, txt=row['HEX'], border=1)
                                pdf.cell(20, 10, txt=row['Comment'], border=1)
                                pdf.ln(10)

                        else:
                            pass

                pdf.output(pdf_name)
                pdf.close()

# testowy fragment kodu
MDC = xml.ElementTree()


root = xml.Element("LogicalObjectTypes")
ObjectType = xml.Element("LogicalObjectType", name="TCSTATUS")
ObjectTypeVariable = xml.Element("LogicalObjectTypeVariable")
root.append(ObjectType)
ObjectType.append(ObjectTypeVariable)
MDC._setroot(root)
MDC.write('test.xml')
