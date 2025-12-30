import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def plot_readiness_radar(profile_data):
    categories = ['Technical Skills', 'Experience', 'Soft Skills', 'Market Match', 'Education']
    
    # Mock scores ensuring they exist
    scores = [
        profile_data.get('readiness_score', 60), 
        70, 
        85, 
        profile_data.get('readiness_score', 60) + 10, 
        90
    ]
    
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
      r=scores,
      theta=categories,
      fill='toself',
      name='Candidate Profile',
      line_color='#00C9FF'
    ))

    fig.add_trace(go.Scatterpolar(
      r=[80, 80, 80, 80, 80],
      theta=categories,
      name='Market Average',
      line_color='#2ea043',
      line_dash='dash'
    ))

    fig.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 100],
          gridcolor='rgba(255, 255, 255, 0.1)',
          linecolor='rgba(255, 255, 255, 0.1)'
        ),
        bgcolor='rgba(0,0,0,0)'
      ),
      paper_bgcolor='rgba(0,0,0,0)',
      font=dict(color='white'),
      showlegend=True,
      margin=dict(l=40, r=40, t=20, b=20)
    )
    return fig

def plot_market_trends(market_data):
    # Skill demand bar chart
    skills = market_data.get('skill_demand', {})
    if not skills:
        return None
        
    df = pd.DataFrame(list(skills.items()), columns=['Skill', 'Demand'])
    
    fig = px.bar(
        df, 
        x='Skill', 
        y='Demand', 
        color='Demand',
        color_continuous_scale=['#00C9FF', '#92FE9D']
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.1)'),
        xaxis=dict(showgrid=False),
        coloraxis_showscale=False
    )
    return fig

def plot_growth_trajectory(weeks=4):
    weeks_label = [f'Week {i+1}' for i in range(weeks)]
    scores = [45, 58, 65, 75] # Mock progression
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=weeks_label, 
        y=scores,
        mode='lines+markers',
        line=dict(color='#00C9FF', width=4),
        marker=dict(size=10, color='#92FE9D')
    ))
    
    fig.update_layout(
        title="Projected Growth",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        yaxis=dict(range=[0, 100], gridcolor='rgba(255, 255, 255, 0.1)'),
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
    )
    return fig
