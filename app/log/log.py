# -*- coding: utf-8 -*-

import time
import hashlib

class API_Logging:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(API_Logging, cls).__new__(cls)
        return cls._instance

    def calculate_md5(self, data):
        md5_hash = hashlib.md5()
        md5_hash.update(data)
        md5_hexdigest = md5_hash.hexdigest()
        return md5_hexdigest

    def write_api_error(
        self,
        error_file: str,
        error_params: list,
        error_name: str,
        error_info: str
    ):
        form_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        track_id = self.calculate_md5((form_time + error_name).encode()).upper()
        now_day = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        with open(f'{now_day}.txt', "a", encoding="utf-8") as f:
            f.write('-------------------------------------------------------------------------------------------------------------\n')
            f.write(f">Platform:     API\n")
            f.write(f">Track ID:     {track_id}\n")
            f.write(f">Error Time:   {form_time}\n")
            f.write(f">Error File:   {error_file}\n")
            f.write(f">Error Name:   {error_name}\n")
            f.write(f">Error Params: {error_params}\n")
            f.write(f">Error Info: \n")
            f.write(f"{error_info}\n")
            f.write('-------------------------------------------------------------------------------------------------------------\n')
        f.close()
        return 'API_' + track_id
    
    def write_mysql_error(
        self,
        error_file: str,
        error_code: str,
        error_info: str,
        error_query: str,
        error_data: str
    ):
        form_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        track_id = self.calculate_md5((form_time + error_code).encode()).upper()
        now_day = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        with open(f'{now_day}.txt', "a", encoding="utf-8") as f:
            f.write('-------------------------------------------------------------------------------------------------------------\n')
            f.write(f">Platform:     MYSQL\n")
            f.write(f">Track ID:     {track_id}\n")
            f.write(f">Error Time:   {form_time}\n")
            f.write(f">Error File:   {error_file}\n")
            f.write(f">Error Code:   {error_code}\n")
            f.write(f">Error Info:   {error_info}\n")
            f.write(f">Error SQL: {error_query + error_data}\n")
            f.write('-------------------------------------------------------------------------------------------------------------\n')
        f.close()
        return 'MYSQL_' + track_id
    
    def write_redis_error(
        self,
        error_file: str,
        error_params: list,
        error_name: str,
        error_info: str
    ):
        form_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        track_id = self.calculate_md5((form_time + error_name).encode()).upper()
        now_day = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        with open(f'{now_day}.txt', "a", encoding="utf-8") as f:
            f.write('-------------------------------------------------------------------------------------------------------------\n')
            f.write(f">Platform:     REDIS\n")
            f.write(f">Track ID:     {track_id}\n")
            f.write(f">Error Time:   {form_time}\n")
            f.write(f">Error File:   {error_file}\n")
            f.write(f">Error Name:   {error_name}\n")
            f.write(f">Error Params: {error_params}\n")
            f.write(f">Error Info: \n")
            f.write(f"{error_info}\n")
            f.write('-------------------------------------------------------------------------------------------------------------\n')
        f.close()
        return 'REDIS_' + track_id
