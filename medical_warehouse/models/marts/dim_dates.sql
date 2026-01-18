with date_series as (
    -- Generate dates for the next 5 years starting from 2024
    select generate_series(
        '2024-01-01'::timestamp, 
        '2030-01-01'::timestamp, 
        '1 day'::interval
    ) as date_day
),

formatted_dates as (
    select
        date_day,
        cast(to_char(date_day, 'YYYYMMDD') as integer) as date_key, -- Surrogate Key
        cast(date_day as date) as full_date,
        cast(extract(year from date_day) as integer) as year,
        cast(extract(quarter from date_day) as integer) as quarter,
        cast(extract(month from date_day) as integer) as month,
        to_char(date_day, 'Month') as month_name,
        cast(extract(week from date_day) as integer) as week_of_year,
        cast(extract(doy from date_day) as integer) as day_of_year,
        cast(extract(day from date_day) as integer) as day_of_month,
        cast(extract(isodow from date_day) as integer) as day_of_week,
        to_char(date_day, 'Day') as day_name,
        case 
            when extract(isodow from date_day) in (6, 7) then true 
            else false 
        end as is_weekend
    from date_series
)

select * from formatted_dates