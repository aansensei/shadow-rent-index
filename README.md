# Shadow Rent Index: Real-Time Housing Affordability Tracker

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg) ![Database](https://img.shields.io/badge/Database-PostgreSQL-informational.svg) ![Frontend](https://img.shields.io/badge/Frontend-Streamlit-red.svg) ![Pipeline](https://img.shields.io/badge/Pipeline-Automated_ETL-orange.svg) ![Series](https://img.shields.io/badge/Series-Hidden_Inflation_Part_1-purple.svg)

**[Live Demo App: The Shadow Rent Oracle](https://shadow-rent-index-ncta.streamlit.app/)**

> Part 1 of a hidden inflation research series. Part 2: **[The Shrinkflation Detective](https://github.com/aansensei/shrinkflation-detective)**, tracking product size reductions that CPI also misses.

**[Read in English](#english-version) | [Đọc bằng Tiếng Việt](#vietnamese-version)**

---

<a name="english-version"></a>

## English Version

### Project Overview

**Context:** In macroeconomic analysis, Shelter Cost accounts for approximately one-third of the Consumer Price Index (CPI) weight in the United States. However, the methodology used by the Bureau of Labor Statistics (BLS) to calculate housing inflation inherently introduces a lag of 6 to 9 months compared to real-time market dynamics.

**The Catalyst:** As an international student at the University of Wisconsin Madison, I observed a stark disconnect between the official cooling CPI reports and the surging rent prices in fast-growing college towns and tech hubs. Traditional economic indicators look in the rearview mirror, failing to capture the immediate financial reality faced by tenants.

**Purpose:** This project bridges the gap between theoretical macroeconomics and real-world data engineering. My goal was to construct a fully automated Data Pipeline that scrapes, cleans, and aggregates live rental market data to generate a "Shadow Rent Index", a zero-lag leading indicator for housing inflation.

### System Architecture (ETL Pipeline)

This project was my way to practice initializing a PostgreSQL database and managing relational schemas from scratch. The system is built on a robust Extract, Transform, Load (ETL) architecture:

1. **Extract:** Automated web scraping scripts using undetected-chromedriver navigate major real estate platforms weekly to extract raw rental listings across targeted zip codes in Madison, WI.
2. **Transform:** Python-based data processing via Pandas handles dirty data. This includes regex cleaning for prices, room type extraction, and outlier removal to ensure statistical accuracy.
3. **Load:** Cleaned datasets are systematically ingested into a local PostgreSQL relational database to build historical time-series data.
4. **Serve & Automate:** Automated SQL views aggregate the data. A Streamlit web application connects directly to the database to visualize spot prices, supply distribution via Plotly Mapbox, and macro policy analysis. The entire pipeline is automated using Windows Task Scheduler via batch scripts.

### Key Takeaways

* **Data Infrastructure:** Learned to initialize and manage a PostgreSQL database independently.
* **ETL Orchestration:** Gained hands-on experience in building an end to end pipeline, moving from raw web data to actionable insights.
* **Economic Insights:** Successfully applied macroeconomic theories regarding inflation lags to create a functional technical tool.

### Tech Stack & Skills Demonstrated

* **Languages:** Python, SQL
* **Data Extraction:** Selenium, undetected-chromedriver, BeautifulSoup4
* **Data Transformation:** Pandas, Regular Expressions (Regex)
* **Database Management:** PostgreSQL, SQLAlchemy, psycopg2
* **Data Visualization:** Streamlit, Plotly Express, Mapbox
* **DevOps:** Batch Scripting, Windows Task Scheduler

### See Also

This project is Part 1 of a hidden inflation research series. The Shadow Rent Index addresses the shelter cost blind spot in CPI. Part 2, **[The Shrinkflation Detective](https://github.com/aansensei/shrinkflation-detective)**, extends the same framework to product-level inflation by tracking package size reductions across grocery categories.

---

<a name="vietnamese-version"></a>

## Phiên bản Tiếng Việt

### Khái quát Dự án

**Bối cảnh:** Trong phân tích kinh tế vĩ mô, Chi phí nhà ở (Shelter Cost) chiếm khoảng một phần ba trọng số của Chỉ số giá tiêu dùng (CPI) tại Mỹ. Tuy nhiên, phương pháp đo lường của chính phủ vốn tạo ra độ trễ từ 6 đến 9 tháng so với diễn biến thực tế của thị trường.

**Lý do thực hiện:** Từ góc nhìn của một sinh viên tại University of Wisconsin Madison, mình nhận thấy sự lệch pha rõ rệt giữa các báo cáo lạm phát hạ nhiệt của chính phủ và giá thuê nhà thực tế đang tăng vọt tại các thành phố đại học. Các chỉ báo kinh tế truyền thống giống như việc nhìn vào gương chiếu hậu, không phản ánh đúng áp lực tài chính hiện tại của người đi thuê.

**Mục đích:** Dự án này kết nối lý thuyết kinh tế vĩ mô và kỹ thuật dữ liệu thực chiến. Mình muốn xây dựng một luồng dữ liệu (Data Pipeline) hoàn toàn tự động nhằm thu thập, làm sạch và tổng hợp dữ liệu thị trường cho thuê để tạo ra "Shadow Rent Index", một chỉ báo sớm với độ trễ bằng không.

### Kiến trúc Hệ thống (ETL)

Dự án này là cách mình tập khởi động một cơ sở dữ liệu PostgreSQL và quản lý các lược đồ quan hệ từ con số không. Hệ thống được xây dựng trên kiến trúc ETL (Extract, Transform, Load):

1. **Trích xuất (Extract):** Kịch bản tự động hóa duyệt các nền tảng bất động sản hàng tuần để lấy tin đăng thô tại các khu vực trọng điểm ở Madison.
2. **Biến đổi (Transform):** Mình sử dụng Pandas và Biểu thức chính quy (Regex) để xử lý dữ liệu bẩn, chuẩn hóa giá tiền và loại bỏ các giá trị ngoại lai nhằm đảm bảo tính chính xác thống kê.
3. **Tải dữ liệu (Load):** Dữ liệu sạch được nạp tự động vào cơ sở dữ liệu PostgreSQL để xây dựng kho dữ liệu lịch sử.
4. **Phân phối & Tự động hóa (Serve & Automate):** Các View SQL tự động tổng hợp dữ liệu. Ứng dụng Streamlit kết nối trực tiếp với cơ sở dữ liệu để hiển thị giá giao ngay và phân tích chính sách vĩ mô. Toàn bộ luồng chạy được tự động hóa bằng Task Scheduler.

### Bài học rút ra (Key Takeaways)

* **Hạ tầng dữ liệu:** Mình đã biết cách tự khởi tạo và quản lý một cơ sở dữ liệu PostgreSQL độc lập.
* **Vận hành ETL:** Có kinh nghiệm thực tế trong việc xây dựng một luồng dữ liệu xuyên suốt, từ dữ liệu thô trên web đến các thông tin phân tích có giá trị.
* **Kết nối lý thuyết và thực tế:** Áp dụng thành công các lý thuyết kinh tế vĩ mô về độ trễ lạm phát vào một công cụ kỹ thuật thực tiễn.

### Công nghệ & Kỹ năng áp dụng

* **Ngôn ngữ:** Python, SQL
* **Thu thập dữ liệu:** Selenium, undetected-chromedriver, BeautifulSoup4
* **Xử lý dữ liệu:** Pandas, Biểu thức chính quy (Regex)
* **Cơ sở dữ liệu:** PostgreSQL, SQLAlchemy, psycopg2
* **Trực quan hóa:** Streamlit, Plotly Express, Mapbox
* **Tự động hóa:** Batch Script, Windows Task Scheduler

### Xem thêm

Dự án này là Phần 1 trong chuỗi nghiên cứu lạm phát ẩn. Shadow Rent Index giải quyết điểm mù chi phí nhà ở trong CPI. Phần 2, **[The Shrinkflation Detective](https://github.com/aansensei/shrinkflation-detective)**, mở rộng cùng hướng tiếp cận sang lạm phát cấp độ sản phẩm bằng cách theo dõi việc giảm khối lượng đóng gói trên các danh mục hàng tạp hóa.

---
*Last update: April 2026*
