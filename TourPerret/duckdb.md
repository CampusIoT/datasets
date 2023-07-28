# Exploring dataset with DuckDB

## Install DuckDB

```bash
brew install duckdb
duckdb
```

## Query

```sql
create table frames as
   select * from read_json_auto('tourperret.log.gz', ignore_errors=true);

select applicationName, devEUI, count(*)  from frames group by applicationName, devEUI;

update frames set applicationName='ELSYS_EMS' where applicationName='51c7ba4f796a50a3352d318d1e8ff26d';

create table elsys as
   select * from read_json_auto('tourperret.log.gz', ignore_errors=true)
   where applicationName='ELSYS_EMS';

create table wyres as
   select * from read_json_auto('tourperret.log.gz', ignore_errors=true)
   where applicationName='WYRES_BASE';

describe frames;

select distinct(devEUI) from frames;

select devEUI, count(*)  from frames group by devEUI;

select applicationName, count(*)  from frames group by applicationName;

select devEUI, _timestamp, object  from frames where applicationName='ELSYS_EMS';

select devEUI, _timestamp, object.dewpoint, object.temperature, object.humidity  from frames where applicationName='ELSYS_EMS';

select devEUI, avg(object.temperature), avg(object.dewpoint), avg(object.humidity)  from frames where applicationName='ELSYS_EMS' group by devEUI;

select devEUI, avg(object.temperature), avg(object.pressure), avg(object.light) from frames where applicationName='WYRES_BASE' group by devEUI;

```

## Jupyter Notebook

https://duckdb.org/docs/guides/python/jupyter.html
