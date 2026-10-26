
# ============================================================
# REAL ESTATE INVESTMENT ADVISOR
# Streamlit Dashboard
# KPIs | Charts | Filters | Business Recommendations
# ============================================================

import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# ------------------------------------------------------------
# 1. PAGE CONFIGURATION
# ------------------------------------------------------------

st.set_page_config(
    page_title="Real Estate Investment Advisor",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Real Estate Investment Advisor")
st.subheader("Property Analysis, Investment Insights & Price Trends")

st.markdown("""
Explore Indian housing data, compare property prices, and identify
properties that may be worth investigating further.
""")

# ------------------------------------------------------------
# 2. LOAD DATASET
# ------------------------------------------------------------

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)


possible_paths = [
    "cleaned_housing_data.csv",
    "india_housing_prices.csv",
    os.path.join("data", "cleaned_housing_data.csv"),
    os.path.join("data", "india_housing_prices.csv")
]

data_path = next(
    (path for path in possible_paths if os.path.exists(path)),
    None
)

if data_path is None:
    st.error(
        "Dataset not found. Place india_housing_prices.csv "
        "or cleaned_housing_data.csv in the project folder "
        "or inside its data folder."
    )

    uploaded_file = st.file_uploader(
        "Alternatively, upload your housing CSV file",
        type=["csv"]
    )

    if uploaded_file is None:
        st.stop()

    df = pd.read_csv(uploaded_file)

else:
    try:
        df = load_data(data_path)
    except Exception as error:
        st.error(f"Unable to load the dataset: {error}")
        st.stop()

if df.empty:
    st.error("The dataset is empty.")
    st.stop()

# ------------------------------------------------------------
# 3. VALIDATE IMPORTANT COLUMNS
# ------------------------------------------------------------

