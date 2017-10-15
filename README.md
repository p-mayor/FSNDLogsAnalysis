# FSND SQL newsdata logs analysis project

SQL code was generated to analyze a large dataset of news articles.

1. Install VirtualBox - found [here](virtualbox.org)
2. Install Vagrant - found [here](vagrantup.com)
3. Download the VM configuration [here](https://github.com/udacity/fullstack-nanodegree-vm)
4. Download the newsdata.sql file [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
5. Unzip the newsdata.sql file and move it into the VM configurations vagrant directory.
6. Pull the news.py file and move it into the VM configurations vagrant directory.
7. Copy the view code below into the end of newsdata.sql file to create the views used in news.py
8. Navigate to vagrant directory in terminal and run vagrant using vagrant up and then vagrant ssh
9. Change into your vagrant directory with cd /vagrant. 
10. Type psql -d news -f newsdata.sql to load the data.
11. Run news.py by typing python news.py to display the logs analysis.


Create the following views:

```sql
create or replace view hits as
    select path, count(*) as num
    from log
    group by path 
    order by num desc
    limit 9;

create or replace view articlecount as
    select articles.title, hits.num
    from articles join hits
    on hits.path
    like '%' || articles.slug
    order by num desc;

create or replace view hitsauthor as
    select articlecount.num, articles.author
    from articlecount join articles
    on articlecount.title = articles.title
    order by num desc;

create or replace view authorhitsum as
    select hitsauthor.author, sum(hitsauthor.num)
    from hitsauthor
    group by hitsauthor.author
    order by sum desc;

create or replace view authorcount as
    select authors.name, authorhitsum.sum
    from authorhitsum join authors
    on authorhitsum.author = authors.id;

create or replace view errors as
    select to_char(log.time, 'DD Mon YYYY') as day, count(log.status) as err
    from log
    where log.status LIKE '%404%'
    group by day
    order by err desc
    limit 5;

create or replace view requests as
    select to_char(log.time, 'DD Mon YYYY') as day, count(log.status) as hits
    from log
    group by day
    order by hits desc;

create or replace view req_total as
    select errors.day, errors.err, requests.hits
    from errors join requests
    on errors.day = requests.day
    order by err desc;

create or replace view err_percent as
    select day, (100.0 / (hits / err)) as perc from req_total order by perc desc;

create or replace view err_days as
    select * from err_percent where err_percent.perc>1;
```
