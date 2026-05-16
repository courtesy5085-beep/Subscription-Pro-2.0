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
            
            'status': 'Active', 'usage_frequency': 'Daily', 'value_rating': 5,
            'auto_renew': True, 'signup_date': '2022-03-10',
            'payment_method': 'Visa *1234', 'website': 'netflix.com'
        },
        {
            'id': 2, 'service': 'Spotify Family', 'category': 'Entertainment',            'amount': 15.99, 'billing_cycle': 'Monthly', 'next_billing': '2024-01-10',
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
            'status': 'Acti
            'id': 7, 'service': 'Link
