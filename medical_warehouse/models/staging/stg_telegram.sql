with raw_data as (
    select * from {{ source('telegram', 'telegram_messages') }}
),

cleaned as (
    select
        -- Generate a unique ID if message_id is not unique globally, 
        -- but here we assume (channel_name + message_id) is unique.
        cast(message_id as integer) as message_id,
        cast(channel_name as varchar(100)) as channel_name,
        
        -- Fix timestamp format
        cast(message_date as timestamp) as message_date,
        
        -- Handle text content
        cast(message_text as text) as message_text,
        length(message_text) as message_length,
        
        -- Media flags
        cast(has_media as boolean) as has_media,
        cast(image_path as text) as image_path,
        
        -- Metrics (default to 0 if null)
        coalesce(views, 0) as view_count,
        coalesce(forwards, 0) as forward_count

    from raw_data
    where message_date is not null
)

select * from cleaned