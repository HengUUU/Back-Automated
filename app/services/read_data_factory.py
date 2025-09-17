import json
import pandas as pd
from typing import List, Dict, Any

def read_nested_data_fac(file_path: str) -> pd.DataFrame:
    try:
        with open(file_path, 'r') as f:
            data_dict = json.load(f)
        data = data_dict['data']['children']

        dic_key = []

        for prov in data:
            # print(prov)
            factory = []
            for child in prov['children']:
                factory.append({"deviceId":child['code'], 
                                "Company":child['name'], 
                                "Type":child['type']})

            
            dic_key.append({"province": prov['name'], "province_total": prov['total'],"factory": factory}
)
        
        return dic_key
        
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return pd.DataFrame()
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the file at {file_path}.")
        return pd.DataFrame()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()
    

def nested_data_factory(data_dict: json) -> pd.DataFrame:
    data = data_dict['data']['children']

    dic_key = []

    for prov in data:
            # print(prov)
        factory = []
        for child in prov['children']:
            factory.append({"deviceId":child['code'], 
                            "Company":child['name'], 
                            "Type":child['type']})

            
        dic_key.append({"province": prov['name'], "province_total": prov['total'],"factory": factory}
)
        
    return dic_key
        
    

def get_factory_infor(device_id:str, all_station_data):
    
    for province in all_station_data:
        fact_info = province['factory']
        for ind,j in enumerate(fact_info):
            if fact_info[ind]['deviceId'] == device_id:
                return {"Province": province['province'], 
                        "Company": fact_info[ind]['Company'], 
                        "Type": fact_info[ind]['Type']}

