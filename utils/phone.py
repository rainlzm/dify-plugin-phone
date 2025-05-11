import phonenumbers
from phonenumbers import carrier, geocoder, PhoneNumberMatcher, PhoneNumberType, number_type

class PhoneNumberUtils:
    """电话号码处理工具类（支持国际/国内号码）"""

    TYPE_MAP = {
        PhoneNumberType.MOBILE: "手机号",
        PhoneNumberType.FIXED_LINE: "固定电话",
        PhoneNumberType.VOIP: "网络电话",
        PhoneNumberType.TOLL_FREE: "免费电话"
    }

    @staticmethod
    def parse(phone_str: str, default_region="CN") -> phonenumbers.PhoneNumber:
        """
        解析电话号码（自动处理带/不带国际区号的情况）
        :param phone_str: 原始电话号码字符串
        :param default_region: 默认国家/地区代码（如CN表示中国）
        :return: PhoneNumber对象
        """
        try:
            return phonenumbers.parse(phone_str, default_region)
        except phonenumbers.NumberParseException as e:
            raise ValueError(f"号码解析失败: {str(e)}") from e

    @staticmethod
    def validate(phone_str: str, default_region="CN") -> bool:
        """
        验证电话号码有效性
        :return: True/False
        """
        try:
            num = PhoneNumberUtils.parse(phone_str, default_region)
            return phonenumbers.is_valid_number(num)
        except ValueError:
            return False

    @staticmethod
    def extract_phone_numbers(text: str, default_region="CN") -> list:
        """从文本中提取电话号码（支持国际/国内格式）"""
        try:
            matches = PhoneNumberMatcher(text, default_region)
            results = []
            for match in matches:
                number = phonenumbers.format_number(
                    match.number,
                    phonenumbers.PhoneNumberFormat.E164
                )
                results.append(number)
            return results
        except ValueError:
            return []

    @staticmethod
    def batch_validate(phone_list: list, default_region="CN") -> dict:
        """
        批量验证电话号码
        :return: {号码: 有效性} 的字典
        """
        results = {}
        for num in phone_list:
            results[num] = PhoneNumberUtils.validate(num, default_region)
        return results

    @staticmethod
    def get_location_info(phone_str: str, default_region="CN", lang="zh") -> dict:
        """
        获取归属地、运营商信息
        :param phone_str: 电话号码
        :param default_region: 默认国家/地区代码
        :param lang: 语言代码（zh/zh_TW/en等）
        :return: 包含归属地、运营商、时区的字典
        """
        try:
            num = PhoneNumberUtils.parse(phone_str, default_region)
            num_type = number_type(num)
            # 获取运营商信息（处理空值情况）
            carrier_name = carrier.name_for_number(num, lang)
            if not carrier_name:
                carrier_name = "电信(固定电话一般推断)" if num_type == PhoneNumberType.FIXED_LINE else "未知"
            return {
                "归属地": geocoder.description_for_number(num, lang),
                "运营商": carrier_name,
                # "时区": timezone.time_zones_for_number(num),
                "类型": PhoneNumberUtils.TYPE_MAP.get(num_type, "未知类型")
            }
        except ValueError:
            return {"错误": "无效号码"}


# test
if __name__ == "__main__":
    phone = "15872394334"
    print(f"有效性: {PhoneNumberUtils.validate(phone)}")
    print(get_location_info(phone))
    print(PhoneNumberUtils.extract_phone_numbers('sdfsdfwer 15872324322 dfsdf'))