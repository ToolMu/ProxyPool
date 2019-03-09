CREATE DATABASE proxypool;

USE proxypool;

CREATE TABLE proxyip (
  ip_id int  NOT NULL  AUTO_INCREMENT,
  ip_str varchar(32) NOT NULL,
  ip_channel varchar(32) NOT NULL,
  ip_in_time varchar(64),
  PRIMARY KEY(ip_id)
) ENGINE=InnoDB;
