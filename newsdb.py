# encoding: utf-8
# Database code for the DB news -Log Analysis Assignment.

import psycopg2

DBNAME = "news"
# FIRST QUESTION
db = psycopg2.connect(database=DBNAME)
c = db.cursor()
c.execute(
    "select title, count(articles.id) as num from log left join articles on substring(path,10,88)=slug inner join "
    "authors on authors.id=articles.author group by title,"
    "status  having status='200 OK' order by num desc limit 3")
posts = c.fetchall()
# And let's loop over it too:
print("\n1. Quais são os três artigos mais populares de todos os tempos?")
print("Titles and views:")
for post in posts:
    print("  {}---------{} views".format(post[0], post[1]))
db.close()

# SECOND QUESTION
db = psycopg2.connect(database=DBNAME)
c = db.cursor()
c.execute(
    "select authors.name, count(articles.id) as num from log left join articles on substring(path,10,88)=slug inner "
    "join authors on authors.id=articles.author group by status,authors.name  having status='200 OK' order by num desc")
posts = c.fetchall()
# And let's loop over it too:
print("\n2. Quem são os autores de artigos mais populares de todos os tempos?")
print("Author's name and views:")
for post in posts:
    print("  {} --------- {} views".format(post[0], post[1]))
db.close()


# THIRD QUESTION


db = psycopg2.connect(database=DBNAME)
c = db.cursor()
c.execute(
    "select days, success, failures,to_char(cast(failures as decimal)/(success+failures)*100,'0.99%') as "
    "errors from (select to_char(s.time,'DD Mon YYYY') as days,s.status,count(s.id) as success from log "
    "as s  group by days,s.status) as s,(select to_char(f.time,'DD Mon YYYY') as dayf,f.status,count(f.id) "
    "as failures from log as f group by dayf, f.status) as f where days=dayf and success>failures")
posts = c.fetchall()
# And let's loop over it too:
print("\n3. Em quais dias mais de 1% das requisições resultaram em erros?")
print("Date and status views:")
print("     DATE       VIEWS   ERRORS          %ERRORS")
for post in posts:
    # colorize only the rows wich percentage of errors is greater than 1%
    if float(post[3][1:3]) > 1:
        print('\033[0;32;41m {}     {}    {}-----------{}\033[m'.format(post[0], post[1], post[2], post[3]))
    else:
        print(" {}     {}    {}-----------{}".format(post[0], post[1], post[2], post[3]))
db.close()


db = psycopg2.connect(database=DBNAME)
c = db.cursor()
c.execute(
    "select days, success, failures,to_char(cast(failures as decimal)/(success+failures)*100,'0.99%') as errors from "
    "(select to_char(s.time,'DD Mon YYYY') as days,s.status,count(s.id) as success from log as s  group "
    "by days,s.status) as s,(select to_char(f.time,'DD Mon YYYY') as dayf,f.status,count(f.id) "
    "as failures from log as f group by dayf,f.status) as f where days=dayf and success>failures "
    "and cast(failures as decimal)/(success+failures)>0.01;")
posts = c.fetchall()
# And let's loop over it too:
print("\n****Dia(s) com falha maior que 1%:")
for post in posts:
    print('\033[0;32;41m {}---------{} Erros \033[m'.format(post[0], post[3]))
db.close()
