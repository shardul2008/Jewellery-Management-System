import streamlit as st
import pandas as pd
from database import add_jewellery, view_jewellery, update_jewellery, delete_jewellery, search_jewellery
from bill import generate_bill
from database import get_jewellery_by_id
import reportlab
# import requests
#from api import get_gold_rate, get_silver_rate

if "gold_rate" not in st.session_state:
    st.session_state.gold_rate = 14634.40

if "silver_rate" not in st.session_state:
    st.session_state.silver_rate = 250.00



def get_gold_rate_by_purity(rate_24k, purity):

    purity_percentage = {
        "24K": 1.000,
        "22K": 0.916,
        "20K": 0.833,
        "18K": 0.750,
        "14K": 0.585
    }

    return round(rate_24k * purity_percentage[purity], 2)


def get_silver_rate_by_purity(rate_999, purity):

    purity_percentage = {
        "999": 1.000,
        "925": 0.925,
        "900": 0.900,
        "835": 0.835,
        "800": 0.800
    }

    return round(rate_999 * purity_percentage[purity], 2)



# Page Configuration
st.set_page_config(
    page_title="Jewellery Management System",
    page_icon="💍",
    layout="wide"
)

# Sidebar
st.sidebar.title("💍 Jewellery Shop")
menu = st.sidebar.radio(
    "Menu",
    [
        "🏠 Dashboard",
        "➕ Add Jewellery",
        "📋 View Jewellery",
        "✏️ Edit Jewellery",
        "🗑️ Delete Jewellery",
        "⚙️ Settings"
    ]
)

# Dashboard
if menu == "🏠 Dashboard":
    st.title("💍 Jewellery Management System")
    st.markdown("---")



    st.subheader("Today's Metal Rates")
        
    rate_col,_ = st.columns([1,4])
    st.session_state.gold_rate = st.number_input(
        "Gold Rate (₹/gm)",
        value=st.session_state.gold_rate
    )

    st.session_state.silver_rate = st.number_input(
    "Silver Rate (₹/gm)",
    value=st.session_state.silver_rate
    )

    st.markdown("---")
    st.subheader("🔍 Search Jewellery")

    search = st.text_input("Enter Jewellery Name")


    if search:

        result = search_jewellery(search)

        if len(result) > 0:

            df = pd.DataFrame(
            result,
            columns=[
                "ID",
                "Name",
                "Metal",
                "Purity",
                "Weight",
                "Making",
                "GST",
                "Other",
                "final_price"                
            ]
        )

        st.dataframe(df, use_container_width=True)

    else:
        st.warning("No Jewellery Found")

# Add Jewellery
elif menu == "➕ Add Jewellery":

    st.title("➕ Add Jewellery")

    jewellery_name = st.text_input("Jewellery Name")

    metal = st.selectbox(
        "Metal",
        ["Gold", "Silver"]
    )

    if metal == "Gold":
        purity = st.selectbox(
         "Purity",
         ["24K", "22K", "20K", "18K", "14K"]
    )
    else:
     purity = st.selectbox(
        "Purity",
        ["999", "925", "900", "835", "800"]
    )
     

    weight = st.number_input(
        "Weight (gm)",
        min_value=0.0
    )

    making = st.number_input(
        "Making Charges (₹)",
        min_value=0.0
    )

    gst = st.number_input(
        "GST (%)",
        value=3.0
    )

    other = st.number_input(
        "Other Charges (₹)",
        min_value=0.0
    )

    # Client enters today's rates

    gold_rate = st.session_state.gold_rate
    silver_rate = st.session_state.silver_rate

    st.write(f"Today's Gold Rate: ₹{gold_rate:.2f}/gm")
    st.write(f"Today's Silver Rate: ₹{silver_rate:.2f}/gm")

# Rate according to metal and purity
    if metal == "Gold":

        rate = get_gold_rate_by_purity(gold_rate, purity)

        st.write(f"Current {purity} Gold Rate : ₹ {rate:.2f}/gm")
    
    else: 
        rate = get_silver_rate_by_purity(silver_rate, purity)

        st.write(f"Current {purity} Silver Rate : ₹ {rate:.2f}/gm")

