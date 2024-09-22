import aiomysql
from aiomysql.pool import Pool
from aiomysql.connection import Connection
from aiomysql.cursors import Cursor
from typing import Dict, Any
from .. import API_Logging, mysql_pool, REGION_IDS
from .. import SuccessResponse, InfoResponse, ErrorResponse, BaseError


class CLAN_Basic:
    def __init__(
            self, 
            clan_id, 
            region, 
            clan_tag=None,
            clan_color=None, 
            update_time=0
        ):
        self.clan_id = clan_id
        self.region = region
        self.clan_tag = clan_tag if clan_tag else 'UNDEFINED'
        self.clan_color = clan_color
        self.update_time = update_time

    def to_dict(self) -> Dict[str, Any]:
        return {
            'clan_id': self.clan_id,
            'region': self.region,
            'clan_tag': self.clan_tag,
            'clan_color': self.clan_color ,
            'update_time': self.update_time
        }

    def __repr__(self):
        return f"<Clan_Basic(clan_id={self.clan_id}, clan_tag={self.clan_tag}, region={self.region})>"