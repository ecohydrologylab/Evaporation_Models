import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# XXX can we make the slider in the main column instead of side column
# XXX also only 4 significant digits in the evaporation value

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; '>Diurnal surface evaporation models</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
        section[daTa oC-testid="stSidebar"] {
            width: 200px !imporTa oCnt; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

time = np.array([0.0,4.0,8.0,12.0,16.0,20.0,24.0])
Rn = np.array([-60.0,-40.0,85.0,330.0,75.0,-55.0,-55.0])
Ta = np.array([30.0,28.0,30.0,35.0,38.0,33.0,32.0])
Tw = np.array([33.0,32.0,33.0,34.0,35.0,34.0,33.0])
RH = np.array([90.0,85.0,75.0,60.0,70.0,85.0,85.0])
velocity = np.array([3.5,3.1,2.6,1.6,2.1,2.4,3.1])
df = pd.DataFrame([time,Rn,Ta,Tw,velocity,RH],index=["Time h","Rn Wm-2","Ta oC","Tw oC","Vel ms-1","RH %"]).T


if 'df' not in st.session_state:
    st.session_state.df = df


zc,zo1 = st.columns([1,1])
with zc:
    z = st.slider(label="Measurement height = $z$ $[m]$",
                  key='z',min_value=0.0,max_value=10.0,value=2.0,format='%.5f')
with zo1:
    z0 = st.slider(label="Surface roughness height = $z_o$ $[m]$",
                          key='zo',min_value=0.0,max_value=1.0,value=0.003,format='%.5f') 

col1, col2 = st.columns([1.5,1])
with col1:
    st.latex(r'''\text{Climate forcings} ''')
    
    df = st.data_editor(df,num_rows="dynamic",use_container_width=True,
                                        key="editor",height=500)
    
c = 1000*3600*24
# Aerodynamic
esTw = 611*np.exp((17.27*df['Tw oC'])/(237.3+df['Tw oC']))*1e-3
esTa = 611*np.exp((17.27*df['Ta oC'])/(237.3+df['Ta oC']))*1e-3
eaTa = 0.01*df["RH %"]*esTa  
Kv = 1.132*1e-6/((np.log(z/z0))**2)
Ea = c*Kv*df["Vel ms-1"]*(esTw-eaTa)
# Energy balance
Kh = 184.92/((np.log(z/z0))**2)
H = Kh*df["Vel ms-1"]*(df['Tw oC']-df['Ta oC'])
Eb = c*(df['Rn Wm-2'] - H)/(998*(2500-2.36*df['Tw oC'])*1000)
# Combined
delta = 4098*esTa/(237.3 + df['Ta oC'])**2 # kPa
gamma = 1005*101.3/(0.622*(2500-2.36*df['Tw oC']))/1E3 # kPa
Ec = c*(delta/(gamma+delta)*(df['Rn Wm-2']/(998*(2500-2.36*df['Tw oC'])*1E3)) + \
     gamma/(gamma+delta)*(Kv*df["Vel ms-1"]*(esTa-eaTa)))

df2 = pd.DataFrame(np.array([esTw,esTa,Ea,Eb,Ec]).T,columns =["es [kPa]","ea [kPa]","Ea [mm d-1]",\
                                                           "Eb [mm d-1]","Ec [mm d-1]"],index=df["Time h"])
with col2:
    st.latex(r'''\text{Diurnal Evaporation } [mm d^{-1}]''')
    st.dataframe(df2,use_container_width=True,height=500,hide_index=True)
    st.write("$K_v$ = ",str(np.round(Kv*1E10)),'E-10 [kPa$^{-1}$]')
    st.write("$K_h$ = ",str(np.round_(Kh,2)),'&emsp; [$J ^{o}C m^{-3}$]')

c1,c2,c3 = st.columns([1,2,1])
with c2:
    fig = plt.figure(figsize=(8,8))
    plt.plot(df['Time h'],df2['Ea [mm d-1]'],color='b',label='Ea: Aerodynamic model')
    plt.plot(df['Time h'],df2['Eb [mm d-1]'],color='r',label='Eb: Energy balance model')
    plt.plot(df['Time h'],df2['Ec [mm d-1]'],color='k',label='Ec: Combined model')
    plt.legend()
    plt.xlabel('Time [hr]')
    plt.ylabel('Evaporation rate [mm d$^{-1}$]')
    plt.title("Diurnal Evaporation")
    st.pyplot(fig,use_container_width=True)