required_columns = [
    "City",
    "Property_Type",
    "Price_in_Lakhs",
    "Size_in_SqFt"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    st.error(
        "Your dataset is missing required columns: "
        + ", ".join(missing_columns)
    )
    st.write("Available columns:", df.columns.tolist())
    st.stop()

# Convert numerical columns safely
numeric_columns = [
    "Price_in_Lakhs",
    "Size_in_SqFt",
    "Price_per_SqFt",
    "BHK",
    "Year_Built",
    "Nearby_Schools",
    "Nearby_Hospitals",
    "Parking_Space"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove records without valid prices and sizes
df = df.dropna(
    subset=["Price_in_Lakhs", "Size_in_SqFt"]
)

df = df[
    (df["Price_in_Lakhs"] > 0)
    & (df["Size_in_SqFt"] > 0)
].copy()

if df.empty:
    st.error("No records with valid property prices and sizes.")
    st.stop()

# Calculate price per square foot consistently.
# Price is stored in lakhs; 1 lakh = 100,000 currency units.
df["Price_per_SqFt"] = (
    df["Price_in_Lakhs"] * 100000
    / df["Size_in_SqFt"]
)

# ------------------------------------------------------------
# 4. SIDEBAR FILTERS
# ------------------------------------------------------------

st.sidebar.header("🔎 Property Filters")

filtered_df = df.copy()

# State filter
if "State" in df.columns:
    states = sorted(
        df["State"].dropna().astype(str).unique().tolist()
    )

    selected_states = st.sidebar.multiselect(
        "Select State",
        states,
        default=states
    )

    filtered_df = filtered_df[
        filtered_df["State"].astype(str).isin(selected_states)
    ]

# City filter based on selected states
cities = sorted(
    filtered_df["City"].dropna().astype(str).unique().tolist()
)

selected_cities = st.sidebar.multiselect(
    "Select City",
    cities,
    default=cities
)

filtered_df = filtered_df[
    filtered_df["City"].astype(str).isin(selected_cities)
]

# Property type filter
property_types = sorted(
    filtered_df["Property_Type"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_types = st.sidebar.multiselect(
    "Property Type",
    property_types,
    default=property_types
)

filtered_df = filtered_df[
    filtered_df["Property_Type"].astype(str).isin(selected_types)
]

# BHK filter
if "BHK" in filtered_df.columns:
    bhk_values = sorted(
        filtered_df["BHK"].dropna().unique().tolist()
    )

    if bhk_values:
        selected_bhk = st.sidebar.multiselect(
            "Select BHK",
            bhk_values,
            default=bhk_values
        )

        filtered_df = filtered_df[
            filtered_df["BHK"].isin(selected_bhk)
        ]

# Price range filter
if not filtered_df.empty:
    min_price = float(filtered_df["Price_in_Lakhs"].min())
    max_price = float(filtered_df["Price_in_Lakhs"].max())

    if min_price < max_price:
        price_range = st.sidebar.slider(
            "Property Price Range (Lakhs)",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price)
        )

        filtered_df = filtered_df[
            filtered_df["Price_in_Lakhs"].between(
                price_range[0],
                price_range[1]
            )
        ]

# Property size filter
if not filtered_df.empty:
    min_size = float(filtered_df["Size_in_SqFt"].min())
    max_size = float(filtered_df["Size_in_SqFt"].max())

    if min_size < max_size:
        size_range = st.sidebar.slider(
            "Property Size (Sq Ft)",
            min_value=min_size,
            max_value=max_size,
            value=(min_size, max_size)
        )

        filtered_df = filtered_df[
            filtered_df["Size_in_SqFt"].between(
                size_range[0],
                size_range[1]
            )
        ]

# Optional furnished-status filter
if "Furnished_Status" in filtered_df.columns:
    furnished_options = sorted(
        filtered_df["Furnished_Status"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_furnished = st.sidebar.multiselect(
        "Furnished Status",
        furnished_options,
        default=furnished_options
    )

    filtered_df = filtered_df[
        filtered_df["Furnished_Status"]
        .astype(str)
        .isin(selected_furnished)
    ]

st.sidebar.caption(
    f"Matching properties: {len(filtered_df):,}"
)

# ------------------------------------------------------------
# 5. HANDLE EMPTY FILTER RESULTS
# ------------------------------------------------------------

if filtered_df.empty:
    st.warning(
        "No properties match your filters. "
        "Please change your selections."
    )
    st.stop()

# ------------------------------------------------------------
# 6. KPI CARDS
# ------------------------------------------------------------

st.header("📊 Key Performance Indicators")

total_properties = len(filtered_df)

average_price = filtered_df["Price_in_Lakhs"].mean()

median_price = filtered_df["Price_in_Lakhs"].median()

average_price_sqft = filtered_df["Price_per_SqFt"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Properties",
    f"{total_properties:,}"
)

col2.metric(
    "Average Property Price",
    f"₹{average_price:,.2f} L"
)

col3.metric(
    "Median Property Price",
    f"₹{median_price:,.2f} L"
)

col4.metric(
    "Average Price / Sq Ft",
    f"₹{average_price_sqft:,.0f}"
)

st.divider()

# ------------------------------------------------------------
# 7. PRICE DISTRIBUTION
# ------------------------------------------------------------

st.header("📈 Property Price Analysis")

col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(
        filtered_df,
        x="Price_in_Lakhs",
        nbins=40,
        title="Distribution of Property Prices",
        labels={
            "Price_in_Lakhs": "Price (Lakhs)"
        }
    )

    fig.update_layout(
        xaxis_title="Property Price (Lakhs)",
        yaxis_title="Number of Properties"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    city_prices = (
        filtered_df.groupby("City", as_index=False)
        ["Price_in_Lakhs"]
        .mean()
        .sort_values(
            "Price_in_Lakhs",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        city_prices,
        x="City",
        y="Price_in_Lakhs",
        title="Top 10 Cities by Average Property Price",
        labels={
            "City": "City",
            "Price_in_Lakhs": "Average Price (Lakhs)"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# 8. PROPERTY TYPE COMPARISON
# ------------------------------------------------------------

st.header("🏘️ Property Type Analysis")

col1, col2 = st.columns(2)

with col1:
    type_prices = (
        filtered_df.groupby("Property_Type", as_index=False)
        ["Price_in_Lakhs"]
        .mean()
        .sort_values("Price_in_Lakhs", ascending=False)
    )

    fig = px.bar(
        type_prices,
        x="Property_Type",
        y="Price_in_Lakhs",
        title="Average Price by Property Type",
        labels={
            "Property_Type": "Property Type",
            "Price_in_Lakhs": "Average Price (Lakhs)"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.box(
        filtered_df,
        x="Property_Type",
        y="Price_in_Lakhs",
        title="Property Price Distribution by Type",
        labels={
            "Property_Type": "Property Type",
            "Price_in_Lakhs": "Price (Lakhs)"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# 9. SIZE VS PRICE
# ------------------------------------------------------------

st.header("📐 Property Size vs Price")

scatter_df = filtered_df.sample(
    n=min(5000, len(filtered_df)),
    random_state=42
)

fig = px.scatter(
    scatter_df,
    x="Size_in_SqFt",
    y="Price_in_Lakhs",
    color="Property_Type",
    hover_data=["City"],
    title="Relationship Between Property Size and Price",
    labels={
        "Size_in_SqFt": "Property Size (Sq Ft)",
        "Price_in_Lakhs": "Price (Lakhs)"
    }
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# 10. PRICE PER SQUARE FOOT BY STATE
# ------------------------------------------------------------

if "State" in filtered_df.columns:
    st.header("📍 Location Analysis")

    state_prices = (
        filtered_df.groupby("State", as_index=False)
        ["Price_per_SqFt"]
        .mean()
        .sort_values("Price_per_SqFt", ascending=False)
        .head(15)
    )

    fig = px.bar(
        state_prices,
        x="Price_per_SqFt",
        y="State",
        orientation="h",
        title="Average Price per Sq Ft by State",
        labels={
            "Price_per_SqFt": "Average Price per Sq Ft",
            "State": "State"
        }
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# 11. BHK ANALYSIS
# ------------------------------------------------------------

if "BHK" in filtered_df.columns:
    st.header("🛏️ BHK Analysis")

    bhk_data = (
        filtered_df.groupby("BHK", as_index=False)
        .agg(
            Property_Count=("BHK", "size"),
            Average_Price=("Price_in_Lakhs", "mean")
        )
        .sort_values("BHK")
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            bhk_data,
            x="BHK",
            y="Property_Count",
            title="Number of Properties by BHK",
            labels={
                "BHK": "Bedrooms (BHK)",
                "Property_Count": "Property Count"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            bhk_data,
            x="BHK",
            y="Average_Price",
            title="Average Price by BHK",
            labels={
                "BHK": "Bedrooms (BHK)",
                "Average_Price": "Average Price (Lakhs)"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# 12. BUSINESS RECOMMENDATIONS
# ------------------------------------------------------------

st.header("💡 Business Recommendations")

recommendations = []

# Recommendation 1: Compare city prices
city_summary = (
    filtered_df.groupby("City")
    ["Price_in_Lakhs"]
    .mean()
    .sort_values()
)

if len(city_summary) >= 2:
    lower_city = city_summary.index[0]
    higher_city = city_summary.index[-1]

    recommendations.append(
        f"**Compare locations:** {lower_city} has the lowest "
        f"average price among the currently filtered cities, "
        f"while {higher_city} has the highest. Investigate "
        f"rental demand, location quality, and resale prospects "
        f"before choosing a property."
    )

# Recommendation 2: Compare property types
type_summary = (
    filtered_df.groupby("Property_Type")
    ["Price_in_Lakhs"]
    .mean()
    .sort_values()
)

if len(type_summary) >= 2:
    recommendations.append(
        f"**Compare property types:** "
        f"{type_summary.index[0]} has the lowest average purchase "
        f"price in the filtered dataset. Compare maintenance costs, "
        f"expected rent, and resale demand before investing."
    )

# Recommendation 3: Price per square foot
if len(filtered_df) >= 2:
    median_sqft = filtered_df["Price_per_SqFt"].median()

    lower_price_properties = filtered_df[
        filtered_df["Price_per_SqFt"] < median_sqft
    ]

    recommendations.append(
        f"**Investigate relative value:** "
        f"{len(lower_price_properties):,} properties are priced "
        f"below the filtered dataset's median price per square foot "
        f"of ₹{median_sqft:,.0f}. Check property condition, "
        f"location, legal title, and comparable sales. A lower "
        f"price alone does not prove a property is undervalued."
    )

# Recommendation 4: Schools
if "Nearby_Schools" in filtered_df.columns:
    school_corr = filtered_df[
        ["Nearby_Schools", "Price_in_Lakhs"]
    ].corr().iloc[0, 1]

    if pd.notna(school_corr):
        if school_corr > 0.2:
            school_message = (
                "The data shows a positive association between "
                "nearby schools and property prices."
            )
        elif school_corr < -0.2:
            school_message = (
                "The data shows a negative association between "
                "nearby schools and property prices."
            )
        else:
            school_message = (
                "The relationship between nearby schools and "
                "property prices is weak in this filtered dataset."
            )

        recommendations.append(
            f"**Evaluate nearby schools:** {school_message} "
            "This is an association, not proof that schools "
            "cause prices to change."
        )

# Recommendation 5: Transport
if "Public_Transport_Accessibility" in filtered_df.columns:
    transport_summary = (
        filtered_df.groupby("Public_Transport_Accessibility")
        ["Price_in_Lakhs"]
        .mean()
        .sort_values(ascending=False)
    )

    if len(transport_summary) >= 2:
        recommendations.append(
            "**Evaluate connectivity:** Compare average prices "
            "across public transport accessibility categories. "
            "Consider commute times and access to employment "
            "centres alongside purchase price."
        )

if recommendations:
    for recommendation in recommendations:
        st.markdown(f"- {recommendation}")
else:
    st.info(
        "Select a broader range of properties to generate "
        "more comparisons."
    )

st.warning(
    "These recommendations are exploratory data insights, "
    "not guaranteed investment returns or personalized "
    "financial advice."
)

# ------------------------------------------------------------
# 13. PROPERTY PRICE ESTIMATOR
# ------------------------------------------------------------

st.header("🔮 Property Price Estimator")

st.write(
    "Estimate a property's current market price from its area "
    "and the median price per square foot in the filtered data. "
    "This is a simple benchmark, not a trained machine learning model."
)

col1, col2 = st.columns(2)

with col1:
    area_input = st.number_input(
        "Property Area (Sq Ft)",
        min_value=100,
        max_value=100000,
        value=1000,
        step=100
    )

with col2:
    price_per_sqft_input = st.number_input(
        "Price per Sq Ft (₹)",
        min_value=1,
        value=max(
            1,
            int(filtered_df["Price_per_SqFt"].median())
        ),
        step=100
    )

estimated_price = (
    area_input * price_per_sqft_input / 100000
)

st.metric(
    "Estimated Current Price",
    f"₹{estimated_price:,.2f} Lakhs"
)

st.caption(
    "This estimate multiplies the entered area by the entered "
    "price per square foot. It does not forecast future value "
    "or determine investment profitability."
)

# ------------------------------------------------------------
# 14. FILTERED DATA TABLE
# ------------------------------------------------------------

st.header("📋 Property Details")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Properties",
    data=csv_data,
    file_name="filtered_housing_properties.csv",
    mime="text/csv"
)

# ------------------------------------------------------------
# 15. FOOTER
# ------------------------------------------------------------

st.divider()

st.caption(
    "Real Estate Investment Advisor | Python | Pandas | "
    "Plotly | Streamlit"
)
