# Kokomi - Clan db design

## DB: clans

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

### Table_2: clan_basic

#### Create SQL:
```sql
CREATE TABLE clan_basic (
    clan_id BIGINT NOT NULL,
    region TINYINT NOT NULL,
    clan_tag VARCHAR(25) DEFAULT NULL,
    clan_color INT DEFAULT NULL,
    update_time INT DEFAULT 0,
    PRIMARY KEY (clan_id),
    UNIQUE INDEX idx_region_clan_id (region, clan_id)
);
```