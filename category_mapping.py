from google.cloud import bigquery
import pandas as pd

# 1. BigQuery 클라이언트 생성 (인증 필요)
client = bigquery.Client()

# 2. BigQuery에서 raw category를 갖는 데이터 쿼리
query = """
SELECT 
  category,
  payment_date,
  total
FROM `sales-data-analysis-442801.sales_data.daily_sales`
WHERE DATE(payment_date) BETWEEN '2024-01-01' AND '2024-12-31'
"""
df_sales = client.query(query).to_dataframe()

# df_sales는 category, payment_date, total 컬럼을 가진 DataFrame이라고 가정

# 3. 매핑 CSV 로드
# category_map.csv 파일을 같은 폴더에 있다고 가정
df_map = pd.read_csv("category_map.csv")  
# df_map은 raw, category1, category2, category3 컬럼을 가짐

# 4. merge 수행
# df_sales의 category 컬럼과 df_map의 raw 컬럼을 기준으로 매핑
df_merged = df_sales.merge(df_map, left_on='category', right_on='raw', how='left')

# df_merged에는 category1, category2, category3 컬럼이 추가된 상태
# 이제 payment_date, total 등 기존 칼럼과 함께 사용 가능

# 5. 결과 확인
print(df_merged.head())

# df_merged를 이용해 원하는 분석, 시각화, 필터링 등을 수행할 수 있음.
