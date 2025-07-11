import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

team_colors = {
    "Red Bull Racing": "#1E41FF",
    "Ferrari": "#DC0000",
    "Mercedes": "#00D2BE",
    "McLaren": "#FF8700",
    "Aston Martin": "#006F62",
    "Alpine": "#0090FF",
    "Williams": "#005AFF",
    "Kick Sauber": "#52E252",
    "RB": "#6692FF",
    "Haas F1 Team": "#B6BABD"
}

country_flags = {
    "VER": "🇳🇱",
    "LEC": "🇲🇨",
    "HAM": "🇬🇧",
    "NOR": "🇬🇧",
    "SAI": "🇪🇸",
    "PER": "🇲🇽",
    "ALO": "🇪🇸",
    "PIA": "🇦🇺",
    "RUS": "🇬🇧",
    "ALB": "🇹🇭",
    "HUL": "🇩🇪",
    "STR": "🇨🇦",
    "ZHO": "🇨🇳",
    "TSU": "🇯🇵",
    "RIC": "🇦🇺",
    "OCO": "🇫🇷",
    "GAS": "🇫🇷",
    "BOT": "🇫🇮",
    "SAR": "🇺🇸",
    "MAG": "🇩🇰"
}

def load_session_data(session, d1, d2):
    laps1 = session.laps.pick_driver(d1).pick_quicklaps()
    laps2 = session.laps.pick_driver(d2).pick_quicklaps()
    return laps1, laps2

def plot_lap_times(laps1, laps2, d1, d2):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=laps1['LapNumber'], y=laps1['LapTime'].dt.total_seconds(),
        mode='lines+markers', name=d1
    ))
    fig.add_trace(go.Scatter(
        x=laps2['LapNumber'], y=laps2['LapTime'].dt.total_seconds(),
        mode='lines+markers', name=d2
    ))
    fig.update_layout(
        title='Lap Time Comparison',
        xaxis_title='Lap Number',
        yaxis_title='Lap Time (seconds)',
        template='plotly_dark'
    )
    return fig

def summarize_battle(laps1, laps2, d1, d2):
    avg1 = laps1['LapTime'].mean().total_seconds()
    avg2 = laps2['LapTime'].mean().total_seconds()

    # Fastest lap + lap number
    fastest1 = laps1.loc[laps1['LapTime'].idxmin()]
    fastest2 = laps2.loc[laps2['LapTime'].idxmin()]

    summary = {
        f"{d1} Avg Lap Time": f"{avg1:.3f} s",
        f"{d2} Avg Lap Time": f"{avg2:.3f} s",

        f"{d1} Fastest Lap": f"{fastest1['LapTime'].total_seconds():.3f} s (Lap {int(fastest1['LapNumber'])})",
        f"{d2} Fastest Lap": f"{fastest2['LapTime'].total_seconds():.3f} s (Lap {int(fastest2['LapNumber'])})",

        f"{d1} Tyre for Fastest Lap": f"{get_tyre_emoji(fastest1['Compound'])} {fastest1['Compound']}",
        f"{d2} Tyre for Fastest Lap": f"{get_tyre_emoji(fastest2['Compound'])} {fastest2['Compound']}",

        "Faster Driver": d1 if avg1 < avg2 else d2,
        "Avg Gap": f"{abs(avg1 - avg2):.3f} s/lap"
    }

    return summary

def get_driver_info(session, driver_code):
    driver = session.get_driver(driver_code)
    name = driver.FullName
    team = driver.TeamName
    color = team_colors.get(team, "#aaa")
    flag = country_flags.get(driver_code, "")
    return name, team, color, flag

def get_tyre_emoji(compound):
    tyre_colors = {
        "SOFT": "🔴",
        "MEDIUM": "🟡",
        "HARD": "⚪",
        "INTERMEDIATE": "🟢",
        "WET": "🔵"
    }
    return tyre_colors.get(compound.upper(), "❔")

def get_race_summary(session):
    summary = {
        "Track": session.event['EventName'],
        "Date": session.event['EventDate'].strftime("%d %b %Y"),
        "Winner": session.results.iloc[0]['FullName'],
        "Team": session.results.iloc[0]['TeamName']
    }

    try:
        fl = session.laps.pick_fastest()
        summary["Fastest Lap Driver"] = fl['Driver']
        summary["Fastest Lap Time"] = f"{fl['LapTime'].total_seconds():.3f}s"
        summary["Fastest Lap Tyre"] = fl['Compound']
    except Exception:
        summary["Fastest Lap Driver"] = "N/A"
        summary["Fastest Lap Time"] = "N/A"
        summary["Fastest Lap Tyre"] = "N/A"

    return summary



