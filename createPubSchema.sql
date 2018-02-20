drop table if exists PubSchema;
create table PubSchema (key text, title text, author text, conf text, journal text, year text, url text);
copy PubSchema from '/home/meng/webalpha/pubSchema.txt' with delimiter E'\t';
