# 📊 Sales Data Analysis Dashboard

A Python-based project for **cleaning, transforming, analyzing, and visualizing sales data**.
The project uses the Superstore dataset and provides an interactive dashboard for exploring sales and business performance.

## ✨ Features

* Load and inspect raw sales data
* Handle missing values and duplicates
* Clean and transform the dataset
* Analyze sales, profit, products, categories, and regions
* Generate interactive charts
* Display insights through a Streamlit dashboard

## 🏗️ Project Structure

```text
Sales-Data-Analysis-Dashboard/
│
├── data/
│   └── raw/
│       └── superstore.csv
│
├── dashboard/
│   ├── app.py
│   └── charts.py
│
├── src/
│   ├── data_loader.py
│   ├── data_cleaning.py
│   ├── data_transformation.py
│   ├── data_analysis.py
│   └── visualization.py
│
├── main.py
├── requirements.txt
└── README.md
```

## 🛠️ Technologies

* **Python** — Core development
* **Pandas** — Data processing and analysis
* **Plotly** — Interactive visualizations
* **Streamlit** — Dashboard
* **Rich** — Data inspection in the CLI
* **Git & GitHub** — Version control

## 🔄 Workflow

```text
Raw Data
   ↓
Load & Inspect
   ↓
Clean
   ↓
Transform
   ↓
Analyze
   ↓
Visualize
   ↓
Dashboard
```

## 📊 Dashboard

The dashboard provides an overview of:

* Total sales and profit
* Sales trends
* Category and sub-category performance
* Regional performance
* Product performance
* Key business metrics

## 🚀 Getting Started

Clone the repository and install the dependencies:

```bash
git clone https://github.com/YOUR_USERNAME/Sales-Data-Analysis-Dashboard.git
cd Sales-Data-Analysis-Dashboard
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run dashboard/app.py
```

## 🚧 Status

**In Development**

Future improvements will include additional analysis, filters, visualizations, and dashboard features.

## 👩‍💻 Author

**Hagar Mohamed**
