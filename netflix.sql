create table movies (
id int auto_increment primary key,
title varchar(255) not null,
release_year int not null,
genre varchar(100),
director varchar(255),
duration_minutes int,
rating decimal(3,1) default null,--πεδιο τυπου decimal με συνολικα 3 ψηφια και 1 δεκαδικο
image_path varchar(255)
);

create table actors (
id int auto_increment primary key,
name varchar(255) not null,
birth_date date,
nationality varchar(100)
);

--χρησιμοποιειται για τη συνδεση ταινιων με ηθοποιους
create table movies_actors (
id int auto_increment primary key,
movie_id int not null,
actor_id int not null,
role varchar(255),
foreign key (movie_id) references movies(id),--διασφαλιζουν οτι καθε εγγραφη στον πινακα movie_actor αναφερεται σε υπαρχουσα εγγραφη στον πινακα movies και actors
foreign key (actor_id) references actors(id)
);

create table reviews (
id int auto_increment primary key,
movie_id int not null,
reviewer_name varchar(255),
review_text text,
rating decimal(3, 1),
review_date date default current_date,
foreign key (movie_id) references movies(id)
);

create table users (
id int auto_increment primary key,
username varchar(255) unique not null,
email varchar(255) unique not null,
password_hash varchar(255) not null,
role ENUM('admin','customer') DEFAULT 'customer', --το ENUM περιοριζει τις επιτρεπομενες τιμες στα admin και customer
signup_date date default current_date
);

create table watchlist (
id int auto_increment primary key,
user_id int not null,
movie_id int not null,
added_date date default current_date,
foreign key (user_id) references users(id),
foreign key (movie_id) references movies(id)
);