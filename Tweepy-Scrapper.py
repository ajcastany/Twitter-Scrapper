#!/usr/bin/env python3
"""=============================================================================
                       Q U E S T I O N  -  T H R E E
================================================================================

                              IMPORTS
****************************************************************************"""
import sqlite3
import tweepy
import json
import os
from textblob import TextBlob
try:
    import ui
except ModuleNotFoundError as e:
    print("Please install python-cli-ui package: pip install python-cli-ui")
    print("Program terminated")
    exit()
try:
    import graph_module as q_four
except ModuleNotFoundError as e:
    ui.warning("graph-module.py not found!")


"""=============================================================================
                    S E C U R I T Y  -  T O K E N S
===============================================================================
The following code was taken from a story created by Lucas Kohorst on freecodecamp.org on 8th-April-unknown.  Accessed on 15-Nov-2018: https://medium.freecodecamp.org/creating-a-twitter-bot-in-python-with-tweepy-ac524157a607.  It also appears on tweepy documentation by Joshua Roesslein, 2009, accessed on 21-Nov-2018: http://docs.tweepy.org/en/v3.5.0/getting_started.html
****************************************************************************"""

consumer_key = 'fj5RNQTL1p9XHaYysf5uYj2NP'
consumer_secret = 'XHeDxpDX7GbBe435NmsNukDMAKcSGT1uxyMrEUbTJE85QUZ2lN'
access_token = '52681286-TMzzPMOyS8k8QOKtAawolyKWn1gWi3OWXbUrQHjXF'
access_token_secret = 'k77qveVFaTbrXcpyyGEcZASlYNRTOVwDb8Rqho2qCNU3Y'

"""============================================================================
                    G L O B A L  -  C O N S T A N T S
============================================================================"""

TWEETS_DB = "tweets.sqlite"
CSV_FILE = 'tweets.csv'
TABLE_NAME = "trump"

"""============================================================================
                          V A R I A B L E S
============================================================================"""

tweet_id = "Tweets_ID"
tweet_text = "Tweet_Text"
created_at = "Created_At"
locaton = "Location"
coordinates = "Geo-coordinates"
user_followers = "User_followers"
friends_no = "Number_of_Friends"
senti = "Sentiment_Analysis"

"""============================================================================
             F U N C T I O N  -  D E F I N I T I O N S
============================================================================"""


def create_conection(db_file=TWEETS_DB):
    """Connects to the database.
    :param db_file: database file, default tweets_db
    :return conn: returns connection object

    This code was taken from SQLite Tutorial, http://www.sqlitetutorial.net/sqlite-python/creating-database/ (2018) accessed on 22-Nov-2018
    """

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except :
        ui.error()
    return None


def create_table(conn, create_table_sql):
    """Creates a new table from create_table_sql
    :param conn: connection to database object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    This code was take from SQLite Tutorial,
    http://www.sqlitetutorial.net/sqlite-python/create-tables/ (2018), accessed on 22-Nov-2018
    The except Error field was changed to OperationalError instead.
    """

    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        ui.error(e)
        ui.error("Illegal name" )
        ui.info(ui.bold, "Program Finished")
        exit()


def number_rows(conn=create_conection(), db_file=TWEETS_DB, table_name=TABLE_NAME):
    """Shows number of rows in Database
    :param conn:
    :param db_file:
    :param table_name:
    """
    cur = conn.cursor()
    select_all = """SELECT COUNT(*) FROM {tn}""".format(tn=table_name)
    count = cur.execute(select_all)
    count_value = count.fetchone()
    count_value = str(count_value).strip('(').strip(')').strip(',')
    ui.info(ui.green, "{} rows in {}".format(count_value, db_file))



def tweets_table_create(conn=create_conection(), sql_file=TWEETS_DB, table_name=TABLE_NAME):
    """Create tweets table.
    :param:
    :return:
    This code was take from SQLite Tutorial,
    http://www.sqlitetutorial.net/sqlite-python/create-tables/ (2018), accessed on 22-Nov-2018
    It was modified to have {tn} instead of the table name, and added ui interface.
    """

    tweet_id = "tweets_id"
    tweet_text = "tweet_text"
    created_at = "created_at"
    location = "location"
    coordinates = "geocoordinates"
    user_followers = "user_followers"
    friends_no = "number_of_friends"
    senti = "sentiment_analysis"

    create_tweets_database = """CREATE TABLE IF NOT EXISTS {tn} (
    {ti} interger NOT NULL,
    {tt} text NOT NULL,
    {ct} text NOT NULL,
    {loc} text,
    {coor} text,
    {uf} interger,
    {fn} interger,
    {sn} text)""".format(tn=table_name, ti=tweet_id, tt=tweet_text, ct=created_at, loc=location, coor=coordinates, uf=user_followers, fn=friends_no, sn=senti)

    if conn is not None:
        create_table(conn, create_tweets_database)
        ui.info_1("New table created:", ui.blue, table_name)
    else:
        ui.error("Cannot create connection to DATABASE")

