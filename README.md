# Shadow Rent Index: Real-Time Housing Affordability Tracker

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg) ![Database](https://img.shields.io/badge/Database-PostgreSQL-informational.svg) ![Pipeline](https://img.shields.io/badge/Pipeline-Automated_ETL-orange.svg) ![Status](https://img.shields.io/badge/Status-In_Progress-yellow.svg)

**[Read in English](#english-version) | [Đọc bằng Tiếng Việt](#vietnamese-version)**

---

<a name="english-version"></a>

## English Version

### Project Overview

* **Context:** In macroeconomic analysis, Shelter Cost accounts for approximately one-third of the Consumer Price Index (CPI) weight in the United States. However, the methodology used by the Bureau of Labor Statistics (BLS) to calculate housing inflation inherently introduces a lag of 6 to 9 months compared to real-time market dynamics.
* **The Catalyst:** As an international student at the University of Wisconsin-Madison, I observed a stark disconnect between the official cooling CPI reports and the surging rent prices in fast-growing college towns and tech hubs. Traditional economic indicators look in the rearview mirror, failing to capture the immediate financial reality faced by tenants.
* **Purpose:** This project bridges the gap between theoretical macroeconomics and real-world data engineering. The goal is to construct a fully automated Data Pipeline that scrapes, cleans, and aggregates live rental market data to generate a "Shadow Rent Index"—a zero-lag leading indicator for housing inflation.

### System Architecture

This project is built on a robust Extract, Transform, Load (ETL) architecture:

1. **Extract:** Automated web scraping scripts navigate major real estate platforms (e.g., Zillow, Apartments.com) weekly to extract raw rental listings across targeted zip codes.
2. **Transform:** Python-based data processing handles dirty data, including missing square footage imputation, address standardization, and outlier removal to ensure statistical accuracy.
3. **Load:** Cleaned datasets are systematically ingested into a local PostgreSQL relational database.
4. **Serve:** Automated SQL views aggregate the data to track the weekly moving average of Price-per-Square-Foot, providing the baseline for the Shadow Rent Index.

### Tech Stack

* **Programming:** Python 3
* **Data Extraction:** Selenium WebDriver, BeautifulSoup4
* **Data Transformation:** Pandas, NumPy
* **Database Management:** PostgreSQL, SQLAlchemy, psycopg2
* **Environment & Security:** python-dotenv (Credential management)

### Database Schema

* **Listings Table:** listing_id (PK), address, zip_code, property_type, year_built.
* **Price_Snapshots Table:** snapshot_id (PK), listing_id (FK), scrape_date, price, sqft, beds, baths, price_per_sqft.

### Contact Information

* **Full Name:** Nguyen, Cao Thien An
* **University:** University of Wisconsin-Madison
* **Major:** Data Science & Economics

---

<a name="vietnamese-version"></a>

## Phiên bản Tiếng Việt

### Khái quát Dự án

* **Bối cảnh:** Trong phân tích kinh tế vĩ mô, Chi phí nhà ở (Shelter Cost) chiếm khoảng 1/3 trọng số của Chỉ số giá tiêu dùng (CPI) tại Mỹ. Tuy nhiên, phương pháp đo lường lạm phát nhà ở của chính phủ vốn dĩ tạo ra độ trễ từ 6 đến 9 tháng so với diễn biến thực tế của thị trường.
* **Lý do thực hiện:** Từ góc nhìn của một sinh viên tại Viện đại học Wisconsin-Madison, tôi nhận thấy sự lệch pha rõ rệt giữa các báo cáo lạm phát đang hạ nhiệt của chính phủ và giá thuê nhà đang tăng vọt thực tế tại các thành phố đại học. Các chỉ báo kinh tế truyền thống giống như việc nhìn vào gương chiếu hậu, không phản ánh đúng áp lực tài chính hiện tại của người dân.
* **Mục đích:** Dự án này kết nối lý thuyết kinh tế vĩ mô và kỹ thuật dữ liệu thực chiến. Mục tiêu là xây dựng một luồng dữ liệu (Data Pipeline) hoàn toàn tự động nhằm thu thập, làm sạch và tổng hợp dữ liệu thị trường cho thuê. Kết quả đầu ra là "Chỉ số Giá Thuê Nhà Ngầm" (Shadow Rent Index) - một chỉ báo sớm (leading indicator) với độ trễ bằng không.

### Kiến trúc Hệ thống

Dự án được xây dựng dựa trên kiến trúc ETL (Extract, Transform, Load):

1. **Extract (Trích xuất):** Kịch bản tự động hóa duyệt các nền tảng bất động sản lớn hàng tuần để thu thập tin đăng cho thuê thô tại các khu vực trọng điểm.
2. **Transform (Biến đổi):** Xử lý dữ liệu bẩn bằng Python, bao gồm: điền khuyết diện tích bị thiếu, chuẩn hóa địa chỉ và loại bỏ các giá trị ngoại lai để đảm bảo tính chính xác thống kê.
3. **Load (Tải dữ liệu):** Dữ liệu sạch được nạp tự động vào hệ quản trị cơ sở dữ liệu quan hệ PostgreSQL.
4. **Serve (Phân phối):** Các View SQL tự động tổng hợp dữ liệu để theo dõi trung bình trượt của Đơn giá trên mỗi mét vuông, tạo nền tảng cho Chỉ số Shadow Rent.

### Công nghệ sử dụng

* **Ngôn ngữ:** Python 3
* **Thu thập dữ liệu:** Selenium WebDriver, BeautifulSoup4
* **Xử lý dữ liệu:** Pandas, NumPy
* **Cơ sở dữ liệu:** PostgreSQL, SQLAlchemy, psycopg2
* **Bảo mật & Môi trường:** python-dotenv

### Cấu trúc Cơ sở dữ liệu

* **Bảng Listings:** listing_id (Khóa chính), address, zip_code, property_type, year_built.
* **Bảng Price_Snapshots:** snapshot_id (Khóa chính), listing_id (Khóa ngoại), scrape_date, price, sqft, beds, baths, price_per_sqft.

---
*Last Updated: March 2026*
