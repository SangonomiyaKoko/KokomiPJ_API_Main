# Kokomi后端设计（初版）

## MySQL数据库设计

这里只讨论最基础和最复杂的表的设计，对于用户绑定数据这些逻辑相对简单的表暂时不讨论

### Table 1: Region

用于储存id对应的地区（主要是为了减少数据库大小）

```sql
CREATE TABLE region (
    region_id      TINYINT        NOT NULL,
    region_str     VARCHAR(5)     NOT NULL,
    PRIMARY KEY (region_id)
);

INSERT INTO region 
    (region_id, region_str) 
VALUES
    (1, "asia"), (2, "eu"), (3, "na"), (4, "ru"), (5, "cn");
```

### Table 2: User_Basic

用于存储用户的基本信息

```sql
CREATE TABLE user_basic (
    id               INT          AUTO_INCREMENT,
    -- 用户基础信息 aid rid name
    account_id       BIGINT       NOT NULL,    -- 1-11位的非连续数字
    region_id        TINYINT      NOT NULL,
    username         VARCHAR(25)  NOT NULL,    -- 最大25个字符，编码：utf-8
    -- 用户账号查询次数，每次查询就自增1
    query_count      INT          DEFAULT 0,
    -- 关于用户所在工会的缓存
    clan_id          BIGINT       DEFAULT NULL,
    clan_ts          INT          DEFAULT 0,    -- 表示缓存更新时间，有效期为24h
    -- 关于用户账号缓存的数据，level表示用户的活跃等级
    -- 越活跃的用户level越高，更新cache的频率越高
    -- 用户账号缓存是用来实现用户排行榜
    cache_level      TINYINT      DEFAULT 0,
    cache_ts         INT          DEFAULT 0,    -- 表示用户账号缓存更新时间
    -- 关于用户活跃的信息，上面的cache_level取决于此
    -- 同时还是recent和recents功能查询用户有无战斗记录的关键
    is_public        TINYINT(1)   DEFAULT 0,    -- 用户是否隐藏战绩，0表示隐藏，1表示公开
    total_battles    INT          DEFAULT 0,    -- 用户总场次
    last_battle_time INT          DEFAULT 0,    -- 用户最后战斗时间
    update_ts        INT          DEFAULT 0,    -- 上面数据的更新时间

    PRIMARY KEY (id),
    UNIQUE INDEX idx_rid_aid (region_id, account_id) -- 索引
);
```

### Table 3：Clan_Basic

用于存储工会的基本信息，通过cid获取tag和color等信息

```sql
CREATE TABLE clan_basic (
    id               INT          AUTO_INCREMENT,
    -- 工会基础信息 cid rid tag
    clan_id          BIGINT       NOT NULL,     -- 11位的非连续数字
    region_id        TINYINT      NOT NULL,
    tag              VARCHAR(5)   NOT NULL,     -- 最大25个字符，编码：utf-8
    -- 工会段位对应的颜色
    color            TINYINT      DEFAULT 0,    -- 0紫金 1白金 2黄金 3白银 4青铜 5未知
    color_ts         INT          DEFAULT 0,    -- 上面数据的更新时间
    -- 工会段位数据缓存，用于实现工会排行榜
    season           TINYINT      DEFAULT 0,    -- 当前赛季代码 1-27
    public_rating    INT          DEFAULT 0,    -- 工会评分 1199 - 3000
    league           TINYINT      DEFAULT 0,    -- 段位 0紫金 1白金 2黄金 3白银 4青铜
    division         TINYINT      DEFAULT 0,    -- 分段 1 2 3
    division_rating  INT          DEFAULT 0,    -- 分段分数，示例：白金 1段 25分
    team_data        VARCHAR(255) DEFAULT NULL  -- 存储当前赛季的队伍数据，具体格式在下面
    update_ts        INT          DEFAULT 0,    -- 上面数据的更新时间

    PRIMARY KEY (id),
    UNIQUE INDEX idx_rid_cid (region_id, clan_id)
);
```

```python
# 这部分主要是用来统计工会战对战记录
# 更新逻辑：
#     每分钟请求wg接口获取所有活跃工会的update_ts
#     检查update_ts是否改变，如果改变则更新team_data
#     计算两次数据的差值，差值就是刚刚的工会战对战记录

team_data_example = {
    '1': {
        'battles_count': 15, 
        'wins_count': 4, 
        'league': 4, 
        'division': 3, 
        'division_rating': 14, 
        'public_rating': 1014, 
        'stage': None
    }, 
    '2': {
        'battles_count': 33, 
        'wins_count': 21, 
        'league': 3, 
        'division': 1, 
        'division_rating': 99, 
        'public_rating': 1599, 
        'stage': {
            'type': 'promotion',    # 晋级赛/保级赛
            'progress': ['victory', 'defeat']    # 结果 victory/defeat
        }
    }
}
```

## 接口基本请求逻辑

以wws me功能的接口为例

### 请求参数

- aid
- region

### 后台处理流程

![图片](./png/app_basic.png)
