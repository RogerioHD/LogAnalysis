# $ python newsdb.py
# encoding: utf-8
# Database code for the DB news -Log Analysis Assignment.

import psycopg2

DBNAME = "news"


def connect(database_name):
    """
       Connect to the PostgreSQL database.  Returns a database connection.
       Use this like so:
       db, cursor = connect(DBNAME)
    """
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor

    except psycopg2.Error as err:
        print ("Unable to connect to database")
        print (err)
        sys.exit(1)      # The easier method - exit the program

# FIRST QUESTION QUERY


query_1 = """
SELECT title,
       count(articles.id) AS num
FROM log
LEFT JOIN articles ON substring(PATH, 10, 88)=slug
INNER JOIN authors ON authors.id=articles.author
GROUP BY title,
         status
HAVING status='200 OK'
ORDER BY num DESC
LIMIT 3;
"""

# SECOND QUESTION QUERY

query_2 = """
SELECT authors.name,
       count(articles.id) AS num
FROM log
LEFT JOIN articles ON substring(PATH, 10, 88)=slug INNER
JOIN authors ON authors.id=articles.author
GROUP BY status,
         authors.name
HAVING status='200 OK'
ORDER BY num DESC;
"""

# THIRD QUESTION GENERAL QUERY

query_3 = """
SELECT days,
       success,
       failures,
       to_char(cast(failures AS decimal)/(success+failures)*100, '0.99%')
       AS errors
FROM
  (SELECT to_char(s.time, 'DD Mon YYYY') AS days,
          s.status,
          count(s.id) AS success
   FROM log AS s
   GROUP BY days,
            s.status) AS s,
  (SELECT to_char(f.time, 'DD Mon YYYY' ) AS dayf,
          f.status,
          count(f.id) AS failures
   FROM log AS f
   GROUP BY dayf,
            f.status) AS f
WHERE days=dayf
  AND success>failures;
"""

# THIRD QUESTION SPECIFIC QUERY


query_3_plus = """
SELECT days,
       success,
       failures,
       to_char(cast(failures AS decimal)/(success+failures)*100, '0.99%')
       AS errors
FROM
  (SELECT to_char(s.time, 'DD Mon YYYY') AS days,
          s.status,
          count(s.id) AS success
   FROM log AS s
   GROUP BY days,
            s.status) AS s,
  (SELECT to_char(f.time, 'DD Mon YYYY') AS dayf,
          f.status,
          count(f.id) AS failures
   FROM log AS f
   GROUP BY dayf,
            f.status) AS f
WHERE days=dayf
  AND success>failures
  AND cast(failures AS decimal)/(success+failures)>0.01
"""


def answer1():
    """Answer the first question ..."""
    print("Question 1:What are the most popular three articles of all time?\n")
    cursor.execute(query_1)
    posts = cursor.fetchall()
    print("Titles and views:")
    # And let's loop over it too:
    for post in posts:
        print("  {}---------{} views".format(post[0], post[1]))


def answer2():
    """Answer second question ..."""
    print("Question 2:Who are the most popular article authors of all time?\n")
    cursor.execute(query_2)

    print("Author's name and views:")
    # And let's loop over it too:
    for post in posts:
        print("  {} --------- {} views".format(post[0], post[1]))


def answer3():
    """Answer the third first question ..."""
    print("Question 3:Which days had more than 1% of requests errors?\n")
    cursor.execute(query_3)
    posts = cursor.fetchall()
    print("Date and status views:")
    print("     DATE       VIEWS   ERRORS          %ERRORS")
    for post in posts:
        # colorize only the rows wich percentage of errors is greater than 1%
        if float(post[3][1:3]) > 1:
            print('\033[0;32;41m {}     {}    {}-----------'
                  '{}\033[m'.format(post[0], post[1], post[2], post[3]))
        else:
            print(" {}     {}    {}-----------"
                  "{}".format(post[0], post[1], post[2], post[3]))


def answer3plus():
    cursor.execute(query_3_plus)
    posts = cursor.fetchall()
    print("\n****Day (s) with failure rate greater than 1%:")
    # And let's loop over it too:
    for post in posts:
        print('\033[0;32;41m {}-----{} Erros \033[m'.format(post[0], post[3]))


def run():
    """Running report ..."""
    print("Running reporting tools...\n")
    answer1()
    print("\n")

    answer2()
    print("\n")

    answer3()
    print("\n")

    answer3plus()
    print("\n")

    db.close()


db, cursor = connect(DBNAME)
run()

