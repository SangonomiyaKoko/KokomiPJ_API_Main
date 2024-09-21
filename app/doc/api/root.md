# Kokomi - RootAPI Docs

### Functions: used by administrators to manage interface users and view interface call data

### Permissions: root

| No.  | Methods | Prefix  | URL                         | Description                                       | Links        |
| ---- | ------- | ------- | --------------------------- | ------------------------------------------------- | ------------ |
| 1    | GET     | `/root` | `/api-users`                | Get a list of all API users                       | [Here](#api-1-get-api-users) |
| 2    | POST    | `/root` | `/api-users`                | Create a new api user                             | [Here](#...) |
| 3    | DELETE  | `/root` | `/api-users/{username}`     | Delete the API user with the specified username   | [Here](#...) |

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