def insert_tweet(tweet, table_name=TABLE_NAME):
    """Insert a new tweet on the database
    :param conn: create connection.

        This code was take from SQLite Tutorial,
    http://www.sqlitetutorial.net/sqlite-python/create-tables/ (2018), accessed on 22-Nov-2018
    It was modified to have {tn} instead of the table name.
    """
    tweet_id = "tweets_id"
    tweet_text = "tweet_text"
    created_at = "created_at"
    location = "location"
    coordinates = "geocoordinates"
    user_followers = "user_followers"
    friends_no = "number_of_friends"
    senti = "sentiment_analysis"

    conn = create_conection()

    insert_db = """INSERT INTO {tn} (
    {ti},
    {tt},
    {ct},
    {loc},
    {coor},
    {uf},
    {fn},
    {sn})
    VALUES(?,?,?,?,?,?,?,?)""".format(tn=table_name, ti=tweet_id, tt=tweet_text, ct=created_at, loc=location, coor=coordinates, uf=user_followers, fn=friends_no, sn=senti)
    cur = conn.cursor()
    cur.execute(insert_db, tweet)
    conn.commit()
    cur.close()
    # Bellow is no longer used
    # ui.info_progress("Now gathering tweet #", cur.lastrowid, MyStreamListener.tweet_stop)
    # print("Now fetching tweet #{}".format(cur.lastrowid))
    # return cur.lastrowid


def count_rows(table_name=TABLE_NAME):
    conn = create_conection()
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM {tn}".format(tn=table_name))  # Shows current table
    count_row = cur.fetchone()
    conn.close()                # conn is context-managed, close() is not needed
    return count_row


"""=============================================================================
                              Tweepy starts here
============================================================================="""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):
    """Streamer
    I got this from http://docs.tweepy.org/en/v3.5.0/streaming_how_to.html by Joshua Roesslein (2009), accessed on 22-Nov-2018
"""
    tweet_counter = 0
    tweet_stop = 10
    table_name = 'trump'

    def on_status(self, status):
        pass
        # print(status.text)


    def on_data(self,data):

        tweet_data = json.loads(data)
        if not tweet_data['text'].startswith('RT'):
            user_data = tweet_data["user"]
            # print(tweet_data)
            tweets_id = (tweet_data["id"])
            tweet_checker = lambda x: (x["extended_tweet"]["full_text"]) if "extended_tweet" in x else x["text"]
            tweet_string = tweet_checker(tweet_data)
            tweet_text = str(tweet_string)
            created_at = (tweet_data["created_at"])
            location = (user_data["location"])
            coordinates = (tweet_data["coordinates"])
            user_followers = (user_data["followers_count"])
            friends_no = (user_data["friends_count"])
            senti = str(TextBlob(tweet_text).sentiment)

            tweet = tweets_id, tweet_text, created_at, location, coordinates, user_followers, friends_no, senti
            if self.tweet_counter >= self.tweet_stop:
                ui.info_2(ui.blue, "{} Tweets added!".format(self.tweet_stop), ui.check)
                number_rows()
    #            print("Done! {} tweets added!".format(self.tweet_counter))
                return False
            else:
                # Locks the db while fetching...
                # //TODO: queue of list of tweets so the db does not remain locked while fetch_tweets()
                insert_tweet(tweet, self.table_name)
                self.tweet_counter += 1

            ui.info_progress("Fetching...",self.tweet_counter, self.tweet_stop)


    def on_error(self, status_code):
        if status_code == 420:
            ui.error("Calm down! Error code:", status_code)
            return False
        else:
            ui.error(status_code)
            return True


def fetch_tweets():
    """This will start collection and will store them in the database.

    //DONE: Ask the user to change filter keyword value.
    //TODO bug: counter resets on disconnection so it starts gathering x tweets
    on top of whatever it gathered before.
     """
    try:
        trump = change_filter()     # A variable named trump
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.filter(track=[trump])
        myStream.disconnect()
    except sqlite3.InterfaceError as e:
        ui.info_3(e)
        ui.error("Connection timeout... Reconnecting...")
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.filter(track=[trump])
        myStream.disconnect()
    except urlib3.exceptions.ProtocolError as e:
        ui.info_3(e)
        ui.error("Connection broken... Reconnecting...")
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.filter(track=[trump])
        myStream.disconnect()

"""=============================================================================
                         U S E R  -  I N T E R F A C E
============================================================================="""