# Price Calculation
    metal_price = rate * weight

    subtotal = metal_price + making + other

    gst_amount = subtotal * gst / 100

    final_price = subtotal + gst_amount

    st.subheader("Estimated Price")

    st.write(f"Metal Price : ₹ {metal_price:.2f}")
    st.write(f"GST Amount : ₹ {gst_amount:.2f}")

    st.success(f"Final Jewellery Price : ₹ {final_price:.2f}")

    if st.button("Save Jewellery"):

        add_jewellery(
         jewellery_name,
         metal,
         purity,
         weight,
         making,
         gst,
         other,
         final_price
        )

        st.success("Jewellery Saved Successfully!")

# View Jewellery
elif menu == "📋 View Jewellery":

    st.title("📋 View Jewellery")
    

    data = view_jewellery()

    if len(data) > 0:

        df = pd.DataFrame(
           data,
          columns=[
            "ID",
            "Name",
            "Metal",
            "Purity",
            "Weight",
            "Making",
            "GST",
            "Other",
            "final_price"            
           ]
        )

        st.dataframe(df, 
        use_container_width=True)

        st.markdown("---")
        st.subheader("🧾 Generate Bill")

    selected_id = st.selectbox(
    "Select Jewellery ID",
    df["ID"]
    )

    if st.button("Generate Bill"):
        selected_data = df[df["ID"] == selected_id].iloc[0]

        st.subheader("🧾 Jewellery Bill")

        st.write(f"**ID:** {selected_data['ID']}")
        st.write(f"**Name:** {selected_data['Name']}")
        st.write(f"**Metal:** {selected_data['Metal']}")
        st.write(f"**Purity:** {selected_data['Purity']}")
        st.write(f"**Weight:** {selected_data['Weight']} gm")
        st.write(f"**Making Charges:** ₹{selected_data['Making']}")
        st.write(f"**GST:** {selected_data['GST']}%")
        st.write(f"**Other Charges:** ₹{selected_data['Other']}")
        st.write(f"## Total Price: ₹{selected_data['final_price']}")

        pdf = generate_bill(selected_data)

        st.download_button(
        label="⬇ Download Bill",
        data=pdf,
        file_name=f"Bill_{selected_id}.pdf",
        mime="application/pdf"
        )
    
    else:
       st.warning("No Jewellery Added Yet.")

# Edit Jewellery
elif menu == "✏️ Edit Jewellery":


    st.title("✏️ Edit Jewellery")

    data = view_jewellery()

    if len(data) > 0:

        ids = [row[0] for row in data]

        selected_id = st.selectbox("Select Jewellery ID", ids)

        record = [row for row in data if row[0] == selected_id][0]

        name = st.text_input("Jewellery Name", record[1])

        metal = st.text_input("Metal", record[2])

        purity = st.text_input("Purity", record[3])

        weight = st.number_input("Weight", value=float(record[4]))

        making = st.number_input("Making Charge", value=float(record[5]))

        gst = st.number_input("GST", value=float(record[6]))

        other = st.number_input("Other Charges", value=float(record[7]))

        if metal == "Gold":
            rate = get_gold_rate_by_purity(st.session_state.gold_rate, purity)
        else:
         rate = get_silver_rate_by_purity(st.session_state.silver_rate, purity)

        metal_price = rate * weight
        subtotal = metal_price + making + other
        gst_amount = subtotal * gst / 100
        final_price = subtotal + gst_amount
        st.info(f"Updated Price: {final_price:.2f}/-")


        if st.button("Update Jewellery"):

            update_jewellery(
                selected_id,
                name,
                metal,
                purity,
                weight,
                making,
                gst,
                other,
                final_price
            )

            st.success("Jewellery Updated Successfully!")

    else:

        st.warning("No Jewellery Found")

# Delete Jewellery
elif menu == "🗑️ Delete Jewellery":

    st.title("🗑️ Delete Jewellery")

    data = view_jewellery()

    if len(data) > 0:

        ids = [row[0] for row in data]

        selected_id = st.selectbox("Select Jewellery ID", ids)

        if st.button("Delete Jewellery"):

            delete_jewellery(selected_id)

            st.success("Jewellery Deleted Successfully!")

    else:

        st.warning("No Jewellery Found")

# Settings
elif menu == "⚙️ Settings":

    st.title("⚙️ Settings")

    st.subheader("Application Information")

    st.write("Application Name: Jewellery Management System")
    st.write("Version: 1.0")
    st.write("Developed By: Shardul")

    st.markdown("---")

    if st.button("🗑️ Clear Search"):
        st.success("Search Cleared!")

    if st.button("ℹ️ About"):
        st.info("""
        Jewellery Management System
        Built using:
        - Python
        - Streamlit
        - SQLite
        """)