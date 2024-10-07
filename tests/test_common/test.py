# -*- coding: utf-8 -*-

from app.common.utils import (
    Personal_Rating
)

def main():
    result = Personal_Rating.get_pr_by_sid_and_region(
        sid = '4180621264',
        region = 'asia',
        battle_type = 'pvp',
        ship_data = [2,1,150000,2]
    )
    print(result)