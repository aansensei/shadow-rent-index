import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import random  # gotta look like a human browsing at 2 AM lol
import pandas as pd
import re
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# load our cloud db secrets
load_dotenv()


def setup_driver():
    options = uc.ChromeOptions()
    # keeping the window open so we can see if cloudflare blocks us
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--window-size=1920,1080')
    driver = uc.Chrome(options=options)
    return driver


def extract_listings_from_html(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')
    listings = soup.find_all('article', class_='placard')
    extracted_data = []

    for item in listings:
        try:
            raw_text = item.get_text(separator='|', strip=True)
            parts = [p.strip() for p in raw_text.split('|') if p.strip()]

            if len(parts) < 2:
                continue

            title, address = parts[0], parts[1]
            full_address = f"{title} - {address}"

            price_match = re.search(r'\$[0-9,]+', raw_text)
            price = price_match.group(0) if price_match else "N/A"

            bed_match = re.search(r'Studio|\d+\s+Bed', raw_text, re.IGNORECASE)
            beds = bed_match.group(0) if bed_match else "N/A"

            if price != "N/A":
                extracted_data.append(
                    {"address": full_address, "price": price, "beds": beds})
        except:
            pass
    return extracted_data


def transform_data(raw_data):
    df = pd.DataFrame(raw_data)
    try:
        df['price_clean'] = df['price'].replace(
            r'[\$,]', '', regex=True).astype(int)
        df['beds_clean'] = df['beds'].str.replace('Studio', '0', case=False)
        df['beds_clean'] = df['beds_clean'].str.extract(r'(\d+)').astype(int)
        df['zip_code'] = df['address'].str.extract(r'(\d{5})$')
        return df.dropna(subset=['price_clean', 'zip_code'])[['address', 'zip_code', 'beds_clean', 'price_clean']]
    except:
        return pd.DataFrame()


def load_data_to_db(clean_df):
    if clean_df.empty:
        return
    try:
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")

        # neon requires ssl
        engine_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?sslmode=require"
        engine = create_engine(engine_url)
        clean_df.to_sql(name='listings', con=engine,
                        if_exists='append', index=False)
        print(f"[SUCCESS] Dumped {len(clean_df)} new rows to Neon Cloud.")
    except Exception as e:
        print(f"[ERROR] DB upload failed: {e}")


def run_hardcore_scrape():
    driver = setup_driver()
    all_raw_data = []

    try:
        print("[INFO] Initiating 100-page deep dive. Grab some coffee...")

        for page in range(1, 101):  # the ultimate loop
            url = "https://www.apartments.com/madison-wi/" if page == 1 else f"https://www.apartments.com/madison-wi/{page}/"

            print(f"[PAGE {page}/100] Scanning...")
            driver.get(url)

            # very important: random long sleeps to avoid the ban hammer
            time.sleep(random.uniform(10, 15))

            page_data = extract_listings_from_html(driver.page_source)

            if not page_data:
                print(
                    f"[CRITICAL] Page {page} is empty. Web might be blocking us or we hit the end.")
                break

            all_raw_data.extend(page_data)

            # intermediate save every 10 pages just in case the bot crashes
            if page % 10 == 0:
                print(
                    f"[SAVE POINT] Processing {len(all_raw_data)} listings collected so far...")
                temp_df = transform_data(all_raw_data)
                load_data_to_db(temp_df)
                all_raw_data = []  # clear list to save memory
                print("[INFO] Taking a 30s tactical break...")
                time.sleep(30)

        # final batch
        if all_raw_data:
            final_df = transform_data(all_raw_data)
            load_data_to_db(final_df)

    except Exception as e:
        print(f"[ERROR] Bot died: {e}")
    finally:
        driver.quit()
        print("[INFO] Mission accomplished. Browser closed.")


if __name__ == "__main__":
    run_hardcore_scrape()
