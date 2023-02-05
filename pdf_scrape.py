import pandas as pd
import tabula as tb
import unittest


def scrape_pdf(file_data):
    # df = new dataframe
    df = pd.concat(file_data)
    # drop rows called Unnamed: X
    df.drop(df.filter(regex="Unnamed"), axis=1, inplace=True)

    # rename column called either Name or Namn to Course
    df.rename(columns={'Namn': 'Course', 'Name': 'Course'}, inplace=True)
    # rename column called either Personnummer or Personal identity number to Grade
    df.rename(columns={'Personnummer': 'Grade',
              'Personal identity number': 'Grade'}, inplace=True)
    # drop rows 0-3
    df.drop(df.index[0:3], inplace=True)
    # where column 1 is nan, drop that row and all rows below
    index = 0
    for i in df['Grade']:
        if pd.isna(i):
            df.drop(df.index[index:], inplace=True)
            break
        index += 1

    # drop all rows where Grade contains "fup"
    df = df[~df['Grade'].str.contains("fup")]
    # drop all rows where Grade contains capital P
    df = df[~df['Grade'].str.contains("P")]
    # set all values in grade to format_grade()
    df['Grade'] = df['Grade'].apply(format_grade)

    # reset index
    df.reset_index(drop=True, inplace=True)

    return df


def format_grade(grade):
    vals = grade.split(" ")
    formatted = vals[0]+" "+vals[2]
    return formatted


def calculate_merit(column):
    merit = 0
    total_hp = 0
    for i in column:
        # hp is all number until first space
        # grade is all last letter
        hp, grade = i.split(" ")
        # set , to .
        hp = hp.replace(",", ".")
        hp = float(hp)

        # grade_num = 5 if A, 4.5 if B, 4 if C, 3.5 if D, 3 if E, 0 if F
        grade_num = 5 if grade == 'A' else 4.5 if grade == 'B' else 4 if grade == 'C' else 3.5 if grade == 'D' else 3 if grade == 'E' else 0
        # convert to float
        grade_num = float(grade_num)
        merit += hp * grade_num
        total_hp += hp
    ans = merit/total_hp
    # round to 3 decimals
    ans = round(ans, 3)
    return ans


class test(unittest.TestCase):
    def test_merit_swe(self):

        file_name = 'betyg.pdf'
        # all pages
        file_data = tb.read_pdf(file_name, pages='all')
        df = scrape_pdf(file_data)
        merit = calculate_merit(df['Grade'])
        self.assertEqual(merit, 4.714)
        print(merit)

    def test_merit_eng(self):
        file_name = 'Intyg-3.pdf'
        # all pages
        file_data = tb.read_pdf(file_name, pages='all')
        df = scrape_pdf(file_data)
        merit = calculate_merit(df['Grade'])
        self.assertEqual(merit, 4.529)
        print(merit)

def get_merit(pdf_file):
    df = tb.read_pdf(pdf_file, pages='all')
    df = scrape_pdf(df)
    merit = calculate_merit(df['Grade'])
    return merit


if __name__ == '__main__':
    unittest.main()

