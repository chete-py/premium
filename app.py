import streamlit as st
import pandas as pd
from google.oauth2 import service_account
import gspread
import base64
import datetime


# Define your Google Sheets credentials JSON file (replace with your own)
credentials_path = 'renewals-423611-a0e5b69ee774.json'
    
# Authenticate with Google Sheets using the credentials
credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://spreadsheets.google.com/feeds'])
    
# Authenticate with Google Sheets using gspread
gc = gspread.authorize(credentials)
    
# Your Google Sheets URL
url = "https://docs.google.com/spreadsheets/d/10RkBeRYprne_5q2GDCwW5n_xC3F3ryAGdy4-bMLdxs0/edit#gid=0"
    
# Open the Google Sheets spreadsheet
worksheet = gc.open_by_url(url).worksheet("July")

view1, view2 = st.tabs(["Premium", "Renewal"])

with view1:
    
    tab1, tab2, tab3 = st.tabs(["Motor Private", "📈 Motor Private PSV",  "📈 Motor Private TPO"])
    
    with tab1:
        view = st.radio("Client Type", ["Renewal", "New", "Comperative Quote"])
        if view == 'Renewal':
                        
            reg = st.text_input('Enter Registration')
            underwriter = st.selectbox("Choose Underwriter", ["APA INSURANCE", "FIDELITY INSURANCE", "CANNON GENERAL INSURANCE", "GA INSURANCE", "MAYFAIR INSURANCE", "ICEA LION INSURANCE", "JUBILEE ALLIANZ"])
            if underwriter == "CANNON GENERAL INSURANCE":
                eabl =  st.selectbox("Choose EABL or NON-EABL", ["EABL", "NON-EABL"])
            value = int(st.number_input('Sum Insured'))
            windscreen = int(st.number_input('Windscreen Chargeable difference (above 50K/EABL 250K)'))
            rate = st.number_input('Rate as a number eg 4 0r 3.5')
            days = st.number_input('Pro-Rated Days')
            excess_protector = st.selectbox("Choose excess protector rate", ["Inclusive", "0.25%", "0.5%", "Excluded"])
            pvt = st.selectbox("Choose pvt rate", ["Inclusive", "0.25%", "0.5%", "Excluded"])
            loss_of_use = st.selectbox("Choose amount charged", ["Inclusive", "Excluded", 1500, 3000, 4500, 6000])
            policy_fee = st.selectbox("Choose cover", ["Renewal", "New Business",])
            notes1 = st.text_input("Include Important Remarks 1 eg. Political/Terrorism Risks/RSCC - Reinstated at 0.35% of Value Once utilized")
            notes2 = st.text_input("Include Important Remarks 2 eg.  Days Loss of use/Courtesy Car - Reinstated at KShs. 3,000/- Once Utilized")
            notes3 = st.text_input("Include Important Remarks 3 eg. Excess Protector - Own Damage Reinstated at 0.25% of Value Once utilized")
                                                                
        
            car_hire = 0
            fee = 0
            ex_pr = 0
            pvt_value = 0
        
            if st.button("Calculate"):
                if underwriter == 'FIDELITY INSURANCE':
                    prorata_premium = (max(value * (rate/100), 30000)) + (windscreen * (10/100))
                    premium = prorata_premium * (days/366)
                elif underwriter == 'APA INSURANCE':
                    prorata_premium = (max(value * (rate/100), 25000)) + (windscreen * (10/100))
                    premium = prorata_premium * (days/366)
                elif eabl == 'EABL':
                    prorata_premium = (max(value * (rate/100), 25000)) + (windscreen * (10/100))
                    premium = prorata_premium * (days/366)
                elif eabl == 'NON-EABL':
                    prorata_premium = (max(value * (rate/100), 30000)) + (windscreen * (10/100))
                    premium = prorata_premium * (days/366)
                else:
                    premium = (value * (rate/100) * (days/366)) + (windscreen * (10/100))
    
                
                if pvt == 'Inclusive' or  pvt == 'Excluded':
                    pvt_value += 0
                elif pvt == '0.25%':
                    pvtworking = (0.25/100) * value
                    newpvtworking = max(pvtworking, 2500)
                    pvt_value += newpvtworking
                elif pvt == '0.5%':
                    pvtworking = (0.5/100) * value
                    newpvtworking = max(pvtworking, 2500)
                    pvt_value += newpvtworking
        
                if excess_protector == 'Inclusive' or excess_protector == 'Exluded':
                    ex_pr += 0
                elif excess_protector == '0.25%':
                    working = (0.25/100) * value
                    newworking = max(working, 2500)
                    ex_pr += newworking
                elif excess_protector == '0.5%':
                    working = (0.5/100) * value
                    newworking = max(working, 2500)
                    ex_pr += newworking
        
                if loss_of_use == 'Inclusive' or loss_of_use == 'Exluded':
                    car_hire += 0
                elif loss_of_use == 1500:
                    car_hire += 1500
                elif loss_of_use == 3000:
                    car_hire += 3000
                elif loss_of_use == 4500:
                    car_hire += 4500
                elif loss_of_use == 6000:
                    car_hire += 6000
               
        
                    
                if policy_fee == "Renewal":
                    fee += 100
                elif policy_fee == "New Business":
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
                    width: 30%;
                    margin: 0.25px auto; /* Center the table */
                    font-size: 10px;
                    font-family: Candara;
                }}
        
                th, td {{
                    border: 1px solid black;
                    padding: 2.5px; /* Increased padding for better spacing */
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
                        <td style="color:red" >{loss_of_use}</td>
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
                    
                        <th colspan="4" style='color:white'>
                        {notes1}<br>
                        {notes2}<br>
                        {notes3}
                        </th>
                        
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
    
    
        if view == 'New':
            
            reg = st.text_input('Enter Registration')
            underwriter = st.selectbox("Choose Underwriter", ["APA INSURANCE", "FIDELITY INSURANCE", "CANNON GENERAL INSURANCE", "GA INSURANCE", "MAYFAIR INSURANCE", "ICEA LION INSURANCE", "JUBILEE ALLIANZ"])
            value = int(st.number_input('Sum Insured'))
            rate = st.number_input('Rate as a number eg 4 0r 3.5')
            days = st.number_input('Pro-Rated Days')
            excess_protector = st.selectbox("Choose excess protector rate", ["Inclusive", "0.25%", "0.5%", "Excluded"])
            pvt = st.selectbox("Choose pvt rate", ["Inclusive", "0.25%", "0.5%", "Excluded"])
            loss_of_use = st.selectbox("Choose amount charged", ["Inclusive", "Excluded", 1500, 3000, 4500])
            policy_fee = st.selectbox("Choose cover", ["Renewal", "New Business",])
            notes1 = st.text_input("Include Important Remarks 1 eg. Political/Terrorism Risks/RSCC - Reinstated at 0.35% of Value Once utilized")
            notes2 = st.text_input("Include Important Remarks 2 eg.  Days Loss of use/Courtesy Car - Reinstated at KShs. 3,000/- Once Utilized")
            notes3 = st.text_input("Include Important Remarks 3 eg. Excess Protector - Own Damage Reinstated at 0.25% of Value Once utilized")
                                                                
        
            car_hire = 0
            fee = 0
            ex_pr = 0
            pvt_value = 0
        
            if st.button("Calculate"):
                premium = value * (rate/100) * (days/366)
        
                if pvt == 'Inclusive' or  pvt == 'Excluded':
                    pvt_value += 0
                elif pvt == '0.25%':
                    pvtworking = (0.25/100) * value
                    newpvtworking = max(pvtworking, 2500)
                    pvt_value += newpvtworking
                elif pvt == '0.5%':
                    pvtworking = (0.5/100) * value
                    newpvtworking = max(pvtworking, 2500)
                    pvt_value += newpvtworking
        
                if excess_protector == 'Inclusive' or excess_protector == 'Exluded':
                    ex_pr += 0
                elif excess_protector == '0.25%':
                    working = (0.25/100) * value
                    newworking = max(working, 2500)
                    ex_pr += newworking
                elif excess_protector == '0.5%':
                    working = (0.5/100) * value
                    newworking = max(working, 2500)
                    ex_pr += newworking
        
                if loss_of_use == 'Inclusive' or loss_of_use == 'Exluded':
                    car_hire += 0
                elif loss_of_use == 1500:
                    car_hire += 1500
                elif loss_of_use == 6000:
                    car_hire += 6000
                elif loss_of_use == 4500:
                    car_hire += 4500
                elif loss_of_use == 3000:
                    car_hire += 3000
               
        
                    
                if policy_fee == "Renewal":
                    fee += 100
                elif policy_fee == "New Business":
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
                    border: 1.5px solid black;
                    padding: 2.5px; /* Increased padding for better spacing */
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
                        <td style="color:red" >{loss_of_use}</td>
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
                    
                        <th colspan="4" style='color:white'>
                        {notes1}<br>
                        {notes2}<br>
                        {notes3}
                        </th>
                        
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
 
        if view == 'Comperative Quote':
            
            reg = st.text_input('Enter Registration')            
            value = int(st.number_input('Sum Insured')) 
            loss_of_use = st.selectbox("Choose amount charged", ["Inclusive", "Excluded", 3000])
            windscreen = int(st.number_input('Windscreen Amount Above Free Limit'))
            days = st.number_input('Pro-Rated Days')           
            notes1 = st.text_input("Include Important Remarks 1 eg. Political/Terrorism Risks/RSCC - Reinstated at 0.35% of Value Once utilized")
            notes2 = st.text_input("Include Important Remarks 2 eg.  Days Loss of use/Courtesy Car - Reinstated at KShs. 3,000/- Once Utilized")
            notes3 = st.text_input("Include Important Remarks 3 eg. Excess Protector - Own Damage Reinstated at 0.25% of Value Once utilized")
            
            
            if value > 0:
                cannon_rate = 4
                cannon_premium = max(value * (cannon_rate/100) * (days/366),37500)
            elif value < 0:
                cannon_rate = 0               
            
            
            if value > 600000 and value < 1000000:
                apa_rate = 6
                apa_premium = max(value * (apa_rate/100) * (days/366),42500)
            elif value > 999999 and value < 2500000:
                apa_rate = 4
                apa_premium = (value * (apa_rate/100) * (days/366))
            elif value > 2499999 and value < 5000000:
                apa_rate = 3.5
                apa_premium = (value * (apa_rate/100) * (days/366))
            elif value > 4999999 and value < 10000000:
                apa_rate = 3
                apa_premium = (value * (apa_rate/100) * (days/366))
            elif value > 10000000:
                apa_rate = 3.5
                apa_premium = (value * (apa_rate/100) * (days/366))


            if value > 0 and value < 1000000:
                fidelity_rate = 6                
                fidelity_one = (value * (fidelity_rate/100) * (days/366))
                fidelity_premium = max(fidelity_one, 37500)                 
            elif value > 999999 and value < 1500000:
                fidelity_rate = 4.75
                fidelity_premium = (value * (fidelity_rate/100) * (days/366))
            elif value > 1499999 and value < 2500000:
                fidelity_rate = 3.75
                fidelity_premium = (value * (fidelity_rate/100) * (days/366))            
            elif value > 2500000:
                fidelity_rate = 3
                fidelity_premium = (value * (fidelity_rate/100) * (days/366))

            fidelity_pvt = max(value * (0.25/100), 2500)
            fidelity_ex_prt = max(value * (0.25/100), 2500)
            

            if value > 0 and value < 1000000:
                icea_rate = 6
                icea_premium = max((value * (icea_rate/100) * (days/366)),37500)
            elif value > 999999 and value < 1500000:
                icea_rate = 5
                icea_premium = max(value * (icea_rate/100) * (days/366), 60000)
            elif value > 1499999 and value < 2500000:
                icea_rate = 4
                icea_premium = max(value * (icea_rate/100) * (days/366), 75000)
            elif value > 2499999 and value < 5000000:
                icea_rate = 3.5
                icea_premium = max(value * (icea_rate/100) * (days/366), 100000)
            elif value > 5000000:
                icea_rate = 3
                icea_premium = max(value * (icea_rate/100) * (days/366), 175000)
            
        
            car_hire = 0
            fee = 100
            ex_pr = 0
            pvt_value = 0
        
            if st.button("Calculate"):

                

                if loss_of_use == 'Inclusive' or loss_of_use == 'Exluded':
                    car_hire += 0
                elif loss_of_use == 1500:
                    car_hire += 1500
                elif loss_of_use == 6000:
                    car_hire += 6000
                elif loss_of_use == 4500:
                    car_hire += 4500
                elif loss_of_use == 3000:
                    car_hire += 3000
                              
                cannon_gross_premium = (cannon_premium + fidelity_pvt + fidelity_ex_prt + car_hire)
                fidelity_gross_premium = (fidelity_premium + fidelity_pvt + fidelity_ex_prt + car_hire)
                icea_gross_premium = ( icea_premium + fidelity_pvt + fidelity_ex_prt + car_hire)
                apa_gross_premium = ( apa_premium + car_hire)
        
                cannon_levies = cannon_gross_premium * 0.0045
                fidelity_levies = fidelity_gross_premium * 0.0045
                icea_levies = icea_gross_premium * 0.0045
                apa_levies = apa_gross_premium * 0.0045 
               
        
                cannon_total = ( cannon_gross_premium + fee + cannon_levies  )
                fidelity_total = ( fidelity_gross_premium + fee + fidelity_levies  )
                icea_total = ( icea_gross_premium + fee + icea_levies  )
                apa_total = ( apa_gross_premium + fee + apa_levies  )
               
        
                # Format numbers with commas for thousands
                def format_with_commas(number):
                    rounded_number = round(number, 2)
                    return "{:,.2f}".format(rounded_number)
                    
                
                formatted_value = format_with_commas(value)

                formatted_value = format_with_commas(fidelity_pvt)

                formatted_value = format_with_commas(fidelity_ex_prt)

                formatted_cannon_premium = format_with_commas(cannon_premium)
                formatted_icea_premium = format_with_commas(icea_premium)
                formatted_fidelity_premium = format_with_commas(fidelity_premium)
                formatted_apa_premium = format_with_commas(apa_premium)
             
               
                formatted_car_hire = format_with_commas(car_hire)

                
                formatted_icea_gross_premium = format_with_commas(icea_gross_premium)
                formatted_fidelity_gross_premium = format_with_commas(fidelity_gross_premium)
                formatted_apa_gross_premium = format_with_commas(apa_gross_premium)
                formatted_cannon_gross_premium = format_with_commas(cannon_gross_premium)

                
                formatted_icea_levies = format_with_commas(icea_levies)
                formatted_fidelity_levies = format_with_commas(fidelity_levies)
                formatted_apa_levies = format_with_commas(apa_levies)
                formatted_cannon_levies = format_with_commas(cannon_levies)

                
                formatted_icea_total = format_with_commas(icea_total)
                formatted_fidelity_total = format_with_commas(fidelity_total)
                formatted_apa_total = format_with_commas(apa_total)              
                formatted_cannon_total = format_with_commas(cannon_total)
        
        
                # Create an HTML report
                html_report = f"""
                <html>
                <head>
                <style>
                    table {{
                    border-collapse: collapse;
                    width: 45%;
                    margin: 0.5px auto; /* Center the table */
                    font-size: 8px;
                    font-family: Candara;
                }}
        
                th, td {{
                    border: 1px solid black;
                    padding: 2.5px; /* Increased padding for better spacing */
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
                        <th colspan="2">CANNON</th>                       
                        <th colspan="2">APA</th>
                        <th colspan="2">FIDELITY</th>
                        <th colspan="2">ICEA LION</th>
                        
                    </tr>
                    <tr >
                        <th style="background-color: #17B169"></th>
                        <th style="background-color: #17B169">Value - KES</th>
                        <th style="background-color: #17B169">Rate</th>
                        <th style="background-color: #17B169">Premium</th>
                        <th style="background-color: #17B169">Rate</th>
                        <th style="background-color: #17B169">Premium</th>
                        <th style="background-color: #17B169">Rate</th>
                        <th style="background-color: #17B169">Premium</th>
                        <th style="background-color: #17B169">Rate</th>
                        <th style="background-color: #17B169">Premium</th>
                    </tr>
                    <tr>
                        <td>Basic Premium</td>
                        <td>{value}</td> <!-- Updated formatting for better readability -->
                        <td style="color:red">{cannon_rate}%</td>
                        <td>{formatted_cannon_premium}</td> <!-- Updated formatting for better readability -->
                        <td style="color:red">{apa_rate}%</td>
                        <td>{formatted_apa_premium}</td> <!-- Updated formatting for better readability -->
                        <td style="color:red">{fidelity_rate}%</td>
                        <td>{formatted_fidelity_premium}</td> <!-- Updated formatting for better readability -->
                        <td style="color:red">{icea_rate}%</td>
                        <td>{formatted_icea_premium}</td> <!-- Updated formatting for better readability -->
                    </tr>
                    

                    <tr>
                        <td>Excess Protector</td>
                        <td></td>
                        <td style="color:red">0.25%</td>
                        <td >{fidelity_ex_prt}</td>                       
                        <td style="color:red">Inclusive</td>  
                        <td >0.00</td>
                        <td style="color:red">0.25%</td>
                        <td >{fidelity_ex_prt}</td>              
                        <td style="color:red">0.25%</td>
                        <td>{fidelity_ex_prt}</td>
                    </tr>

                    
                    <tr>
                        <td>Political/Terrorism Risks</td>
                        <td></td>
                        <td style="color:red">0.25%</td>
                        <td >{fidelity_pvt}</td>                       
                        <td style="color:red">Inclusive</td>  
                        <td >0.00</td>
                        <td style="color:red">0.25%</td>
                        <td >{fidelity_pvt}</td>              
                        <td style="color:red">0.25%</td>
                        <td>{fidelity_pvt}</td>                        
                    </tr>
                    
                    
                    <tr>
                        <td>Courtesy Car</td>                        
                        <td></td>
                        <td style="color:red" >{loss_of_use}</td>
                        <td>{formatted_car_hire}</td>
                        <td style="color:red" >{loss_of_use}</td>
                        <td>{formatted_car_hire}</td>
                        <td style="color:red" >{loss_of_use}</td>
                        <td>{formatted_car_hire}</td>
                        <td style="color:red" >{loss_of_use}</td>
                        <td>{formatted_car_hire}</td>
                    </tr>
                    
                    <tr>
                        <td>Gross Premium</td>
                        <td></td> 
                        <td></td>
                        <td class='gross_premium'>{formatted_cannon_gross_premium}</td> 
                        <td></td>
                        <td class='gross_premium'>{formatted_apa_gross_premium}</td> 
                        <td></td>
                        <td class='gross_premium'>{formatted_fidelity_gross_premium}</td> 
                        <td></td>
                        <td class='gross_premium'>{formatted_icea_gross_premium}</td> 
                    </tr>
                    <tr>
                        <td>Levies</td>
                        <td></td>
                        <td style="color:red">0.45%</td>
                        <td >{formatted_cannon_levies}</td> <!-- Updated formatting for better readability -->
                        <td style="color:red">0.45%</td>
                        <td >{formatted_apa_levies}</td> <!-- Updated formatting for better readability -->
                        <td style="color:red">0.45%</td>
                        <td >{formatted_fidelity_levies}</td> <!-- Updated formatting for better readability -->
                        <td style="color:red">0.45%</td>
                        <td >{formatted_icea_levies}</td> <!-- Updated formatting for better readability -->
                    </tr>
                    <tr>
                        <td>Policy Fee</td>
                        <td></td>
                        <td></td>
                        <td>{fee}</td>
                        <td></td>
                        <td>{fee}</td>
                        <td></td>
                        <td>{fee}</td>
                        <td></td>
                        <td>{fee}</td>
                    </tr>
                    <tr style=" border-top: 2px double black;  border-bottom: 2px double black;">
                        <td class= 'bold' style="color:#152637">Total Premium Payable</td>
                        <td></td>
                        <td></td>
                        <td class = 'bold' style="color:#152637">{formatted_cannon_total} /-</td>
                        <td></td>
                        <td class = 'bold' style="color:#152637">{formatted_apa_total} /-</td>
                        <td></td>
                        <td class = 'bold' style="color:#152637">{formatted_fidelity_total} /-</td>
                        <td></td>
                        <td class = 'bold' style="color:#152637">{formatted_icea_total} /-</td>
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
        underwriter = st.selectbox("Select Underwriter", ["GA INSURANCE", "JUBILEE ALLIANZ"])
        value = int(st.number_input('Enter Sum Insured'))
        rate = st.number_input('Enter Rate as a number eg 7.5 ')
        excess_protector = st.selectbox("Select excess protector rate", ["Inclusive", "0.25%", "0.45", "0.5", "Excluded"])
        pvt = st.selectbox("Select pvt rate", ["Inclusive", "0.25%", "0.5%", "Excluded"])
        pll = st.number_input('Number of Passangers eg 4')
        policy_fee = st.selectbox("Select cover", ["Renewal", "New Business",])
        notes = st.text_input("Include Important Remarks eg. LIMITED TO UBER ONLY")
        
                                                            
    
        car_hire = 0
        fee = 0
        ex_pr = 0
        pvt_value = 0
    
        if st.button("Calculate Quote"):
            if underwriter == 'GA INSURANCE':
                premium = max(value * (rate/100), 37500)                                
    
            if pvt == 'Inclusive' or 'Excluded':
                pvt_value += 0
            if pvt == '0.25%':
                pvtworking = max((0.25/100) * value, 5000)
                pvt_value += pvtworking

            if pvt == '0.5%':
                pvtworking = max((0.5/100) * value, 5000)
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

    with tab3:
        reg = st.text_input('Enter Vehicle Reg')
        underwriter = st.selectbox("Select Underwriter", ["APA INSURANCE", "FIDELITY INSURANCE", "CANNON GENERAL INSURANCE", "GA INSURANCE", "MAYFAIR INSURANCE", "ICEA LION GENERAL INSURANCE", "JUBILEE ALLIANZ"])
        premium = int(st.number_input('Enter Premium Payable'))      
        notes = st.text_input("Include Important Remarks eg. COVERS THIRD PARTY ONLY")
        
                                                            
        fee = 0
    
        if st.button("Calculate Quote", key='tpo'):          
            
            if policy_fee == "Renewal":
                fee += 100
            if policy_fee == "New Business":
                fee += 40
    
            
    
            gross_premium = (premium + 0)
    
            levies = gross_premium * 0.0045
    
            total = ( gross_premium + fee + levies  )
    
            # Format numbers with commas for thousands
            def format_with_commas(number):
                rounded_number = round(number, 2)
                return "{:,.2f}".format(rounded_number)
                
        
            formatted_premium = format_with_commas(premium)
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
                    <th colspan="2">{reg} - MOTOR PRIVATE TPO COVER</th>
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
                    <td>{premium}/-</td> <!-- Updated formatting for better readability -->
                    <td style="color:red"></td>
                    <td>{formatted_gross_premium}</td> <!-- Updated formatting for better readability -->
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
                label=f"Download {reg}'s_tpo_premium_quote(HTML)",
                data=html_report.encode('utf-8'),
                file_name=f"{reg}_quote.html",
                mime="text/html"
            )
                

                



with view2:
    def check_password():
        """Returns `True` if the user entered a correct password."""
        return st.session_state.get("password_correct", False)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False
    
    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Submit", on_click=password_entered)
        st.stop()
    
    if not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Submit", on_click=password_entered)
        st.error("User not known or incorrect password")
        st.stop()
    
    if check_password():     
       
        # Read data from the Google Sheets worksheet
        data = worksheet.get_all_values()
        headers = data[0]
        data = data[1:]
    
        df = pd.DataFrame(data, columns=headers)

        df['Key'] = df['Key'].astype(int)

        
        df['Date'] = pd.to_datetime(df['Date'])
        
        df['Renewal Month'] = df['Date'].dt.month_name()

        # Get the unique reviewer names from the DataFrame
        unique_outcome = df['Renewal Month'].unique()
  
        # Create a dropdown to select a reviewer with "All" option
        selected = st.selectbox("Filter by Outcome:", ["All"] + list(unique_outcome))
  
        if selected != "All":
            # Filter the DataFrame based on the selected reviewer
            final_df = df[df['Renewal Month'] == selected]
  
        else:
            # If "All" is selected, show the entire DataFrame
            final_df = df

        task1, task2, task3, task4, task5, task6 = st.tabs(["Work Load", "Invite Sent", "Valuation", "Renewed", "Debited", "Exits"])

        with task1:
            workload = final_df[final_df['Status'] == 'Pending']
            edited_df =  st.data_editor(workload, key = 'workload')
            merged = pd.concat([final_df, edited_df])
            finalmerged = merged.drop_duplicates(subset=['Key'], keep='last')
            descending = finalmerged.sort_values(by=['Key'], ascending=True)
            df1 = descending.astype(str).fillna('')
            num = len(workload)
            st.markdown(f'Pending Invites: {num}')
            # Add a button to update Google Sheets with the changes
            if st.button("Update Records", key='button1'):   
                worksheet.clear()
                worksheet.update([df1.columns.tolist()] + df1.values.tolist())
        
        with task2:
            invited = final_df[final_df['Status'] == 'Invited']            
            edited_df =  st.data_editor(invited, key = 'invited')
            merged = pd.concat([final_df, edited_df])
            finalmerged = merged.drop_duplicates(subset=['Key'], keep='last')
            descending = finalmerged.sort_values(by=['Key'], ascending=True)
            df2 = descending.astype(str).fillna('')    
            num = len(invited)
            st.markdown(f'Invite Sent: {num}')
            # Add a button to update Google Sheets with the changes
            if st.button("Update Records", key='button2'):   
                worksheet.clear()
                worksheet.update([df2.columns.tolist()] + df2.values.tolist())



        with task3:
            valued = final_df[final_df['Status'] == 'Valued']
            edited_df =  st.data_editor(valued, key = 'valued')
            merged = pd.concat([final_df, edited_df])
            finalmerged = merged.drop_duplicates(subset=['Key'], keep='last')
            descending = finalmerged.sort_values(by=['Key'], ascending=True)
            df3 = descending.astype(str).fillna('') 
            num = len(valued)
            st.markdown(f'Valued: {num}')
            # Add a button to update Google Sheets with the changes
            if st.button("Update Records", key='button3'):   
                worksheet.clear()
                worksheet.update([df3.columns.tolist()] + df3.values.tolist())      
           
        
        with task4:
            renewed = final_df[final_df['Status'] == 'Renewed']
            edited_df =  st.data_editor(renewed, key = 'renewed')
            merged = pd.concat([final_df, edited_df])
            finalmerged = merged.drop_duplicates(subset=['Key'], keep='last')
            descending = finalmerged.sort_values(by=['Key'], ascending=True)
            df4 = descending.astype(str).fillna('') 
            num = len(renewed)
            st.markdown(f'Renewed: {num}')
            # Add a button to update Google Sheets with the changes
            if st.button("Update Records", key='button4'):   
                worksheet.clear()
                worksheet.update([df4.columns.tolist()] + df4.values.tolist())
        
            
        with task5:
            debited = final_df[final_df['Status'] == 'Debited']
            edited_df = st.data_editor(debited, key='debited')
            merged = pd.concat([final_df, edited_df])
            finalmerged = merged.drop_duplicates(subset=['Key'], keep='last')
            descending = finalmerged.sort_values(by=['Key'], ascending=True)
            df5 = descending.astype(str).fillna('') 
            num = len(debited)
            st.markdown(f'Certificate Issued: {num}')
            # Add a button to update Google Sheets with the changes
            if st.button("Update Records", key='button5'):   
                worksheet.clear()
                worksheet.update([df5.columns.tolist()] + df5.values.tolist())
        
           
                
        with task6:
            exits = final_df[final_df['Status'] == 'Exits']
            edited_df = st.data_editor(exits, key='exits')
            merged = pd.concat([final_df, edited_df])
            finalmerged = merged.drop_duplicates(subset=['Key'], keep='last')
            descending = finalmerged.sort_values(by=['Key'], ascending=True)
            df6 = descending.astype(str).fillna('')  
            num = len(exits)
            st.markdown(f'Cancelled Policy: {num}')
            # Add a button to update Google Sheets with the changes
            if st.button("Update Records", key='button6'):   
                worksheet.clear()
                worksheet.update([df6.columns.tolist()] + df6.values.tolist())
        

            



    






    


