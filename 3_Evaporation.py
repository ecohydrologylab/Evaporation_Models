import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import math

# XXX can we make the slider in the main column instead of side column
# XXX also only 4 significant digits in the evaporation value

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; '>Water surface evaporation models</h1>", unsafe_allow_html=True)

colEa, colEe, colEc = st.columns(3)
with colEa:
    # Aerodynamic method
    st.header("Aerodynamic method")
    aerodynamicExpander = st.expander("Documentaion")
    with aerodynamicExpander:
        
        st.latex(r''' E_a = c K_v v (e_s-e_a) ''')        
        st.markdown("where,")
        st.markdown("$E_a$ = Evaporation rate &emsp; [$mm$ $d^{-1}$]")
        st.markdown("$c$ = $8.64 E7$ &nbsp; Conversion Factor &nbsp; \
                    [$m$ $s^{-1}$] &nbsp; to &nbsp; [$mm$ $d^{-1}$]")
        st.markdown("$K_v$ = Vertical vapour transfer coefficient [$kPa^{-1}$]")
        st.latex(r'''= \frac{0.622 k^2 \rho_a}{P_a \rho_w [ln(z/z_o)]^{2}} \quad [kPa^{-1}] ''')
        st.markdown("where,")
        st.latex(r''' 
                 \small
                 k = 0.4 = \text{von karman} \text{ constant } [-] \\
                 \rho_a = 1.15 \text{= density} \text{ of air } [kg m^{-3}] \\
                 \rho_w = 998 \text{= density} \text{ of water }  [kg m^{-3}] \\
                 Pa = \text{Atm.} \text{pressure } [kPa] \quad \quad  \\
                 z_o = \text{Surface roughness} \text{ height } [m] \\
                 z = \text{Measurement} \text{ height } [m] \\
                 ''')
        st.markdown("$v$ = Wind speed at height z &emsp; [$m$ $s^{-1}$]")
        st.markdown("$e_s$ = Saturation vapour pressure at $T_w$ &emsp; [$kPa$]")
        st.latex(r''' = 0.611 \exp \left( \frac{17.27 T_w}{237.3 + T_w} \right) ''')
        st.markdown("where,")
        st.latex(r''' \small T_w = \text{Water surface temperature } ^{o}C ''')
        st.markdown("$e_a$ = Actual vapour pressure of air &nbsp; [$kPa$]")
        st.latex(r''' = \frac{RH}{100}0.611\exp\left( \frac{17.27 T_a}{237.3 + T_a} \right) ''')
        st.markdown("where,")
        st.latex(r''' \small T_a = \text{Air temperature at hieght z}''')
        
        
    
    # z = st.slider("z",min_value=0.00,max_value=10.00,value=5.00,step=0.01)
    # zo = st.slider("zo",min_value=0.000,max_value=10.000,value=0.500,step=1e-3,format = "%.3f")
    
    v_A = st.slider(label='$v$ = wind speed [m s$^{-1}$]', 
                           key="v", min_value=0.0, max_value=10.0, value=3.0)
    Tw_A = st.slider(label='$T_w$ = water surface temperature [$^o$C]', 
                           key="Tw", min_value=0.0, max_value=45.0, value=26.0)
    Ta_A = st.slider(label='$T_a$ = air temperature [$^o$C]', 
                           key="Ta", min_value=0.0, max_value=45.0,value=30.0)
    RH_A = st.slider(label='$RH$ = relative humidity of air [-]', 
                           key="RH", min_value=0.0, max_value=100.0, value=30.0)
    KvRadio = st.radio(label="How would you like to input $K_v$ &emsp; \
             [$k Pa^{-1}$]",options=('Input Kv','Calculate Kv'),index = 0,horizontal=True)
    if KvRadio == 'Input Kv':
        Kv = st.slider(label='Vapor transfer coefficient = $K_v$ x $10^{-10}$ &emsp; [kPa$^{-1}$]', 
                       key="Kv", min_value=1.0, max_value=5E3, value=266.0,format='%.5f')
        Kv = Kv*1E-10
        st.write("$K_v$ = ",str(np.round(Kv*1E10)),'E-10 [kPa$^{-1}$]')
    if KvRadio == 'Calculate Kv':
        z_A = st.slider(label="Measurement height = $z$ $[m]$",
                      key='z',min_value=0.0,max_value=10.0,value=2.0,format='%.5f')
        z0_A = st.slider(label="Surface roughness height = $z_o$ $[m]$",
                      key='zo',min_value=0.0,max_value=1.0,value=0.003,format='%.5f') 
        Kv = 1.132*1e-6/((math.log(z_A/z0_A))**2)
        st.write("$K_v$ = ",str(np.round(Kv*1E10)),'E-10 [kPa$^{-1}$]')
            
   
    c = 1000*3600*24
    esTw_A = 611*math.exp((17.27*Tw_A)/(237.3+Tw_A))*1e-3
    esTa_A = 611*math.exp((17.27*Ta_A)/(237.3+Ta_A))*1e-3
    eaTa_A = 0.01*RH_A*esTa_A       
    Ea = c*Kv*v_A*(esTw_A-eaTa_A)
    st.success("$E_a$ = "+str(np.round_(Ea,2))+"[mm day$^{-1}$]")


