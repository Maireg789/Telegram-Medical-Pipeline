{{ config(materialized='table') }}

WITH messages AS (
    SELECT * FROM {{ ref('fct_messages') }}
),

detections AS (
    -- This pulls from the raw table you uploaded via Python
    SELECT * FROM {{ source('raw', 'yolo_results') }}
)

SELECT 
    m.message_id,
    m.channel_key,
    m.date_key,
    d.image_category,
    d.confidence_score,
    d.detected_class
FROM messages m
INNER JOIN detections d ON m.message_id = d.message_id