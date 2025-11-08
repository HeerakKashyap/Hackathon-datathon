

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import os

print("=" * 80)
print("CREATING VISUALIZATIONS - UDISE 2024-25")
print("=" * 80)

output_dir = Path('visualizations')
output_dir.mkdir(exist_ok=True)

print("\nLoading data...")
df = pd.read_csv('data/processed/merged_2024-25.csv', low_memory=False)
print(f"Loaded: {df.shape[0]:,} schools")

print("\n1. Creating state-wise school distribution chart...")

state_counts = df['state'].value_counts().reset_index()
state_counts.columns = ['State', 'School_Count']
state_counts = state_counts.sort_values('School_Count', ascending=False)

fig1 = px.bar(
    state_counts.head(20),
    x='State',
    y='School_Count',
    title='Top 20 States by School Count (UDISE 2024-25)',
    labels={'School_Count': 'Number of Schools', 'State': 'State'},
    color='School_Count',
    color_continuous_scale='Viridis'
)
fig1.update_layout(
    xaxis_tickangle=-45,
    height=600,
    showlegend=False,
    title_font_size=16
)
fig1.write_html(str(output_dir / '01_state_school_distribution.html'))
print("   Saved: 01_state_school_distribution.html")

print("\n2. Creating rural-urban distribution chart...")

ru_counts = df['rural_urban'].value_counts().sort_index()
ru_labels = {1.0: 'Rural', 2.0: 'Urban'}
ru_data = pd.DataFrame({
    'Type': [ru_labels.get(k, f'Type {k}') for k in ru_counts.index],
    'Count': ru_counts.values,
    'Percentage': (ru_counts.values / len(df) * 100).round(1)
})

fig2 = px.pie(
    ru_data,
    values='Count',
    names='Type',
    title='Rural-Urban School Distribution',
    hole=0.4
)
fig2.update_traces(textposition='inside', textinfo='percent+label')
fig2.update_layout(height=500)
fig2.write_html(str(output_dir / '02_rural_urban_distribution.html'))
print("   Saved: 02_rural_urban_distribution.html")


print("\n3. Creating state-wise rural-urban breakdown...")

state_ru = df.groupby(['state', 'rural_urban']).size().reset_index(name='count')
state_ru['Type'] = state_ru['rural_urban'].map(ru_labels).fillna('Other')
state_ru = state_ru[state_ru['state'].isin(state_counts.head(15)['State'].values)]

fig3 = px.bar(
    state_ru,
    x='state',
    y='count',
    color='Type',
    title='Rural-Urban Distribution by State (Top 15 States)',
    labels={'count': 'Number of Schools', 'state': 'State'},
    barmode='group'
)
fig3.update_layout(
    xaxis_tickangle=-45,
    height=600
)
fig3.write_html(str(output_dir / '03_state_rural_urban.html'))
print("   Saved: 03_state_rural_urban.html")


print("\n4. Creating district-wise distribution for top states...")

top_states = state_counts.head(5)['State'].tolist()
district_counts = df[df['state'].isin(top_states)].groupby(['state', 'district']).size().reset_index(name='school_count')
district_counts = district_counts.sort_values('school_count', ascending=False).head(30)

fig4 = px.bar(
    district_counts,
    x='district',
    y='school_count',
    color='state',
    title='Top 30 Districts by School Count (Top 5 States)',
    labels={'school_count': 'Number of Schools', 'district': 'District'},
    barmode='group'
)
fig4.update_layout(
    xaxis_tickangle=-45,
    height=700
)
fig4.write_html(str(output_dir / '04_top_districts.html'))
print("   Saved: 04_top_districts.html")


print("\n5. Creating school type distribution...")

if 'school_type' in df.columns:
    type_counts = df['school_type'].value_counts().head(10).reset_index()
    type_counts.columns = ['School_Type', 'Count']
    
    fig5 = px.bar(
        type_counts,
        x='School_Type',
        y='Count',
        title='School Type Distribution (Top 10)',
        labels={'Count': 'Number of Schools', 'School_Type': 'School Type'},
        color='Count',
        color_continuous_scale='Blues'
    )
    fig5.update_layout(height=500, showlegend=False)
    fig5.write_html(str(output_dir / '05_school_types.html'))
    print("   Saved: 05_school_types.html")

print("\n6. Creating school category distribution...")

if 'school_category' in df.columns:
    cat_counts = df['school_category'].value_counts().head(10).reset_index()
    cat_counts.columns = ['Category', 'Count']
    cat_counts['Percentage'] = (cat_counts['Count'] / len(df) * 100).round(1)
    
    fig6 = px.bar(
        cat_counts,
        x='Category',
        y='Count',
        title='School Category Distribution (Top 10)',
        labels={'Count': 'Number of Schools', 'Category': 'Category'},
        text='Percentage'
    )
    fig6.update_traces(textposition='outside', texttemplate='%{text}%')
    fig6.update_layout(height=500, showlegend=False)
    fig6.write_html(str(output_dir / '06_school_categories.html'))
    print("   Saved: 06_school_categories.html")

