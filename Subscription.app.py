# app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from streamlit_option_menu import option_menu
from streamlit_extras import add_vertical_space as avs
from streamlit_extras.colored_header import colored_header

# ---------------------------- Page config ---------------------------- #
st.set_page_config(
    page_title="Subscription Killer Pro 2.0",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------- Custom CSS ---------------------------- #
st.markdown(
    """
<style>
    /* Gradient header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
    }
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }

    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
        border-left: 5px solid #667eea;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    .metric-label {
        color: #555;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #333;
    }
    .metric-delta {
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }

    /* Subscription cards */
    .sub-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.2s;
        border: 2px solid #eee;
    }
    .sub-card:hover {
        box-shadow: 0 6px 16px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .wasteful {
        border-left: 6px solid #e74c3c;
        background: #fff5f5;
    }
    .good-value {
        border-left: 6px solid #27ae60;
        background: #f0fff4;
    }
    .sub-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
    }
    .sub-detail {
        color: #7f8c8d;
        font-size: 0.9rem;
        margin: 0.3rem 0;
    }
    .value-bar {
        width: 100%;
        height: 10px;
        background: #eee;
        border-radius: 5px;
        margin-top: 0.5rem;
        overflow: hidden;
    }
    .value-fill {
        height: 100%;
        border-radius: 5px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }

    /* Buttons */
    .stButton button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s;
    }
    .cancel-btn button {
        background: #e74c3c;
        color: white;
        border: none;
    }
    .cancel-btn button:hover {
        background: #c0392b;
        color: white;
    }
    .edit-btn button {
        background: #f1c40f;
        color: #333;
        border: none;
    }
    .edit-btn button:hover {
        background: #d4ac0d;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------- Session state ---------------------------- #
def init_session():
    defaults = {
        "subscriptions": [
            {
                "service": "Netflix",
                "category": "Entertainment",
                "amount": 15.49,
                "billing_cycle": "Monthly",
                "usage_frequency": "Daily",
                "value_rating": 4,
                "next_billing": date.today() + timedelta(days=15),
                "payment_method": "Credit Card",
                "website": "https://netflix.com",
                "status": "Active",
            },
            {
                "service": "Spotify",
                "category": "Music",
                "amount": 9.99,
                "billing_cycle": "Monthly",
                "usage_frequency": "Daily",
                "value_rating": 5,
                "next_billing": date.today() + timedelta(days=8),
                "payment_method": "PayPal",
                "website": "https://spotify.com",
                "status": "Active",
            },
            {
                "service": "Adobe Creative Cloud",
                "category": "Software",
                "amount": 54.99,
                "billing_cycle": "Monthly",
                "usage_frequency": "Daily",
                "value_rating": 5,
                "next_billing": date.today() + timedelta(days=21),
                "payment_method": "Credit Card",
                "website": "https://adobe.com",
                "status": "Active",
            },
            {
                "service": "Amazon Prime",
                "category": "Shopping",
                "amount": 139.00,
                "billing_cycle": "Yearly",
                "usage_frequency": "Weekly",
                "value_rating": 3,
                "next_billing": date.today() + timedelta(days=30),
                "payment_method": "Credit Card",
                "website": "https://amazon.com",
                "status": "Active",
            },
            {
                "service": "Gym Membership",
                "category": "Health & Fitness",
                "amount": 29.99,
                "billing_cycle": "Monthly",
                "usage_frequency": "Rarely",
                "value_rating": 2,
                "next_billing": date.today() + timedelta(days=10),
                "payment_method": "Bank Transfer",
                "website": "https://gym.example.com",
                "status": "Active",
            },
            {
                "service": "Dropbox",
                "category": "Cloud Storage",
                "amount": 9.99,
                "billing_cycle": "Monthly",
                "usage_frequency": "Weekly",
                "value_rating": 3,
                "next_billing": date.today() + timedelta(days=18),
                "payment_method": "Credit Card",
                "website": "https://dropbox.com",
                "status": "Active",
            },
            {
                "service": "LinkedIn Premium",
                "category": "Career",
                "amount": 29.99,
                "billing_cycle": "Monthly",
                "usage_frequency": "Rarely",
                "value_rating": 2,
                "next_billing": date.today() + timedelta(days=5),
                "payment_method": "Credit Card",
                "website": "https://linkedin.com",
                "status": "Active",
            },
        ],
        "cancellation_queue": [],
        "savings_history": [],
        "user_profile": {
            "name": "",
            "email": "",
            "monthly_budget": 200.0,
            "notifications": True,
            "currency": "$",
        },
        "edit_index": None,
        "cancel_confirm_index": None,
        "negotiator_chat": [],
        "negotiator_sub_index": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()

# ---------------------------- Helper functions ---------------------------- #
def monthly_cost(sub):
    """Convert any billing cycle to monthly cost."""
    amount = sub["amount"]
    cycle = sub["billing_cycle"]
    if cycle == "Monthly":
        return amount
    elif cycle == "Yearly":
        return amount / 12
    elif cycle == "Weekly":
        return amount * 4.33
    elif cycle == "Bi-Weekly":
        return amount * 2.165
    elif cycle == "Quarterly":
        return amount / 3
    else:
        return amount  # fallback

def calculate_monthly_spend(subs):
    return sum(monthly_cost(s) for s in subs if s.get("status", "Active") != "Cancelled")

def calculate_yearly_spend(subs):
    return calculate_monthly_spend(subs) * 12

def get_wasteful_subs(subs):
    wasteful = []
    for s in subs:
        if s.get("status", "Active") == "Cancelled":
            continue
        if s["value_rating"] <= 2 or s["usage_frequency"] == "Rarely":
            wasteful.append(s)
    return wasteful

def get_category_breakdown(subs):
    active = [s for s in subs if s.get("status", "Active") != "Cancelled"]
    df = pd.DataFrame(active)
    df["monthly"] = df.apply(monthly_cost, axis=1)
    breakdown = df.groupby("category")["monthly"].sum().to_dict()
    return breakdown

def simulate_cancellation(category):
    """Return a dict with difficulty, steps, retention offers based on category."""
    mapping = {
        "Entertainment": {
            "difficulty": "Easy",
            "steps": [
                "Log into your account",
                "Go to Account Settings",
                "Click 'Cancel Subscription'",
                "Confirm cancellation",
            ],
            "offers": ["One month free", "50% off for 3 months"],
        },
        "Music": {
            "difficulty": "Easy",
            "steps": [
                "Log in",
                "Navigate to Subscription",
                "Cancel plan",
                "Confirm",
            ],
            "offers": ["Free month", "Family plan discount"],
        },
        "Software": {
            "difficulty": "Hard",
            "steps": [
                "Contact customer support (chat/phone)",
                "Request cancellation",
                "Confirm no early termination fee",
                "Receive cancellation confirmation",
            ],
            "offers": ["2 months free", "20% off annual plan"],
        },
        "Shopping": {
            "difficulty": "Medium",
            "steps": [
                "Go to Your Account",
                "Manage Prime Membership",
                "End membership",
                "Confirm",
            ],
            "offers": ["30-day free extension", "Student discount offer"],
        },
        "Health & Fitness": {
            "difficulty": "Hard",
            "steps": [
                "Visit gym or call",
                "Fill out cancellation form",
                "Pay any remaining balance",
                "Return access card",
            ],
            "offers": ["Free month", "Freeze membership"],
        },
        "Cloud Storage": {
            "difficulty": "Medium",
            "steps": [
                "Log into account",
                "Billing settings",
                "Cancel plan",
                "Confirm downgrade",
            ],
            "offers": ["Extra 100GB free", "30% off yearly"],
        },
        "Career": {
            "difficulty": "Easy",
            "steps": [
                "Go to Premium settings",
                "Cancel subscription",
                "Confirm cancellation",
            ],
            "offers": ["50% off for 6 months", "Free month"],
        },
    }
    return mapping.get(category, {
        "difficulty": "Medium",
        "steps": ["Log in", "Cancel subscription", "Confirm"],
        "offers": ["10% discount"],
    })

def generate_ai_insights(monthly_spend, yearly_spend, wasteful_count, total_active, budget):
    insights = []
    if budget and monthly_spend > budget:
        over = monthly_spend - budget
        insights.append(f"⚠️ You're ${over:.2f} over your monthly budget of ${budget:.2f}. Consider trimming low-value services.")
    if wasteful_count > 0:
        insights.append(f"🗑️ You have {wasteful_count} wasteful subscription(s) with low usage or value. Cancelling them could save you money immediately.")
    if total_active > 5:
        insights.append("📦 You have more than 5 active subscriptions. Review if you really need all of them.")
    if monthly_spend > 100:
        insights.append("💸 Your monthly spend is over $100. A quarterly audit can help you stay on track.")
    else:
        insights.append("✅ Your subscription spending looks healthy. Keep monitoring for unused services.")
    insights.append(f"📅 Yearly spend projected at ${yearly_spend:,.2f}. Imagine what else you could do with that money!")
    return insights

def cancel_subscription(index):
    """Update status, record savings, add to cancellation queue."""
    sub = st.session_state.subscriptions[index]
    if sub.get("status", "Active") == "Cancelled":
        return
    sub["status"] = "Cancelled"
    savings = monthly_cost(sub)
    st.session_state.subscriptions[index] = sub
    # Record in savings history
    st.session_state.savings_history.append({
        "service": sub["service"],
        "date": str(date.today()),
        "monthly_savings": savings,
    })
    # Add to cancellation queue
    st.session_state.cancellation_queue.append({
        "service": sub["service"],
        "cancelled_date": str(date.today()),
        "savings": savings,
        "difficulty": simulate_cancellation(sub["category"])["difficulty"],
    })
    st.session_state.cancel_confirm_index = None

# ---------------------------- Sidebar navigation ---------------------------- #
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.markdown("<h2 style='text-align: center; color: #667eea;'>Subscription Killer</h2>", unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Subscriptions", "AI Negotiator", "Analytics", "Settings"],
        icons=["speedometer2", "card-checklist", "robot", "graph-up", "gear"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#f9f9f9"},
            "icon": {"color": "#667eea", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#667eea", "color": "white"},
        },
    )

# ---------------------------- Pages ---------------------------- #
# --- Dashboard ---
if selected == "Dashboard":
    st.markdown(
        "<div class='main-header'><h1>💸 Subscription Killer Pro 2.0</h1><p>Take control of your recurring costs</p></div>",
        unsafe_allow_html=True,
    )

    subs = st.session_state.subscriptions
    active_subs = [s for s in subs if s.get("status", "Active") != "Cancelled"]
    wasteful = get_wasteful_subs(subs)
    monthly_spend = calculate_monthly_spend(subs)
    yearly_spend = calculate_yearly_spend(subs)
    potential_savings = sum(monthly_cost(w) for w in wasteful)
    budget = st.session_state.user_profile.get("monthly_budget", 200)

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Monthly Spend</div><div class='metric-value'>{st.session_state.user_profile.get('currency','$')}{monthly_spend:,.2f}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Yearly Spend</div><div class='metric-value'>{st.session_state.user_profile.get('currency','$')}{yearly_spend:,.2f}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Active Subs</div><div class='metric-value'>{len(active_subs)}</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Potential Savings</div><div class='metric-value' style='color:#27ae60;'>{st.session_state.user_profile.get('currency','$')}{potential_savings:,.2f}</div><div class='metric-delta'>(monthly)</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # AI Insights
    colored_header(label="🧠 AI-Generated Insights", description="Smart recommendations based on your data", color_name="violet-70")
    insights = generate_ai_insights(monthly_spend, yearly_spend, len(wasteful), len(active_subs), budget)
    for ins in insights:
        st.markdown(f"- {ins}")

    st.markdown("---")

    # Charts
    left, right = st.columns(2)
    with left:
        st.subheader("📊 Spending by Category")
        cat_breakdown = get_category_breakdown(subs)
        if cat_breakdown:
            pie_df = pd.DataFrame(list(cat_breakdown.items()), columns=["Category", "Monthly"])
            fig = px.pie(pie_df, values="Monthly", names="Category", hole=0.4, color_discrete_sequence=px.colors.sequential.Purples_r)
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No active subscriptions.")

    with right:
        st.subheader("📈 Value Matrix (Cost vs Rating)")
        if active_subs:
            scatter_df = pd.DataFrame(active_subs)
            scatter_df["monthly"] = scatter_df.apply(monthly_cost, axis=1)
            fig2 = px.scatter(
                scatter_df, x="monthly", y="value_rating",
                size=[20]*len(scatter_df), color="category",
                hover_name="service", text="service",
                labels={"monthly": "Monthly Cost", "value_rating": "Value Rating"},
                title="",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig2.update_traces(textposition='top center')
            fig2.update_layout(xaxis=dict(showgrid=True), yaxis=dict(range=[0.5,5.5], tickvals=[1,2,3,4,5]))
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No data.")

    st.markdown("---")

    # Alert section for low-value subscriptions
    colored_header(label="🚨 Wasteful Subscriptions Alert", description="Quick cancel to save money", color_name="red-70")
    if wasteful:
        for i, sub in enumerate(wasteful):
            # find original index
            orig_idx = next(idx for idx, s in enumerate(subs) if s["service"] == sub["service"] and s.get("status","Active")!="Cancelled")
            with st.container():
                col1, col2, col3 = st.columns([3,2,1])
                with col1:
                    st.markdown(f"**{sub['service']}** ({sub['category']})")
                    st.caption(f"Usage: {sub['usage_frequency']} | Value: {'⭐'*sub['value_rating']}")
                with col2:
                    st.metric("Monthly Cost", f"${monthly_cost(sub):.2f}")
                with col3:
                    if st.button("Cancel Now", key=f"dash_cancel_{orig_idx}", type="primary"):
                        cancel_subscription(orig_idx)
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.success("No wasteful subscriptions found! 🎉")

# --- Subscriptions Page ---
elif selected == "Subscriptions":
    st.markdown("<div class='main-header'><h1>📋 My Subscriptions</h1></div>", unsafe_allow_html=True)

    subs = st.session_state.subscriptions
    # Filters
    with st.expander("🔍 Filter & Sort", expanded=True):
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            categories = list({s["category"] for s in subs if s.get("status","Active")!="Cancelled"})
            selected_cat = st.multiselect("Category", options=categories, default=categories)
        with col_f2:
            freqs = ["Daily", "Weekly", "Monthly", "Rarely"]
            selected_freq = st.selectbox("Usage Frequency", ["All"] + freqs)
        with col_f3:
            sort_by = st.selectbox(
                "Sort by",
                ["Amount (High→Low)", "Amount (Low→High)", "Value Rating (High→Low)", "Value Rating (Low→High)"],
                index=0
            )

    # Filter
    filtered = [s for s in subs if s.get("status","Active")!="Cancelled" and s["category"] in 
