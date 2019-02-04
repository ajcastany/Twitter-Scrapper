
# Twitter Scrapper
-------------------------------------------------------

## Introduction

 Listen to the Twitter API Stream and store in a database tweets containing a keyword.
 `Q4_c1868921` module will plot two graphs: **Frequency over time** and **Sentiment Polarity over Time**.

 **Retweets** (RT) has been removed since 04-12-2018.

    Info stored from tweet:
      - tweet_id
      - tweet_text
      - created_at
      - location
      - coordinates
      - user_followers
      - friends_no
      - sentiment

The following database tables has been provided, populated with search keywords:

    - trump: collected in a short interval, no RT
        - default database
        - keyword trump:
    - old_trump: collected among a few days, includes RT
        - keyword trump:
    - brexit:
        - keyword brexit:
    - deadpool:
        - keyword deadpool:
    - theresa_may:
        - keyword theresa may:

## Usage

When run, the program will show:

```python
:: DEFAULT TABLE FOUND! => 'trump'
:: Add tweets to table 'trump'? (Y/n)
```
If answered 'Yes', or left blank; it will perform the following operations, as required by the assessment specifications:

    1 Create Database if it doesn't exist
    2 Create table `'trump'` if it doesn't exist
    3 Prompt the user for an amount of tweets to fetch (integer)
    4 It will display the default search keyword: `'trump'`
    5 Ask the user to change the default keyword (leave blank for No).
    6 Start fetching tweets containing the keyword.
    7 Ask to create, show and save the plots.
    8 Exit.

If answered 'No' it will display the following menu:

```python
:: Select:
   1 Create New Table
   2 Load table
   3 Plot
   4 Quit
```

Options:

    1 Create New Table: creates new table and fetches tweets with a keyword

    2 Load Table: Add tweets with a keyword to a specific table in database and show plots

    3 Plot: Select a table plot the graphs from *Q4_c1868921* module without adding tweets.

    4 Quit: Terminates the program.

The user can assign *database table names* and *keywords* to search on each database.
The program can generate **Frequency over Time** and **Polarity over Time** graphs on any table.  The frequencies are arranged

The **default keyword** is `trump` and needs to be overridden on each interaction.  This is to prevent writing non-trump data into the assignment table `trump`.

## Known Bugs...

- Some connection errors are not correctly excepted: `urlib3.exceptions.ProtocolError`.

- After recovering from a disconnection the tweet counter `MyStreamListener.tweet_counter` resets to zero. The program will start fetching the total amount, regardless of the number he already added to the database before disconnection.

## Fix

Bellow bugs has been fixed:

    - xticks on the *Sentiment Polarity over Time* graph show integer values instead of floats. My failed attempts are kept in the comments.

    - Previous occurs because there are abnormal values in the list.

I thought table `old_trump` had incorrect sentiment values (5.00+, etc).  But the sentiment analysis actually gave values of 5+.  `old_trump` has data collected along a few days while default `trump` has 10,000 tweets collected in a short interval.

## Tested on...

Linux Mint Tara 19

## Package contains:

    [ ] Cover Sheet
    [ ] Q1_Q2_c1868921.py
    [ ] Q3_c1868921.py: main program
    [ ] Q4_c1868921.py: plot module.  If run on its own it will show and save the plots for table trump.
    [ ] Q3_sqlite_c1868921.sqlite: Database with tables: trump, old_trump, brexit, theresa_may and deadpool.
    [ ] Q4_graphs_c1868921.doc or pdf
    [ ] README.md:
