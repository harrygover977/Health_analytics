from analysis import *
from clean_data import *
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

hr_file_path = BASE_DIR / "data" / "sample" / "heartRate.csv"
sleep_file_path = BASE_DIR / "data" / "sample" / "sleep.csv"

if "hr_csv" not in st.session_state:
    st.session_state["hr_csv"] = None
    
    
if "sleep_csv" not in st.session_state:
    st.session_state["sleep_csv"] = None

def main():
    st.set_page_config(layout="wide", page_title="Health Dashboard", page_icon="📈")
    
    with st.sidebar:
        st.title("📁 Data Upload")
        with st.form("My form"):
            st.session_state["hr_csv"] = st.file_uploader("Heart Rate File", type=["csv"])
            st.caption("Column Format: date,heartRate")
            st.session_state["sleep_csv"] = st.file_uploader("Sleep File", type=["csv"])
            st.caption("Column Format: date,deepSleepTime,shallowSleepTime,wakeTime,start,stop,REMTime")
            st.form_submit_button()
        
    if st.session_state["hr_csv"] == None or st.session_state["sleep_csv"] == None:
        st.info("📊 No data available yet — upload your Heart Rate and Sleep CSV files above to get started.")
        st.title("Sample Data", text_alignment="center")
        st.divider()
        with open(hr_file_path, "rb") as f:
            st.download_button(
                label="heart rate data ⬇️",
                data=f,
                file_name="heartRate.csv",
                mime="text/csv"
            )
            
        with open(sleep_file_path, "rb") as f:
            st.download_button(
                label="sleep data ⬇️",
                data=f,
                file_name="sleep.csv",
                mime="text/csv"
            )
            
    else:
        hr_df = pd.read_csv(st.session_state["hr_csv"], encoding="utf-8-sig", escapechar="\\")
        sleep_df = pd.read_csv(st.session_state["sleep_csv"], encoding="utf-8-sig", escapechar="\\")
        
        hr_df.to_csv("../data/cleaned/hr_data_cleaned.csv", index=False)
        sleep_df.to_csv("../data/cleaned/sleep_data_cleaned.csv", index=False)
        
        df = clean_data(hr_df, sleep_df)
        
        avg_hr = average_heartrate(df)
        avg_sleep_hrs, avg_sleep_mins = average_sleep_time(df)
        avg_bedtime_hrs, avg_bedtime_mins = average_bedtime(df)
        avg_wake_hrs, avg_wake_mins = average_waketime(df)
        
        tab1, tab2, tab3 = st.tabs(["Overview", "Sleep", "Heart Rate"])
        
        date = df["date"]
        heart_rate = df["heartRate"]
        total_sleep_time = df["totalSleepTime"]
        bedtime = df["start"]
        deep_time, rem_time, shallow_time, wake_time = average_sleep_stages(df)
        monthly_sleep_hrs, monthly_sleep_mins = monthly_sleep_time(total_sleep_time)
        dept_hrs, dept_mins = sleep_dept(total_sleep_time)
        min_hr, max_hr, hr_std = hr_stats(heart_rate)
        
        # --- Overview Tab ---
        with tab1:
            
            st.title("Overview", text_alignment="center")
            st.divider()
            
            # --- Summary Statistics ---
            with st.container(border=True):
                col11, col12, col13 = st.columns(3, gap="medium")
                
                with col11:
                    st.metric(label="Avg HR:", value=f"{avg_hr} bpm")
                    
                with col12:
                    st.metric(label="Avg Sleep Time:", value=f"{avg_sleep_hrs}h {avg_sleep_mins}m")
                
                with col13:
                    st.metric(label="Avg Bedtime:", value=f"{avg_bedtime_hrs}:{avg_bedtime_mins}")
            
            st.write("")
            
            col21, col22 = st.columns(2)
            
            # --- Heart rate overe time graph ---
            with col21:
                with st.container(border=True):
                    st.subheader("Heart Rate Over Time")
                    fig, ax = plt.subplots(figsize=(6, 3.5))
                    ax.plot(date, heart_rate,
                            color="#E6727B",
                            linewidth=2,
                            marker="o",
                            markeredgecolor="white",
                            markeredgewidth=1)
                    ax.set_xlabel("Day of the Month")
                    ax.set_ylabel("Heart Rate (bpm)")
                    ax.spines["top"].set_visible(False)
                    ax.spines["right"].set_visible(False)
                    ax.grid(axis="y", alpha=0.3)
                    fig.tight_layout()
                    st.pyplot(fig)

            # --- Time asleep over time graph ---
            with col22:
                with st.container(border=True):
                    st.subheader("Time Asleep Over Time")
                    fig, ax = plt.subplots(figsize=(6, 3.5))
                    ax.plot(date, total_sleep_time,
                            color="#61879E",
                            linewidth=2, 
                            marker="o",
                            markeredgecolor="white",
                            markeredgewidth=1)
                    
                    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_time))
                    ax.set_xlabel("Day of the Month")
                    ax.set_ylabel("Time Asleep (HH:MM)")
                    ax.spines["top"].set_visible(False)
                    ax.spines["right"].set_visible(False)
                    ax.grid(axis="y", alpha=0.3)
                    fig.tight_layout()
                    st.pyplot(fig)
            
        # --- Sleep Tab ---     
        with tab2:
            st.title("Sleep", text_alignment="center")
            st.divider()
            
            col1, col2 = st.columns(2)
            
            # --- Bedtime over time graph ---
            with col1:
                with st.container(border=True):
                    st.subheader("Bedtime Over Time")
                    fig, ax = plt.subplots(figsize=(6, 3.5))
                    
                    ax.plot(
                        date, bedtime,
                        color="#1D3557",
                        linewidth=2,
                        marker="o",
                        markersize=5,
                        markerfacecolor="#1D3557",
                        markeredgecolor="white",
                        markeredgewidth=1,
                    )
                    
                    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_time))
                    ax.set_xlabel("Day of the Month")
                    ax.set_ylabel("Bedtime")
                    ax.spines["top"].set_visible(False)
                    ax.spines["right"].set_visible(False)
                    ax.grid(axis="y", alpha=0.3)
                    
                    fig.tight_layout()
                    st.pyplot(fig)
                    
            # --- Average sleep stage breakdown pie chart ---        
            with col2:
                with st.container(border=True):
                    st.subheader("Average Sleep Stage Breakdown")
                    fig, ax = plt.subplots(figsize=(6, 3.5))
                    labels = ["Deep Sleep", "REM Sleep", "Shallow Sleep", "Time Awake"]
                    colors = ["#1D3557", "#457B9D", "#A8DADC", "#E63946"]
                    wedges, _, autotexts = ax.pie(
                        [deep_time, rem_time, shallow_time, wake_time],
                        labels=None,
                        colors=colors,
                        autopct="%1.0f%%",
                        pctdistance=0.75,
                        startangle=90,
                        counterclock=False,
                        wedgeprops={"edgecolor": "white", "linewidth": 2, "width": 0.4},
                    )
                    for text in autotexts:
                        text.set_color("white")
                        text.set_fontsize(9)
                        text.set_fontweight("bold")
                    ax.legend(
                        wedges, labels,
                        loc="center left",
                        bbox_to_anchor=(1, 0.5),
                        frameon=False,
                    )
                    fig.tight_layout()
                    st.pyplot(fig)
        
            st.write("")
            
            # --- Sleep Dept Information ---
            with st.container(border=True):
                
                st.subheader("Sleep Dept")
                col3, col4 = st.columns(2, gap="large")
                
                with col3:
                    fig, ax = plt.subplots(figsize=(6, 3.5))

                    goal = 480
                    min_threshold = 420
                    colors = [sleep_bar_color(val) for val in total_sleep_time]

                    ax.set_ylabel("Time Asleep (HH:MM)")
                    ax.set_xlabel("Day of the Month")
                    
                    ax.axhline(y=goal, color="#444444", linestyle="--", linewidth=1, zorder=2)
                    ax.text(32, goal, "8h", ha="right", va="bottom",
                    fontsize=9, color="#444444")
                    
                    ax.bar(date, total_sleep_time, width=1, color=colors,
                        edgecolor="white", linewidth=0.5)

                    # Axis formatting
                    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_time))
                    ax.set_ylim(300, 550)

                    # Strip visual noise, add a light grid for readability
                    ax.spines["top"].set_visible(False)
                    ax.spines["right"].set_visible(False)
                    ax.spines["left"].set_visible(False)
                    ax.grid(axis="y", color="#e0e0e0", linewidth=0.8, zorder=0)
                    ax.set_axisbelow(True)

                    ax.tick_params(axis="x", rotation=45)

                    fig.tight_layout()
                    st.pyplot(fig)
                    
                with col4:
                    st.metric("Goal: ", f"{8 * len(date)}h/Month")
                    st.metric("Actual: ", f"{monthly_sleep_hrs}h {monthly_sleep_mins}m/Month")
                    st.metric("Dept: ","", delta=f"{dept_hrs}h {dept_mins}m")
            
            with st.container(border=True):
                
                col5, col6, col7 = st.columns(3, gap="medium")
                
                with col5:
                    st.metric("Avg Sleep Time: ", f"{avg_sleep_hrs}h {avg_sleep_mins}m")
                
                with col6:
                    st.metric("Avg Bedtime: ", f"{avg_bedtime_hrs}:{avg_bedtime_mins}")
                    
                with col7:
                    st.metric("Avg Time Awake: ", f"{avg_wake_hrs}h {avg_wake_mins :02d}m")
            
        with tab3:
            st.title("Heart Rate", text_alignment="center")
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                with st.container(border=True):
                    fig, ax = plt.subplots(figsize=(6, 3.5))

                    bins = [50, 52, 54, 56, 58, 60, 62, 64, 66]
                    ax.hist(heart_rate, bins=bins, color="#457B9D", edgecolor="white",
                            linewidth=0.8, zorder=3)

                    # Strip clutter, add light grid
                    ax.spines["top"].set_visible(False)
                    ax.spines["right"].set_visible(False)
                    ax.spines["left"].set_visible(False)
                    ax.grid(axis="y", color="#e0e0e0", linewidth=0.7, zorder=0)
                    ax.set_axisbelow(True)

                    ax.set_title("Heart Rate Distribution", fontsize=13, fontweight="bold", loc="left", pad=10)
                    ax.set_xlabel("Heart Rate (bpm)", fontsize=10)
                    ax.set_ylabel("Frequency", fontsize=10)

                    fig.tight_layout()
                    st.pyplot(fig)  
            
            with col2:
                with st.container(border=True):
                    st.metric("Avg HeartRate: ", f"{avg_hr} bpm")
                    st.metric("Min HeartRate: ", f"{min_hr} bpm")
                    st.metric("Max HeartRate: ", f"{max_hr} bpm")
                    st.metric("Standard Deviation: ", f"{hr_std} bpm")
                      
if __name__ == "__main__":
    main()


