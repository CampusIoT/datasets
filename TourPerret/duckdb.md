# Exploring dataset with DuckDB

[DuckDB](https://duckdb.org/) is an in-process SQL OLAP database management systemi. Data can be efficiently loaded from files in CSV, JSON, Parquet formats.

## Install DuckDB

https://duckdb.org/docs/installation/

```bash
brew install duckdb
# for transient DB
duckdb
# for persistent DB (~275 MB on disk)
duckdb tourperret.duckdb
```

## Prepare subfiles

```bash
gunzip -c tourperret.log.gz | grep -E 'ELSYS_EMS|51c7ba4f796a50a3352d318d1e8ff26d' |  gzip -c > elsys_ems.ndjson.gz
gunzip -c tourperret.log.gz | grep WYRES_BASE | gzip -c > wyres_base.ndjson.gz
```
## Query

```sql
create table frames as
   select * from read_json_auto('tourperret.log.gz', ignore_errors=true);
select applicationName, devEUI, count(*)  from frames group by applicationName, devEUI;
-- fix applicationName
update frames
   set applicationName='ELSYS_EMS'
   where applicationName='51c7ba4f796a50a3352d318d1e8ff26d';
describe frames;

select distinct(devEUI) from frames;

select devEUI, count(*) from frames group by devEUI;

select applicationName, count(*)  from frames group by applicationName;

select devEUI, _timestamp, object from frames where applicationName='ELSYS_EMS';

select devEUI, _timestamp, object.dewpoint, object.temperature, object.humidity
from frames where applicationName='ELSYS_EMS';
```

Import Elsys EMS data
```sql
create table elsys as
   select devEUI, _timestamp, _date, object
   from read_json_auto('elsys_ems.ndjson.gz', ignore_errors=true);
describe elsys;

select devEUI, avg(object.temperature), avg(object.dewpoint), avg(object.humidity),
         avg(object.accMotion), avg(object.vdd)
from elsys group by devEUI;

COPY elsys TO 'elsys.parquet' (FORMAT PARQUET);
COPY elsys TO 'elsys.csv' (FORMAT CSV);
```

Import Wyres Base data
```sql
create table wyres as
   select devEUI, _timestamp, _date, object
   from read_json_auto('wyres_base.ndjson.gz', ignore_errors=true);
describe wyres;

select devEUI, avg(object.temperature), avg(object.pressure), avg(object.light)
from wyres group by devEUI;

COPY wyres TO 'wyres.parquet' (FORMAT PARQUET);
COPY wyres TO 'wyres.csv' (FORMAT CSV);
```

```sql
.quit
```


## Explore with SQL editors

https://duckdb.org/docs/guides/sql_editors/harlequin

```bash
pip install harlequin
harlequin
```

## Jupyter Notebook

https://duckdb.org/docs/guides/python/jupyter.html
