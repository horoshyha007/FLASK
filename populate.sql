delete from entries;

insert into entries(date, title, content) values (now() - interval '10 days', 'First post!', 'This is my first post.  It is exciting!');
insert into entries(date, title, content) values (now() - interval '1 day', 'I love Flask', 'I am finding Flask incredibly fun.');
insert into entries(title, content) values ('Databases', 'My databases class is a lot of work, but I am enjoying it.');
insert into entries(title, content) values ('Databases MY', 'This is flask app was written by Katya Khoroshykh SAD-21');


