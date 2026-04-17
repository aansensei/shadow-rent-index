import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# load secrets securely
load_dotenv()

# wide layout to fit the map
st.set_page_config(page_title="The Data Nexus", layout="wide")


@st.cache_data
def get_data():
    user = os.getenv("DB_USER")
    pwd = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db = os.getenv("DB_NAME")

    db_url = f"postgresql://{user}:{pwd}@{host}:{port}/{db}?sslmode=require"
    engine = create_engine(db_url)

    sql = "SELECT * FROM shadow_rent_index;"
    df = pd.read_sql(sql, engine)

    # drop garbage data (scraped sqft instead of beds by accident)
    df = df[df['room_type'] < 10]

    # force zip_code to string type immediately
    df['zip_code'] = df['zip_code'].astype(str)

    return df


try:
    df = get_data()
except Exception as e:
    st.error(f"Rip, cannot connect to db: {e}")
    st.stop()

# mapping zip codes to actual madison neighborhoods so it's readable
zip_map = {
    '53703': 'Downtown / Isthmus',
    '53704': 'East / North',
    '53705': 'Near West / Campus',
    '53711': 'Fitchburg / Near West',
    '53715': 'South Campus',
    '53719': 'West / Fitchburg',
    '53562': 'Middleton',
    '53590': 'Sun Prairie',
    '53527': 'Cottage Grove',
    '53532': 'DeForest',
    '53593': 'Verona',
    '53597': 'Waunakee'
}

# create a new column combining zip and name
df['area_name'] = df['zip_code'].apply(
    lambda z: f"{z} - {zip_map.get(z, 'Madison Area')}")

# headers
st.title("The Data Nexus")
st.subheader(
    "Shadow Rent Oracle: Real-time Housing Inflation Tracker (Madison, WI)")

# econ narrative tabs
tab1, tab2, tab3 = st.tabs(
    ["Local Market", "The Macro Lag", "Fed Policy Risks"])

with tab1:
    st.markdown("### Madison Rental Market Map")
    st.write("Live spot prices directly from the market. No 6-month government delay.")

    # sort the new area names alphabetically (which also sorts them by zip number)
    areas = sorted(df['area_name'].unique())

    col1, col2 = st.columns(2)
    with col1:
        pick_area = st.selectbox("Select Neighborhood", areas)
    with col2:
        pick_bed = st.selectbox(
            "Select Room Type (0 = Studio)", sorted(df['room_type'].unique()))

    # extract the raw zip code back from the selected string (e.g. "53703 - Downtown" -> "53703")
    pick_zip = pick_area.split(" ")[0]

    # filter based on what user picked
    sub_df = df[(df['zip_code'] == pick_zip) & (df['room_type'] == pick_bed)]

    if not sub_df.empty:
        mean_price = sub_df['avg_rent_price'].values[0]
        count = sub_df['total_listings'].values[0]
        max_p = sub_df['max_price'].values[0]
        min_p = sub_df['min_price'].values[0]

        # 4 core metrics layout
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(label="Average Rent",
                  value=f"${mean_price:,.0f}", delta="Live")
        m2.metric(label="Lowest Found", value=f"${min_p:,.0f}")
        m3.metric(label="Highest Found", value=f"${max_p:,.0f}")
        m4.metric(label="Active Listings", value=f"{count}")
    else:
        st.warning(
            "No data for this exact filter yet. Waiting for the scraper to pick it up.")

    st.markdown("---")

    # lat/lon coordinates to plot bubbles on the map
    zip_coords = {
        '53703': [43.074, -89.384], '53704': [43.116, -89.345],
        '53705': [43.078, -89.458], '53711': [43.033, -89.444],
        '53715': [43.066, -89.399], '53719': [43.028, -89.501],
        '53562': [43.101, -89.497], '53590': [43.180, -89.230],
        '53527': [43.075, -89.324], '53532': [43.167, -89.260],
        '53593': [43.021, -89.570], '53597': [43.160, -89.460]
    }

    df['lat'] = df['zip_code'].map(
        lambda x: zip_coords.get(x, [43.07, -89.40])[0])
    df['lon'] = df['zip_code'].map(
        lambda x: zip_coords.get(x, [43.07, -89.40])[1])

    st.markdown("#### Market Supply Map")
    st.caption("Circle size = Number of listings. Color = Average price.")

    # setup the map dataset
    map_df = df[df['room_type'] == pick_bed]
    if not map_df.empty:
        map_fig = px.scatter_mapbox(
            map_df,
            lat="lat", lon="lon",
            size="total_listings",
            color="avg_rent_price",
            color_continuous_scale=px.colors.sequential.Sunsetdark,
            hover_name="area_name",  # showing the full name on hover now
            mapbox_style="carto-positron",
            zoom=10,
            height=400
        )
        st.plotly_chart(map_fig, use_container_width=True)

    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Average Price per Area")
        # sorting by zip_code now instead of price, so the bars go in order
        bar = px.bar(
            map_df.sort_values('zip_code'),
            x='area_name', y='avg_rent_price', color='avg_rent_price',
            labels={'area_name': 'Neighborhood',
                    'avg_rent_price': 'Average Rent ($)'}
        )
        # telling plotly explicitly that x is categorical text
        bar.update_xaxes(type='category')
        st.plotly_chart(bar, use_container_width=True)

    with c2:
        st.markdown("#### Supply Concentration")
        pie = px.pie(
            map_df,
            values='total_listings', names='area_name', hole=0.5
        )
        st.plotly_chart(pie, use_container_width=True)

with tab2:
    st.markdown("### The Macro Disconnect: Lagging Indicators")
    st.write("""
    **The BLS Blindspot:** Shelter costs make up over 30% of the Core CPI. But the Bureau of Labor Statistics (BLS) surveys all existing leases. This means a lease signed almost a year ago still impacts today's official inflation rate.
    
    **The 6-Month Lag:** Because of this method, official housing inflation metrics lag the real market prices by 6 to 9 months.
    
    **Our Solution:** By scraping real-time data every week, the *Shadow Rent Index* works as a leading indicator with no lag. We measure what people actually pay today, not last year.
    """)

with tab3:
    st.markdown("### Monetary Policy Risks")
    st.write("""
    The gap between official CPI and real-time rent data creates a big risk for the Federal Reserve.
    
    * **Risk of Overtightening:** If real rent prices are dropping fast, but official CPI still looks high because of the lag, the Fed might keep interest rates too high for too long.
    * **Economic Harm:** Making policy choices based on old data can hurt economic growth and cause a recession.
    * **Takeaway:** Policymakers need to look at real-time alternative data like the Shadow Rent Index to make better choices about interest rates.
    """)
