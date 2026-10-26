# 🏠 Real Estate Investment Advisor: Predicting Property Profitability & Future Value

## 📌 Project Overview

The **Real Estate Investment Advisor** is a data analytics and machine learning project designed to help users explore Indian housing data, compare property prices, and investigate potential real estate investment opportunities.

The project uses Python for data analysis and visualization and Streamlit to build an interactive dashboard.

The planned machine learning component includes classifying properties as good investments and estimating their future prices.

## 🎯 Project Objectives

- Analyze housing prices across Indian cities and states.
- Identify patterns in property prices and sizes.
- Compare property types, BHK configurations, and locations.
- Understand relationships between property prices and available amenities.
- Develop an interactive dashboard with filters and KPI cards.
- Provide data-driven business recommendations.
- Build machine learning models for investment classification and future price prediction.
- Track machine learning experiments using MLflow.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Data Analysis:** Pandas, NumPy
- **Data Visualization:** Matplotlib, Seaborn, Plotly
- **Dashboard:** Streamlit
- **Machine Learning:** Scikit-learn
- **Experiment Tracking:** MLflow
- **Version Control:** Git and GitHub

## 📂 Project Structure

```text
Real-Estate-Investment-Advisor/
│
├── data/
│   └── india_housing_prices.csv
│
├── outputs/
│   └── EDA charts
│
├── models/
│   └── Trained models (planned)
│
├── app.py
├── eda.py
├── clean_data.py
├── train_model.py
├── requirements.txt
└── README.md
```

*Note: The structure above describes the intended project organization. Include only files and folders that exist in your GitHub repository.*

## 📊 Dataset Description

The project uses the `india_housing_prices.csv` dataset.

Important features include:

| Column | Description |
|---|---|
| `State` | State where the property is located |
| `City` | Property city |
| `Locality` | Neighborhood of the property |
| `Property_Type` | Type of property |
| `BHK` | Number of bedrooms, hall, and kitchen |
| `Size_in_SqFt` | Property size in square feet |
| `Price_in_Lakhs` | Property price in lakhs |
| `Price_per_SqFt` | Price per square foot |
| `Year_Built` | Year the property was constructed |
| `Furnished_Status` | Furnishing status |
| `Nearby_Schools` | Nearby school information |
| `Nearby_Hospitals` | Nearby hospital information |
| `Parking_Space` | Parking availability |
| `Public_Transport_Accessibility` | Public transport accessibility |

## 🔍 Exploratory Data Analysis (EDA)

The EDA component examines:

- Dataset structure and data types.
- Missing values and duplicate records.
- Property price distribution.
- Property size distribution.
- Average property prices by city.
- Average price per square foot by state.
- Property price comparisons by property type.
- Relationships between property size and price.
- Correlations among numerical features.
- Property prices in relation to amenities and location characteristics.

## 📈 Dashboard Features

The Streamlit dashboard includes:

### 1. KPI Cards
- Total properties analyzed.
- Average property price.
- Median property price.
- Average price per square foot.

### 2. Interactive Filters
- State.
- City.
- Property type.
- BHK configuration.
- Property price range.
- Property size range.
- Furnishing status, when available.

### 3. Visualizations
- Property price distribution.
- Average property prices by city.
- Property type price comparison.
- Property size versus price.
- Price per square foot by state.
- BHK distribution and average prices.

### 4. Business Recommendations
The dashboard provides exploratory recommendations based on filtered property data, location comparisons, and price patterns.

### 5. Property Price Estimator
A simple estimator calculates an indicative current price using property area and price per square foot.

**Important:** This estimator is not a trained machine learning model and does not predict five-year future prices.

## 🤖 Machine Learning Objectives

The planned machine learning component includes two models:

**1. Investment Classification**

Classify properties as good investments or not good investments using a clearly documented labeling rule.

**2. Future Property Price Prediction**

Develop a regression model to estimate property prices after five years.

Historical price information or a justified appreciation assumption is needed to support meaningful future-price estimates. Classification labels should also be validated before the model is used for investment decisions.

MLflow will be used to track model experiments when that component is implemented.

## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone <your-github-repository-url>
```

Replace the placeholder with your actual GitHub repository URL.

### Step 2: Open the Project Folder

```bash
cd Real-Estate-Investment-Advisor
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Prepare the Dataset

Place `india_housing_prices.csv` in the project root or inside the `data/` folder, according to the paths supported by your scripts.

### Step 5: Run Exploratory Data Analysis

```bash
python eda.py
```

### Step 6: Run the Streamlit Dashboard

```bash
streamlit run app.py
```

The dashboard should open in your browser.

## 📦 Requirements

The project uses the following Python packages:

```text
pandas
numpy
matplotlib
seaborn
plotly
scikit-learn
streamlit
mlflow
joblib
```

Ensure that `requirements.txt` contains the dependencies needed by the scripts in your repository.

## 💼 Business Use Cases

- Help prospective buyers compare properties across locations.
- Support preliminary analysis of housing market prices.
- Explore property characteristics associated with higher prices.
- Assist real estate analysts in understanding property datasets.
- Provide an interactive interface for exploratory housing analysis.

## 📌 Expected Outcomes

- A cleaned housing dataset.
- Exploratory data analysis and visualizations.
- An interactive Streamlit dashboard.
- Data-driven property comparisons and recommendations.
- Machine learning models for investment classification and future-price estimation, once implemented and evaluated.
- Experiment tracking through MLflow, once integrated.

## ⚠️ Disclaimer

This project is intended for educational and analytical purposes. Dashboard comparisons and indicative price estimates do not guarantee property appreciation or investment returns. Users should independently verify property details, legal documentation, market conditions, and other relevant risks before making investment decisions.

## 👩‍💻 Author

**C Pujitha**

Aspiring Data Analyst | Python | SQL | Data Analytics | Machine Learning

## ⭐ Acknowledgment

This project was developed as a real estate analytics and machine learning learning project using Python and interactive data visualization tools.
