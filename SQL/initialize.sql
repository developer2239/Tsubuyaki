
DROP DATABASE IF EXISTS tsubuyaki_db;
CREATE DATABASE tsubuyaki_db;

USE tsubuyaki_db;


create table account (
  account_id INT NOT NULL AUTO_INCREMENT
  , id VARCHAR(10) not null UNIQUE
  , name VARCHAR(10) not null
  , password VARCHAR(256) not null
  , profile VARCHAR(50)
  , created_at DATETIME default CURRENT_TIMESTAMP not null
  , updated_at DATETIME default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP not null
  , primary key (account_id)
);

create table post (
  post_id INT NOT NULL AUTO_INCREMENT
  , account_id INT not null
  , content VARCHAR(50) not null
  , created_at DATETIME default CURRENT_TIMESTAMP not null
  , updated_at DATETIME default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP not null
  , primary key (post_id)
  , FOREIGN KEY (account_id) REFERENCES account (account_id) ON DELETE CASCADE
);

create table follow (
  follow_id INT NOT NULL AUTO_INCREMENT
  ,account_id INT NOT NULL
  , follow_account_id INT NOT NULL
  , created_at DATETIME default CURRENT_TIMESTAMP not null
  , primary key (follow_id)
  , FOREIGN KEY (account_id) REFERENCES account (account_id) ON DELETE CASCADE
  , FOREIGN KEY (follow_account_id) REFERENCES account (account_id) ON DELETE CASCADE
);

create table favorite (
  favorite_id INT NOT NULL AUTO_INCREMENT
  ,post_id INT NOT NULL 
  , account_id INT NOT NULL
  , created_at DATETIME default CURRENT_TIMESTAMP not null
  , primary key (favorite_id)
  , FOREIGN KEY (post_id) REFERENCES post (post_id) ON DELETE CASCADE
  , FOREIGN KEY (account_id) REFERENCES account (account_id) ON DELETE CASCADE
);

create table post_favorites (
  id INT not null UNIQUE
  , post_id INT 
  , favorite_id INT
  , primary key (id)
);