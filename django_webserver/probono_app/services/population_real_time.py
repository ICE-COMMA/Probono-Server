import os
import requests
from pathlib import Path

import openpyxl
from concurrent.futures import ThreadPoolExecutor, as_completed

from probono_app.models import PopulRegion

class PopulationRealTime():
    
    def __init__(self):
        self.__base_url   = 'http://openapi.seoul.go.kr:8088/68666f624d6c696d373249736e7649/json/citydata_ppltn'

    def init_population_info(self):
        print('Initializing population region info.. ', end='')
        PopulRegion.objects.all().delete()
        to_insert = self.__get_xl_file_info()
        popul_region_instances = [PopulRegion(**item) for item in to_insert]
        PopulRegion.objects.bulk_create(popul_region_instances)
        print('OK')

    def get_real_time_popul(self):
        
        region_info = PopulRegion.objects.all().values()

        start_index = 1
        end_index   = 5

        ret = []
        # Multithreading for optimization
        with ThreadPoolExecutor() as executor:
            future_to_url = {executor.submit(
                self.__fetch_data, f"{self.__base_url}/{start_index}/{end_index}/{target['AREA_CD']}"): target for target in region_info}
            for future in as_completed(future_to_url):
                target = future_to_url[future]
                try:
                    temp = future.result()['SeoulRtd.citydata_ppltn'][0]
                    area_popul_average = round(
                        (int(temp['AREA_PPLTN_MIN']) + int(temp['AREA_PPLTN_MAX'])) / 2)
                    data = {
                        'area_name'         : temp['AREA_NM'],
                        'area_code'         : temp['AREA_CD'],
                        'area_congest'      : temp['AREA_CONGEST_LVL'],
                        'message'           : temp['AREA_CONGEST_MSG'],
                        'area_popul_min'    : temp['AREA_PPLTN_MIN'],
                        'area_popul_max'    : temp['AREA_PPLTN_MAX'],
                        'area_popul_avg'    : area_popul_average,
                        'area_update_time'  : temp['PPLTN_TIME']
                    }
                    ret.append(data)
                except Exception as exc:
                    print(f'{target["AREA_CD"]} generated an exception: {exc}')

        ret = sorted(ret, key=lambda x: x['area_popul_avg'], reverse=True)
        return ret   

    def __get_xl_file_info(self):
        current_dir = Path(__file__).parent
        base_dir    = current_dir.parent
        file_path   = base_dir / 'files' / 'population_region_info.xlsx'

        xl_file     = openpyxl.load_workbook(file_path)
        xl_sheet    = xl_file.active

        data_list = []
        for row_idx, row in enumerate(xl_sheet.iter_rows(values_only=True), start=1):
            if row_idx == 1:
                continue
            category    = row[0]
            no          = row[1]
            area_cd     = row[2]
            area_nm     = row[3]
            data_list.append({
                'CATEGORY'  : category,
                'NO'        : no,
                'AREA_CD'   : area_cd,
                'AREA_NM'   : area_nm,
            })
        xl_file.close()
        return data_list

    def __fetch_data(self, url):
        response = requests.get(url)
        return response.json()