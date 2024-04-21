import streamlit as st
import pandas as pd

reg = st.text_input('Enter Registration')
underwriter = st.selectbox("Choose Underwriter", ["APA INSURANCE", "FIDELITY INSURANCE", "CANNON GENERAL INSURANCE", "GA INSURANCE", "MAYFAIR INSURANCE", "ICEA LION INSURANCE", "JUBILEE ALLIANZ"])
value = int(st.number_input('Sum Insured'))
rate = st.number_input('Rate as a number eg 4 0r 3.5')
excess_protector = st.selectbox("Choose excess protector rate", ["Inclusive", "0.25%"])
pvt = st.selectbox("Choose pvt rate", ["Inclusive", "0.25%"])
loss_of_use = st.selectbox("Choose number of days", ["N/A", "10 days", "15 days"])
policy_fee = st.selectbox("Choose cover", ["Renewal", "New Business",])
                                                    

car_hire = 0
fee = 0
ex_pr = 0
pvt_value = 0

if st.button("Calculate"):
    premium = value * (rate/100)

    if pvt == 'Inclusive':
        pvt_value += 0
    if pvt == '0.25%':
        pvtworking = (0.25/100) * value
        pvt_value += pvtworking

    if excess_protector == 'Inclusive':
        ex_pr += 0
    if excess_protector == '0.25%':
        working = (0.25/100) * value
        ex_pr += working

    
    if loss_of_use == '10 days':
        car_hire += 3000
    if loss_of_use == 'N/A':
        car_hire += 0
    if loss_of_use == '15days':
        car_hire += 4500
    if policy_fee == "Renewal":
        fee += 100
    if policy_fee == "New Business":
        fee += 40

    gross_premium = ( premium + car_hire )

    levies = gross_premium * 0.0045

    total = ( premium + car_hire + fee + levies + ex_pr + pvt_value )

    # Format numbers with commas for thousands
    def format_with_commas(number):
        rounded_number = round(number, 2)
        return "{:,.2f}".format(rounded_number)
        
    
    formatted_value = format_with_commas(value)
    formatted_premium = format_with_commas(premium)
    formatted_ex_pr = format_with_commas(ex_pr)
    formatted_pvt = format_with_commas(pvt_value)
    formatted_car_hire = format_with_commas(car_hire)
    formatted_gross_premium = format_with_commas(gross_premium)
    formatted_levies = format_with_commas(levies)
    formatted_total = format_with_commas(total)


       # Create an HTML report
    html_report = f"""
    <html>
    <head>
    <style>
        table {{
        border-collapse: collapse;
        width: 40%;
        margin: 10px auto; /* Center the table */
        font-size: 12px;
        font-family: Candara;
    }}

    th, td {{
        border: 1px solid black;
        padding: 5px; /* Increased padding for better spacing */
        text-align: left;
    }}

    th {{
        background-color: #966fd6;
        color: black; /* Text color for table headers */
    }}

    .bold {{
        font-weight: bold;
    }}

    </style>
    </head>
    <body>
    <table>
        <tr>
            <th colspan="2">{reg} - MOTOR PRIVATE COMPREHENSIVE</th1>
            <th colspan="2">{underwriter} </th1>
            
        </tr>
        <tr >
            <th style="background-color: #17B169"></th>
            <th style="background-color: #17B169">Value - KES</th>
            <th style="background-color: #17B169">Rate</th>
            <th style="background-color: #17B169">Premium</th>
        </tr>
        <tr>
            <td>Basic Premium</td>
            <td>{formatted_value}</td> <!-- Updated formatting for better readability -->
            <td>{rate}%</td>
            <td>{formatted_premium}</td> <!-- Updated formatting for better readability -->
        </tr>
        <tr>
            <td>Excess Protector - Own Damage</td>
            <td></td>
            <td>{excess_protector}</td>
            <td>{formatted_ex_pr}</td>
        </tr>
        <tr>
            <td>Political/Terrorism Risks/RSCC</td>
            <td></td>
            <td>{pvt}</td>
            <td>{formatted_pvt}</td>
        </tr>
        <tr>
            <td>Loss of Use/Courtesy Car</td>
            <td></td>
            <td>{loss_of_use}</td>
            <td>{formatted_car_hire}</td>
        </tr>
        <tr>
            <td>Gross Premium</td>
            <td></td> 
            <td></td>
            <td>{formatted_gross_premium}</td> 
        </tr>
        <tr>
            <td>Levies</td>
            <td></td>
            <td>0.45%</td>
            <td>{formatted_levies}</td> <!-- Updated formatting for better readability -->
        </tr>
        <tr>
            <td>Policy Fee</td>
            <td></td>
            <td></td>
            <td>{fee}</td>
        </tr>
        <tr ">
            <td class= 'bold' style="color:#152637">Total Premium Payable</td>
            <td></td>
            <td></td>
            <td class = 'bold' style="color:#152637">{formatted_total} /-</td>
        </tr>
    </table>
    </body>
        
    </html>
    """
    
# Create a download button with customized file name

    st.download_button(
        label=f"Download {reg}'s_premium_quote(HTML)",
        data=html_report.encode('utf-8'),
        file_name=f"{reg}_quote.html",
        mime="text/html"
    )


    


