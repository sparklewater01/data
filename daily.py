import streamlit as st
from google.cloud import bigquery
from datetime import date
from mapping_module import apply_mapping
from category_groups import get_group_config_names, get_group_column

st.set_page_config(layout="wide")
st.title("일별 카테고리별 판매량 대시보드")

# 날짜 입력 받기
start_date = st.date_input("시작일", value=date(2024,1,1))
end_date = st.date_input("종료일", value=date(2024,12,31))

client = bigquery.Client()

# 배송상태 목록
status_options = [
    "주문접수",
    "결제완료",
    "출고준비",
    "배송보류",
    "주문무효",
    "결제취소",
    "결제실패",
    "출고후",
    "출고완료",
    "배송중",
    "배송완료"
]

# 초기값으로 모든 상태를 선택
selected_statuses = st.multiselect("배송상태 선택 (다중 선택 가능)", status_options, default=status_options)

# BigQuery 쿼리 (일자별 집계, raw category만)
base_query = """
SELECT 
  DATE(payment_date) AS day,
  category,
  SUM(total) AS total_quantity
FROM `sales-data-analysis-442801.sales_data.daily_sales`
WHERE DATE(payment_date) BETWEEN @start_date AND @end_date
AND status IN UNNEST(@status_list)
GROUP BY day, category
ORDER BY day, category
"""

query_params = [
    bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
    bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
    bigquery.ArrayQueryParameter("status_list", "STRING", selected_statuses)
]

job_config = bigquery.QueryJobConfig(query_parameters=query_params)
df_sales = client.query(base_query, job_config=job_config).to_dataframe()

# 매핑 적용
df_mapped = apply_mapping(df_sales)

# 원본 데이터 표시 (매핑 전)
st.write("일별 원본 카테고리 데이터(매핑 전):")
st.dataframe(df_sales)

# 그룹 설정 선택
config_names = get_group_config_names()
selected_config = st.selectbox("그룹 설정 선택", config_names)
selected_column = get_group_column(selected_config)

st.write(f"선택한 그룹 컬럼: {selected_column}")

if not df_mapped.empty:
    # 날짜를 문자열로 변환
    df_mapped['day_str'] = df_mapped['day'].astype(str)
    
    # pivot_table 사용: 중복 키 문제 해결 위해 aggfunc='sum'
    pivot_df = df_mapped.pivot_table(
        index=selected_column,
        columns='day_str',
        values='total_quantity',
        aggfunc='sum'
    )
    st.write("피벗 형태(선택한 그룹컬럼별 행, 일자별 열):")
    st.dataframe(pivot_df)

    st.write("일자별 변화 (라인 차트)")
    st.line_chart(pivot_df.T)
else:
    st.write("선택한 기간과 배송상태에 해당하는 데이터가 없습니다.")
