import re

# 이메일 정규 표현식 (간단한 버전)
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# 정규표현식 설명:
# ^                         -> 문자열의 시작
# [a-zA-Z0-9._%+-]+         -> 이메일의 사용자 이름 부분 (영문 대소문자, 숫자, 점, 밑줄, %, +, - 포함 가능, 1글자 이상)
# @                         -> 반드시 '@' 기호가 있어야 함
# [a-zA-Z0-9.-]+            -> 도메인 이름 (예: gmail, naver 등 / 점(.)과 하이픈(-)도 포함 가능)
# \.                        -> 도메인과 최상위 도메인(TLD) 사이에 있는 점(.)을 의미 (반드시 있어야 함)
# [a-zA-Z]{2,}              -> 최상위 도메인 (예: com, net, kr 등 / 영문자 2글자 이상)
# $                         -> 문자열의 끝

# 샘플 이메일 리스트
sample_emails = [
    "john.doe@example.com",      # 유효
    "jane_doe123@sub.domain.co", # 유효
    "user@localhost",            # 무효 (도메인 끝이 없음)
    "hello.world@",              # 무효 (도메인이 없음)
    "foo@bar.com",               # 유효
    "no_at_symbol.com",          # 무효 (@ 없음)
    "user@@doubleat.com",        # 무효 (@가 두 개)
    "valid.email+alias@gmail.com", # 유효
    "user@domain.c",             # 무효 (최상위 도메인이 1글자)
    "user.name@domain.com",      # 유효
]

# 검사 수행
for email in sample_emails:
    if re.match(email_pattern, email):
        print(f"✅ 유효한 이메일: {email}")
    else:
        print(f"❌ 유효하지 않은 이메일: {email}")
