import pandas as pd
import requests
import os
import time

# Load dataset
data = pd.read_csv("dataset/places.csv")

# Create images folder
os.makedirs("static/images", exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0"
}

for index, row in data.iterrows():
    place = row["place"]
    image_name = row["image"]

    # Bing image query
    search_query = place.replace(" ", "+")
    url = f"https://bing.com/images/search?q={search_query}&form=HDRSC2"

    try:
        response = requests.get(url, headers=headers, timeout=10)

        # Extract first image link manually
        if "murl&quot;:&quot;" in response.text:
            start = response.text.find("murl&quot;:&quot;") + 17
            end = response.text.find("&quot;", start)
            image_url = response.text[start:end]

            img_data = requests.get(image_url, headers=headers).content

            with open(f"static/images/{image_name}", "wb") as f:
                f.write(img_data)

            print(f"✅ Downloaded: {image_name}")
        else:
            print(f"❌ No image found: {image_name}")

        time.sleep(1)

    except Exception as e:
        print(f"❌ Error: {image_name} - {e}")

print("🎉 Download process completed")