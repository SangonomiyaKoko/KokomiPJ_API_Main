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
    account_id BIGINT NOT NULL,
    region TINYINT NOT NULL,
    nickname VARCHAR(255) DEFAULT NULL,
    querys INT DEFAULT 0,
    clan_id BIGINT DEFAULT NULL,
    clan_update_time INT DEFAULT 0,
    cache_update_time INT DEFAULT 0,
    PRIMARY KEY (account_id),
    UNIQUE INDEX idx_region_account_id (region, account_id) -- Add region + account_id composite unique index
);
```

### Table_2: user_info

#### Create SQL:
```sql
CREATE TABLE user_info (
    account_id BIGINT NOT NULL,
    region TINYINT NOT NULL,
    update_time INT DEFAULT 0,
    profite TINYINT NOT NULL DEFAULT 0,
    leveling_points INT NOT NULL DEFAULT 0,
    last_battle_time INT NOT NULL DEFAULT 0,
    PRIMARY KEY (account_id),
    UNIQUE INDEX idx_region_account_id (region, account_id)
);
```