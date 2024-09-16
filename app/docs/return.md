# Return data format

```
\\ Successed
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
| code | Description |
|:-----:|-----|
| 200 | Request Success |
| 401 | Invalid token |
| 403 | Insufficient permissions |

# Retrun message list
| No | Message | Description |
|:-----:|-----|-----|
| 1 | SUCCESS | ok |
| 2 | UNAUTHORIZED | No permission to use the interface |
