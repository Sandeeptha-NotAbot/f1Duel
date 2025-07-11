import streamlit as st
import fastf1
from utils import get_driver_info, load_session_data, plot_lap_times, summarize_battle, get_race_summary, format_podium_layout, country_flags
import streamlit.components.v1 as components
from utils import build_lap_delta_animation
from utils import build_ghost_lap_animation

fastf1.Cache.enable_cache('cache')  # Save session data locally

st.set_page_config(page_title="f1Duel", layout="wide")
st.title("f1Duel: A Head-to-Head Driver Battle Analyzer")

year = st.selectbox("Select Season", list(range(2021, 2025))[::-1])
race = st.text_input("Enter Race Name (e.g., Spain, Monaco, Abu Dhabi)", value="Spain")
session_type = st.selectbox("Select Session", ["Race", "Qualifying", "Practice 1", "Practice 2"])

try:
    session = fastf1.get_session(year, race, session_type)
    session.load()

    race_info = get_race_summary(session)

    st.markdown(f"""
    <div style='border:2px solid #666; border-radius:10px; padding:20px; background-color:#111; font-size:16px; color:#eee'>

    <h3>📋 Race Summary</h3>

    🏟️ <b>Track:</b> {race_info["Track"]}  
    📅 <b>Date:</b> {race_info["Date"]}  
    🏆 <b>Winner:</b> {race_info["Winner"]} ({race_info["Team"]})  
    🏎️ <b style='color:#d0aaff;'>Fastest Lap:</b> 
    <span style='color:#d0aaff; font-weight:bold;'>{race_info["Fastest Lap Driver"]}</span>  
    <span style='color:#fff;'>– {race_info["Fastest Lap Time"]} on {race_info["Fastest Lap Tyre"]}</span>

    🎖️ <b>Podium:</b>

    </div>
    """, unsafe_allow_html=True)
    components.html(format_podium_layout(session.results.head(3), country_flags), height=300)
    st.balloons()  



    drivers = session.laps['Driver'].unique().tolist()
    d1 = st.selectbox("Select Driver 1", drivers)
    d2 = st.selectbox("Select Driver 2", [d for d in drivers if d != d1])
    name1, team1, color1, flag1 = get_driver_info(session, d1)
    name2, team2, color2, flag2 = get_driver_info(session, d2)


    laps1, laps2 = load_session_data(session, d1, d2)

    st.plotly_chart(plot_lap_times(laps1, laps2, d1, d2))

    st.subheader("📊 Battle Summary")

    summary = summarize_battle(laps1, laps2, d1, d2)

    st.markdown(f"""
    <div style='border:2px solid #888; border-radius:10px; padding:20px; background-color:#111; font-size:17px'>

    <h3 style='text-align:center;'>
    {flag1} <span style="color:{color1}">{d1}</span> ({team1}) vs {flag2} <span style="color:{color2}">{d2}</span> ({team2})
    </h3>


    🕑 <b>{d1} Avg Lap Time:</b> {summary[f"{d1} Avg Lap Time"]}  
    🕑 <b>{d2} Avg Lap Time:</b> {summary[f"{d2} Avg Lap Time"]}  

    💨 <b>{d1} Fastest Lap:</b> {summary[f"{d1} Fastest Lap"]} on 🛞 {summary[f"{d1} Tyre for Fastest Lap"]}  
    💨 <b>{d2} Fastest Lap:</b> {summary[f"{d2} Fastest Lap"]} on 🛞 {summary[f"{d2} Tyre for Fastest Lap"]}  

    🚀 <b>Faster Driver:</b> <span style="color:#0f0">{summary['Faster Driver']}</span>  
    ⏱️ <b>Average Gap:</b> {summary['Avg Gap']}

    </div>
    """, unsafe_allow_html=True)

    st.subheader("🎞️ Lap-by-Lap Delta Animation")

    st.plotly_chart(build_lap_delta_animation(laps1, laps2, d1, d2))

    st.subheader("Ghost Lap Speed Animation")

    st.plotly_chart(build_ghost_lap_animation(session, d1, d2))



except Exception as e:
    st.warning(f"⚠️ Error loading session: {e}")