def user_ans_tweets(table_name=TABLE_NAME):
    """Asks user how many tweets to append to table, and does so.
    :param table_name: name of table
    """
    ui.info_1(ui.bold, "Add Tweets to", ui.blue, MyStreamListener.table_name)
    ans_int = input("   How many tweets? (interger) >>> ")
    MyStreamListener.tweet_stop = 0
    try:
        ans_int = int(ans_int)
        if ans_int > 0:
            MyStreamListener.tweet_stop = ans_int
            fetch_tweets()
        else:
            print("0 tweets gathered")
            return
    except ValueError:
        ui.info_1(ui.red, "Please write an interger")
        user_ans_tweets()
    except ConnectionError:
        ui.error(ui.cross, "Connection Error")
        ui.info(ui.bold, "Program Finished")
        exit()

def change_filter():
    """Changes the search filter for myStream.filter(track=[trump])
    :param:
    :return trump: New keyword or DEFAULT keyword 'trump'"""
    trump = 'trump'             # A variable named trump.
    ui.info_1(ui.yellow, "SEARCH:", ui.blue, ui.standout, "'trump'")
    ans_filter = ui.ask_yes_no("Change search keyword? [Ctrl-C Quits] >>>", default=False)
    if ans_filter == False:
        return trump
    else:
        ui.info_1(ui.red, "Really change?")
        ans_really = ui.ask_yes_no("[ENTER] for No >>>", default=False)
        if ans_really == False:
            return trump
        else:
            trump = ui.ask_string("Enter new search keyword")
            ui.info_3("Starting search for new keyword:", ui.blue, trump)
            return trump


def ask_database(db_file=TWEETS_DB, conn=create_conection()):
    pass


def ask_table(db_file=TWEETS_DB, conn=create_conection(), table_name=TABLE_NAME):
    """Default table or new table.  Checks if table exists,
    creates one if not with name from user and calls user_ans_tweets().
    :param db_file: DEFAULT database
    :param conn: creates connection()
    :param table_name: name of table
    """
    def ploting(tweets_db=TWEETS_DB, csv_file=CSV_FILE):
        table_name = MyStreamListener.table_name
        plot_question = ui.ask_yes_no("Plot?", default=True)
        if plot_question:
            ui.info(ui.green, "Populating csv file with {}".format(table_name))
            q_four.db_into_csv(TWEETS_DB, CSV_FILE, table_name)
            ui.info_3("Ploting...")
            q_four.frecuency()
            q_four.senti()
        else:
            ui.info(ui.turquoise, "Program Finished")
            exit()

    tables_list = list()
    conn = create_conection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master")
    for table in cur:
        tables = str(table).strip('(').strip(')').strip(',').strip("'")
        tables_list.append(tables)
    if "trump" in tables_list:
        ui.info_1(ui.yellow, ui.bold, "DEFAULT TABLE FOUND! =>", ui.blue, ui.standout, "'trump'")
        new_db_ans = ui.ask_yes_no("Add tweets to table 'trump'?", default=True)
        if new_db_ans:
            ui.warning("Creating database (If it doesn't exist)")
            create_conection()
            ui.info_2(ui.green, "Accessing Database")
            MyStreamListener.table_name = TABLE_NAME
            user_ans_tweets()
            ploting()
        else:
            choices = ["Create New Table", "Load table", "Plot", "Quit"]
            new = ui.ask_choice("Select: ", choices)
            if new == "Create New Table":
                ui.warning("Tables with the same name will not be created")
                new_table_name = ui.ask_string("Enter new table name:")
                new_table_name = new_table_name.lower()
                new_table_name = new_table_name.replace(" ", "_")
                ui.info("Table name with format:", ui.blue, new_table_name)
                create_ans =  ui.ask_yes_no("Create?")
                if create_ans:
                    tweets_table_create(create_conection(), TWEETS_DB, new_table_name)
                    insert_new_tbl = ui.ask_yes_no("Insert new tweets into {}?".format(new_table_name))
                    if insert_new_tbl:
                        MyStreamListener.table_name = new_table_name
                        user_ans_tweets()
                        ploting()
                    else:
                        ui.info(ui.bold, ("Program Finished"))
                else:
                    ui.info(ui.bols, "Program Finished")
            elif new == "Load table":
                new_table_name = ui.ask_choice("Select Table to load:", tables_list)
                MyStreamListener.table_name = new_table_name
                user_ans_tweets()
                ploting()

            elif new == "Plot":
                new_table_name = ui.ask_choice("Select Table to plot:", tables_list)
                MyStreamListener.table_name = new_table_name
                ploting()


            elif new == "Quit":
                ui.warning("Program Finished")
                exit()

if __name__ == '__main__':
    tweets_table_create()
    ui.info
    try:
        ask_table()
    except KeyboardInterrupt as e:
        ui.info(ui.teal, "Program Finished")
        exit()
    except EOFError as e:
        ui.info(ui.turquoise, "Program Finished")
        exit()

#_EOF_
