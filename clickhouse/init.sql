CREATE DATABASE raw;
CREATE DATABASE clean;

-- raw layer
CREATE TABLE raw.users
(
    id UInt64,

    name String,
    email String,

    operation String,

    event_ts DateTime64(3),

    kafka_offset UInt64
)
ENGINE = MergeTree
ORDER BY (id,event_ts);

CREATE TABLE raw.orders
(
    id UInt64,

    user_id UInt64,

    amount Decimal(10,2),

    status String,

    operation String,

    event_ts DateTime64(3),

    kafka_offset UInt64
)
ENGINE = MergeTree
ORDER BY (id,event_ts);

-- clean layer
CREATE TABLE clean.orders
(
    id UInt64,

    user_id UInt64,

    amount Decimal(10,2),

    status String,

    is_deleted UInt8,

    event_ts DateTime64(3)
)
ENGINE = ReplacingMergeTree(event_ts)
ORDER BY id;

CREATE TABLE clean.users
(
    id UInt64,

    name String,

    email String,

    is_deleted UInt8,

    event_ts DateTime64(3)
)
ENGINE = ReplacingMergeTree(event_ts)
ORDER BY id;


-- materialized views
CREATE MATERIALIZED VIEW clean.mv_orders
TO clean.orders
AS
SELECT
    id,
    user_id,
    amount,
    status,

    operation='d' AS is_deleted,

    event_ts
FROM raw.orders;

CREATE MATERIALIZED VIEW clean.mv_users
TO clean.users
AS
SELECT
    id,
    name,
    email,

    operation='d' AS is_deleted,

    event_ts
FROM raw.users;

-- view
CREATE VIEW clean.users_latest
AS
SELECT
    id,

    argMax(name,event_ts) AS name,

    argMax(email,event_ts) AS email,


    argMax(is_deleted,event_ts)
        AS is_deleted
FROM clean.users
GROUP BY id;

CREATE VIEW clean.orders_latest
AS
SELECT
    id,

    argMax(user_id,event_ts) AS user_id,

    argMax(amount,event_ts) AS amount,

    argMax(status,event_ts) AS status,

    argMax(is_deleted,event_ts)
        AS is_deleted
FROM clean.orders
GROUP BY id;

-- dashboard select query
SELECT *
FROM clean.users_latest
WHERE is_deleted=0