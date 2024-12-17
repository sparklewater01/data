# category_groups.py

# 사용할 수 있는 그룹 설정을 딕셔너리 형태로 관리.
# 키: 사용자에게 표시할 이름(라벨), 값: 실제로 DataFrame에서 사용될 컬럼명
group_configs = {
    '원본(raw)로 보기': 'raw',
    '1차 분류(category1)': 'category1',
    '2차 분류(category2)': 'category2',
    '3차 분류(category3)': 'category3'
}

def get_group_config_names():
    """
    사용자에게 표시할 그룹 설정의 이름(라벨) 리스트를 반환.
    """
    return list(group_configs.keys())

def get_group_column(config_name):
    """
    사용자가 선택한 config_name(라벨)에 해당하는 실제 컬럼명을 반환.
    config_name은 get_group_config_names()로 얻은 목록 중 하나여야 함.
    """
    return group_configs[config_name]
