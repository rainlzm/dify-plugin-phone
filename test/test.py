
from utils import PhoneNumberUtils

# 中国手机号码（随机测试号码）
cn_mobile_numbers = [
    "+861381234xxxx",  # 标准国际格式
    "1861234xxxx",  # 国内格式
    "1736231xxxx",  # 国内格式
    "1536231xxxx",  # 国内格式
    "010-12345678",  # 北京固话
    "021 1234 5678",  # 上海固话
    "0755-12345678",  # 深圳固话
    "400-123-4567",  # 400服务号码
    "400-823-4567",  # 400服务号码
    "800-123-4567",  # 800免费号码
    "1-234-5678",  # 短号码(可能在某些地区有效)
]

# 国际电话号码（非个人）
international_numbers = [
    "+1-650-253-0000",  # 美国(Google)
    "+44 20 7031 3000",  # 英国
    "+81 3-1234-5678",  # 日本
    "+33 1 70 39 39 39",  # 法国
    "+49 30 901820",  # 德国
    "+61 2 9876 5432",  # 澳大利亚
    "+82 2-123-4567",  # 韩国
    "+65 6123 4567",  # 新加坡
    "+7 495 123-45-67",  # 俄罗斯
]

if __name__ == "__main__":
    # input your test phone number
    print('----------cn_mobile_numbers---------------')
    for number in cn_mobile_numbers:
        try:
            print(f"number {number}, res: {PhoneNumberUtils.get_location_info(number)}")
        except Exception as e:
            print(f"ERROR {number}: {str(e)}")

    print('------------international_numbers-------------')
    for number in international_numbers:
        try:
            print(f"number {number}, res: {PhoneNumberUtils.get_location_info(number)}")
        except Exception as e:
            print(f"ERROR {number}: {str(e)}")
