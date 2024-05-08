import streamlit as st
import pandas as pd



tab1, tab2, tab3 = st.tabs(["Motor Private", "📈 Motor Private PSV",  "📈 Motor Commercial"])

with tab1:

    reg = st.text_input('Enter Registration')
    underwriter = st.selectbox("Choose Underwriter", ["APA INSURANCE", "FIDELITY INSURANCE", "CANNON GENERAL INSURANCE", "GA INSURANCE", "MAYFAIR INSURANCE", "ICEA LION INSURANCE", "JUBILEE ALLIANZ"])
    value = int(st.number_input('Sum Insured'))
    rate = st.number_input('Rate as a number eg 4 0r 3.5')
    days = st.number_input('Pro-Rated Days')
    excess_protector = st.selectbox("Choose excess protector rate", ["Inclusive", "0.25%", "0.5%", "Excluded"])
    pvt = st.selectbox("Choose pvt rate", ["Inclusive", "0.25%", "0.5%", "Excluded"])
    loss_of_use = st.selectbox("Choose amount charged", ["N/A", "KES 3000", "KES 45000"])
    policy_fee = st.selectbox("Choose cover", ["Renewal", "New Business",])
    notes = st.text_input("Include Important Remarks eg. Cover does not include Excess Protector")
                                                        

    car_hire = 0
    fee = 0
    ex_pr = 0
    pvt_value = 0

    if st.button("Calculate"):
        premium = value * (rate/100) * (days/366)

        if pvt == 'Inclusive' or 'Excluded':
            pvt_value += 0
        if pvt == '0.25%':
            pvtworking = (0.25/100) * value
            pvt_value += pvtworking
        if pvt == '0.5%':
            pvtworking = (0.5/100) * value
            pvt_value += pvtworking

        if excess_protector == 'Inclusive' or 'Exluded':
            ex_pr += 0
        if excess_protector == '0.25%':
            working = (0.25/100) * value
            ex_pr += working
        if excess_protector == '0.5%':
            working = (0.5/100) * value
            ex_pr += working

        
        if loss_of_use == 'KES 3000':
            car_hire += 3000
        if loss_of_use == 'N/A':
            car_hire += 0
        if loss_of_use == 'KES 4500':
            car_hire += 4500
        if policy_fee == "Renewal":
            fee += 100
        if policy_fee == "New Business":
            fee += 40

        gross_premium = ( premium + car_hire + ex_pr + pvt_value )

        levies = gross_premium * 0.0045

        total = ( gross_premium + fee + levies  )

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
            width: 45%;
            margin: 2.5px auto; /* Center the table */
            font-size: 10px;
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

        .gross_premium {{
            border-top: 2px solid black;
            border-bottom: 2px double black;        
        }}

        .footer-row th {{
            background-color: #073980;
        }}

        
        
        </style>
        </head>
        <body>
        <table>
            <tr>
                <th colspan="2">{reg} - MOTOR PRIVATE COMPREHENSIVE</th>
                <th colspan="2">{underwriter} </th>
                
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
                <td style="color:red">{rate}%</td>
                <td>{formatted_premium}</td> <!-- Updated formatting for better readability -->
            </tr>
            <tr>
                <td>Excess Protector - Own Damage</td>
                <td></td>
                <td style="color:red" >{excess_protector}</td>
                <td>{formatted_ex_pr}</td>
            </tr>
            <tr>
                <td>Political/Terrorism Risks/RSCC</td>
                <td></td>
                <td style="color:red">{pvt}</td>
                <td>{formatted_pvt}</td>
            </tr>
            <tr>
                <td>Loss of Use/Courtesy Car</td>
                <td></td>
                <td style="color:red" ></td>
                <td>{formatted_car_hire}</td>
            </tr>
            <tr>
                <td>Gross Premium</td>
                <td></td> 
                <td></td>
                <td class='gross_premium'>{formatted_gross_premium}</td> 
            </tr>
            <tr>
                <td>Levies</td>
                <td></td>
                <td style="color:red">0.45%</td>
                <td >{formatted_levies}</td> <!-- Updated formatting for better readability -->
            </tr>
            <tr>
                <td>Policy Fee</td>
                <td></td>
                <td></td>
                <td>{fee}</td>
            </tr>
            <tr style=" border-top: 2px double black;  border-bottom: 2px double black;">
                <td class= 'bold' style="color:#152637">Total Premium Payable</td>
                <td></td>
                <td></td>
                <td class = 'bold' style="color:#152637">{formatted_total} /-</td>
            </tr>
            <tr class='footer-row'>
            
                <th colspan="4" style='color:white'>{notes} </th>
                
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



    
with tab2:
    reg = st.text_input('Enter Vehicle Registration')
    underwriter = st.selectbox("Select Underwriter", ["APA INSURANCE", "FIDELITY INSURANCE", "CANNON GENERAL INSURANCE", "GA INSURANCE", "MAYFAIR INSURANCE", "ICEA LION INSURANCE", "JUBILEE ALLIANZ"])
    value = int(st.number_input('Enter Sum Insured'))
    rate = st.number_input('Enter Rate as a number eg 4 ')
    excess_protector = st.selectbox("Select excess protector rate", ["Inclusive", "0.25%", "0.45", "0.5", "Excluded"])
    pvt = st.selectbox("Select pvt rate", ["Inclusive", "0.25%", "0.45", "0.5", "Excluded"])
    pll = st.number_input('Number of Passangers eg 4')
    policy_fee = st.selectbox("Select cover", ["Renewal", "New Business",])
    notes = st.text_input("Include Important Remarks eg. LIMITED TO UBER ONLY")
    
                                                        

    car_hire = 0
    fee = 0
    ex_pr = 0
    pvt_value = 0

    if st.button("Calculate Quote"):
        premium = value * (rate/100)

        if pvt == 'Inclusive' or 'Excluded':
            pvt_value += 0
        if pvt == '0.25%':
            pvtworking = (0.25/100) * value
            pvt_value += pvtworking
        if pvt == '0.45%':
            pvtworking = (0.45/100) * value
            pvt_value += pvtworking
        if pvt == '0.5%':
            pvtworking = (0.5/100) * value
            pvt_value += pvtworking

        if excess_protector == 'Inclusive' or 'Exluded':
            ex_pr += 0
        if excess_protector == '0.25%':
            working = (0.25/100) * value
            ex_pr += working
        if excess_protector == '0.45%':
            working = (0.45/100) * value
            ex_pr += working   
        if excess_protector == '0.5%':
            working = (0.5/100) * value
            ex_pr += working

        
        
        if policy_fee == "Renewal":
            fee += 100
        if policy_fee == "New Business":
            fee += 40

        pll_amount = pll * 500

        gross_premium = ( premium + pll_amount + ex_pr + pvt_value )

        levies = gross_premium * 0.0045

        total = ( gross_premium + fee + levies  )

        # Format numbers with commas for thousands
        def format_with_commas(number):
            rounded_number = round(number, 2)
            return "{:,.2f}".format(rounded_number)
            
        
        formatted_value = format_with_commas(value)
        formatted_premium = format_with_commas(premium)
        formatted_ex_pr = format_with_commas(ex_pr)
        formatted_pvt = format_with_commas(pvt_value)
        formatted_pll = format_with_commas(pll_amount)
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
            width: 45%;
            margin: 2.5px auto; /* Center the table */
            font-size: 10px;
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

        .gross_premium {{
            border-top: 2px solid black;
            border-bottom: 2px double black;        
        }}

        .footer-row th {{
            background-color: #073980;
        }}

        
        
        </style>
        </head>
        <body>
        <table>
            <tr>
                <th colspan="2">{reg} - MOTOR PRIVATE PSV</th>
                <th colspan="2">{underwriter} </th>
                
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
                <td style="color:red">{rate}%</td>
                <td>{formatted_premium}</td> <!-- Updated formatting for better readability -->
            </tr>
            <tr>
                <td>Excess Protector - Own Damage</td>
                <td></td>
                <td style="color:red" >{excess_protector}</td>
                <td>{formatted_ex_pr}</td>
            </tr>
            <tr>
                <td>Political/Terrorism Risks/RSCC</td>
                <td></td>
                <td style="color:red">{pvt}</td>
                <td>{formatted_pvt}</td>
            </tr>
            <tr>
                <td>Passenger Legal Liability</td>
                <td>500 /- each</td>
                <td style="color:red" >{pll}</td>
                <td>{formatted_pll}</td>
            </tr>
            <tr>
                <td>Gross Premium</td>
                <td></td> 
                <td></td>
                <td class='gross_premium'>{formatted_gross_premium}</td> 
            </tr>
            <tr>
                <td>Levies</td>
                <td></td>
                <td style="color:red">0.45%</td>
                <td >{formatted_levies}</td> <!-- Updated formatting for better readability -->
            </tr>
            <tr>
                <td>Policy Fee</td>
                <td></td>
                <td></td>
                <td>{fee}</td>
            </tr>
            <tr style=" border-top: 2px double black;  border-bottom: 2px double black;">
                <td class= 'bold' style="color:#152637">Total Premium Payable</td>
                <td></td>
                <td></td>
                <td class = 'bold' style="color:#152637">{formatted_total} /-</td>
            </tr>
            <tr class='footer-row'>
            
                <th colspan="4" style='color:white'>{notes} </th>
                
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
            






    


