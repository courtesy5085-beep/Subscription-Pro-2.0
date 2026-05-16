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
            
            'payment_method': 'MC *5678', 'website': 'spotify.com'
        },
        {
            'i': '2024-01-01',
            'status': 'Active', 'usage_frequency': 'Rarely', 'value_rating'
