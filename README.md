# Datathon: Data-Driven Policy Innovation for Education

## Project Overview
This project analyzes UDISE (Unified District Information System for Education) 2024-25 datasets to derive actionable policy insights for improving public education service delivery at state and district levels. The analysis covers 2,942,946 schools across 36 states and union territories.

## Watch the dataset overview video: [Link](https://drive.google.com/file/d/1Dwh5R3MlQdEyC0Erke6tpOjKEkn0EgxP/view?usp=sharing)


## Problem Statement
How can open data be leveraged to design targeted, state/district level interventions that measurably improve public service delivery?

## Project Structure
```
.
├── data/                    # Raw and processed datasets
│   ├── raw/                # Original downloaded datasets
│   └── processed/          # Cleaned and merged datasets
├── src/                    # Python scripts
│   ├── data_processing.py  # Data loading and preprocessing
│   ├── analysis.py         # Statistical and ML analysis
│   └── visualization.py    # Visualization generation
├── visualizations/         # Generated charts and dashboards
│   └── 00_comprehensive_dashboard.html  # Main interactive dashboard
├── reports/                # Policy recommendations
│   └── Policy_Recommendations_UDISE_2024-25.md
├── visualization.py  # Visualization generation script (main execution)
└── requirements.txt        # Python dependencies
```

## Key Findings

1. **Geographic Concentration**: Uttar Pradesh alone accounts for 8.9% of all schools, with top 5 states representing 23.6% of total schools.

2. **Classification Gap**: 50% of schools lack proper rural-urban classification, limiting targeted policy planning.

3. **District Variation**: Significant variation exists at district level even within states, requiring sub-state targeting.

## Policy Recommendations

1. **State-Specific Resource Allocation**: Implement three-tier resource allocation framework based on state school density.

2. **Complete Rural-Urban Classification**: Mandate complete classification and establish differentiated infrastructure standards.

3. **District-Level Targeting**: Establish district-level performance monitoring and intervention frameworks.

## Deliverables

- Data analysis and visualization (2.9M schools analyzed)
- Modelling approach documentation (included in policy recommendations)
- Three key policy recommendations with data evidence
- Interactive dashboard (Plotly - 00_comprehensive_dashboard.html)

## How to View Results

1. **Policy Recommendations**: See `reports/Policy_Recommendations_UDISE_2024-25.md`

2. **Interactive Dashboard**: Open `visualizations/00_comprehensive_dashboard.html` in a web browser

3. **Additional Visualizations**: All visualization files are in the `visualizations/` folder

## Methodology

The analysis uses descriptive statistics, geographic aggregation, and comparative analysis across states and districts. Detailed methodology is documented in the policy recommendations document.

## Data Sources

- UDISE 2024-25 Dataset: Profile data for 2,942,946 schools
- Geographic identifiers: State, district, block level classification
- School characteristics: Type, category, rural-urban classification

