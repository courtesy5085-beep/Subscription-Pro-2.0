import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from dateutil.relativedelta import relativedelta
import json
import hashlib
import os
from typing import Dict, List, Optional
import time
from streamlit_option_menu import option_menu
import altair as alt

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="Subscription Killer Pro",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SESSION STATE INIT ====================
if 'subscriptions' not in st.session_state:
    # Demo subscriptions with realistic data
    st.session_state.subscriptions = pd.DataFrame([
        {
            'id': 1, 'service': 'Netflix Premium', 'category': 'Entertainment',
            'amount': 19.99, 'billing_cycle': 'Monthly', 'next_billing': '2024-01-15',
            'status': 'Active', 'usage_frequency': 'Daily', 'value_rating': 5,
            'auto_renew': True, 'signup_date': '2022-03-10',
            'payment_method': 'Visa *1234', 'website': 'netflix.com'
        },
        {
            'id': 2, 'service': 'Spotify Family', 'category': 'Entertainment',
            'amount': 15.99, 'billing_cycle': 'Monthly', 'next_billing': '2024-01-10',
            'status': 'Active', 'usage_frequency': 'Daily', 'value_rating': 4,
            'auto_renew': True, 'signup_date': '2021-06-20',
            'payment_method': 'MC *5678', 'website': 'spotify.com'
        },
        {
            'id': 3, 'service': 'Adobe Creative Cloud', 'category': 'Software',
            'amount': 54.99, 'billing_cycle': 'Monthly', 'next_billing': '2024-01-05',
            'status': 'Active', 'usage_frequency': 'Weekly', 'value_rating': 3,
            'auto_renew': True, 'signup_date': '2023-01-15',
            'payment_method': 'Amex *9012', 'website': 'adobe.com'
        },
        {
            'id': 4, 'service': 'Amazon Prime', 'category': 'Shopping',
            'amount': 139.00, 'billing_cycle': 'Yearly', 'next_billing': '2024-06-01',
            'status': 'Active', 'usage_frequency': 'Weekly', 'value_rating': 4,
            'auto_renew': True, 'signup_date': '2020-06-01',
            'payment_method': 'Visa *1234', 'website': 'amazon.com'
        },
        {
            'id': 5, 'service': 'Gym Membership', 'category': 'Fitness',
            'amount': 49.99, 'billing_cycle': 'Monthly', 'next_billing': '2024-01-01',
            'status': 'Active', 'usage_frequency': 'Rarely', 'value_rating': 1,
            'auto_renew': True, 'signup_date': '2023-06-01',
            'payment_method': 'MC *5678', 'website': 'gym.com'
        },
        {
            'id': 6, 'service': 'Dropbox Plus', 'category': 'Software',
            'amount': 9.99, 'billing_cycle': 'Monthly', 'next_billing': '2024-01-20',
            'status': 'Active', 'usage_frequency': 'Monthly', 'value_rating': 2,
            'auto_renew': True, 'signup_date': '2023-08-15',
            'payment_method': 'PayPal', 'website': 'dropbox.com'
        },
        {
            'id': 7, 'service': 'LinkedIn Premium', 'category': 'Career',
            'amount': 29.99, 'billing_cycle': 'Monthly', 'next_billing': '2024-01-12',
            'status': 'Active', 'usage_frequency': 'Weekly', 'value_rating': 3,
            'auto_renew': True, 'signup_date': '2023-09-01',
            'payment_method': 'Amex *9012', 'website': 'linkedin.com'
        }
    ])

if 'cancellation_queue' not in st.session_state:
    st.session_state.cancellation_queue = []

if 'savings_history' not in st.session_state:
    st.session_state.savings_history = []

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'name': 'Alex Johnson',
        'email': 'alex@email.com',
        'monthly_budget': 200,
        'savings_goal': 500
    }

# ==================== HELPER FUNCTIONS ====================
def calculate_monthly_spend(df: pd.DataFrame) -> float:
    """Calculate total monthly spend"""
    monthly_total = 0
    for _, sub in df.iterrows():
        if sub['billing_cycle'] == 'Monthly':
            monthly_total += sub['amount']
        elif sub['billing_cycle'] == 'Yearly':
            monthly_total += sub['amount'] / 12
        elif sub['billing_cycle'] == 'Weekly':
            monthly_total += sub['amount'] * 4.33
    return round(monthly_total, 2)

