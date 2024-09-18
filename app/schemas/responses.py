# -*- coding: utf-8 -*-

from typing import Any, Dict

class BaseResponse:
    def __init__(self, status: str, message: str, data: Any = None) -> None:
        self.status = status
        self.message = message
        self.data = data if data is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the BaseResponse instance to a dictionary.
        """
        return {
            'status': self.status,
            'message': self.message,
            'data': self.data
        }

    def __repr__(self) -> str:
        """
        Custom string representation of the BaseResponse object.
        """
        return f"BaseResponse(status={self.status}, message={self.message}, data={self.data})"
    

class BaseError:
    def __init__(self, error_info: str, track_id: str) -> None:
        self.error_info = error_info
        self.track_id = track_id

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the BaseError instance to a dictionary.
        """
        return {
            'error_info': self.error_info,
            'track_id': self.track_id
        }

    def __repr__(self) -> str:
        """
        Custom string representation of the BaseError object.
        """
        return f"BaseError(error_info={self.error_info}, track_id={self.track_id})"

class SuccessResponse(BaseResponse):
    def __init__(self, data: Any = None) -> None:
        '''
        Call the parent class constructor with status set to 'ok' and message set to 'SUCCESS'
        '''
        super().__init__(
            status = 'ok', 
            message = 'SUCCESS', 
            data = data.to_dict() if hasattr(data, 'to_dict') else data
        )

    def __repr__(self):
        """
        Custom string representation for error response, starting with 'Error'.
        """
        return f"SuccessResponse(status={self.status}, message={self.message}, data={self.data})"

class InfoResponse(BaseResponse):
    def __init__(self, message: str, data: Any = None) -> None:
        '''
        Call the parent class constructor with status set to 'ok' and message set to '...'
        '''
        super().__init__(
            status = 'ok', 
            message = message, 
            data = data.to_dict() if hasattr(data, 'to_dict') else data
        )

    def __repr__(self):
        """
        Custom string representation for error response, starting with 'Error'.
        """
        return f"InfoResponse(status={self.status}, message={self.message}, data={self.data})"

class ErrorResponse(BaseResponse):
    def __init__(self, message: str, data: BaseError) -> None:
        '''
        Call the parent class constructor with status set to 'error'
        '''
        super().__init__(
            status = 'error', 
            message = message, 
            data =  data.to_dict() if hasattr(data, 'to_dict') else data
        )

    def __repr__(self):
        """
        Custom string representation for error response, starting with 'Error'.
        """
        return f"ErrorResponse(status={self.status}, message={self.message}, data={self.data})"

# class User:
#     def __init__(self, user_id: int, username: str, email: str):
#         self.user_id = user_id
#         self.username = username
#         self.email = email

#     def to_dict(self) -> Dict[str, Any]:
#         """
#         Convert the User instance to a dictionary.
#         """
#         return {
#             'user_id': self.user_id,
#             'username': self.username,
#             'email': self.email
#         }
# def main():
#     user1 = User(123,123,123)
#     result = SuccessResponse(data=user1)
#     print(result.to_dict())
# error_response = ErrorResponse(message='Invalid input', error_info='Input value is out of range', track_id='12345')
# print(error_response)
# print(error_response.to_dict())