print("\n7. Creating state-wise school density visualization...")

state_density = state_counts.copy()
state_density['Density_Rank'] = state_density['School_Count'].rank(ascending=False)

fig7 = px.scatter(
    state_density.head(20),
    x='State',
    y='School_Count',
    size='School_Count',
    color='School_Count',
    title='School Distribution by State (Bubble Chart)',
    labels={'School_Count': 'Number of Schools', 'State': 'State'},
    color_continuous_scale='Reds'
)
fig7.update_layout(
    xaxis_tickangle=-45,
    height=600,
    showlegend=False
)
fig7.write_html(str(output_dir / '07_state_density.html'))
print("   Saved: 07_state_density.html")

print("\n8. Creating comprehensive interactive dashboard...")

# Create subplots
fig_dashboard = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        'Top 15 States by School Count',
        'Rural-Urban Distribution',
        'Top 10 Districts (All States)',
        'School Type Distribution'
    ),
    specs=[
        [{"type": "bar"}, {"type": "pie"}],
        [{"type": "bar"}, {"type": "bar"}]
    ]
)

# Chart 1: Top states
fig_dashboard.add_trace(
    go.Bar(x=state_counts.head(15)['State'], y=state_counts.head(15)['School_Count'],
           name='Schools', marker_color='lightblue'),
    row=1, col=1
)

# Chart 2: Rural-Urban pie
fig_dashboard.add_trace(
    go.Pie(labels=ru_data['Type'], values=ru_data['Count'], name='Distribution'),
    row=1, col=2
)

# Chart 3: Top districts
top_districts_all = df.groupby('district').size().sort_values(ascending=False).head(10)
fig_dashboard.add_trace(
    go.Bar(x=top_districts_all.index, y=top_districts_all.values,
           name='Districts', marker_color='lightgreen'),
    row=2, col=1
)

# Chart 4: School types
if 'school_type' in df.columns:
    type_data = df['school_type'].value_counts().head(5)
    fig_dashboard.add_trace(
        go.Bar(x=[str(x) for x in type_data.index], y=type_data.values,
               name='Types', marker_color='lightcoral'),
        row=2, col=2
    )

fig_dashboard.update_layout(
    height=1000,
    title_text="UDISE 2024-25 Education Dashboard",
    showlegend=True,
    title_font_size=20
)

fig_dashboard.update_xaxes(tickangle=-45, row=1, col=1)
fig_dashboard.update_xaxes(tickangle=-45, row=2, col=1)
fig_dashboard.update_xaxes(tickangle=-45, row=2, col=2)

fig_dashboard.write_html(str(output_dir / '00_comprehensive_dashboard.html'))
print("   Saved: 00_comprehensive_dashboard.html")

# STATE COMPARISON TABLE

print("\n9. Creating state comparison summary...")

state_summary = df.groupby('state').agg({
    'pseudocode': 'count',
    'rural_urban': lambda x: (x == 1.0).sum()  # Rural count
}).rename(columns={'pseudocode': 'Total_Schools', 'rural_urban': 'Rural_Schools'})
state_summary['Urban_Schools'] = df.groupby('state')['rural_urban'].apply(lambda x: (x == 2.0).sum())
state_summary['Rural_Percentage'] = (state_summary['Rural_Schools'] / state_summary['Total_Schools'] * 100).round(1)
state_summary = state_summary.sort_values('Total_Schools', ascending=False).reset_index()

# interactive table
fig_table = go.Figure(data=[go.Table(
    header=dict(
        values=['State', 'Total Schools', 'Rural Schools', 'Urban Schools', 'Rural %'],
        fill_color='paleturquoise',
        align='left',
        font=dict(size=12, color='black')
    ),
    cells=dict(
        values=[
            state_summary['state'].head(20),
            state_summary['Total_Schools'].head(20),
            state_summary['Rural_Schools'].head(20),
            state_summary['Urban_Schools'].head(20),
            state_summary['Rural_Percentage'].head(20)
        ],
        fill_color='lavender',
        align='left',
        font=dict(size=11)
    )
)])

fig_table.update_layout(
    title='State-wise School Distribution Summary (Top 20)',
    height=700
)
fig_table.write_html(str(output_dir / '08_state_comparison_table.html'))
print("   Saved: 08_state_comparison_table.html")

state_summary.to_csv(output_dir / 'state_summary.csv', index=False)
print("   Saved: state_summary.csv")
