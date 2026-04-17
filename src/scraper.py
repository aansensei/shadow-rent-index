import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# pull secrets
load_dotenv()


def setup_driver():
    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--window-size=1920,1080')
    driver = uc.Chrome(options=options)
    return driver


def extract_listings_from_html(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')
    listings = soup.find_all('article', class_='placard')
    extracted_data = []

    print(f"[INFO] Found {len(listings)} raw blocks. Parsing...")

    for item in listings:
        try:
            raw_text = item.get_text(separator='|', strip=True)
            parts = [p.strip() for p in raw_text.split('|') if p.strip()]

            if len(parts) < 2:
                continue

            title = parts[0]
            address = parts[1]
            full_address = f"{title} - {address}"

            price_match = re.search(r'\$[0-9,]+', raw_text)
            price = price_match.group(0) if price_match else "N/A"

            bed_match = re.search(r'Studio|\d+\s+Bed', raw_text, re.IGNORECASE)
            beds = bed_match.group(0) if bed_match else "N/A"

            if price != "N/A":
                extracted_data.append({
                    "address": full_address,
                    "price": price,
                    "beds": beds
                })
        except Exception as e:
            pass

    return extracted_data


def transform_data(raw_data):
    df = pd.DataFrame(raw_data)
    print("[INFO] Cleaning data...")

    try:
        df['price_clean'] = df['price'].replace(
            r'[\$,]', '', regex=True).astype(int)
        df['beds_clean'] = df['beds'].str.replace('Studio', '0', case=False)
        df['beds_clean'] = df['beds_clean'].str.extract(r'(\d+)').astype(int)
        df['zip_code'] = df['address'].str.extract(r'(\d{5})$')

        df = df.dropna(subset=['price_clean', 'zip_code'])

        clean_df = df[['address', 'zip_code', 'beds_clean', 'price_clean']]
        return clean_df

    except Exception as e:
        print(f"[ERROR] Clean failed: {e}")
        return pd.DataFrame()


def load_data_to_db(clean_df):
    if clean_df.empty:
        print("[WARNING] Empty df, skipping db load.")
        return

    print("[INFO] Hooking up to postgres...")
    try:
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")

        engine_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(engine_url)

        # appending so we build a historical dataset
        clean_df.to_sql(name='listings', con=engine,
                        if_exists='append', index=False)
        print(f"[SUCCESS] {len(clean_df)} rows dumped to db.")

    except Exception as e:
        print(f"[ERROR] DB load failed: {e}")


def run_test_scrape():
    driver = setup_driver()
    all_raw_data = []

    try:
        print("[INFO] Firing up the stealth browser...")

        # bumping this up to 10 pages so the map doesn't look empty
        for page in range(1, 11):
            if page == 1:
                url = "https://www.apartments.com/madison-wi/"
            else:
                url = f"https://www.apartments.com/madison-wi/{page}/"

            print(f"[INFO] Accessing Page {page}...")
            driver.get(url)

            # waiting out cloudflare checks. don't lower this or we get blocked
            time.sleep(7)

            raw_html = driver.page_source
            page_data = extract_listings_from_html(raw_html)
            all_raw_data.extend(page_data)

            print(
                f"[SUCCESS] Grabbed {len(page_data)} listings from Page {page}.")
            # chill for a bit before hitting next page so we look like a human
            time.sleep(3)

        print(f"[INFO] Total listings collected: {len(all_raw_data)}")

        clean_df = transform_data(all_raw_data)
        load_data_to_db(clean_df)

    except Exception as e:
        print(f"[ERROR] Bot crashed: {e}")

    finally:
        driver.quit()
        print("[INFO] Browser closed.")


if __name__ == "__main__":
    run_test_scrape()
