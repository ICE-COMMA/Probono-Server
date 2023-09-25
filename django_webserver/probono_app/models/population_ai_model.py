import requests
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

from pathlib import Path

# AI modules
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np

class Population_AI_model():
    
    def __init__(self):
        self.holi_url       = 'https://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo'
        self.holi_key       = '4cwiloFmPQxO3hXwmJy3jruoPPh6m8PQZqxBkWecSAgIIeRjq6UIdo0r7ZnmT4Rm4kVErRaD9jd1XU5CS7Chwg=='

    def get_predict_value(self):
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                '11500540'  : executor.submit(self.predict_pop, 'hwagok1'),
                '11380625'  : executor.submit(self.predict_pop, 'yeokchon'),
                '11380690'  : executor.submit(self.predict_pop, 'jingwan'),
                '11740685'  : executor.submit(self.predict_pop, 'gil')
            }

            predict_dict = {}
            for key, future in futures.items():
                predict_dict[key] = future.result()[0]

        print('Predict finished')
        return predict_dict

    def predict_pop(self, district_name):
        # modeling 단계와 동일하게 변수설정
        n_steps = 24  # 하루치 데이터
        n_features = 1  # 변수 개수
        n_output = 24  # 출력 길이

        target_district = district_info(district_name)

        ai_model = target_district.ai_model
        resource_data = np.reshape(target_district.batch_data, (-1, 1))

        scaler = target_district.fitted_scaler
        # 최근 24개 data를 scaling해서 예측 과정에 입력
        scaled_data = scaler.transform(resource_data)

        predictions = []  # 예측 결과를 저장하기 위한 빈 배열

        # RNN에 맞춰 timeseriesgenerator 출력 형식으로 형 변환 (batch 사이즈: 24) -> (n, 24)
        current_batch = scaled_data.reshape(n_features, n_steps)  # (1, 24)

        # 예측할 범위 지정 (len_week 데이터 길이만큼 예측) -> 24의 크기를 가진 batch가 7개 필요
        for i in range(n_output):
            current_pred = ai_model.predict(
                current_batch)  # 한 배치를 통해 예측된 결과값 1개

            # 예측값을 저장
            predictions.append(current_pred)  # 예측한 결과를 하나씩 추가
            # batch의 시작 포인트를 하나씩 뒤로 밀고, 새로운 예측값을 마지막에 저장하여 batch 업데이트
            current_batch = np.append(
                current_batch[:, 1:], current_pred, axis=1)

        # list 형식의 결과값을 numpy 형태로 변환
        predictions = np.array(predictions).reshape(n_output, 1)  # (24,1)
        predictions = scaler.inverse_transform(predictions)  # 예측값 역정규화

        print(f'Predict region : {district_name}')
        return predictions.reshape(1, 24).tolist()  # 길이가 24인 list 형식으로 반환

    '''
    def get_holiday(self):

        ret = []
        params = {'serviceKey': self.holi_key,
                  'solYear': '2023', 'solMonth': '09'}
        response = requests.get(self.base_url, params=params)
        print(response)
        print(response.content)

        return ret
    '''


class district_info:  # 해당 지역 정보
    def __init__(self, district_name):
        self.base_url = 'http://openapi.seoul.go.kr:8088/4b4c477a766c696d39314965686a66/json/SPOP_LOCAL_RESD_DONG/1/24'
        # Hwagok1(화곡동), Yeokchon(역촌동), Jingwan(진관동), Gil(길동)
        self.district_code = ['11500540', '11380625', '11380690', '11740685']

        self.ai_model = tf.keras.models.load_model(self.file_loc(
            f'{district_name}_model.h5'))  # 해당 지역에 맞는 ai모델 호출
        self.datasets = self.read_csv(
            f'{district_name}_pop_data.csv')  # 해당 지역에 맞는 datasets 호출
        self.batch_data = self.update_batch(district_name)

        self.scaler = MinMaxScaler()  # data scaler 모듈 호출
        self.fitted_scaler = self.scaler.fit(
            self.datasets)  # 해당 지역의 전체 data에 대해 scaling

    def update_batch(self, district_name):
        district_code = {
            'hwagok1'   : '11500540',
            'yeokchon'  : '11380625',
            'jingwan'   : '11380690',
            'gil'       : '11740685'
        }
        one_week_ago = self.get_one_week_ago_date()

        target = district_code[district_name]  # 해당 지역에 대한 정보만 업데이트
        real = f"{self.base_url}/{one_week_ago}/ /{target}"
        fetched_data = self.fetch_data(real)

        fetched_data = fetched_data['SPOP_LOCAL_RESD_DONG']['row']
        data = []

        for data_row in fetched_data:
            temp = {
                'STDR_DE_ID'        : data_row['STDR_DE_ID'],  # 기준일 ID
                'TMZON_PD_SE'       : data_row['TMZON_PD_SE'],  # 시간대 구분
                'ADSTRD_CODE_SE'    : data_row['ADSTRD_CODE_SE'],  # 행정동코드
                'TOT_LVPOP_CO'      : data_row['TOT_LVPOP_CO']  # 총생활인구수
            }
            # print(temp)
            data.append(temp['TOT_LVPOP_CO'])

        return np.reshape(data, (1, -1))  # (1,24)

    # file 위치 반환해주는 함수
    def file_loc(self, file_name):
        # file_path = os.path.join(os.path.dirname(__file__), 'files', file_name)
        current_dir = Path(__file__).parent
        base_dir = current_dir.parent
        file_path = base_dir / 'files' / file_name

        print(file_path)
        return file_path

    # datasets(csv파일)을 호출하는 함수
    def read_csv(self, file_name):
        datasets = pd.read_csv(self.file_loc(file_name),
                               index_col=0, parse_dates=True)
        datasets.index.freq = 'H'  # index를 1시간 단위로 설정

        return datasets

    def fetch_data(self, url):
        response = requests.get(url)
        return response.json()

    def get_one_week_ago_date(self):  # 일주일전 날짜를 반환해주는 함수

        current_date = datetime.now().strftime('%Y-%m-%d')
        date = datetime.strptime(current_date, '%Y-%m-%d')

        one_week_ago_datetime = date - timedelta(days=7)

        month_diff = (date.month - one_week_ago_datetime.month) % 12
        if month_diff < 0:
            one_week_ago_datetime = one_week_ago_datetime.replace(
                year=date.year - 1)
            one_week_ago_datetime = one_week_ago_datetime.replace(
                month=date.month)

        if one_week_ago_datetime.day > date.day:
            one_week_ago_datetime = one_week_ago_datetime.replace(day=date.day)
        result_date = one_week_ago_datetime.strftime('%Y%m%d')
        return result_date