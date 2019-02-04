#!/usr/bin/env python3
"""
                         Q U E S T I O N  # 4
=============================================================================
                           P L O T I N G
=============================================================================
"""
import csv
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter
import datetime
from itertools import groupby
import re
try:
    import ui
except ModuleNotFoundError as e:
    print("Please install python-cli-ui package: pip install python-cli-ui")
    print("Program terminated")
    exit()


TWEETS_DB = "Q3_sqlite_c1868921.sqlite"
CSV_FILE = 'Q3_csv_c1868921.csv'
TABLE_NAME = 'tweets'


def db_into_csv(database=TWEETS_DB, csv_file=CSV_FILE, table_name=TABLE_NAME):
    """Reads database and stores it as csv file
    :param database: database to be stored
    :return:
    This function is from a post on StackOverflown by user Sci Prog, 24-03-2016, accessed on 30-11-2018: https://stackoverflow.com/questions/36188721/exporting-csv-file-from-python-sqlite3
    I have changed most variable names, and added flexibility to be called with a different db name.
    """
    copy_db = sqlite3.connect('{}'.format(database))
    cur = copy_db.cursor()
    cur.execute('SELECT * FROM {tn}'.format(tn=table_name))
    with open(csv_file, 'w') as out_file:
        writer_object = csv.writer(out_file)
        #Write header
        writer_object.writerow([d[0] for d in cur.description])
        #Transfer DB content onto csv file
        for row in cur:
            writer_object.writerow(row)
        #end of for loop
        cur.close()
    print("Data lines in '{}': {}".format(csv_file, (str(many_lines(csv_file) -1))))
    print("-Header not included in count-")


def many_lines(csv_file=CSV_FILE):
    """I got his code from a post by user Simon Brunning on Bytes.com, created 27-08-2008, accessed on 30-11-2018: https://bytes.com/topic/python/answers/833358-finding-out-number-rows-csv-file
    I just wraped it in a function.
    :param csv_file: the csv file you want to know the size
    :return lines_csv int: amount of lines on csv file
    """

    lines_csv = len(list(csv.reader(open(csv_file))))
    return lines_csv


def frequency_map():
    """map showing the frecuency of tweets by location (optional)
    :param:
    :return:
    """
    pass

def senti_map():
    """map showing the number of positive or negative tweets by location(optional)
    :param:
    :return:
    """
    pass

def numpy_freq(csv_file=CSV_FILE):
    """Same as frecuency but using numpy"""


def frecuency(csv_file=CSV_FILE):
    """Frecuency of the tweets over time (mandatory)
    :param csv_file: the csv file containing the data to be graphed.
    :return:
    # line of code bellow is from the Python Documentation, last updated 04-12-2018 by the Python Software Foundation, accessed on 4-12-2018: https://docs.python.org/3/library/datetime.html#strafed-strptime-behavior
          **************************************************
    I believe a scatter plot is better for representing this kind of data.  With pandas is trivial to group the times of the day in hour intervarls, but I could not find a way to do it with just lists.  My attempts at this task are kept in the comments bellow.
    """


    created_list = list()
    dates_list = list()
    dates_tweets = list()
    datetimex = list()
    x_list = list()
    x = list()
    y = list()

    with open(csv_file) as file_object:
        reader_object = csv.reader(file_object)
        next(reader_object, None)  # Skip headers
        created_list = [i[2] for i in reader_object]
        for i in created_list:
            # this is dt object, not subscriptable
            dates_tweets = datetime.datetime.strptime(i,'%a %b %d %H:%M:%S %z %Y')  # Thu Apr 23 13:38:19 +0000 2009
            # datetime objects
            # Convert into string of dates and times  + GMT
            # dates_tweets = str(dates_tweets_1)
            # Remove +GMT
            # dates_tweets = dates_tweets[:-6]
            # Make a ['date','time'] list.
            # dates_tweets = dates_tweets.split('')
            # Make a tuple ('date', 'time')
            # dates_tweets = tuple(dates_tweets)
            # Adds tuples together in a list [('date', 'time'), ('date', 'time')]
            dates_list.append(dates_tweets)
    # Make test list(100 entries) comment this lines for production
    # jig = list()
    # for x, i in dates_list[3100:3200]:
    #     jig.append(i)
    # dates_list = jig
    # End of test list

    # This sorts the list:
    dates_list = sorted(dates_list)
    dates_list = [(key, len(list(group))) for key, group in groupby(dates_list)]
    # print(dates_list) = (datetime.datetime(2018, 12, 6, 18, 2, 25, tzinfo=datetime.timezone.utc), 6)]


    for i in dates_list:
        x.append(i[0])
    # for i in x:
    #     print(i)
    # for i in x:
    #     i = str(i)
    #     datetime_x = datetime.datetime.strptime(i, '%Y-%m-%d %H:%M:%S%z')
    #     x_list.append(datetime_x)

    dates = mdates.date2num(x)

        # datetime_x = datetime.datetime.strptime(i, '%b %d %Y %I:%M%p')
