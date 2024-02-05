
DROP DATABASE IF EXISTS tsubuyaki_db;
CREATE DATABASE tsubuyaki_db;

USE tsubuyaki_db;


create table account (
  account_id INT NOT NULL AUTO_INCREMENT
  , id VARCHAR(10) not null
  , name VARCHAR(10) not null
  , password VARCHAR(256) not null
  , created_at DATETIME default CURRENT_TIMESTAMP not null
  , updated_at DATETIME default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP not null
  , primary key (account_id,id)
);

create table post (
  post_id INT NOT NULL AUTO_INCREMENT
  , account_id INT not null
  , content VARCHAR(50) not null
  , created_at DATETIME default CURRENT_TIMESTAMP not null
  , updated_at DATETIME default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP not null
  , primary key (post_id)
  , FOREIGN KEY (account_id) REFERENCES account (account_id)
);
