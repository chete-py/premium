import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, datetime, timedelta
from google.oauth2 import service_account
import gspread
import json
import base64
import re
    
view1, view2, view3 = st.tabs(["Premium", "Renewal", "Aviation"])

with view1:
   
    tab1, tab2, tab3, tab4 = st.tabs(["Motor Private", "📈 Motor Private PSV",  "📈 Motor Private TPO", "Motor Commercial"])
    
    with tab1:
        view = st.radio("Client Type", ["Renewal",  "Comperative Quote"])
        if view == 'Renewal':
                        
            reg = st.text_input('Enter Registration')
            underwriter = st.selectbox("Choose Underwriter", ["APA INSURANCE", "FIDELITY INSURANCE", "CANNON GENERAL INSURANCE", "GA INSURANCE", "ICEA LION INSURANCE"])
            if underwriter == "CANNON GENERAL INSURANCE":
                scheme =  st.selectbox("Choose EABL/VIVO/INDIVIDUAL", ["EABL", "VIVO", "INDIVIDUAL"])
            elif underwriter == "FIDELITY INSURANCE":
                tetra =  st.selectbox("Choose INDIVIDUAL or TETRA PAK STAFF", ["INDIVIDUAL", "TETRA PAK STAFF", "DIVERSEY"])
            value = int(st.number_input('Sum Insured'))            
            windscreen = int(st.number_input('Windscreen Chargeable difference (above 50K/EABL 250K)'))
            rate = st.number_input('Rate as a number eg 4 0r 3.5')
            days = st.number_input('Pro-Rated Days')
            excess_protector = st.selectbox("Choose excess protector rate", ["Inclusive", "0.25%", "0.5%", "Excluded"])
            pvt = st.selectbox("Choose pvt rate", ["Inclusive", "0.25%", "0.5%", "Excluded"])
            loss_of_use = st.selectbox("Choose Loss Of Use Amount Charged", [1500, 3000, "Inclusive", "Excluded", 4500, 6000])
            aa_membership = st.selectbox("Choose AA Memebreship Amount Charged", ["Excluded", 5000, 6500])
            policy_fee = st.selectbox("Choose cover", ["Renewal", "New Business",])
            notes1 = st.text_input("Include Important Remarks 1 eg. Political/Terrorism Risks/RSCC - Reinstated at 0.35% of Value Once utilized")
            notes2 = st.text_input("Include Important Remarks 2 eg.  Days Loss of use/Courtesy Car - Reinstated at KShs. 3,000/- Once Utilized")
            notes3 = st.text_input("Include Important Remarks 3 eg. Excess Protector - Own Damage Reinstated at 0.25% of Value Once utilized")
                                                                
        
            car_hire = 0
            fee = 0
            ex_pr = 0
            pvt_value = 0
            aa_fee = 0
        
            if st.button("Calculate"):
                if underwriter == 'APA INSURANCE':
                    prorata_premium = (max(value * (rate/100), 25000)) + (windscreen * (10/100))
                    premium = prorata_premium * (days/365)                            
                elif underwriter == 'GA INSURANCE':
                    prorata_premium = (max(value * (rate/100), 25000)) + (windscreen * (10/100))
                    premium = prorata_premium * (days/365)
                elif underwriter == 'ICEA LION INSURANCE':
                    prorata_premium = (max(value * (rate/100), 37500)) + (windscreen * (10/100))
                    premium = prorata_premium * (days/365)
                elif underwriter == 'FIDELITY INSURANCE' and tetra == 'INDIVIDUAL':
                    prorata_premium = (max(value * (rate/100), 30000)) + (windscreen * (10/100))
                    premium = prorata_premium * (days/365)                
                elif underwriter == 'FIDELITY INSURANCE' and tetra == 'TETRA PAK STAFF':
                    prorata_premium = (max(value * (3.5/100), 25000)) + (windscreen * (10/100))
                    premium = prorata_premium * (days/365) 
                elif underwriter == 'FIDELITY INSURANCE' and tetra == 'DIVERSEY':
                    prorata_premium = (max(value * (3.5/100), 20000)) + (windscreen * (10/100))
                    premium = prorata_premium * (days/365) 
                elif underwriter == "CANNON GENERAL INSURANCE" and scheme == 'EABL':
                    prorata_premium = (max(value * (rate/100), 25000)) + (windscreen * (10/100))
                    premium = prorata_premium * (days/365)
                elif underwriter == "CANNON GENERAL INSURANCE" and scheme == 'VIVO':
                    prorata_premium = (max(value * (3/100), 22500)) + (windscreen * (10/100))
                    premium = prorata_premium * (days/365)
                elif underwriter == "CANNON GENERAL INSURANCE" and scheme == 'INDIVIDUAL':
                    prorata_premium = (max(value * (rate/100), 30000)) + (windscreen * (10/100))
                    premium = prorata_premium * (days/365)
                else:
                    premium = (value * (rate/100) * (days/365)) + (windscreen * (10/100))
    
                
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

                if aa_membership ==  'Exluded':
                    aa_fee += 0
                elif aa_membership == 5000:
                    aa_fee += 5000
                elif aa_membership == 6500:
                    aa_fee += 6500                           
                    
                if policy_fee == "Renewal":
                    fee += 100
                elif policy_fee == "New Business":
                    fee += 40
        
                gross_premium = ( premium + car_hire + ex_pr + pvt_value )
        
                levies = gross_premium * 0.0045
        
                total = ( gross_premium + aa_fee + fee + levies  )
        
                # Format numbers with commas for thousands
                def format_with_commas(number):
                    rounded_number = round(number, 2)
                    return "{:,.2f}".format(rounded_number)
                    
                
                formatted_value = format_with_commas(value)
                formatted_premium = format_with_commas(premium)
                formatted_ex_pr = format_with_commas(ex_pr)
                formatted_pvt = format_with_commas(pvt_value)
                formatted_car_hire = format_with_commas(car_hire)
                formatted_aa_fee = format_with_commas(aa_fee)
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
                    font-size: 7px;
                    font-family: Candara;
                }}
        
                th, td {{
                    border: 1.5px solid black;
                    padding: 0.5px; /* Increased padding for better spacing */
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
                        <th colspan="2">MOTOR PRIVATE COMPREHENSIVE</th>
                        <th colspan="2">{underwriter} </th>
                        
                    </tr>
                    <tr >
                        <th style="background-color: #17B169">{reg}</th>
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
                        <td>Excess Protector</td>
                        <td></td>
                        <td style="color:red" >{excess_protector}</td>
                        <td>{formatted_ex_pr}</td>
                    </tr>
                    <tr>
                        <td>Political/Terrorism Risks</td>
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
                    <tr>
                        <td>AA Membership Fee(Optional)</td>
                        <td></td>
                        <td style="color:red">{aa_membership}</td>
                        <td>{formatted_aa_fee}</td>
                    </tr>
                    <tr style=" border-top: 2px double black;  border-bottom: 2px double black;">
                        <td class= 'bold' style="color:#152637">Total Premium</td>
                        <td></td>
                        <td></td>
                        <td class = 'bold' style="color:#152637">{formatted_total}</td>
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
            staff = st.selectbox("Prepared By:", ["Collins Chetekei", "Daniel Cheruiyot", "Patrick Kimani", "Ephantus Ngari", "Samuel Ndoto", "Charity Rono", "Monica Waruguru"])
            loss_of_use = st.selectbox("Choose Loss Of Use Amount charged", [3000, 5000, "Excluded"])
            windscreen = int(st.number_input('Windscreen Amount Above Free Limit'))
            span = st.selectbox("Choose Length of cover", ["Annual Cover", "Pro-Rated Cover"])
            if span == "Pro-Rated Cover":                
                days = st.number_input('Number of days on cover')   
            else:
                days = 365        

            
            today = date.today()
            long_date = today.strftime("%A, %B %d, %Y")

          # Format numbers with commas for thousands
            def format_with_commas(number):
                rounded_number = round(number, 2)
                return "{:,.2f}".format(rounded_number)
            
            if staff == "Collins Chetekei":
                phone = '0791 530 369'
            elif staff == "Daniel Cheruiyot":
                phone = "0796 224 855"
            elif staff == "Samuel Ndoto":
                phone = "0758 704 545"
            elif staff == "Patrick Kimani":
                phone = "0718 246 921"
            elif staff == "Ephantus Ngari":
                phone = "0712 853 717"
            elif staff == "Charity Rono":
                phone = "0793 269 588"
            elif staff == "Monica Waruguru":
                phone = "0792 448 161"
                

            if value > 3000000:
                om_pvt = 'Inclusive'
                om_ex_prt = 'Inclusive'
                formatted_om_pvt = 0.00
                formatted_om_ex_prt = 0.00
                lou_rate = '3000'
                lou = 3000
            else:
                om_pvt = '0.25%'
                om_ex_prt = '0.25%'
                formatted_om_pvt = format_with_commas(max(value * (0.25/100), 2500))
                formatted_om_ex_prt = format_with_commas(max(value * (0.25/100), 2500))
                if loss_of_use == 3000:
                    lou_rate = 3000
                    lou = 3000
                else:
                    lou_rate = 'Excluded'
                    lou = 0.00

            
            
            car_hire = 0
            fee = 100
            ex_pr = 0
            pvt_value = 0
            excess = (value * 2.5/100)
            
            if excess < 20000:
                excess = 20000
            elif excess > 100000:
                excess = 100000
            new_excess = format_with_commas(excess)

            if loss_of_use == 'Exluded':
                car_hire += 0                
            elif loss_of_use == 3000:
                car_hire += 3000
            elif loss_of_use == 5000:
                car_hire += 5000


            if value < 500000:
                cannon_rate = 'Minimum 500K'
                formatted_cannon_gross_premium = 'NA'
                formatted_cannon_premium = 'NA'
                formatted_cannon_levies = 'NA'
                formatted_cannon_total = 'Consider TPO'
                formatted_cannon_car_hire = 'NA'
            else:                
                if value > 499999 and value < 1000000:
                    cannon_rate = 5.5
                    cannon_premium = max(value * (cannon_rate/100) * (days/365), (42500 * (days/365)))
                 
                elif value > 999999 and value < 1499999:
                    cannon_rate = 5.5
                    cannon_premium = max(value * (cannon_rate/100) * (days/365), (60000 * (days/365)))
                elif value > 1499999 and value < 2499999:
                    cannon_rate = 4
                    cannon_premium = max(value * (cannon_rate/100) * (days/365), (75000 * (days/365)))
                elif value > 2499999 and value < 4999999:
                    cannon_rate = 3.5
                    cannon_premium = max(value * (cannon_rate/100) * (days/365), (100000 * (days/365)))
                elif value > 4999999:
                    cannon_rate = 3.25
                    cannon_premium = max(value * (cannon_rate/100) * (days/365), (175000 * (days/365)))

                cannon_gross_premium = (cannon_premium + car_hire)
                cannon_levies = cannon_gross_premium * 0.0045
                cannon_total = ( cannon_gross_premium + fee + cannon_levies )
                formatted_cannon_premium = format_with_commas(cannon_premium)
                formatted_cannon_gross_premium = format_with_commas(cannon_gross_premium)
                formatted_cannon_levies = format_with_commas(cannon_levies)
                formatted_cannon_total = format_with_commas(cannon_total)
                formatted_cannon_car_hire = format_with_commas(car_hire)

            
            
            if value < 600000:
                apa_rate = 'Minimum 500K'
                formatted_apa_gross_premium = 'NA'
                formatted_apa_premium = 'NA'
                formatted_apa_levies = 'NA'
                formatted_apa_total = 'Consider TPO'
                formatted_apa_car_hire = 'NA'
            else:
                if value > 599999 and value < 1000000:
                    apa_rate = 6
                    apa_premium = max(value * (apa_rate/100) * (days/365), (42500 * (days/365)))
             
                elif value > 999999 and value < 2500000:
                    apa_rate = 4
                    apa_premium = max(value * (apa_rate/100) * (days/365), (42500 * (days/365)))
                elif value > 2499999 and value < 5000001:
                    apa_rate = 3.5
                    apa_premium = (value * (apa_rate/100) * (days/365))
                elif value > 5000000:
                    apa_rate = 3
                    apa_premium = (value * (apa_rate/100) * (days/365))
                # elif value > 9999999:
                #     apa_rate = 3.5
                #     apa_premium = (value * (apa_rate/100) * (days/365))

                apa_gross_premium = ( apa_premium + car_hire)
                apa_levies = apa_gross_premium * 0.0045
                apa_total = ( apa_gross_premium + fee + apa_levies )
                formatted_apa_premium = format_with_commas(apa_premium)
                formatted_apa_gross_premium = format_with_commas(apa_gross_premium)
                formatted_apa_levies = format_with_commas(apa_levies)
                formatted_apa_total = format_with_commas(apa_total)  
                formatted_apa_car_hire = format_with_commas(car_hire)


            if value > 0 and value < 1000000:
                fidelity_rate = 6                
                fidelity_one = (value * (fidelity_rate/100) * (days/365))
                fidelity_premium = max(fidelity_one, 37500)                 
            elif value > 999999 and value < 1500000:
                fidelity_rate = 4.75
                fidelity_premium = (value * (fidelity_rate/100) * (days/365))
            elif value > 1499999 and value < 2500000:
                fidelity_rate = 3.75
                fidelity_premium = (value * (fidelity_rate/100) * (days/365))            
            elif value > 2499999:
                fidelity_rate = 3
                fidelity_premium = (value * (fidelity_rate/100) * (days/365))

            fidelity_pvt = max(value * (0.25/100), 2500)
            fidelity_ex_prt = max(value * (0.25/100), 2500)
            

            if value > 0 and value < 1000001:
                icea_rate = 6
                icea_premium = max((value * (icea_rate/100) * (days/365)),(37500 * (days/365)))
            elif value > 1000000 and value < 1500001:
                icea_rate = 5
                icea_premium = max(value * (icea_rate/100) * (days/365), (60000 * (days/365)))
            elif value > 1500000 and value < 2500001:
                icea_rate = 4
                icea_premium = max(value * (icea_rate/100) * (days/365), (67500 * (days/365)))
            elif value > 2500000 and value < 5000001:
                icea_rate = 3
                icea_premium = max(value * (icea_rate/100) * (days/365), (75000 * (days/365)))
            elif value > 5000000 and value < 10000001:
                icea_rate = 2.75
                icea_premium = max(value * (icea_rate/100) * (days/365), (137500 * (days/365)))
            elif value > 10000001 and value < 15000001:
                icea_rate = 2.5
                icea_premium = max(value * (icea_rate/100) * (days/365), (250000 * (days/365)))
            elif value > 15000000:
                icea_rate = 3
                icea_premium = max(value * (icea_rate/100) * (days/365), (450000 * (days/365)))

            if value > 5000000:
                aig_rate = 3
                formatted_aig_premium = format_with_commas((value * (aig_rate/100) * (days/365)))
                aig_gross_premium = ((value * (aig_rate/100) * (days/365)) + (max(value * 0.25/100, 5000)))
                formatted_aig_gross_premium = format_with_commas((value * (aig_rate/100) * (days/365)) + (max(value * 0.25/100, 5000)))
                aig_levies = (0.0045 * aig_gross_premium)
                formatted_aig_levies = format_with_commas(0.0045 * aig_gross_premium)
                formatted_aig_total = format_with_commas(aig_gross_premium + aig_levies)
                formatted_aig_car_hire = 0.00
            else:
                if value < 1000001:
                    aig_rate = 6
                  
                    aig_premium = max((value * (aig_rate/100) * (days/365)),(37500 * (days/365))) +  (max(value * 0.25/100, 2500))
                elif value > 1000001 and value < 1500001:
                    aig_rate = 5
                   
                    aig_premium = (value * (aig_rate/100) * (days/365)) +  (max(value * 0.25/100, 2500))
                elif value > 1500000 and value < 2500001:
                    aig_rate = 4.25
                    new_aig_rate = 4
                    aig_premium = (value * (aig_rate/100) * (days/365)) +  (max(value * 0.25/100, 2500))
                elif value > 2500001 and value < 3000000:                   
                    aig_rate = 3.5
                    aig_premium = (value * (aig_rate/100) * (days/365)) +  (max(value * 0.25/100, 2500))
                elif value > 3000001 and value < 5000000:
                    aig_rate = 3.5                    
                    aig_premium = (value * (aig_rate/100) * (days/365)) +  (max(value * 0.25/100, 2500))
                elif value > 5000000:                   
                    aig_rate = 3.25
                    aig_premium = (value * (aig_rate/100) * (days/365)) +  (max(value * 0.25/100, 2500))

                aig_gross_premium = (aig_premium + fidelity_pvt)
                aig_levies = aig_gross_premium * 0.0045
                aig_total = ( aig_gross_premium + fee + aig_levies )
                formatted_aig_premium = format_with_commas(aig_premium)
                formatted_aig_gross_premium = format_with_commas(aig_gross_premium)
                formatted_aig_levies = format_with_commas(aig_levies)
                formatted_aig_total = format_with_commas(aig_total)
           
            
            if value > 0 and value < 1000000:
                ga_rate = 6
                ga_premium = max((value * (ga_rate/100) * (days/365)),(37500 * (days/365)))
            elif value > 999999 and value < 1500000:
                ga_rate = 5
                ga_premium = max(value * (ga_rate/100) * (days/365), (60000 * (days/365)))
            elif value > 1499999 and value < 2500000:
                ga_rate = 4
                ga_premium = max(value * (ga_rate/100) * (days/365), (75000 * (days/365)))
            elif value > 2499999 and value < 5000000:
                ga_rate = 3.5
                ga_premium = max(value * (ga_rate/100) * (days/365), (100000 * (days/365)))
            elif value > 4999999:
                ga_rate = 3
                ga_premium = max(value * (ga_rate/100) * (days/365), (175000 * (days/365)))

              
            if value > 0 and value < 1000001:
                om_rate = 6
                om_premium = max((value * (om_rate/100) * (days/365)),(37500 * (days/365)))
                om_gross_premium = ( om_premium + fidelity_pvt + fidelity_ex_prt + car_hire)
            elif value > 1000001 and value < 1500001:
                om_rate = 5
                om_premium = max(value * (om_rate/100) * (days/365), (60000 * (days/365)))
                om_gross_premium = ( om_premium + fidelity_pvt + fidelity_ex_prt + car_hire)
            elif value > 1500001 and value < 2500001:
                om_rate = 4
                om_premium = max(value * (om_rate/100) * (days/365), (75000 * (days/365)))
                om_gross_premium = ( om_premium + fidelity_pvt + fidelity_ex_prt + car_hire)
            elif value > 2500000 and value < 3000001:
                om_rate = 3.5
                om_premium = max(value * (ga_rate/100) * (days/365), (100000 * (days/365)))
                om_gross_premium = ( om_premium + fidelity_pvt + fidelity_ex_prt + car_hire)
            elif value > 3000001 and value < 5000001:
                om_rate = 3.25
                om_premium = (value * (om_rate/100) * (days/365))
                om_gross_premium = ( om_premium + car_hire )
            elif value > 5000001:
                om_rate = 3
                om_premium = (value * (om_rate/100) * (days/365))
                om_gross_premium = ( om_premium + car_hire)
               
          
        
            if st.button("Calculate"):                
                              
                
                fidelity_gross_premium = (fidelity_premium + fidelity_pvt + fidelity_ex_prt + car_hire)
                icea_gross_premium = ( icea_premium + fidelity_pvt + car_hire)
                ga_gross_premium = ( ga_premium + fidelity_pvt + fidelity_ex_prt + car_hire)
               
        
                
                fidelity_levies = fidelity_gross_premium * 0.0045
                icea_levies = icea_gross_premium * 0.0045
                ga_levies = ga_gross_premium * 0.0045
                om_levies = om_gross_premium * 0.0045               
               
        
                
                fidelity_total = ( fidelity_gross_premium + fee + fidelity_levies )
                icea_total = ( icea_gross_premium + fee + icea_levies )
                ga_total = ( ga_gross_premium + fee + ga_levies )
                om_total = ( om_gross_premium + fee + om_levies )
                

                
                formatted_value = format_with_commas(value)

                formatted_fidelity_pvt = format_with_commas(fidelity_pvt)

                formatted_fidelity_ex_prt = format_with_commas(fidelity_ex_prt)

                
                formatted_icea_premium = format_with_commas(icea_premium)
                formatted_ga_premium = format_with_commas(ga_premium)
                formatted_om_premium = format_with_commas(om_premium)
                formatted_fidelity_premium = format_with_commas(fidelity_premium)
                
               
                formatted_car_hire = format_with_commas(car_hire)

                
                formatted_icea_gross_premium = format_with_commas(icea_gross_premium)
                formatted_ga_gross_premium = format_with_commas(ga_gross_premium)
                formatted_om_gross_premium = format_with_commas(om_gross_premium)
                formatted_fidelity_gross_premium = format_with_commas(fidelity_gross_premium)
               
               
                
                formatted_icea_levies = format_with_commas(icea_levies)
                formatted_ga_levies = format_with_commas(ga_levies)
                formatted_om_levies = format_with_commas(om_levies)
                formatted_fidelity_levies = format_with_commas(fidelity_levies)
               
               
                
                formatted_icea_total = format_with_commas(icea_total)
                formatted_ga_total = format_with_commas(ga_total)
                formatted_om_total = format_with_commas(om_total)
                formatted_fidelity_total = format_with_commas(fidelity_total)          
               

                   # Create an HTML report
                html_report = f"""
                <html>
                <head>
                <style>
                    table {{
                    border-collapse: collapse;
                    width: 50%;
                    margin: 0.5px auto;
                    font-size: 12px;
                    font-family: Candara;
                }}
        
                th, td {{
                    border: 1px solid black;
                    padding: 5px; 
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

                img {{
                    width: 100%;
                    height: 45px; 
                    display: block;
                    margin: 0 auto;
                    object-fit: cover;
                }}    
            
                .footer-row th {{
                    background-color: #073980; 
                }}                
    
                .card {{font-family: Candara; border: 1.5px solid; width:100%; margin: 1px auto; font-size:16px; padding: 2.5px;}}         
                
                </style>
                </head>
                <body>

               

                <div class="card">

                    <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAsJCQcJCQcJCQkJCwkJCQkJCQsJCwsMCwsLDA0QDBEODQ4MEhkSJRodJR0ZHxwpKRYlNzU2GioyPi0pMBk7IRP/2wBDAQcICAsJCxULCxUsHRkdLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCz/wAARCAEOAQsDASIAAhEBAxEB/8QAGwABAAMBAQEBAAAAAAAAAAAAAAQFBgMHAgH/xAA/EAABBAIBAgUCAwUFBQkAAAABAAIDBAUREgYhEzFBUWEUIjJxgRUjQpGhByRSYrEzY4KS0RY2Q1NyhKKy8f/EABoBAQEBAQEBAQAAAAAAAAAAAAABAwIEBQb/xAAuEQEBAAIBAwIDBwQDAAAAAAAAAQIRAxIhMQQTBUFRFCJhcYGh8CMyQtHB4fH/2gAMAwEAAhEDEQA/APW0REBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQERR7lypQry2rUrY4Y/Nx8yT5NaB3JPoAiWzGbqQiz+J6ox+WuvpxQ2In+G+SJ03DUgYRsaYTo+vmtApLMpuM+Lmw5serju4IiKtRERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQFQdTZHpqrRfUzVrwm3GkRMia+SwSwgiSNjGk/adHZGvT10b5eB9XX5Mh1Fm5nP5MhsvpQd9tbFWJiAb8Ehzv+L5WvFxzkur4Z8mrjZZvbadLYqSxlauRpWoZ8ZVkmeLcLu8ruJjELonaka/vtwc0a+dgn0leA9O9S5Lpua1JUjgmitiIWIbHMNJjJ4vYWEad3I3o/l27biv8A2p0HcRaw9uP/ABGvPDMPzAkDCn2W8fbDvHm9Lw8fpsbjh8+70ZFk6fXvTt6LIzRQ5FooRQTTNlgiBc2aXwWlhbIR2PnshXGIzNfMxTTQVrcMcbwwOsxt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" alt="Description" style="display:block; margin:auto; width:120px; height:auto;">
               
                
                <p> Thank you for choosing <b>Gras Savoye Kenya</b> as your trusted insurance broker. We are honored to support you in protecting what matters most.

                    In line with your instructions, we are pleased to confirm that we have approached insurers best suited to your needs and secured the most competitive terms, with the widest scope of coverage available.<br>

                    <p><u><b>Cover summary</b></u><br>
                    Comprehensive Covers accidental loss or damage to insured motor vehicles and/or death, bodily injury or loss  or damage to property of third parties arising out of use of motor vehicles owned and/or operated by the insured/authorized driver. </p>

                    Please find below a comparative quotation for your review and consideration.
                </p>
                
                <table>
                    <tr>                      
                        <th colspan="2">MOTOR PRIVATE COMPREHENSIVE</th>
                        <th colspan="2"><img src="https://th.bing.com/th/id/OIP.FKycthqs_eBeEyXkHC5blAHaHa?rs=1&pid=ImgDetMain" alt="Cannon Logo"></th>                       
                        <th colspan="2"><img src="https://i.ytimg.com/vi/7BORiuBsmyo/maxresdefault.jpg" alt="APA Logo"></th>
                        <th colspan="2"><img src="https://th.bing.com/th/id/OIP.pqmNPWTCP_Ef4Eqo_Vp5-wAAAA?w=400&h=400&rs=1&pid=ImgDetMain" alt="Fidelity Logo"></th>
                        <th colspan="2"><img src="https://th.bing.com/th/id/OIP.Jz5UcTVU1JbjzmCGb2nt8gAAAA?w=194&h=186&rs=1&pid=ImgDetMain" alt="ICEA Logo"></th>
                        <th colspan="2"><img src="https://tse3.mm.bing.net/th/id/OIP.KgIcxDUjv9Uf3w9gPYmJAgHaEK?cb=thfc1falcon&w=1080&h=608&rs=1&pid=ImgDetMain&o=7&rm=3" alt="GA Logo"></th> 
                        <th colspan="2"><img src="https://th.bing.com/th/id/OIP.AqCcq8bj35a3GLSBoCm_uAHaEK?w=260&h=180&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3" alt="AIG Logo"></th> 
             
                       
                     </tr>
                    
                    <tr>
                        <th style="background-color: #17B169">{reg}</th>
                        <th style="background-color: #17B169">Value - KES</th>
                        <th style="background-color: #17B169">Rate</th>
                        <th style="background-color: #17B169">Premium</th>
                        <th style="background-color: #17B169">Rate</th>
                        <th style="background-color: #17B169">Premium</th>
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
                        <td>{value}</td> 
                        <td style="color:red">{cannon_rate}</td>
                        <td>{formatted_cannon_premium}</td>
                        <td style="color:red">{apa_rate}</td>
                        <td>{formatted_apa_premium}</td> 
                        <td style="color:red">{fidelity_rate}%</td>
                        <td>{formatted_fidelity_premium}</td> 
                        <td style="color:red">{icea_rate}%</td>
                        <td>{formatted_icea_premium}</td>                        
                        <td style="color:red">{ga_rate}%</td>
                        <td>{formatted_ga_premium}</td>
                        <td style="color:red">{aig_rate}%</td>
                        <td>{formatted_aig_premium}</td>
                       
                                        
                    </tr>                     

                    <tr>
                        <td>Excess Protector</td>
                        <td></td>
                        <td style="color:red">Inclusive</td>
                        <td >0.00</td>                       
                        <td style="color:red">Inclusive</td>  
                        <td >0.00</td>
                        <td style="color:red">0.25%</td>
                        <td >{formatted_fidelity_ex_prt}</td>              
                        <td style="color:red">Inclusive</td>
                        <td>0.00</td>
                        <td style="color:red">0.25%</td>
                        <td>{formatted_fidelity_ex_prt}</td>
                        <td style="color:red">Inclusive</td>
                        <td>0.00</td>
                      
                                                    
                    </tr>           
                                                
                    <tr>
                        <td>Political/Terrorism</td>
                        <td></td>
                        <td style="color:red">Inclusive</td>
                        <td >0.00</td>                       
                        <td style="color:red">Inclusive</td>  
                        <td >0.00</td>
                        <td style="color:red">0.25%</td>
                        <td >{formatted_fidelity_pvt}</td>              
                        <td style="color:red">0.25%</td>
                        <td>{formatted_fidelity_pvt}</td>
                        <td style="color:red">0.25%</td>
                        <td>{formatted_fidelity_pvt}</td>
                        <td style="color:red">0.25%</td>
                        <td>{formatted_fidelity_pvt}</td>
                       
                                                              
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
                        <td>{lou}</td>
                        <td style="color:red" >{loss_of_use}</td>
                        <td>{formatted_car_hire}</td>
                        <td style="color:red" >Excluded</td>
                        <td>0.00</td>
                      
                      
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
                        <td></td>
                        <td class='gross_premium'>{formatted_ga_gross_premium}</td>
                        <td></td>
                        <td class='gross_premium'>{formatted_aig_gross_premium}</td>
                      
                        
                
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
                        <td style="color:red">0.45%</td>
                        <td >{formatted_ga_levies}</td>
                        <td style="color:red">0.45%</td>
                        <td >{formatted_aig_levies}</td>
                     
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
                        <td></td>
                        <td>{fee}</td>
                        <td></td>
                        <td>{fee}</td>
                      
                                                        
                    </tr>
                    
                    <tr style=" border-top: 2px double black;  border-bottom: 2px double black;">
                        <td class= 'bold' style="color:#152637">Total Premium</td>
                        <td></td>
                        <td></td>
                        <td class = 'bold' style="color:#152637">{formatted_cannon_total}</td>
                        <td></td>
                        <td class = 'bold' style="color:#152637">{formatted_apa_total}</td>
                        <td></td>
                        <td class = 'bold' style="color:#152637">{formatted_fidelity_total}</td>
                        <td></td>
                        <td class = 'bold' style="color:#152637">{formatted_icea_total}</td>
                        <td></td>
                        <td class = 'bold' style="color:#152637">{formatted_ga_total}</td>
                        <td></td>
                        <td class = 'bold' style="color:#152637">{formatted_aig_total}</td>

                                                      
                    </tr>          

                    <tr>
                        <th colspan="16" style="background-color: #073980; color:white;">
                        <p style=" font-size: 12px; font-family: Candara;">
                        <u><b>Important Notes</b></u><br>
                        Vehicles will only qualify for comprehensive cover where age is below 15 years. ( Year Of Manufacture north of 2010)<br>
                        It is advisable to have the vehicle valued. Kindly note that the above quote is subject to change as per valuation results.<br>
                        Your applicable excess in the event of a material damage claim will be KES. {new_excess} (<b>NCBAIG</b> Excess at KES. 20,000)<br>
                        This is a summarized comparative quote; kindly review your risk note once cover is placed; it contains detailed information on scope of cover.                                                   
                        </p>
                        </th>
                    </tr>
                </table>

                <br>

                <p><u><b>Benefit Summary</b></u></p>

                <p>
                1. Death or Bodily Injury to any Third Party - As per statute (KES. 3,000,000).<br>

                2. Third Party Property Damage - Up to KES. 20,000,000/-.<br>

                3. Passenger Legal Liability - Up to KES. 5,000,000/- per person and KES. 50,000,000/- per year.<br>

                4. Towing & Recovery on <b>accidental damage</b> - Up to KES. 50,000/- per year.<br>

                5. Emergency Medical Expenses - Up to KES. 50,000/- per year.<br>

                6. Authorized Repair Limit - Up to KES. 30,000/- per year.<br>

                7. Windscreen/Window Glass Replacement - Up to KES. 50,000/-.<br>

                8. Car Entertainment Unit - Up to KES. 50,000/-.<br>

                9. Side Mirror Cover - Up to KES. 50,000/- on reimbursement basis, subject to a flat excess of KES. 5,000/-<br>

                10. Valuation - Free                 
                
                </p>

            

                <p><u><b>Policy Excess</b></u> - <i>Excess is the portion of a claim borne by the insured(policy holder)</i></p>

                <p>

                1. Accidental Material Damage - 2.5% of vehicle value. (Minimum: KES. 20,000/- Maximum: KES. 100,000/-)<br>

                2. Third Party Property Damage - KES. 7,500/-<br>

                3. Injury Claims - NIL (no excess applicable)<br>

                4. Total Theft Loss (with Anti-theft Device) - 10% of vehicle value, minimum KES. 20,000/-<br>

                5. Total Theft Loss (without Anti-theft Device) - 20% of vehicle value, minimum KES. 20,000/-<br>

                6. Total Theft Loss (with Tracking Device),- 2.5% of vehicle value, minimum KES. 20,000/-<br>

                7. Young & Novice Driver - Additional KES. 5,000/- each (under 21 years / less than 1 year driving experience)<br>

                8. Loss of Use (if applicable) - Time excess of 3 days

                </p>

                <br>

                <p>
                <b>Prepared By:</b> {staff}<br>
                <b>Phone:</b>{phone}<br>
                <b>Date:</b>{long_date}
                </p>

                
                </div>
                </body>                    
                </html>"""
        
                
            # Create a download button with customized file name
        
                st.download_button(
                    label=f"Download {reg}'s_premium_quote(HTML)",
                    data=html_report.encode('utf-8'),
                    file_name=f"{reg}_quote.html",
                    mime="text/html"
                )

             
                # config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")  # Default install path
                # pdfkit.from_string(html_report, "report.pdf", configuration=config)

                # file_name = 'report.pdf'
                # pdfkit.from_string(html_report, file_name, configuration=config)
                # with open(file_name, "rb") as pdf_file:
                #     st.download_button(
                #         'Download PDF',
                #         data = pdf_file,
                #         file_name = file_name,
                #         mime = 'application/octet-stream')
                  
            
        
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
                premium = max((value * (rate/100)), 50000)       
            
            if pvt == 'Inclusive' or 'Excluded':
                pvt_value += 0
            elif pvt == '0.25%':
                pvtworking = max((0.25/100) * value, 5000)
                pvt_value += pvtworking
            elif pvt == '0.5%':
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
        underwriter = st.selectbox("Select Underwriter", ["APA INSURANCE", "FIDELITY INSURANCE", "CANNON GENERAL INSURANCE", "GA INSURANCE", "HERITAGE INSURANCE", "ICEA LION GENERAL INSURANCE", "JUBILEE ALLIANZ"])
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

            img {{
                    width: 100%;
                    height: 45px; 
                    display: block;
                    margin: 0 auto;
                    object-fit: cover;
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


    with tab4: 
        
        reg = st.text_input('Enter Plate No')
        value = int(st.number_input('Enter Vehicle Sum Insured'))
        notes = st.text_input("Include any Important Remarks")    
                                                            
        fee = 0
        ex_pr = 0
        pvt_value = 0
    
        if st.button("Calculate MC Quote"):
            
            cannon_premium = max(value * (4.5/100), 40000)             
            fidelity_premium = max(value * (4.8/100), 50000)
            icea_premium = max(value * (5/100), 40000)  
            icea_pvt = max(value * (0.35/100), 2500)

            fee = 100
            pll_amount = pll * 500
    
            cannon_gross_premium = (cannon_premium + pll_amount)
            cannon_levies = cannon_gross_premium * 0.0045

            icea_gross_premium = (icea_premium + pll_amount + icea_pvt)
            icea_levies = icea_gross_premium * 0.0045

            fidelity_gross_premium = (fidelity_premium + pll_amount)    
            fidelity_levies = fidelity_gross_premium * 0.0045
    
            cannon_total = ( cannon_gross_premium + fee + cannon_levies  )
            icea_total = ( icea_gross_premium + fee + icea_levies  )
            fidelity_total = ( fidelity_gross_premium + fee + fidelity_levies  )
    
            # Format numbers with commas for thousands
            def format_with_commas(number):
                rounded_number = round(number, 2)
                return "{:,.2f}".format(rounded_number)
                
            
            formatted_value = format_with_commas(value)
            formatted_cannon_gross_premium = format_with_commas(cannon_gross_premium)
            formatted_icea_gross_premium = format_with_commas(icea_gross_premium)
            formatted_fidelity_gross_premium = format_with_commas(fidelity_gross_premium)
            formatted_cannon_premium = format_with_commas(cannon_premium)
            formatted_icea_premium = format_with_commas(icea_premium)
            formatted_fidelity_premium = format_with_commas(fidelity_premium)
            formatted_pll = format_with_commas(pll_amount)
            formatted_cannon_levies = format_with_commas(cannon_levies)
            formatted_icea_levies = format_with_commas(icea_levies)
            formatted_fidelity_levies = format_with_commas(fidelity_levies)
            formatted_cannon_total = format_with_commas( cannon_total)
            formatted_icea_total = format_with_commas( icea_total)
            formatted_fidelity_total = format_with_commas( fidelity_total)
            formatted_icea_pvt = format_with_commas(icea_pvt)
    
    
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

            img {{
                    width: 100%;
                    height: 45px; 
                    display: block;
                    margin: 0 auto;
                    object-fit: cover;
                }}    
    
            .footer-row th {{
                background-color: #073980;
            }}
    
            
            
            </style>
                </head>
                <body>
                <table>
                    <tr>
                        <th colspan="2">MOTOR COMMERCIAL - OWN GOODS</th>
                        <th colspan="2"><img src="https://th.bing.com/th/id/OIP.FKycthqs_eBeEyXkHC5blAHaHa?rs=1&pid=ImgDetMain" alt="Cannon Logo"></th>                       
                        <th colspan="2"><img src="https://th.bing.com/th/id/OIP.pqmNPWTCP_Ef4Eqo_Vp5-wAAAA?w=400&h=400&rs=1&pid=ImgDetMain" alt="Fidelity Logo"></th>
                        <th colspan="2"><img src="https://th.bing.com/th/id/OIP.Jz5UcTVU1JbjzmCGb2nt8gAAAA?w=194&h=186&rs=1&pid=ImgDetMain" alt="ICEA Logo"></th>
             
                     </tr>
                    
                        <tr>
                        <th style="background-color: #17B169">{reg}</th>
                        <th style="background-color: #17B169">Value - KES</th>
                        <th style="background-color: #17B169">Rate</th>
                        <th style="background-color: #17B169">Premium</th>
                        <th style="background-color: #17B169">Rate</th>
                        <th style="background-color: #17B169">Premium</th>
                        <th style="background-color: #17B169">Rate</th>
                        <th style="background-color: #17B169">Premium</th>
                                                                       
                    <tr>
                        <td>Basic Premium</td>
                        <td>{value}</td> 
                        <td style="color:red">4.75%</td>
                        <td>{formatted_cannon_premium}</td>
                        <td style="color:red">4.5%</td>
                        <td>{formatted_fidelity_premium}</td> 
                        <td style="color:red">5%</td>
                        <td>{formatted_icea_premium}</td> 
                                        
                    </tr>                     

                    <tr>
                        <td>Excess Protector</td>
                        <td></td>
                        <td style="color:red">Inclusive</td>
                        <td >0.00</td>                       
                        <td style="color:red">Inclusive</td>  
                        <td >0.00</td>
                        <td style="color:red">Inclusive</td>  
                        <td >0.00</td>
                                                    
                    </tr>           
                                                
                    <tr>
                        <td>Political/Terrorism</td>
                        <td></td>
                        <td style="color:red">Inclusive</td>
                        <td >0.00</td>                       
                        <td style="color:red">Inclusive</td>  
                        <td >0.00</td>
                        <td style="color:red">0.35</td>  
                        <td >{formatted_icea_pvt}</td>
                                                              
                    </tr>             
    
                        
                    
                    <tr>
                        <td>Gross Premium</td>
                        <td></td> 
                        <td></td>
                        <td class='gross_premium'>{formatted_cannon_gross_premium}</td> 
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
                        <td >{formatted_fidelity_levies}</td> <!-- Updated formatting for better readability -->      
                        <td style="color:red">0.45%</td>
                        <td >{formatted_icea_levies}</td> <!-- Updated formatting for better readability -->                       
                
                
                    <\tr>
                    
                    <tr>
                        <td>Policy Fee</td>
                        <td></td>
                        <td></td>
                        <td>100</td>
                        <td></td>
                        <td>100</td>
                        <td></td>
                        <td>100</td>
                        
                    </tr>
                    
                    <tr style=" border-top: 2px double black;  border-bottom: 2px double black;">
                        <td class= 'bold' style="color:#152637">Total Premium</td>
                        <td></td>
                        <td></td>
                        <td class = 'bold' style="color:#152637">{formatted_cannon_total}</td>
                        <td></td>                    
                        <td class = 'bold' style="color:#152637">{formatted_fidelity_total}</td>
                        <td></td>                    
                        <td class = 'bold' style="color:#152637">{formatted_icea_total}</td>
                    </tr>                   
                </table>
                </body>                    
                </html>"""

        # Create a download button with customized file name
    
            st.download_button(
                label=f"Download {reg}'s_premium_quote(HTML)",
                data=html_report.encode('utf-8'),
                file_name=f"{reg}_quote.html",
                mime="text/html"
            )        

    

# # Define your Google Sheets credentials JSON file (replace with your own)
# credentials_path = 'newretail-b682d2880f30.json'
    
# # Authenticate with Google Sheets using the credentials
# credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://spreadsheets.google.com/feeds'])
    
# # Authenticate with Google Sheets using gspread
# gc = gspread.authorize(credentials)
    
# # Your Google Sheets URL
# url = "https://docs.google.com/spreadsheets/d/1e09gr3_1UI7yaX_Kjo21nh4m-5d6n0ITJwyA4-L1fTw/edit?gid=0#gid=0"
    
# # Open the Google Sheets spreadsheet
# worksheet = gc.open_by_url(url).worksheet("Renewals")
# worksheet2 = gc.open_by_url(url).worksheet("New_Business")

# # Read data from the Google Sheets worksheet
# data = worksheet.get_all_values()
# headers = data[0]
# data = data[1:]

# df = pd.DataFrame(data, columns=headers)
                

# with view2:
#     def check_password():
#         """Returns `True` if the user entered a correct password."""
#         return st.session_state.get("password_correct", False)

#     def password_entered():
#         """Checks whether a password entered by the user is correct."""
#         if (
#             st.session_state["username"] in st.secrets["passwords"]
#             and st.session_state["password"]
#             == st.secrets["passwords"][st.session_state["username"]]
#         ):
#             st.session_state["password_correct"] = True
#             del st.session_state["password"]  # Don't store username + password
#             del st.session_state["username"]
#         else:
#             st.session_state["password_correct"] = False
    
#     if "password_correct" not in st.session_state:
#         # First run, show inputs for username + password.
#         st.text_input("Username", key="username")
#         st.text_input("Password", type="password", key="password")
#         st.button("Submit", on_click=password_entered)
#         st.stop()
    
#     if not st.session_state["password_correct"]:
#         # Password not correct, show input + error.
#         st.text_input("Username", key="username")
#         st.text_input("Password", type="password", key="password")
#         st.button("Submit", on_click=password_entered)
#         st.error("User not known or incorrect password")
#         st.stop()
    
#     if check_password():           

#         df['Key'] = df['Key'].astype(int)
        
#         df['Date'] = pd.to_datetime(df['Date'])
        
#         df['Renewal Month'] = df['Date'].dt.month_name()

#         # Get the unique reviewer names from the DataFrame
#         unique_outcome = df['Renewal Month'].unique()
  
#         # Create a dropdown to select a reviewer with "All" option
#         selected = st.selectbox("Filter by Outcome:", ["All"] + list(unique_outcome))
  
#         if selected != "All":
#             # Filter the DataFrame based on the selected reviewer
#             final_df = df[df['Renewal Month'] == selected].copy()
  
#         else:
#             # If "All" is selected, show the entire DataFrame
#             final_df = df

#         task1, task2, task3, task4, task5, task6 = st.tabs(["Work Load", "Invite Sent", "Valuation", "Renewed", "Debited", "Lost"])

#         with task1:
#             workload = final_df[final_df['Status'] == 'Pending']
#             edited_df =  st.data_editor(workload, key = 'workload')
#             merged = pd.concat([df, edited_df])
#             finalmerged = merged.drop_duplicates(subset=['Key'], keep='last')
#             descending = finalmerged.sort_values(by=['Key'], ascending=True)
#             df1 = descending.astype(str).fillna('')
#             num = len(workload)
#             st.markdown(f'Pending Invites: {num}')
#             # Add a button to update Google Sheets with the changes
#             if st.button("Update Records", key='button1'):   
#                 worksheet.clear()
#                 worksheet.update([df1.columns.tolist()] + df1.values.tolist())
        
#         with task2:
#             invited = final_df[final_df['Status'] == 'Invited']            
#             edited_df =  st.data_editor(invited, key = 'invited')
#             merged = pd.concat([df, edited_df])
#             finalmerged = merged.drop_duplicates(subset=['Key'], keep='last')
#             descending = finalmerged.sort_values(by=['Key'], ascending=True)
#             df2 = descending.astype(str).fillna('')    
#             num = len(invited)
#             st.markdown(f'Invite Sent: {num}')
#             # Add a button to update Google Sheets with the changes
#             if st.button("Update Records", key='button2'):   
#                 worksheet.clear()
#                 worksheet.update([df2.columns.tolist()] + df2.values.tolist())



#         with task3:
#             valued = final_df[final_df['Status'] == 'Valued']
#             edited_df =  st.data_editor(valued, key = 'valued')
#             merged = pd.concat([df, edited_df])
#             finalmerged = merged.drop_duplicates(subset=['Key'], keep='last')
#             descending = finalmerged.sort_values(by=['Key'], ascending=True)
#             df3 = descending.astype(str).fillna('') 
#             num = len(valued)
#             st.markdown(f'Valued: {num}')
#             # Add a button to update Google Sheets with the changes
#             if st.button("Update Records", key='button3'):   
#                 worksheet.clear()
#                 worksheet.update([df3.columns.tolist()] + df3.values.tolist())      
           
        
#         with task4:
#             renewed = final_df[final_df['Status'] == 'Renewed']
#             edited_df =  st.data_editor(renewed, key = 'renewed')
#             merged = pd.concat([df, edited_df])            
#             finalmerged = merged.drop_duplicates(subset=['Key'], keep='last')
#             descending = finalmerged.sort_values(by=['Key'], ascending=True)
#             df4 = descending.astype(str).fillna('') 
#             num = len(renewed)
#             st.markdown(f'Renewed: {num}')
#             # Add a button to update Google Sheets with the changes
#             if st.button("Update Records", key='button4'):   
#                 worksheet.clear()
#                 worksheet.update([df4.columns.tolist()] + df4.values.tolist())
        
            
#         with task5:
#             debited = final_df[final_df['Status'] == 'Debited']
#             edited_df = st.data_editor(debited, key='debited')
#             merged = pd.concat([df, edited_df])
#             finalmerged = merged.drop_duplicates(subset=['Key'], keep='last')
#             descending = finalmerged.sort_values(by=['Key'], ascending=True)
#             df5 = descending.astype(str).fillna('') 
#             num = len(debited)
#             st.markdown(f'Certificate Issued: {num}')
#             # Add a button to update Google Sheets with the changes
#             if st.button("Update Records", key='button5'):   
#                 worksheet.clear()
#                 worksheet.update([df5.columns.tolist()] + df5.values.tolist())
        
           
                
#         with task6:
#             lost = final_df[final_df['Status'] == 'Lost']
#             edited_df = st.data_editor(lost, key='lost')
#             merged = pd.concat([df, edited_df])
#             finalmerged = merged.drop_duplicates(subset=['Key'], keep='last')
#             descending = finalmerged.sort_values(by=['Key'], ascending=True)
#             df6 = descending.astype(str).fillna('')  
#             num = len(lost)
#             st.markdown(f'Cancelled Policy: {num}')
#             # Add a button to update Google Sheets with the changes
#             if st.button("Update Records", key='button6'):   
#                 worksheet.clear()
#                 worksheet.update([df6.columns.tolist()] + df6.values.tolist())
#             # Add a button to download the filtered data as a CSV
#         if st.button("Download CSV"):
#             csv_data = df6.to_csv(index=False, encoding='utf-8')
#             b64 = base64.b64encode(csv_data.encode()).decode()
#             href = f'<a href="data:file/csv;base64,{b64}" download="renewal_list.csv">Download CSV</a>'
#             st.markdown(href, unsafe_allow_html=True) 


# with view3:
#     tab31, tab32, tab33 = st.tabs(["Add Entry", "📈 Clients",  "📈 Summary"])
#     with tab31:
#         name = st.text_input('Enter Client Name')
#         plate = st.text_input('Enter Car Registration')
#         date = json.dumps(st.date_input("Date"), default=str)
#         premium = st.number_input('Premium Charged')
    
#         if st.button("Add Entry"):
#             # Create a new row of data to add to the Google Sheets spreadsheet
#             new_data = [name, plate, date, premium] 
            
#             # Append the new row of data to the worksheet
#             worksheet2.append_row(new_data)         
#             st.success("Data submitted successfully!")
            
#     with tab32:
#         new = worksheet2.get_all_values()        
#         second_headers = new[0]
#         new_data_frame = new[1:]              
#         newdf =  pd.DataFrame(new_data_frame, columns=second_headers) 
#         newdf['Premium'] = newdf['Premium'].astype(int)
#         total = newdf['Premium'].sum()
#         st.table(newdf)
#         st.write(total)

#     with tab33:
#         # Regular expression to capture date values in the format YYYY-MM-DD
#         date_pattern = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")

#         new = worksheet2.get_all_values()
#         renew = worksheet.get_all_values()
#         second_headers = new[0]
#         third_headers = renew[0]
#         new_data_frame = new[1:]
#         renew_data_frame = renew[1:]
#         renew_df = pd.DataFrame(renew_data_frame, columns=third_headers)        
#         newdf =  pd.DataFrame(new_data_frame, columns=second_headers)  
        
#         newdf['Date Onboarded'] = newdf['Date'].str.extract(date_pattern)
#         newdf['Date Onboarded'] = pd.to_datetime(newdf['Date Onboarded'])
#         newdf['Month Onboarded'] = newdf['Date Onboarded'].dt.month_name()
#         newdf['Count'] = 1
#         renew_df['Count'] = 1
#         renewals = renew_df[renew_df['Status'] == 'Debited']
#         lost  = renew_df[renew_df['Status'] == 'Lost']
#         # renew_df['Renewal Month'] = renew_df['Date'].dt.month_name()

#         newdf['Premium'] = pd.to_numeric(newdf['Premium'], errors='coerce')
#         renewals['Premium'] = pd.to_numeric(renewals['Premium'], errors='coerce')


#         # Calculate the sum of amounts for each category
#         bar_renew = renewals.groupby('Renewal Month')['Count'].sum().reset_index()
#         bar_new = newdf.groupby('Month Onboarded')['Count'].sum().reset_index()
#         bar_lost = lost.groupby('Renewal Month')['Count'].sum().reset_index()

#         bar_renew_total = renewals.groupby('Renewal Month')['Premium'].sum().reset_index()
#         bar_renew_total['Premium'] = bar_renew_total['Premium'] / 10
#         bar_new_total = newdf.groupby('Month Onboarded')['Premium'].sum().reset_index()
#         bar_new_total['Premium'] = bar_new_total['Premium'] / 10

        

#         fig = go.Figure()

#         fig.add_trace(go.Bar(
#                 width= 0.25,
#                 x= bar_renew['Renewal Month'],
#                 y= bar_renew['Count'],   
#                 name = 'Renewals',
#                 marker_color="#e49b0f"                   
#                 )) 

#         fig.add_trace(go.Bar(
#                 width= 0.25,
#                 x= bar_new['Month Onboarded'],
#                 y= bar_new['Count'],   
#                 name = 'New Clients',
#                 marker_color="#00ab66"
                   
#                 )) 

#         fig.add_trace(go.Bar(
#                 width= 0.25,
#                 x= bar_lost['Renewal Month'],
#                 y= bar_lost['Count'],   
#                 name = 'Lost',
#                 marker_color="#e32636"                   
#                 )) 

#         fig.update_layout(title={'text': 'RETAIL MONTHLY BUSINESS TRACKING', 'x': 0.5, 'xanchor': 'center'},  width=650,
#                                                 xaxis_title='Month',
#                                                 yaxis_title='No Of Policies',
#                                                 xaxis=dict(tickfont=dict(size=7)),                                  
#                                                 )

#         st.plotly_chart(fig)

        
#         fig2 = go.Figure()

#         fig2.add_trace(go.Bar(
#                 width= 0.35,
#                 x= bar_renew_total['Renewal Month'],
#                 y= bar_renew_total['Premium'],   
#                 name = 'Renewals',
#                 marker_color="#e49b0f"                   
#                 )) 

#         fig2.add_trace(go.Bar(
#                 width= 0.35,
#                 x= bar_new_total['Month Onboarded'],
#                 y= bar_new_total['Premium'],   
#                 name = 'New Clients',
#                 marker_color="#00ab66"
                   
#                 )) 
 

#         fig2.update_layout(title={'text': 'RETAIL MONTHLY INCOME TRACKING', 'x': 0.5, 'xanchor': 'center'},  width=650,
#                                                 xaxis_title='Month',
#                                                 yaxis_title='Commission Earned',
#                                                 xaxis=dict(tickfont=dict(size=7)),                                  
#                                                 )

#         st.plotly_chart(fig2)

        

    
    
