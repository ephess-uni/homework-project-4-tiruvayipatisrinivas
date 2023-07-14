# hp_4.py
#
from datetime, import datetime, timedeltadatetime,
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    date_list = []
    for date in old_dates:
        date_list.append(datetime.strptime(date, "%Y-%m-%d").strftime("%d %b %Y"))
    return date_list


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError("start must be a string in format 'yyyy-mm-dd'")
    elif not isinstance(n, int):
        raise TypeError("n must be an integer")
    else:
        date_list = []
        for i in range(0, n):
            date_list.append(datetime.strptime(start, "%Y-%m-%d") + timedelta(days=i))
        return date_list


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`. The date, value pairs are returned as tuples
    in the returned list."""
    final_list = []
    seq = 0
    for i in values:
        date_list = []
        date_list.append(datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=seq))
        date_list.append(i)
        final_list.append(tuple(date_list))
        seq += 1
    return final_list


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    with open(infile) as f:
        li = []
        DictReader_obj = DictReader(f)
        for item in DictReader_obj:
            di = {}
            day1 = datetime.strptime(item['date_returned'], '%m/%d/%Y') - datetime.strptime(item['date_due'],
                                                                                            '%m/%d/%Y')
            if day1.days > 0:
                di["patron_id"] = item['patron_id']
                di["late_fees"] = round(day1.days * 0.25, 2)
                li.append(di)
            else:
                di["patron_id"] = item['patron_id']
                di["late_fees"] = float(0)
                li.append(di)
        aggregated_data = defaultdict(float)

        for dictionary in li:
            key = dictionary['patron_id']
            aggregated_data[key] += dictionary['late_fees']

        tax = [{'patron_id': key, 'late_fees': value} for key, value in aggregated_data.items()]
        for dict in tax:
            for k, v in dict.items():
                if k == "late_fees":
                    if len(str(v).split('.')[-1]) != 2:
                        dict[k] = str(v)

        with open(outfile, "w", newline="") as file:
            col = ['patron_id', 'late_fees']
            writer = DictWriter(file, fieldnames=col)
            writer.writeheader()
            writer.writerows(tax)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