#    return dates_list
    # for i in dates_list:
    #     x.append(i[1])
    # x = list(range(9))
    # jig = [(len(list(group)), key) for key, group in groupby(jig)]
    # below doesnt work properly
    # x = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(9)]
    # dates_tweets_3 = dates_tweets_2[1100:1200]
#    print(dates_tweets_3)
    # dates_tweets_3 = sorted(dates_tweets_3, reverse=True)
    # dates_tweets_3 = [(len(list(key)), group) for key, group in groupby(dates_tweets_3)]
    # x = mdates.date2num(dates_tweets_3)

    for i in dates_list:
        y.append(i[1])

    fig, ax = plt.subplots(1)
    fig.autofmt_xdate()
    plt.title("Frequency of tweets over time")
    plt.xlabel('Date and Time')
    plt.ylabel('No of tweets')
    plt.plot_date(dates, y)

    # plt.plot(dates, y)
    # xmft = mdates.DateFormatter('%Y-%m-%d %H:%M:%S%z')
    # ax.xaxis.set_major_formatter(xmft)

    # print(x)
    # print(y)
    ui.info_1("Saving...")
    plt.savefig('Q4_Frequency.png')
    plt.show()


def senti(csv_file=CSV_FILE):
    """graph of positive and negative tweets over time (mandatory)
    :param:
    :return:
    """
    polar_pattern = re.compile(r'[-]?\d+\.\d+')
    sentiment_list = list()
    polar_list = list()
    dates_list = list()

    with open(csv_file) as file_object:
        reader_object = csv.reader(file_object)
        next(reader_object, None)  # Skip headers
        sentiment_list = [i[-1] for i in reader_object]  # get sentiment column

    for i in sentiment_list:
        polarity = re.findall(polar_pattern, i)  # Just the numbers
        polarity = polarity[0]                   # Only the polarity part
        polar_list.append(polarity)              # In a list.

    polar_float = [float(i) for i in polar_list]  # Make if float.
    # for i in polar_float:                         # For testing
    #     print(i)
    # print(polar_float)
    with open(csv_file) as file_object:
        reader_object = csv.reader(file_object)
        next(reader_object, None)  # Skip headers
        created_list = [i[2] for i in reader_object]
        for i in created_list:
            # this is dt object, not subscriptable
            dates_tweets_1 = datetime.datetime.strptime(i,'%a %b %d %H:%M:%S %z %Y')
            # Convert into string of dates and times  + GMT
#            dates_tweets = str(dates_tweets_1)
            # Adds tuples together in a list [('date', 'time'), ('date', 'time')]
            dates_list.append(dates_tweets_1)

        try:

            # dates = mdates.date2num(dates_list)
            # yearsFmt = mdates.DateFormatter('%a %b %d %H:%M:%S %z %Y')
            fig, ax = plt.subplots()
            ax.scatter(dates_list, polar_float)
            # print(polar_float)
            plt.title("Sentiment analysis over Time")
            plt.xlabel("Time and Date")
            plt.ylabel("Sentiment Polarity")
            # The following lines does not seem to have any effect
            # ax.format_xdata = mdates.DateFormatter('%a %b %d %H:%M:%S %z %Y')
            # ax.format_ydata = polar_float
            # ax.yaxis.set_major_formatter(FormatStrFormatter('%f'))
            ax.grid(True)       # Cute grid.


            ui.info_1("Saving...")
            plt.savefig("Q4_sentiment.png")
            plt.show()
        except TypeError as e:
            print("TypeError")
            exit()


if __name__ == '__main__':
    db_into_csv()
    print("Saving Databases...")
    frecuency()
    senti()
