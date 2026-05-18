# rise_hack_2026
# nordcast 🌦️

Predictive climate analysis based on SMHI's open temperature data.  
Built at **RISE Hackathon 2026**.

## About

nordcast analyses 30 years of historical temperature data from SMHI and forecasts 4 years into the future with confidence intervals. We combine two models — linear regression as a baseline and Prophet as the main model — to deliver a credible and explainable prediction.

## Team

| Name | Role |
|---|---|
| Niloo | ML & Prediction — Prophet Backend & Integration (FastAPI)|
| Josefin | Data & Quality (cleaning, validation) |
| Sadia | Visualisation & Analysis (Plotly) |
| Dawit | Frontend + Linear Regression |

## Dataset

Source: [SMHI Open Data](https://www.smhi.se/data/meteorologi/ladda-ner-meteorologiska-observationer)

- `smhi-opendata_19_71380_199604_200603`
- `smhi-opendata_19_71380_200603_201602`
- `smhi-opendata_19_71380_201602_202601`

## Tech Stack

| Layer | Technology |
|---|---|
| Data | pandas |
| ML | scikit-learn, Prophet |
| Visualisation | Plotly |
| Backend | FastAPI |
| Frontend | Streamlit (React if time allows) |
| Language | Python 3 |

## Getting Started

```bash
pip install -r requirements.txt
jupyter notebook notebooks/eda.ipynb
```

## Project Structure

```
nordcast/
├── backend/
│   └── main.py          # FastAPI app
├── notebooks/
│   └── eda.ipynb        # Exploration & model training
├── models/
│   └── model.pkl        # Saved model
├── frontend/            # Streamlit or React
├── requirements.txt
└── README.md
```

## API

```
POST /predict
→ { temperature: 9.5, ci_lower: 9.0, ci_upper: 10.0 }
```

## Model Approach

We run two models in parallel and compare results:

- **Linear Regression** — baseline, captures long-term trend
- **Prophet** — main model, handles seasonality and outputs built-in confidence intervals