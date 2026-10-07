import os
import streamlit as st 
import google.generativeai as genai

# Page settings
st.set_page_config(
    page_title="PocketSmart AI",
    page_icon="💰"
)

# Gemini API
api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None

# App title
st.title("💰 PocketSmart AI")
st.subheader("Smart Budget Planner for Students")
st.write("Your AI money manager for students!")

# Income
income = st.number_input(
    "Monthly Income / Pocket Money ₹",
    min_value=0,
    value=15000,
    step=1000
)

# Expenses
st.subheader("📊 Monthly Expenses")

col1, col2 = st.columns(2)

with col1:
    rent = st.number_input("🏠 Rent / Hostel ₹", min_value=0, value=5000)
    food = st.number_input("🍱 Food ₹", min_value=0, value=4000)
    travel = st.number_input("🚌 Travel ₹", min_value=0, value=1000)

with col2:
    shopping = st.number_input("🛍️ Shopping / OTT ₹", min_value=0, value=1000)
    others = st.number_input("📦 Others ₹", min_value=0, value=1000)

# Calculations
total_expense = rent + food + travel + shopping + others
savings = income - total_expense

# Display results
st.subheader("💰 Your Summary")

col3, col4 = st.columns(2)

with col3:
    st.metric("Total Expense", f"₹{total_expense}")

with col4:
    st.metric("Remaining", f"₹{savings}")

# Saving goal
goal = st.selectbox(
    "🎯 Your Saving Goal",
    [
        "Save ₹5,000 per month",
        "Buy a Laptop",
        "Plan a Trip",
        "Just Manage My Money"
    ]
)

# AI button
if st.button("💡 Get AI Budget Plan"):

    if client is None:
        st.error(
            "Gemini API key is not configured. "
            "Add GEMINI_API_KEY in Streamlit Secrets."
        )
    else:
        with st.spinner("🤖 Creating your budget plan..."):

            prompt = f"""
You are a friendly budget assistant for an Indian college student.

Monthly income: ₹{income}
Rent/Hostel: ₹{rent}
Food: ₹{food}
Travel: ₹{travel}
Shopping/OTT: ₹{shopping}
Other expenses: ₹{others}

Total expenses: ₹{total_expense}
Remaining money: ₹{savings}
Saving goal: {goal}

Give:
1. A simple budget review.
2. Three ways to reduce unnecessary spending.
3. Three practical saving tips.
4. A simple monthly plan to reach the student's goal.

Use simple Tamil + English mix.
Keep the advice educational and easy for a college student to understand.
"""

            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                st.success("✨ Your Personalized Budget Plan")
                st.write(response.text)

            except Exception as e:
                st.error("Something went wrong while generating the AI plan.")
                st.write(str(e))

# Sidebar
st.sidebar.title("ℹ️ About")
st.sidebar.info(
    "PocketSmart AI - Smart Budget Planner\n\n"
    "NASSCOM FSP SB Project"
)
