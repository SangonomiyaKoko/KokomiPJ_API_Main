# Kokomi - Cache db design

## DB: caches

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

### Table_2: ship_{sid}

#### Create SQL:
```sql
CREATE TABLE ship_sid (
    account_id BIGINT NOT NULL,
    region TINYINT NOT NULL,
    update_time INT DEFAULT 0,
    battles_count INT NULL,
    wins INT NULL,
    damage_dealt BIGINT NULL,
    frags INT NULL,
    exp BIGINT NULL,
    survived INT NULL,
    scouting_damage BIGINT NULL,
    art_agro BIGINT NULL,
    planes_killed INT NULL,
    max_exp INT NULL,
    max_damage_dealt INT NULL,
    max_frags INT NULL,
    PRIMARY KEY (account_id),
    UNIQUE INDEX idx_region_account_id (region, account_id)
);
```