with colEe:
    # Energy balance method
    st.header("Energy balance method")
    energyBalanceExpander = st.expander("Documentaion")
    with energyBalanceExpander:        
        st.latex(r''' \text{Energy balance eauation}\\
                 \text{On the water surface}: \\
                 R_n = L + H + \Delta S/ \Delta t + G ''')
        st.markdown("where,")
        st.markdown(" $R_n$ = Net radiation absorbed  [$W m^{-2}$]")
        st.latex(r'''\small = SW_{in} - SW_{out} + LW_{in} - LW_{out}''')
        st.markdown("where,")
        st.latex(r'''
                 \small
                 SW_{in} = \text{Incoming shortwave}\\
                 SW_{out} = \text{Outgoing shortwave}\\
                 LW_{in} = \text{Incoming longwave}\\
                 LW_{out} = \text{Outgoing longwave}''')
        st.markdown("$L$ = Latent heat loss [$W m^{-2}$]")
        st.latex(r'''= E \rho _{w} \lambda''')
        st.markdown("where,")
        st.latex(r'''
                 \small
                 E = \text{Evaporation rate }[m s^{-1}] \\
                 \rho_{w} = 998=\text{density of water }[kg m^{-3}] \\
                 \lambda = \text{Latent heat of vaporization } \\
                     = 2500 - 2.36T_w \quad [kJ kg^{-1}]''')
        st.markdown("$H$ = Sensible heat flux [$W m^{-2}$]")
        st.latex(r'''= K_h v (T_w - T_a)''')
        st.markdown("where,")
        st.latex(r'''\small
                 v = \text{wind speed at height z } [m s^{-1}] \\
                 T_w = \text{water surface temperature }[^{o}C] \\
                 T_a = \text{air temperature at height z }[^{o}C] \\
                 K_h = \text{Vertical heat transfer coefficient }\\
                 \large 
                 = \frac{k^2 c_a \rho_a}{[ln(z/z_{o})]^2} \quad [J ^{o}C m^{-3}]''')
        st.markdown("where,")
        st.latex(r'''
                 \small
                 k = 0.4 = \text{von Karman constant } [-] \\
                 \rho_a = 1.15 = \text{density of air } [kg m^{-3}] \\
                 c_a = \text{specific heat capacity of air }\\
                     = 1005 \quad [J kg^{-1} K^{-1}] \\
                 z_o = \text{Surface roughness} \text{ height } [m] \\
                 z = \text{Measurement} \text{ height } [m] \\
                 ''')
        st.markdown("$\Delta S/ \Delta t$ = Storage heat &emsp; [$Wm^{-2}$]")
        st.latex(r'''= c_w \rho_w h \frac{(T_{w1}-T_{w1}}{\Delta t})''')
        st.markdown("where,")
        st.latex(r'''
                 \small
                 c_w = \text{specific heat capacity of water} \\
                     = 4184 \quad [J kg^{-1} K^{-1}] \\
                 h = \text{height of water layer } [m] \\
                 T_{w1} = T_{air} \text{ at time $t_1$ }[^{o}C]\\
                 T_{w2} = T_{air} \text{ at time $t_2$ }[^{o}C]\\
                 \Delta t = t_2 - t_1 \quad [s] ''')
        st.markdown("$G$ = Ground heat flux [$W m^{-2}$]")
        st.latex(r'''
                 \small
                 \bullet
                 \text{\textcolor{red}{ Usually we ignore:
                                       "$\Delta$ S/$\Delta t$"  and "G"}} \\
                 \bullet\text{\textcolor{red}{After simplification}}
                 ''')
        st.markdown("$E$ = Evaporation rate &emsp; [$m s^{-1}$]")
        st.latex(r'''E = c \frac{R_n - H}{\rho_w \lambda} \quad \text{[mm d$^{-1}$]}
                 ''')
        st.markdown("where,")
        st.markdown("$c$ = $8.64 E7$ &nbsp; Conversion Factor &nbsp; \
                    [$m$ $s^{-1}$] &nbsp; to &nbsp; [$mm$ $d^{-1}$]")

    Rn = st.slider("$R_n$ = Net Radiation [Wm$^{-2}$]",min_value=-200.0,max_value=1000.0,value=250.0,step=0.1)
    v = st.slider(label='$v$ = wind speed [m s$^{-1}$]', 
                           key="v_Eb", min_value=0.0, max_value=10.0, value=3.0)
    Tw = st.slider(label='$T_w$ = water surface temperature [$^o$C]', 
                           key="Tw_Eb", min_value=0.0, max_value=45.0, value=26.0)
    Ta = st.slider(label='$T_a$ =  air temperature [$^o$C]', 
                           key="Ta_Eb", min_value=0.0, max_value=45.0,value=30.0)
    KhRadio = st.radio(label="How would you like to input $K_h$ &emsp; \
             [$J ^{o}C m^{-3}$]",options=('Input Kh','Calculate Kh'),index = 0,horizontal=True)
    if KhRadio == 'Input Kh':
        Kh = st.slider(label='Vapor transfer coefficient = $K_h$ &emsp; [$J ^{o}C m^{-3}$]', 
                       key="Kh", min_value=0.01, max_value=50.00, value=4.37,format='%.5f')
    if KhRadio == 'Calculate Kh':
        z = st.slider(label="Measurement height = $z$ $[m]$",
                      key='z_Eb',min_value=0.0,max_value=10.0,value=2.0,format='%.5f')
        z0 = st.slider(label="Surface roughness height = $z_o$ $[m]$",
                      key='zo_Eb',min_value=0.0,max_value=1.0,value=0.003,format='%.5f') 
        Kh = 184.92/((np.log(z/z0))**2)
    H = Kh*v*(Tw-Ta)
    st.write("$K_h$ = ",str(np.round_(Kh,2)),'&emsp; [$J ^{o}C m^{-3}$]')
    st.write("$H$ = ",str(np.round_(H,2)),'[$W m^{-2}$]')
    Eb = c*(Rn - H)/(998*(2500-2.36*Tw)*1000)
    st.success("$E_b$ = "+str(np.round_(Eb,2))+"[mm day$^{-1}$]")
