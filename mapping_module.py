import pandas as pd

# 모듈 로드 시 CSV를 메모리에 로드해둔다.
# 실제 경로는 CSV 파일이 위치한 곳에 맞게 수정
df_map = pd.read_csv("category_map.csv")

def apply_mapping(df_sales):
    """
    df_sales: category 컬럼을 가진 판매 데이터 DataFrame.
    return: df_sales + category1, category2, category3 컬럼이 추가된 DataFrame
    """
    df_merged = df_sales.merge(df_map, left_on='category', right_on='raw', how='left')
    return df_merged





