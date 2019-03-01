CREATE DATABASE proxypool;

USE proxypool;

CREATE TABLE proxyip (
  ip_id int  NOT NULL  AUTO_INCREMENT,
  ip_str varchar(32) NOT NULL,
  ip_in_time DATETIME,
  PRIMARY KEY(ip_id)
) ENGINE=InnoDB;
