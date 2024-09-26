# Kokomi - RootAPI Docs

### Functions: used by administrators to manage interface users and view interface call data

### Permissions: root

| No.  | Methods | Prefix  | URL                         | Description                                       | Links        |
| ---- | ------- | ------- | --------------------------- | ------------------------------------------------- | ------------ |
| 1    | GET     | `/elec` | `/user-stats`               | Get a list of all API users                       | [Here](#api-1-get-api-users) |

## API-1: Get API users

### Request method

- Methods: `GET`
- Full URL: `/root/api-users`


### Request parameters
#### 1. **Headers**
| Parameter name  | Type     | Required | Description                                                         |
|-----------------|----------|----------|---------------------------------------------------------------------|
| `Content-Type`  | `string` | ❌      | Request content type, fixed to `application/json`                   |
| `Authorization` | `string` | ✅      | Token authentication is required, the format is `Bearer {token}`    |

#### 2. **Params**

None

#### 3. **Body**
 
None

### Request example

```
curl -X 'GET' \
  'http://{host}:{port}/root/api-users' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer {your_token}'
```

### Response