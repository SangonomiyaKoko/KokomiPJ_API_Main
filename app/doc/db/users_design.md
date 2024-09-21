# Kokomi - User db design

## DB: users

### Table_1: servers

#### Create SQL:
```sql
CREATE TABLE servers (
    id TINYINT NOT NULL,
    region VARCHAR(10) NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO servers (id, region) VALUES
(1, 'asia'),
(2, 'eu'),
(3, 'na'),
(4, 'ru'),
(5, 'cn');
```

### Table_2: user_basic

#### Create SQL:
```sql
CREATE TABLE user_basic (
    account_id BIGINT(11) UNSIGNED NOT NULL UNIQUE,
    region INT NOT NULL,
    nickname VARCHAR(255) DEFAULT NULL,
    querys INT DEFAULT 0,
    clan_id BIGINT(11) UNSIGNED DEFAULT NULL,
    clan_update_time INT DEFAULT 0,
    PRIMARY KEY (account_id),
    INDEX (account_id)
);
```