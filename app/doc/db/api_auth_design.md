# Kokomi - API db design

## DB: auth_db

### Table1: api_users

#### Create SQL:
```sql
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password CHAR(64) NOT NULL,
    role VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);
```

	