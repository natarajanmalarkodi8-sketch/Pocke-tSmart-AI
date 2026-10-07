import os
import streamlit as st
from google import generativeai as genai

# ---------------------------------------------------------
# Page Settings
# ---------------------------------------------------------
st.set_page_config(
    page_title="PocketSmart AI",
    page_icon="💰",
    layout="wide"
)

# ---------------------------------------------------------
# Gemini API Configuration
# ---------------------------------------------------------
api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

if not api_key:
    client = None
else:
    client = genai.Client(api_key=api_key)

# ---------------------------------------------------------
# App Header
# ---------------------------------------------------------
st.title("💰 PocketSmart AI")
st.subheader("Smart Budget Planner for Students")
st.write("Your AI money manager for students!")

st.divider()

# ---------------------------------------------------------
# Income
# ---------------------------------------------------------
income = st.number_input(
    "💵 Monthly Income / Pocket Money (₹)",
    min_value=0,
    value=15000,
    step=1000,
    format="%d"
)

# ---------------------------------------------------------
# Expenses
# ---------------------------------------------------------
st.subheader("📊 Monthly Expenses")

col1, col2 = st.columns(2)

with col1:
    rent = st.number_input(
        "🏠 Rent / Hostel (₹)",
        min_value=0,
        value=5000,
        step=500,
        format="%d"
    )

    food = st.number_input(
        "🍱 Food (₹)",
        min_value=0,
        value=4000,
        step=500,
        format="%d"
    )

    travel = st.number_input(
        "🚌 Travel (₹)",
        min_value=0,
        value=1000,
        step=500,
        format="%d"
    )

with col2:
    shopping = st.number_input(
        "🛍️ Shopping / OTT (₹)",
        min_value=0,
        value=1000,
        step=500,
        format="%d"
    )

    others = st.number_input(
        "📦 Other Expenses (₹)",
        min_value=0,
        value=1000,
        step=500,
        format="%d"
    )

# ---------------------------------------------------------
# Calculations
# ---------------------------------------------------------
total_expense = rent + food + travel + shopping + others
savings = income - total_expense

# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------
st.subheader("💰 Your Summary")

col3, col4, col5 = st.columns(3)

with col3:
    st.metric(
        "Total Expense",
        f"₹{total_expense:,}"
    )

with col4:
    st.metric(
        "Remaining",
        f"₹{savings:,}"
    )

with col5:
    if income > 0:
        saving_percentage = (savings / income) * 100
    else:
        saving_percentage = 0

    st.metric(
        "Saving Rate",
        f"{saving_percentage:.1f}%"
    )

# ---------------------------------------------------------
# Budget Status
# ---------------------------------------------------------
if savings < 0:
    st.error(
        f"⚠️ You are overspending by ₹{abs(savings):,}. "
        "Try reducing your unnecessary expenses."
    )
elif savings == 0:
    st.warning(
        "⚠️ Your income and expenses are equal. "
        "Try to save at least a small amount every month."
    )
elif saving_percentage >= 20:
    st.success(
        "🎉 Great job! You are saving 20% or more of your income."
    )
else:
    st.info(
        "💡 You have some savings. Try to gradually increase your "
        "monthly saving rate."
    )

# ---------------------------------------------------------
# Saving Goal
# ---------------------------------------------------------
st.subheader("🎯 Saving Goal")

goal = st.selectbox(
    "Choose your saving goal",
    [
        "Save ₹5,000 per month",
        "Buy a Laptop",
        "Plan a Trip",
        "Build an Emergency Fund",
        "Just Manage My Money"
    ]
)

# ---------------------------------------------------------
# AI Budget Plan
# ---------------------------------------------------------
st.subheader("🤖 AI Budget Advisor")

if st.button(
    "💡 Get AI Budget Plan",
    type="primary",
    use_container_width=True
):

    if client is None:
        st.error(
            "Gemini API key is not configured.\n\n"
            "Please add GEMINI_API_KEY to your Streamlit Secrets."
        )

    else:

        prompt = f"""
You are PocketSmart AI, a friendly personal budget assistant
for an Indian college student.

Analyze the student's monthly budget.

Monthly income: ₹{income}
Rent / Hostel: ₹{rent}
Food: ₹{food}
Travel: ₹{travel}
Shopping / OTT: ₹{shopping}
Other expenses: ₹{others}

Total expenses: ₹{total_expense}
Remaining money: ₹{savings}
Saving rate: {saving_percentage:.1f}%
Saving goal: {goal}

Provide the following:

1. Give a short review of the student's current budget.
2. Explain whether the student is overspending or saving well.
3. Give exactly 3 practical ways to reduce unnecessary expenses.
4. Give exactly 3 practical saving tips.
5. Create a simple monthly budget plan.
6. Give specific advice related to the selected saving goal.

Use a friendly Tamil + English mix (Tanglish).
Keep the advice simple, practical, educational, and suitable
for a college student in India.

Do not give investment, loan, cryptocurrency, or gambling advice.
"""

        with st.spinner("🤖 Creating your personalized budget plan..."):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                if response and response.text:
                    st.success("✨ Your Personalized Budget Plan")
                    st.markdown(response.text)
                else:
                    st.warning(
                        "The AI did not return a response. "
                        "Please try again."
                    )

            except Exception as e:
                st.error(
                    "❌ Unable to generate the AI budget plan."
                )

                st.caption(
                    f"Error details: {str(e)}"
                )

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
st.sidebar.title("ℹ️ About")

st.sidebar.info(
    "PocketSmart AI\n\n"
    "Smart Budget Planner for Students\n\n"
    "NASSCOM FSP SB Project"
)

st.sidebar.divider()

st.sidebar.caption(
    "💡 This application provides educational budgeting "
    "guidance and is not professional financial advice."
)