def format_podium_layout(results, country_flags):
    p1 = results.iloc[0]
    p2 = results.iloc[1]
    p3 = results.iloc[2]

    d1 = p1['Abbreviation']
    d2 = p2['Abbreviation']
    d3 = p3['Abbreviation']

    f1 = country_flags.get(d1, "")
    f2 = country_flags.get(d2, "")
    f3 = country_flags.get(d3, "")

    t1 = p1['TeamName']
    t2 = p2['TeamName']
    t3 = p3['TeamName']

    podium_html = f"""
    <div style='
        background: linear-gradient(to bottom right, #1e1e1e, #2a2a2a);
        border: 2px solid #444;
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
        color: #eee;
        font-family: monospace;
        text-align: center;
        max-width: 400px;
        margin-left: auto;
        margin-right: auto;
    '>

        <div style='font-size: 22px; font-weight: bold; color: gold;'>
            🥇 {d1} {f1}
            <div style='font-size: 14px; color: #ccc;'>{t1}</div>
        </div>

        <div style='display: flex; justify-content: space-between; margin-top: 20px;'>

            <div style='width: 45%; text-align: center; font-size: 18px; color: silver;'>
                🥈 {d2} {f2}
                <div style='font-size: 13px; color: #bbb;'>{t2}</div>
            </div>

            <div style='width: 45%; text-align: center; font-size: 18px; color: #cd7f32;'>
                🥉 {d3} {f3}
                <div style='font-size: 13px; color: #bbb;'>{t3}</div>
            </div>
        </div>

    </div>
    """
    return podium_html


def build_lap_delta_animation(laps1, laps2, d1, d2):
    df1 = laps1[['LapNumber', 'LapTime', 'Compound']].rename(columns={
        'LapTime': f'LapTime_{d1}', 'Compound': f'Compound_{d1}'
    })
    df2 = laps2[['LapNumber', 'LapTime', 'Compound']].rename(columns={
        'LapTime': f'LapTime_{d2}', 'Compound': f'Compound_{d2}'
    })

    df = pd.merge(df1, df2, on='LapNumber')
    df['Delta'] = df[f'LapTime_{d1}'].dt.total_seconds() - df[f'LapTime_{d2}'].dt.total_seconds()
    df['Faster'] = df['Delta'].apply(lambda x: d1 if x < 0 else d2)
    df['Hover'] = (
        "Lap " + df['LapNumber'].astype(str) + "<br>" +
        f"{d1} Tyre: " + df[f'Compound_{d1}'] + "<br>" +
        f"{d2} Tyre: " + df[f'Compound_{d2}']
    )
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['LapNumber'],
        y=df['Delta'],
        mode='lines+markers',
        name='Delta',
        line=dict(color='gray', width=2),
        showlegend=False
    ))

    frames = []
    for i in range(len(df)):
        frame_data = go.Scatter(
            x=[df.iloc[i]['LapNumber']],
            y=[df.iloc[i]['Delta']],
            mode='markers+text',
            marker=dict(size=18, color='#1f77b4' if df.iloc[i]['Faster'] == d1 else '#ff7f0e'),
            text=[df.iloc[i]['Faster']],
            textposition='top center',
            hovertext=[df.iloc[i]['Hover']],
            showlegend=False
        )
        frames.append(go.Frame(data=[frame_data], name=str(df.iloc[i]['LapNumber'])))

    fig.frames = frames

    fig.update_layout(
        title=f"Lap Time Delta Animation: {d1} vs {d2}",
        xaxis_title="LapNumber",
        yaxis_title=f"{d1} - {d2} Lap Time (s)",
        updatemenus=[{
            "type": "buttons",
            "buttons": [
                {"label": "Play", "method": "animate", "args": [None]},
                {"label": "Pause", "method": "animate", "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]},
            ]
        }],
        sliders=[{
            "steps": [
                {"args": [[str(df.iloc[i]['LapNumber'])], {"frame": {"duration": 300, "redraw": True}, "mode": "immediate"}],
                 "label": str(df.iloc[i]['LapNumber']),
                 "method": "animate"}
                for i in range(len(df))
            ],
            "transition": {"duration": 0},
            "x": 0, "y": -0.2,
            "currentvalue": {"prefix": "LapNumber=", "font": {"size": 16}},
        }],
        transition={"duration": 300}
    )

    return fig


def build_ghost_lap_animation(session, d1, d2):
    lap1 = session.laps.pick_driver(d1).pick_fastest()
    lap2 = session.laps.pick_driver(d2).pick_fastest()

    tel1 = lap1.get_telemetry().add_distance().reset_index(drop=True)
    tel2 = lap2.get_telemetry().add_distance().reset_index(drop=True)

    min_len = min(len(tel1), len(tel2))
    tel1 = tel1.iloc[:min_len]
    tel2 = tel2.iloc[:min_len]

    df = pd.DataFrame({
        'Distance': tel1['Distance'],
        'Speed_' + d1: tel1['Speed'],
        'Speed_' + d2: tel2['Speed'],
        'Frame': range(min_len)
    })

    df_melted = df.melt(
        id_vars=['Distance', 'Frame'],
        value_vars=[f'Speed_{d1}', f'Speed_{d2}'],
        var_name='Driver', value_name='Speed'
    )

    df_melted['Driver'] = df_melted['Driver'].apply(lambda x: x.split('_')[1])

    fig = px.scatter(
        df_melted,
        x='Distance',
        y='Speed',
        animation_frame='Frame',
        color='Driver',
        text='Driver',  # Label the dots with driver code
        labels={'Speed': 'Speed (km/h)', 'Distance': 'Distance (m)'},
        color_discrete_map={
            d1: '#1f77b4',
            d2: '#ff7f0e'
        },
        title=f"Ghost Lap Speed Animation: {d1} vs {d2}"
    )

    fig.update_traces(
        marker=dict(size=14, line=dict(width=2, color='white')),
        textposition='top center'
    )

    fig.update_layout(
        transition_duration=30,
        xaxis_range=[0, df['Distance'].max()],
        yaxis_range=[0, max(df[f'Speed_{d1}'].max(), df[f'Speed_{d2}'].max()) + 20]
    )

    return fig





