import os
import streamlit as st
from google import genai

# =========================================================
# PAGE SETTINGS
# =========================================================
st.set_page_config(
    page_title="PocketSmart AI",
    page_icon="💰",
    layout="wide"
)

# =========================================================
# GEMINI API CONFIGURATION
# =========================================================
api_key = st.secrets.get(
    "GEMINI_API_KEY",
    os.getenv("GEMINI_API_KEY")
)

if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None

# =========================================================
# APP TITLE
# =========================================================
st.title("💰 PocketSmart AI")
st.subheader("Smart Budget Planner for Students")
st.write("Your AI money manager for students!")

st.divider()

# =========================================================
# MONTHLY INCOME
# =========================================================
st.subheader("💵 Monthly Income")

income = st.number_input(
    "Monthly Income / Pocket Money (₹)",
    min_value=0,
    value=15000,
    step=1000
)

# =========================================================
# MONTHLY EXPENSES
# =========================================================
st.subheader("📊 Monthly Expenses")

col1, col2 = st.columns(2)

with col1:

    rent = st.number_input(
        "🏠 Rent / Hostel (₹)",
        min_value=0,
        value=5000,
        step=500
    )

    food = st.number_input(
        "🍱 Food (₹)",
        min_value=0,
        value=4000,
        step=500
    )

    travel = st.number_input(
        "🚌 Travel (₹)",
        min_value=0,
        value=1000,
        step=500
    )

with col2:

    shopping = st.number_input(
        "🛍️ Shopping / OTT (₹)",
        min_value=0,
        value=1000,
        step=500
    )

    others = st.number_input(
        "📦 Other Expenses (₹)",
        min_value=0,
        value=1000,
        step=500
    )

# =========================================================
# CALCULATIONS
# =========================================================
total_expense = (
    rent
    + food
    + travel
    + shopping
    + others
)

savings = income - total_expense

if income > 0:
    saving_percentage = (savings / income) * 100
else:
    saving_percentage = 0

# =========================================================
# SUMMARY
# =========================================================
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
    st.metric(
        "Saving Rate",
        f"{saving_percentage:.1f}%"
    )

# =========================================================
# BUDGET STATUS
# =========================================================
if savings < 0:

    st.error(
        f"⚠️ You are overspending by "
        f"₹{abs(savings):,}."
    )

elif savings == 0:

    st.warning(
        "⚠️ Your income and expenses are equal. "
        "Try to reduce some expenses and save money."
    )

elif saving_percentage >= 20:

    st.success(
        "🎉 Great job! You are saving 20% or more "
        "of your monthly income."
    )

else:

    st.info(
        "💡 You have some savings. Try to increase "
        "your monthly saving rate gradually."
    )

# =========================================================
# SAVING GOAL
# =========================================================
st.subheader("🎯 Your Saving Goal")

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

# =========================================================
# AI BUDGET PLAN
# =========================================================
st.subheader("🤖 AI Budget Advisor")

if st.button(
    "💡 Get AI Budget Plan",
    type="primary",
    use_container_width=True
):

    if client is None:

        st.error(
            "Gemini API key is not configured. "
            "Please add GEMINI_API_KEY to Streamlit Secrets."
        )

    else:

        prompt = f"""
You are PocketSmart AI, a friendly budget assistant
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

Provide:

1. A simple review of the student's current budget.
2. Explain whether the student is spending too much
   or saving a reasonable amount.
3. Three practical ways to reduce unnecessary spending.
4. Three practical saving tips.
5. A simple monthly budget plan.
6. Advice specifically related to the student's
   selected saving goal.

Use simple Tamil + English mix (Tanglish).

Keep the advice friendly, educational, practical,
and easy for a college student to understand.

Do not provide investment, cryptocurrency,
gambling, or loan recommendations.
"""

        with st.spinner(
            "🤖 Creating your personalized budget plan..."
        ):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                if response and response.text:

                    st.success(
                        "✨ Your Personalized Budget Plan"
                    )

                    st.markdown(response.text)

                else:

                    st.warning(
                        "The AI did not return a response. "
                        "Please try again."
                    )

            except Exception as error:

                st.error(
                    "❌ Something went wrong while "
                    "generating the AI budget plan."
                )

                st.caption(
                    f"Error details: {error}"
                )

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("ℹ️ About")

st.sidebar.info(
    "PocketSmart AI\n\n"
    "Smart Budget Planner for Students\n\n"
    "NASSCOM FSP SB Project"
)

st.sidebar.divider()

st.sidebar.caption(
    "💡 PocketSmart AI provides educational "
    "budgeting guidance for students."
)
