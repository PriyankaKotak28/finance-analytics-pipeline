-- Run this in pgAdmin Query Tool
CREATE DATABASE finance_analytics;

-- Then connect to finance_analytics and run:
CREATE TABLE transactions (
    transaction_id  VARCHAR(20)     PRIMARY KEY,
    account_id      VARCHAR(20)     NOT NULL,
    date            DATE            NOT NULL,
    merchant        VARCHAR(100)    NOT NULL,
    category        VARCHAR(50)     NOT NULL,
    amount          DECIMAL(10,2)   NOT NULL,
    is_anomaly      INT             NOT NULL,
    year            INT,
    month           INT,
    month_name      VARCHAR(20),
    week            INT,
    day_of_week     VARCHAR(20),
    quarter         INT,
    risk_flag       VARCHAR(10)
);