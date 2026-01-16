with staging as (
    select * from {{ ref('stg_telegram') }}
),

channel_stats as (
    select
        channel_name,
        min(message_date) as first_seen,
        max(message_date) as last_seen,
        count(*) as total_messages,
        avg(view_count) as avg_views
    from staging
    group by channel_name
)

select
    {{ dbt_utils.generate_surrogate_key(['channel_name']) }} as channel_key,
    channel_name,
    first_seen,
    last_seen,
    total_messages,
    avg_views
from channel_stats