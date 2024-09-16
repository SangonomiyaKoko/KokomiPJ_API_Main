# API Documentation Specification

## RootInterface-1: Server Status

### Example: `/root/status`
> View the server interface status.

### Request method
```
get /root/status
```

### Request parameters
#### 1. **Headers**
| Parameter name | Type | Required | Description |
|--------------|--------|------|-------------------|
| `Content-Type` | `string` | Yes | Request content type, fixed to `application/json` |
| `Authorization` | `string` | No | If Token authentication is required, the format is `Bearer {token}` |

#### 2. **Params**

| Parameter name | Type | Required | Description |
|--------------|--------|------|------------------|
| `params` | `string` | Yes | Parameters |

#### 3. **Body**
The request body uses the `JSON` format.

| Parameter name | Type | Required | Description |
|--------------|--------|------|------------------|

##### Example:
```json
{
"username": "exampleUser",
"password": "examplePass123"
}
```

### Response parameters
#### Successful response
| Parameter name | Type | Description |
|--------------|----------|----------------|

##### Example:
```json
{
}
```

#### Error response
| Status code | Description |
|--------|-------------------------|

##### Example:
```json
{
}
```

### Error status code
| Status code | Meaning |
|--------|-------------------------------|

### Notes
- None

### Related links
- [Detailed explanation of API return values](https://example.com/docs/errors)

---