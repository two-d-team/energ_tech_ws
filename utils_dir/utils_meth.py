def select_units():
    st.subheader('Select a Unit')

    unit_1=st.checkbox('Unit1')
    if unit_1:
        unit_list.append("Unit1")
    unit_2=st.checkbox('Unit2')
    if unit_2:
        unit_list.append("Unit2")
    unit_3=st.checkbox('Unit3')
    if unit_3:
        unit_list.append("Unit3")
    unit_4=st.checkbox('Unit4')
    if unit_4:
        unit_list.append("Unit4")
    unit_5=st.checkbox('Unit5')
    if unit_5:
        unit_list.append("Unit5")
    unit_6=st.checkbox('Unit6')
    if unit_6:
        unit_list.append("Unit6")
    unit_7=st.checkbox('Unit7')
    if unit_7:
        unit_list.append("Unit7")
    return unit_list


def choose_unit(unit):
    latitude,longitude,turbine_model,tower_height,rotor_diameter,production_year,start,stop,ins_cap,limitation_to_mw=None,None,None,None,None,None,None,None,None,None
    if unit=="Unit1":
        latitude=48.212883
        longitude=27.696193
        turbine_model="NORDEX N60"
        tower_height=69
        rotor_diameter=60
        production_year=1999
        start=2.5
        stop=25
        ins_cap=1.3
        limitation_to_mw=0
    elif unit=="Unit2":
        latitude = 47.132982
        longitude = 28.193314
        turbine_model = "General Electric 1.5S"
        tower_height = 65
        rotor_diameter = 70
        production_year = 1999
        start = 2.5
        stop = 25
        ins_cap = 1.3
        limitation_to_mw = 0
    elif unit == "Unit3":
        latitude = 48.212883
        longitude = 27.696193
        turbine_model = "NORDEX N60"
        tower_height = 69
        rotor_diameter = 60
        production_year = 1999
        start = 2.5
        stop = 25
        ins_cap = 1.3
        limitation_to_mw = 0
    elif unit == "Unit4":
        latitude = 48.212883
        longitude = 27.696193
        turbine_model = "NORDEX N60"
        tower_height = 69
        rotor_diameter = 60
        production_year = 1999
        start = 2.5
        stop = 25
        ins_cap = 1.3
        limitation_to_mw = 0
    elif unit == "Unit5":
        latitude = 48.212883
        longitude = 27.696193
        turbine_model = "NORDEX N60"
        tower_height = 69
        rotor_diameter = 60
        production_year = 1999
        start = 2.5
        stop = 25
        ins_cap = 1.3
        limitation_to_mw = 0
    elif unit == "Unit6":
        latitude = 48.212883
        longitude = 27.696193
        turbine_model = "NORDEX N60"
        tower_height = 69
        rotor_diameter = 60
        production_year = 1999
        start = 2.5
        stop = 25
        ins_cap = 1.3
        limitation_to_mw = 0
    elif unit == "Unit7":
        latitude = 48.212883
        longitude = 27.696193
        turbine_model = "NORDEX N60"
        tower_height = 69
        rotor_diameter = 60
        production_year = 1999
        start = 2.5
        stop = 25
        ins_cap = 1.3
        limitation_to_mw = 0

    return [latitude,longitude,turbine_model,tower_height,rotor_diameter,production_year,start,stop,ins_cap,limitation_to_mw]