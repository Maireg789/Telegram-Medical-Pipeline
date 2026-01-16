with messages as (
    select * from {{ ref('stg_telegram') }}
),

channels as (
    select * from {{ ref('dim_channels') }}
)

select
    m.message_id,
    c.channel_key,
    m.message_date,
    m.message_text,
    m.message_length,
    m.view_count,
    m.forward_count,
    m.has_media,
    m.image_path
from messages m
left join channels c on m.channel_name = c.channel_name