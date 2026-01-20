import os
import pandas as pd
from ultralytics import YOLO
import cv2

# Load the model
model = YOLO('yolov8n.pt')

def get_category(results):
    if not results or len(results[0].boxes) == 0:
        return "other"
    
    labels = [model.names[int(c)] for c in results[0].boxes.cls]
    has_person = 'person' in labels
    has_product = any(x in ['bottle', 'cup', 'bowl', 'vase', 'toothbrush'] for x in labels)
    
    if has_person and has_product:
        return "promotional"
    elif has_product:
        return "product_display"
    elif has_person:
        return "lifestyle"
    return "other"

def run_detection():
    image_base_dir = 'data/raw/images'
    results_list = []

    if not os.path.exists(image_base_dir):
        print(f"❌ Error: Image directory {image_base_dir} not found!")
        return

    print("🚀 Starting YOLO detection...")

    for channel in os.listdir(image_base_dir):
        channel_path = os.path.join(image_base_dir, channel)
        if not os.path.isdir(channel_path):
            continue

        for img_file in os.listdir(channel_path):
            if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(channel_path, img_file)
                
                # --- FIX: Check if file is empty or missing ---
                if not os.path.isfile(img_path) or os.path.getsize(img_path) == 0:
                    print(f"⚠️ Skipping empty or missing file: {img_path}")
                    continue

                try:
                    message_id = int(os.path.splitext(img_file)[0])
                    
                    # Run inference with a try-except block to catch OpenCV errors
                    results = model(img_path, verbose=False)
                    
                    category = get_category(results)
                    conf = results[0].boxes.conf.tolist()[0] if len(results[0].boxes.conf) > 0 else 0
                    detected_items = [model.names[int(c)] for c in results[0].boxes.cls]

                    results_list.append({
                        "message_id": message_id,
                        "channel_name": channel,
                        "detected_class": ", ".join(detected_items),
                        "confidence_score": conf,
                        "image_category": category
                    })
                except Exception as e:
                    print(f"⚠️ Error processing {img_path}: {e}")
                    continue

    # Save to CSV
    os.makedirs('data', exist_ok=True)
    df = pd.DataFrame(results_list)
    df.to_csv('data/yolo_results.csv', index=False)
    print(f"✅ Detection complete! Saved {len(df)} results to data/yolo_results.csv")

if __name__ == "__main__":
    run_detection()