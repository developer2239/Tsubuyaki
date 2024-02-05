
-- DB作成

DROP DATABASE IF EXISTS tsubuyaki_db;
CREATE DATABASE tsubuyaki_db;

USE tsubuyaki_db;

--------------------------------------------------------------------------------
-- account のレイアウト変更
--   注意！！：テーブルに依存するオブジェクト（ビューなど）が削除される場合があります。それらのオブジェクトは復元されません。
--   2024/02/01 0901JP
--------------------------------------------------------------------------------

-- accountテーブルの作成
create table account (
  account_id INT not null
  , id VARCHAR(10) not null
  , name VARCHAR(10) not null
  , password VARCHAR(255) not null
  , created_at DATETIME default CURRENT_TIMESTAMP not null
  , updated_at DATETIME default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP not null
  , primary key (account_id,id)
);


--------------------------------------------------------------------------------
-- post のレイアウト変更
--   注意！！：テーブルに依存するオブジェクト（ビューなど）が削除される場合があります。それらのオブジェクトは復元されません。
--   2024/02/01 0901JP
--------------------------------------------------------------------------------

-- postテーブルの作成
create table post (
  post_id INT not null
  , account_id INT not null
  , content VARCHAR(50) not null
  , created_at DATETIME default CURRENT_TIMESTAMP not null
  , updated_at DATETIME default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP not null
  , primary key (post_id)
);
/
