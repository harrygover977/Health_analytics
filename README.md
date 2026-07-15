# Health Analytics Dashboard

A simple designed dahsboard made with streamlit, that takes real world heart rate and sleep data and cleans, analyses
and displays patterns found across the month. 

Link - https://hr-sleep-analytics.streamlit.app/

---

## 🖼️ DashBoard Preview

<img width="1918" height="957" alt="Screenshot 2026-07-15 111515" src="https://github.com/user-attachments/assets/9ff61c61-f3cb-4d9a-9539-4997c8f3838a" />

<img width="1917" height="957" alt="Screenshot 2026-07-15 111541" src="https://github.com/user-attachments/assets/991a95c8-21ef-4084-8e93-1e67f6919230" />

<img width="1917" height="877" alt="Screenshot 2026-07-15 111554" src="https://github.com/user-attachments/assets/f67d546a-8231-41bd-a7c9-3d5ca2da7e27" />

<img width="1915" height="957" alt="image" src="https://github.com/user-attachments/assets/af34a8cb-4e6e-4645-98d6-faa6d57c8de8" />


---

## 📌 Overview

This project combines data cleaning and processing using the pandas library with data visualisation through matplotlib, 
numpy and streamlit, to create a clean, minimilistic dashboard that reveals information and patterns between monthly 
heart rate and sleep data. 

The goal was to explore real world data analyses of health data to help gain a better understanding of my metrics. 

---

## 🚀 Features

- Downloadable sample data
- CSV file upload capability
- Average heart rate and sleep metrics
- Line graphs showing variation in heart rate and sleep
- A pie chart providing a detailed sleep stage breakdown
- A bar chart showing accumulated sleep dept across the month
- A distribution of average daily heart rate across the month

---

## 🛠️ Tech Stack

- Python 3.13.1
- Pandas
- Numpy
- Matplotlib
- Streamlit

---

## 💻 Work Flow

1. Upload Data to dashboards side bar
2. Data is cleaned and merged into a single, workable dataframe
3. Data is the processed using matplotlib 
4. The data displayed in a simple, understandable format on a streamlit dashboard.

---

## 🧪 Challenges & Solutions 

### Formatting the date to be worked with

Problem: The date was given in the form YYYY-MM-DD

Solution: Formatted the date as two digit numbers representing the day of the month (e.g. 2026-06-01 -> 01)

### Relative file path of sample data

problem: The relative file path was not recognised by streamlits Linux system

Solution: Dynamically updated the base directory using: BASE_DIR = Path(__file__).resolve().parent.parent

## 📈 What this Project Matters

This project demonstrates:
  - The ability to work with messy data, manipulating it into a workable format
  - The visualisation of data using python framworks
  - The understanding of relationships between data
  - The uderstanding of downloading and uploading csv files

  It relfects core skills required for data analyses and visualisation, an important aspect of AI/ML engineering. 

