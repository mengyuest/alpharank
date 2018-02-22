drop table if exists Faculty;
create table Faculty (name text,affiliation text,homepage text,scholarid text);
copy Faculty from '/home/meng/webalpha/faculty.txt' CSV HEADER;
