# Return data format

```
\\ Success
{
    'status': 'ok',
    'message': 'SUCCESS',
    'data': {
        ...
    }
}
\\ Infomation
{
    'status': 'ok',
    'message': '...',
    'data': {}
}
\\ Error
{
    'status': 'error',
    'message': '...',
    'data': {
        'error_info': '...',
        'track_id'； '...'
    }
}
```

# Return request code list
| code  | Description              |
|:-----:|--------------------------|
|  200  | Request Success          |
|  401  | Invalid token            |
|  403  | Insufficient permissions |
|  500  | Internal Server Error    |

# Retrun message list
| No | Message | Description |
|:-----:|-----|-----|
| 1 | SUCCESS | ok |
| 2 | PROGRAM ERROR | Errors occur when the program is running |
| 5 | MYSQL ERROR | Error encountered when querying Mysql |
| 3 | APIUSER ADDED SUCCESSFULLY | API user added successfully |
| 4 | APIUSER ALREADY EXISTS | The api user already exists, adding failed |
| 6 | APIUSER DELETED SUCCESSFULLY | API user deleted successfully |
| 7 | APIUSER NOT FOUND | API user not found, Deletion failed |
| 8 | APPUSER ADDED SUCCESSFULLY| APP user added successfully |
| 9 | APPUSER UPDATE SUCCESSFULLY | APP user update successfully (querys, nickname or clan) |