def calculate_yearly_spend(df: pd.DataFrame) -> float:
    """Calculate total yearly spend"""
    yearly_total = 0
    for _, sub in df.iterrows():
        if sub['billing_cycle'] == 'Monthly':
            yearly_total += sub['amount'] * 12
        elif sub['billing_cycle'] == 'Yearly':
            yearly_total += sub['amount']
        elif sub['billing_cycle'] == 'Weekly':
            yearly_total += sub['amount'] * 52
    return round(yearly_total, 2)

def get_wasteful_subs(df: pd.DataFrame) -> pd.DataFrame:
    """Identify wasteful subscriptions"""
    return df[(df['value_rating'] <= 2) | (df['usage_frequency'] == 'Rarely')]

def get_category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Get spending by category"""
    breakdown = []
    for cat in df['category'].unique():
        cat_df = df[df['category'] == cat]
        monthly = 0
        for _, sub in cat_df.iterrows():
            if sub['billing_cycle'] == 'Monthly':
                monthly += sub['amount']
            elif sub['billing_cycle'] == 'Yearly':
                monthly += sub['amount'] / 12
            elif sub['billing_cycle'] == 'Weekly':
                monthly += sub['amount'] * 4.33
        breakdown.append({'category': cat, 'monthly_spend': round(monthly, 2)})
    return pd.DataFrame(breakdown)

def simulate_cancellation(sub_id: int) -> Dict:
    """Simulate AI-powered cancellation process"""
    sub = st.session_state.subscriptions[st.session_state.subscriptions['id'] == sub_id].iloc[0]
    
    # Simulate cancellation difficulty based on subscription type
    if sub['category'] == 'Fitness':
        difficulty = 'Hard'
        steps = [
            'Located hidden cancellation page',
            'Filled retention survey',
            'Called customer service (wait time: 12 min)',
            'Confirmed cancellation'
        ]
    elif sub['category'] == 'Software':
        difficulty = 'Medium'
        steps = [
            'Navigated to account settings',
            'Clicked through 3 retention offers',
            'Confirmed cancellation'
        ]
    else:
        difficulty = 'Easy'
        steps = [
            'Went to subscription page',
            'Clicked cancel',
            'Confirmed via email'
        ]
    
    return {
        'service': sub['service'],
        'amount': sub['amount'],
        'cycle': sub['billing_cycle'],
        'difficulty': difficulty,
        'steps': steps,
        'estimated_savings': sub['amount'] * 12 if sub['billing_cycle'] == 'Monthly' else sub['amount'],
        'retention_offers': np.random.choice([
            ['50% off for 3 months', '1 month free'],
            ['30% discount', 'Premium features unlocked'],
            ['No offers']
        ])
    }

def generate_ai_insights(df: pd.DataFrame) -> List[str]:
    """Generate AI-powered insights"""
    insights = []
    monthly = calculate_monthly_spend(df)
    yearly = calculate_yearly_spend(df)
    wasteful = get_wasteful_subs(df)
    
    if monthly > st.session_state.user_profile['monthly_budget']:
        insights.append(f"🚨 You're ${monthly - st.session_state.user_profile['monthly_budget']:.2f} over your monthly budget of ${st.session_state.user_profile['monthly_budget']}")
    
    if len(wasteful) > 0:
        insights.append(f"💡 {len(wasteful)} subscription(s) identified as low-value - potential savings of ${sum(wasteful['amount']):.2f}/month")
    
    if len(df) > 5:
        insights.append("📊 You have more subscriptions than 78% of users in your income bracket")
    
    # Check for duplicate services
    services = df['service'].str.lower()
    for service in services:
        if services.str.contains(service.replace('premium', '').strip()).sum() > 1:
            insights.append(f"🔄 You might have duplicate services similar to {service}")
            break
    
    return insights

# ==================== STYLING ====================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
    }
    .subscription-card {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
        transition: transform 0.2s;
    }
    .subscription-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .wasteful {
        border-left: 4px solid #ff6b6b;
    }
    .good-value {
        border-left: 4px solid #51cf66;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR NAVIGATION ====================
with st.sidebar:
    st.markdown("## 💸 Subscription Killer Pro")
    st.markdown("---")
    
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Subscriptions", "AI Negotiator", "Analytics", "Settings"],
        icons=["speedometer2", "list-check", "robot", "graph-up", "gear"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important"},
            "icon": {"color": "#667eea", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#667eea"},
        }
    )
    
    st.markdown("---")
    st.markdown(f"👤 {st.session_state.user_profile['name']}")
    st.markdown(f"📧 {st.session_state.user_profile['email']}")

# ==================== DASHBOARD PAGE ====================
if selected == "Dashboard":
    st.markdown('<h1 class="main-header">📊 Financial Command Center</h1>', unsafe_allow_html=True)
    
    # Top Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    monthly_spend = calculate_monthly_spend(st.session_state.subscriptions)
    yearly_spend = calculate_yearly_spend(st.session_state.subscriptions)
    wasteful_subs = get_wasteful_subs(st.session_state.subscriptions)
    potential_savings = sum(wasteful_subs['amount'])
    
    with col1:
        st.metric("Monthly Spend", f"${monthly_spend:,.2f}", 
                 delta=f"{monthly_spend - st.session_state.user_profile['monthly_budget']:.2f} vs budget",
                 delta_color="inverse")
    
    with col2:
        st.metric("Yearly Spend", f"${yearly_spend:,.2f}")
    
    with col3:
        st.metric("Active Subscriptions", len(st.session_state.subscriptions))
    
    with col4:
        st.metric("Potential Monthly Savings", f"${potential_savings:,.2f}",
                 delta=f"From {len(wasteful_subs)} subs")
    
    st.markdown("---")
    
    # AI Insights
    st.markdown("### 🤖 AI-Powered Insights")
    insights = generate_ai_insights(st.session_state.subscriptions)
    
    cols = st.columns(2)
    for i, insight in enumerate(insights):
        with cols[i % 2]:
            st.info(insight)
    
    # Spending Trend Chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Monthly Spending by Category")
        cat_breakdown = get_category_breakdown(st.session_state.subscriptions)
        fig = px.pie(cat_breakdown, values='monthly_spend', names='category',
                     color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💡 Value Matrix")
        # Create value matrix
        value_data = st.session_state.subscriptions[['service', 'amount', 'value_rating']].copy()
        value_data['monthly_cost'] = value_data['amount'].apply(
            lambda x: x if x < 100 else x/12  # Convert yearly to monthly
        )
        
        fig = px.scatter(value_data, x='monthly_cost', y='value_rating',
                        size='monthly_cost', color='value_rating',
                        text='service', hover_data=['service', 'monthly_cost'],
                        color_continuous_scale='RdYlGn')
        fig.add_hline(y=3, line_dash="dash", line_color="red", annotation_text="Review Line")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Wasteful Subscriptions Alert
    if len(wasteful_subs) > 0:
        st.markdown("### 🚨 Subscriptions You Should Review")
        for _, sub in wasteful_subs.iterrows():
            with st.container():
                cols = st.columns([3, 1, 1])
                with cols[0]:
                    st.markdown(f"**{sub['service']}** - {sub['category']}")
                    st.caption(f"Used: {sub['usage_frequency']} | Rating: {'⭐'*sub['value_rating']}")
                with cols[1]:
                    st.markdown(f"**${sub['amount']:.2f}**/{sub['billing_cycle'].lower()}")
                with cols[2]:
                    if st.button(f"Cancel", key=f"waste_{sub['id']}"):
                        st.session_state.cancellation_queue.append(sub['id'])
                        st.success(f"Added to cancellation queue!")
                st.markdown("---")

# ==================== SUBSCRIPTIONS PAGE ====================
elif selected == "Subscriptions":
    st.markdown('<h1 class="main-header">📋 Subscription Manager</h1>', unsafe_allow_html=True)
    
    # Add New Subscription
    with st.expander("➕ Add New Subscription", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            new_service = st.text_input("Service Name")
            new_category = st.selectbox("Category", 
                ["Entertainment", "Software", "Fitness", "Shopping", "Career", "Other"])
            new_amount = st.number_input("Amount ($)", min_value=0.0, step=0.99)
        with col2:
            new_cycle = st.selectbox("Billing Cycle", ["Monthly", "Yearly", "Weekly"])
            new_usage = st.selectbox("Usage Frequency", ["Daily", "Weekly", "Monthly", "Rarely"])
            new_value = st.slider("Value Rating", 1, 5, 3)
        with col3:
            new_billing = st.date_input("Next Billing Date")
            new_payment = st.text_input("Payment Method")
            new_website = st.text_input("Website URL")
        
        if st.button("Add Subscription", type="primary"):
            new_id = st.session_state.subscriptions['id'].max() + 1
            new_sub = pd.DataFrame([{
                'id': new_id, 'service': new_service, 'category': new_category,
                'amount': new_amount, 'billing_cycle': new_cycle,
                'next_billing': new_billing.strftime('%Y-%m-%d'),
                'status': 'Active', 'usage_frequency': new_usage,
                'value_rating': new_value, 'auto_renew': True,
                'signup_date': datetime.now().strftime('%Y-%m-%d'),
                'payment_method': new_payment, 'website': new_website
            }])
            st.session_state.subscriptions = pd.concat(
                [st.session_state.subscriptions, new_sub], ignore_index=True
            )
            st.success(f"Added {new_service}!")
            st.rerun()
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_category = st.multiselect("Filter by Category",
            st.session_state.subscriptions['category'].unique())
    with col2:
        filter_usage = st.multiselect("Filter by Usage",
            st.session_state.subscriptions['usage_frequency'].unique())
    with col3:
        sort_by = st.selectbox("Sort by", 
            ["Amount (High to Low)", "Amount (Low to High)", "Value Rating"])
    
    # Apply filters
    df_filtered = st.session_state.subscriptions.copy()
    if filter_category:
        df_filtered = df_filtered[df_filtered['category'].isin(filter_category)]
    if filter_usage:
        df_filtered = df_filtered[df_filtered['usage_frequency'].isin(filter_usage)]
    
    if sort_by == "Amount (High to Low)":
        df_filtered = df_filtered.sort_values('amount', ascending=False)
    elif sort_by == "Amount (Low to High)":
        df_filtered = df_filtered.sort_values('amount', ascending=True)
    else:
        df_filtered = df_filtered.sort_values('value_rating', ascending=False)
    
    # Display subscriptions
    for _, sub in df_filtered.iterrows():
        with st.container():
            card_class = "wasteful" if sub['value_rating'] <= 2 else "good-value" if sub['value_rating'] >= 4 else ""
            st.markdown(f'<div class="subscription-card {card_class}">', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.markdown(f"### {sub['service']}")
                st.caption(f"Category: {sub['category']} | Since: {sub['signup_date']}")
                st.progress(sub['value_rating'] / 5, text=f"Value: {sub['value_rating']}/5")
            
            with col2:
                monthly_cost = sub['amount'] if sub['billing_cycle'] == 'Monthly' else sub['amount']/12
                st.metric("Monthly Cost", f"${monthly_cost:.2f}")
                st.caption(f"Billed: {sub['billing_cycle']}")
            
            with col3:
                st.markdown(f"**Next Billing**")
                st.markdown(f"{sub['next_billing']}")
                st.caption(f"Used: {sub['usage_frequency']}")
            
            with col4:
                if st.button("⚡ Quick Cancel", key=f"cancel_{sub['id']}"):
                    cancel_result = simulate_cancellation(sub['id'])
                    st.session_state.subscriptions.loc[
                        st.session_state.subscriptions['id'] == sub['id'], 'status'
                    ] = 'Cancelled'
                    st.success(f"Cancelled! Saved ${cancel_result['estimated_savings']:.2f}/year")
                    st.rerun()
                
                if st.button("📝 Edit", key=f"edit_{sub['id']}"):
                    st.session_state[f"editing_{sub['id']}"] = True
            
            # Edit form
            if st.session_state.get(f"editing_{sub['id']}", False):
                with st.form(key=f"edit_form_{sub['id']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        new_amount = st.number_input("Amount", value=float(sub['amount']))
                        new_cycle = st.selectbox("Billing Cycle", 
                            ["Monthly", "Yearly", "Weekly"],
                            index=["Monthly", "Yearly", "Weekly"].index(sub['billing_cycle']))
                    with col2:
                        new_value = st.slider("Value Rating", 1, 5, int(sub['value_rating']))
                        new_usage = st.selectbox("Usage", 
                            ["Daily", "Weekly", "Monthly", "Rarely"],
                            index=["Daily", "Weekly", "Monthly", "Rarely"].index(sub['usage_frequency']))
                    
                    if st.form_submit_button("Save Changes"):
                        idx = st.session_state.subscriptions[
       