with colEc:
    # Combined Penman method
    st.header("Combined Penman method")
    combinedExpander = st.expander("Documentaion")
    with combinedExpander:        
        st.latex(r''' 
                 E = \left(\frac{\Delta}{\Delta + \gamma}\right)E_b^{*} + \
                     \left(\frac{\gamma}{\Delta + \gamma}\right)E_a^{*}''')
        st.markdown("where,")
        st.markdown("$\Delta$: Slope of saturation vapour pressure curve [$kPa K^{-1}$]")
        st.latex(r''' 
                 \Delta = \frac{4.098 e_s(T_a)}{(237.3 + T_a)^{2}} \quad [kPa K^{-1}] \\
                 ''')
        st.markdown("where,")
        st.latex(r'''\small
                 e_s(T_a) = \text{sat. vapour pressure @ }T_a [kPa] \\
                 T_a = \text{air temperature at height z }[^{o}C] \\    
                 ''')
        st.markdown("$\gamma$: Psychrometric constant [$P_a K^{-1}$]")
        st.latex(r'''
                 \small
                    \gamma = \frac{c_a P_a}{0.622 \lambda } \quad [PaK^{-1}]
                ''')
        st.markdown("where,")
        st.latex(r'''
                 \small
                 c_a = \text{specific heat capacity of air} \\
                     = 1005 [J kg^{-1}K^{-1}]\\
                 P_a = \text{Atm. Pressure }[kPa] \\
                 \lambda = \text{Latent heat of vaporization } \\
                     = 2500 - 2.36T_w \quad [kJ kg^{-1}]''')
        st.markdown("$E_{b}^{*}$ : &emsp; Analogous to energy balance method")
        st.latex(r''' 
                 E_b^{*} = \frac{R_n}{\rho_w \lambda} \\
                 ''')
        st.markdown("where,")
        st.latex(r'''
                 \small
                 R_n = \text{Net radiation absorbed } \footnotesize [W m^{-2}] \\
                \small \rho_w =998 = \text{density of water }[kg m^{-3}] \\
                 \lambda = \text{Latent heat of vaporization } \\
                     = 2500−2.36T_w ​[kJ kg^{-1}]
                ''')
        st.markdown("$E_{a}^{*}$ : &emsp; Analogous to aerodynamic method")
        st.latex(r''' 
                 E_a^{*} = K_v v [e_s(T_a) - e_a] ''')
        st.markdown("where,")
        st.latex(r''' 
                 \small
                 v = \text{wind speed at height z } [m s^{-1}] \\                 
                 e_a = \text{actual vapour pressure } [kPa] \\
                 T_w = \text{water surface temperature }[^{o}C] \\                 
                 K_v = \text{Vertical vapour transfer coefficient } \\
                     = \frac{0.622 k^2 \rho_a}{P_a \rho_w [ln(z/z_o)]^{2}} \quad [kPa^{-1}]
                     ''')
        st.markdown("where,")
        st.latex(r''' 
                 \small
                 k = 0.4 = \text{von karman} \text{ constant } [-] \\
                 \rho_a = 1.15 \text{= density} \text{ of air } [kg m^{-3}] \\
                 \rho_w = 998 \text{= density} \text{ of water }  [kg m^{-3}] \\
                 Pa = \text{Atm.} \text{pressure } [kPa] \quad \quad  \\
                 z_o = \text{Surface roughness} \text{ height } [m] \\
                 z = \text{Measurement} \text{ height } [m] \\
                 ''')
    Rn_C = st.slider("$R_n$ = Net Radiation [Wm$^{-2}$]",
                   key = "Rn_Ec",min_value=-200.0,max_value=1000.0,value=250.0,step=0.1)
    v_C = st.slider(label='$v$ = wind speed [m s$^{-1}$]', 
                           key="v_Ec", min_value=0.0, max_value=10.0, value=3.0)
    Tw_C = st.slider(label='$T_w$ = water surface temperature [$^o$C]', 
                           key="Tw_Ec", min_value=0.0, max_value=45.0, value=26.0)
    Ta_C = st.slider(label='$T_a$ =  air temperature [$^o$C]', 
                       key="Ta_Ec", min_value=0.0, max_value=45.0,value=30.0)
    RH_C = st.slider(label='$RH$ = relative humidity of air [-]', 
                           key="RH_Ec", min_value=0.0, max_value=100.0, value=30.0)
    KvRadio = st.radio(label="How would you like to input $K_v$ &emsp; \
             [$k Pa^{-1}$]",key = 'radio_Ec',options=('Input Kv','Calculate Kv'),index = 0,horizontal=True)
    if KvRadio == 'Input Kv':
        Kv_C = st.slider(label='Vapor transfer coefficient = $K_v$ x $10^{-10}$ &emsp; [kPa$^{-1}$]', 
                       key="Kv_Ec", min_value=1.0, max_value=5E3, value=266.0,format='%.5f')
        Kv_C = Kv_C*1E-10
        st.write("$K_v$ = ",str(np.round(Kv_C*1E10)),'E-10 [kPa$^{-1}$]')
    if KvRadio == 'Calculate Kv':
        z_C = st.slider(label="Measurement height = $z$ $[m]$",
                      key='z_Ec',min_value=0.0,max_value=10.0,value=2.0,format='%.5f')
        z0_C = st.slider(label="Surface roughness height = $z_o$ $[m]$",
                      key='zo_Ec',min_value=0.0,max_value=1.0,value=0.003,format='%.5f') 
        Kv_C = 1.132*1e-6/((math.log(z_C/z0_C))**2)
        st.write("$K_v$ = ",str(np.round(Kv_C*1E10)),'E-10 [kPa$^{-1}$]')
    c = 1000*3600*24
    esTw_C = 611*math.exp((17.27*Tw_C)/(237.3+Tw_C))*1e-3
    esTa_C = 611*math.exp((17.27*Ta_C)/(237.3+Ta_C))*1e-3
    eaTa_C = 0.01*RH_C*esTa_C 
    delta = 4098*esTa_C/(237.3 + Ta_C)**2 # kPa
    gamma = 1005*101.3/(0.622*(2500-2.36*Tw_C))/1E3 # kPa
    st.write("$\Delta$ = "+str(np.round_(delta,5))+" [$kPa K^{-1}$]")
    st.write("$\gamma$ = "+str(np.round_(gamma,5))+" [$kPa K^{-1}$]")
    Ec = c*(delta/(gamma+delta)*(Rn_C/(998*(2500-2.36*Tw_C)*1E3)) + \
         gamma/(gamma+delta)*(Kv_C*v_C*(esTa_C-eaTa_C)))
    st.success("$E_c$ = "+str(np.round_(Ec,2))+" [mm day$^{-1}$]")
    
    
    
    
    
    
    
    
    
    
    
