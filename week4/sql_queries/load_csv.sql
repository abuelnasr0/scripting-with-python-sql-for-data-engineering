LOAD DATA LOCAL INFILE '/home/mohamed/Mohamed/projects/scripting-with-python-sql-for-data-engineering/week4/sql_queries/ratings.csv' INTO TABLE ratings
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'  
(@name,@grape,@region,@variety,@rating,@notes) set name=@name,rating=@rating,region=@region;

-- TO Enable writing from local file in the server
-- this command in mysql shell in the docker image
-- SET GLOBAL local_infile=1;

-- If you connect manually (not using vscode extension) write this command
-- mysql --local-infile=1 -u root -p
