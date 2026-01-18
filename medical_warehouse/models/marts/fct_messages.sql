with messages as (
    select * from {{ ref('stg_telegram') }}
),

channels as (
    select * from {{ ref('dim_channels') }}
),

dates as (
    select * from {{ ref('dim_dates') }}
)

select
    m.message_id,
    c.channel_key,
    d.date_key,  -- NEW: Connecting to the date dimension
    m.message_date,
    m.message_text,
    m.message_length,
    m.view_count,
    m.forward_count,
    m.has_media,
    m.image_path
from messages m
left join channels c on m.channel_name = c.channel_name
-- Create the join key on the fly (YYYYMMDD)
left join dates d on to_char(m.message_date, 'YYYYMMDD')::integer = d.date_key