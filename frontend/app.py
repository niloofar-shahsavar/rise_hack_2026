import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib


# ------------------------------------------------------------
# Page config
# ------------------------------------------------------------
st.set_page_config(
    page_title="nordcast",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ------------------------------------------------------------
# Custom CSS
# ------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --bg: #0A1628;
            --card: rgba(13, 43, 85, 0.55);
            --card-border: rgba(232, 244, 248, 0.14);
            --accent: #00E5FF;
            --accent-soft: rgba(0, 229, 255, 0.16);
            --text: #E8F4F8;
            --muted: rgba(232, 244, 248, 0.68);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 10% 10%, rgba(0, 229, 255, 0.18), transparent 28%),
                radial-gradient(circle at 90% 20%, rgba(0, 120, 180, 0.16), transparent 26%),
                linear-gradient(135deg, #0A1628 0%, #07101F 48%, #061526 100%);
            color: var(--text);
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        div[data-testid="stToolbar"] {
            visibility: hidden;
            height: 0%;
            position: fixed;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 4.4rem;
            padding-bottom: 4rem;
        }

        .hero {
            position: relative;
            padding: 4rem 3.2rem;
            border: 1px solid var(--card-border);
            border-radius: 34px;
            background: linear-gradient(
                135deg,
                rgba(13, 43, 85, 0.68),
                rgba(13, 43, 85, 0.24)
            );
            box-shadow:
                0 24px 70px rgba(0, 0, 0, 0.32),
                inset 0 1px 0 rgba(255, 255, 255, 0.10);
            backdrop-filter: blur(22px);
            -webkit-backdrop-filter: blur(22px);
            overflow: hidden;
            animation: fadeUp 800ms ease-out both;
        }

        .hero::before {
            content: "";
            position: absolute;
            top: -90px;
            right: -90px;
            width: 260px;
            height: 260px;
            border-radius: 50%;
            background: rgba(0, 229, 255, 0.18);
            filter: blur(18px);
        }

        .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 0.55rem;
            margin-bottom: 1.25rem;
            padding: 0.52rem 0.84rem;
            border: 1px solid rgba(0, 229, 255, 0.28);
            border-radius: 999px;
            background: rgba(0, 229, 255, 0.09);
            color: var(--accent);
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent);
            box-shadow: 0 0 0 rgba(0, 229, 255, 0.7);
            animation: pulse 2s infinite;
        }

        .hero-title {
            margin: 0;
            font-size: clamp(3.6rem, 9vw, 7.7rem);
            line-height: 0.88;
            font-weight: 800;
            letter-spacing: -0.08em;
            color: var(--text);
        }

        .hero-title span {
            background: linear-gradient(90deg, #E8F4F8, #00E5FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .tagline {
            max-width: 700px;
            margin-top: 1.5rem;
            margin-bottom: 0;
            color: var(--muted);
            font-size: clamp(1.05rem, 2vw, 1.28rem);
            line-height: 1.7;
        }

        .section-gap {
            height: 1.6rem;
        }

        .glass-card {
            padding: 1.35rem;
            border: 1px solid var(--card-border);
            border-radius: 28px;
            background: var(--card);
            box-shadow:
                0 20px 55px rgba(0, 0, 0, 0.26),
                inset 0 1px 0 rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            animation: fadeUp 900ms ease-out both;
            transition: transform 220ms ease, border-color 220ms ease, box-shadow 220ms ease;
        }

        .glass-card:hover {
            transform: translateY(-3px);
            border-color: rgba(0, 229, 255, 0.32);
            box-shadow:
                0 26px 70px rgba(0, 0, 0, 0.34),
                0 0 38px rgba(0, 229, 255, 0.08),
                inset 0 1px 0 rgba(255, 255, 255, 0.10);
        }

        .chart-header {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            align-items: flex-start;
            margin-bottom: 1rem;
        }

        .chart-title {
            margin: 0;
            color: var(--text);
            font-size: 1.2rem;
            font-weight: 750;
            letter-spacing: -0.03em;
        }

        .chart-subtitle {
            margin: 0.38rem 0 0 0;
            color: var(--muted);
            font-size: 0.92rem;
            line-height: 1.5;
        }

        .badge {
            white-space: nowrap;
            padding: 0.55rem 0.82rem;
            border-radius: 999px;
            background: var(--accent-soft);
            border: 1px solid rgba(0, 229, 255, 0.22);
            color: var(--accent);
            font-size: 0.82rem;
            font-weight: 700;
        }

        .stat-card {
            min-height: 138px;
            padding: 1.35rem 1.25rem;
            border: 1px solid var(--card-border);
            border-radius: 24px;
            background: linear-gradient(145deg, rgba(13, 43, 85, 0.62), rgba(13, 43, 85, 0.28));
            box-shadow: 0 18px 48px rgba(0, 0, 0, 0.22);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            transition: transform 220ms ease, border-color 220ms ease;
            animation: fadeUp 1000ms ease-out both;
        }

        .stat-card:hover {
            transform: translateY(-4px);
            border-color: rgba(0, 229, 255, 0.35);
        }

        .stat-label {
            margin: 0;
            color: var(--muted);
            font-size: 0.82rem;
            font-weight: 650;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .stat-value {
            margin: 0.85rem 0 0 0;
            color: var(--text);
            font-size: clamp(1.7rem, 3vw, 2.45rem);
            font-weight: 800;
            letter-spacing: -0.05em;
        }

        .stat-note {
            margin: 0.45rem 0 0 0;
            color: rgba(232, 244, 248, 0.55);
            font-size: 0.9rem;
        }

        .footer-note {
            margin-top: 1.2rem;
            color: rgba(232, 244, 248, 0.48);
            font-size: 0.86rem;
            text-align: center;
        }

        @keyframes fadeUp {
            from {
                opacity: 0;
                transform: translateY(18px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes pulse {
            0% {
                box-shadow: 0 0 0 0 rgba(0, 229, 255, 0.65);
            }
            70% {
                box-shadow: 0 0 0 11px rgba(0, 229, 255, 0);
            }
            100% {
                box-shadow: 0 0 0 0 rgba(0, 229, 255, 0);
            }
        }

        /* Streamlit component refinements */
        div[data-testid="stVerticalBlock"] {
            gap: 1.2rem;
        }

        .js-plotly-plot,
        .plotly,
        .plot-container {
            border-radius: 22px;
            overflow: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# Placeholder data generation
# ------------------------------------------------------------
@st.cache_data
def load_real_data():
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Historisk data
    historical = pd.read_csv(os.path.join(BASE_DIR, "data", "clean", "clean_data.csv"))
    historical['ds'] = pd.to_datetime(historical['ds'])
    historical['year'] = historical['ds'].dt.year
    historical = historical.groupby('year')['y'].mean().reset_index()
    historical.columns = ['year', 'temperature']

    # ── Prophet ──
    prophet_model = joblib.load("../models/prophet_model.pkl")
    future = prophet_model.make_future_dataframe(periods=1461, freq='D')
    forecast = prophet_model.predict(future)
    forecast['year'] = forecast['ds'].dt.year
    forecast_yearly = forecast[forecast['year'] > 2026].groupby('year').agg({
        'yhat': 'mean',
        'yhat_lower': 'mean',
        'yhat_upper': 'mean'
    }).reset_index()
    forecast_yearly.columns = ['year', 'prophet', 'lower', 'upper']
    forecast_yearly['confidence'] = (forecast_yearly['upper'] - forecast_yearly['lower']) / 2
    forecast_yearly = forecast_yearly[forecast_yearly['year'] < 2030]

    # ── Linear Regression ──
    reg_model = joblib.load("../models/regression_model.pkl")
    last_date = pd.to_datetime("2026-01-31")
    min_date = pd.to_datetime("1996-04-02")
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=1461, freq='D')
    future_days = (future_dates - min_date).days.values.reshape(-1, 1)
    reg_pred = reg_model.predict(future_days)

    reg_df = pd.DataFrame({'ds': future_dates, 'yhat': reg_pred})
    reg_df['year'] = reg_df['ds'].dt.year
    reg_yearly = reg_df[reg_df['year'] < 2030].groupby('year')['yhat'].mean().reset_index()
    reg_yearly.columns = ['year', 'linear_regression']

    # ── Kombinera ──
    forecast_yearly = forecast_yearly.merge(reg_yearly, on='year', how='left')

    return historical, forecast_yearly



historical_df, forecast_df = load_real_data()

forecast_2029 = forecast_df.loc[forecast_df["year"] == 2029, "prophet"].iloc[0]
ci_2029 = forecast_df.loc[forecast_df["year"] == 2029, "confidence"].iloc[0]


# ------------------------------------------------------------
# Plotly chart
# ------------------------------------------------------------
def build_forecast_chart(historical: pd.DataFrame, forecast: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    # Confidence interval band
    fig.add_trace(
        go.Scatter(
            x=pd.concat([forecast["year"], forecast["year"][::-1]]),
            y=pd.concat([forecast["upper"], forecast["lower"][::-1]]),
            fill="toself",
            fillcolor="rgba(0, 229, 255, 0.13)",
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            name="Confidence interval",
            showlegend=True,
        )
    )

    # Historical temperature
    fig.add_trace(
        go.Scatter(
            x=historical["year"],
            y=historical["temperature"],
            mode="lines+markers",
            name="Historical temperature",
            line=dict(color="#E8F4F8", width=3),
            marker=dict(size=7, color="#E8F4F8"),
            hovertemplate="<b>%{x}</b><br>Observed: %{y:.2f}°C<extra></extra>",
        )
    )

    # Prophet forecast
    fig.add_trace(
        go.Scatter(
            x=forecast["year"],
            y=forecast["prophet"],
            mode="lines+markers",
            name="Prophet forecast",
            line=dict(color="#00E5FF", width=4),
            marker=dict(size=8, color="#00E5FF"),
            hovertemplate="<b>%{x}</b><br>Prophet forecast: %{y:.2f}°C<extra></extra>",
        )
    )

    # Linear regression forecast
    fig.add_trace(
        go.Scatter(
            x=forecast["year"],
            y=forecast["linear_regression"],
            mode="lines",
            name="Linear regression forecast",
            line=dict(color="#7EE7C8", width=3, dash="dash"),
            hovertemplate="<b>%{x}</b><br>Linear regression: %{y:.2f}°C<extra></extra>",
        )
    )

    fig.update_layout(
        height=520,
        margin=dict(l=24, r=24, t=20, b=24),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(5, 18, 34, 0.35)",
        font=dict(family="Inter", color="#E8F4F8"),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="left",
            x=0,
            font=dict(size=12, color="#E8F4F8"),
            bgcolor="rgba(13, 43, 85, 0.38)",
            bordercolor="rgba(232, 244, 248, 0.12)",
            borderwidth=1,
        ),
        xaxis=dict(
            title=None,
            showgrid=True,
            gridcolor="rgba(232, 244, 248, 0.08)",
            zeroline=False,
            tickfont=dict(color="rgba(232, 244, 248, 0.72)"),
            rangeslider=dict(visible=False),
        ),
        yaxis=dict(
    title=dict(
        text="Temperature anomaly / °C",
        font=dict(color="rgba(232, 244, 248, 0.62)")
    ),
    showgrid=True,
    gridcolor="rgba(232, 244, 248, 0.08)",
    zeroline=False,
    tickfont=dict(color="rgba(232, 244, 248, 0.72)"),
),
        modebar=dict(
            bgcolor="rgba(13, 43, 85, 0.58)",
            color="rgba(232, 244, 248, 0.68)",
            activecolor="#00E5FF",
        ),
    )

    fig.update_xaxes(showspikes=True, spikecolor="rgba(0, 229, 255, 0.35)")
    fig.update_yaxes(showspikes=True, spikecolor="rgba(0, 229, 255, 0.35)")

    return fig


chart = build_forecast_chart(historical_df, forecast_df)


# ------------------------------------------------------------
# UI
# ------------------------------------------------------------
st.markdown(
    """
    <section class="hero">
        <div class="eyebrow">
            <span class="pulse-dot"></span>
            Nordic climate intelligence
        </div>
        <h1 class="hero-title">nord<span>cast</span></h1>
        <p class="tagline">
            A minimal climate forecast dashboard for exploring long-term temperature trends,
            uncertainty ranges, and model comparisons across Nordic climate scenarios.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="stat-card">
            <p class="stat-label">Forecast 2029 temperature</p>
            <p class="stat-value">{forecast_2029:.2f}°C</p>
            <p class="stat-note">Prophet model estimate</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="stat-card">
            <p class="stat-label">Confidence interval</p>
            <p class="stat-value">±{ci_2029:.2f}°C</p>
            <p class="stat-note">Model uncertainty, 2029</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="stat-card">
            <p class="stat-label">Historical data</p>
            <p class="stat-value">30 years</p>
            <p class="stat-note">SMHI data: 1996–2026</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="glass-card">
        <div class="chart-header">
            <div>
                <h2 class="chart-title">Temperature forecast model comparison</h2>
                <p class="chart-subtitle">
                    Historical observations, Prophet-style forecast, confidence band,
                    and a linear regression baseline. Station Vinga A · 1996–2026 · Prophet vs Linear Regression.
                </p>
            </div>
            <div class="badge">Interactive chart</div>
        </div>
    """,
    unsafe_allow_html=True,
)

st.plotly_chart(chart, use_container_width=True, config={"displaylogo": False})

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <p class="footer-note">
        nordcast · SMHI data 1996–2026 · RISE Hackathon 2026
    </p>
    """,
    unsafe_allow_html=True,
)
