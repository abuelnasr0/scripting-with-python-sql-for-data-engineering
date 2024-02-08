USE ratings;
(SELECT 'name', 'rating', 'region' FROM ratings)
UNION
SELECT * FROM ratings
INTO OUTFILE '/var/lib/mysql-files/table.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'


-- to get the pass that allow writing files inside the docker container
-- run this in the mysql shell
-- SHOW VARIABLES LIKE "secure_file_priv";