# K = 1.132*1e-9/((math.log(z/z0))**2)      
# #Energy Balance Method
# Kh = 184.92/((math.log(z/z0))**2)
# l = 2500 - (2.36*Tw)
# H = Kh*v*(Tw-Ta)
# E1 = (Rn - H)*86400/(l*998)

# #Combined Method
# d = (611*(((237.3 + Ta)*17.27)-(17.27*Ta))*math.exp((17.27*Ta)/(237.3+Ta)))/(237.3+Ta)**2
# l1 = 2500 - (2.36*Ta)
# g = 163676.045/l1
# h = (g/(g+d))*K*v*(esTa-eaTa)*1000
# i = ((d*Rn*1e-3)/(998*l1*(d+g))) 
# #E2 = (((d*Rn*0.001)/(998*l1*(d+g))) + (g*K*v*(esTa - eaTa)/(d+g)))*86400*1000
# E2 = (h + i)*86400*1000















# st.write("e(Tw) = ",(eaTa))
# st.write("e1(Tw) = ",(esTa))
    
# st.write("E =",E)
# st.write("k =",K)

    
#     #Energy Balance Method
    
    
# st.write("Kh = ",Kh)
# st.write("H = ",H)
# st.write("E = ",E1)

#     #Combined Method
# st.write("d = ",d)
# st.write("g = ",g)
# st.write("E2 = ",E2)
# st.write("l = ",l1)
# st.write("h =",h)
# st.write("i =",i)
