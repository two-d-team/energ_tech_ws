import pandas as pd

unit1_dict = {
    "wind_plant": 'Unit1',
    "ins_cap": 1.3,
    "limitation": 'no',
    "lattitude" : "48.212883",
    "longitute" : "27.696193",
    "Turbine Model" : "NORDEX N60",
    "Tower Height" : 69,
    "Rotor Diameter" : 60 ,
    "Production Year" : 1999,
    "start" : 2.5,
    "stop" : 25
}

unit2_dict = {
    "wind_plant": 'Unit2',
    "ins_cap": 1.5,
    "limitation": 'no',
    "lattitude" : "47.132982",
    "longitute" : "28.193314",
    "Turbine Model" : "General Electric 1.5S",
    "Tower Height" : 65,
    "Rotor Diameter" : 70 ,
    "Production Year" : 2002,
    "start" : 4,
    "stop" : 25
}

unit3_dict = {
    "wind_plant": 'Unit3',
    "ins_cap": 1.5,
    "limitation": 1,
    "lattitude" : "48.3707",
    "longitute" : "27.0547",
    "Turbine Model" : "Enercon E66 1,8/70",
    "Tower Height" : 65,
    "Rotor Diameter" : 66 ,
    "Production Year" : 2000,
    "start" : 2.5,
    "stop" : 25
}

unit4_dict = {
    "wind_plant": 'Unit4',
    "ins_cap": 1.5,
    "limitation": 'no',
    "lattitude" : "47.034746",
    "longitute" : "28.421021",
    "Turbine Model" : "SUEDWIND S70",
    "Tower Height" : 85,
    "Rotor Diameter" : 70 ,
    "Production Year" : 2002,
    "start" : 4,
    "stop" : 25
}


unit5_dict = {
    "wind_plant": 'Unit5',
    "ins_cap": 1.5,
    "limitation": 'no',
    "lattitude" : "48.242849",
    "longitute" : "27.584352",
    "Turbine Model" : "General Electric ",
    "Tower Height" : 65,
    "Rotor Diameter" : 70 ,
    "Production Year" : 2000,
    "start" : 4,
    "stop" : 25
}


unit6_dict = {
    "wind_plant": 'Unit6',
    "ins_cap": 1.3,
    "limitation": 'no',
    "lattitude" : "47.530336",
    "longitute" : "28.795417",
    "Turbine Model" : "SUDWIND S70",
    "Tower Height" : 85,
    "Rotor Diameter" : 70 ,
    "Production Year" : 2000,
    "start" : 4,
    "stop" : 25
}


unit7_dict = {
    "wind_plant": 'Unit7',
    "ins_cap": 1.3,
    "limitation": 'no',
    "lattitude" : "48.37064",
    "longitute" : "27.054691",
    "Turbine Model" : "NORDEX N60",
    "Tower Height" : 65,
    "Rotor Diameter" : 62 ,
    "Production Year" : 1999,
    "start" : 2.5,
    "stop" : 28
}


solar1={
    "latitude":"46.953021 ",
     "longitude":"28.755979"
}

unit_dicts = [unit1_dict, unit2_dict, unit3_dict, unit4_dict, unit5_dict, unit6_dict, unit7_dict]

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(unit_dicts)

