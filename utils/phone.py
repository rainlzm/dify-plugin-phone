import phonenumbers
from phonenumbers import carrier, geocoder, timezone, PhoneNumberType

class PhoneNumberUtils:
    """电话号码处理工具类（支持国际/国内号码）"""

    def __init__(self, default_region="CN"):
        """
        初始化工具类
        :param default_region: 默认国家/地区代码（如CN表示中国）
        """
        self.default_region = default_region

    def parse(self, phone_str: str) -> phonenumbers.PhoneNumber:
        """
        解析电话号码（自动处理带/不带国际区号的情况）
        :param phone_str: 原始电话号码字符串
        :return: PhoneNumber对象
        """
        try:
            return phonenumbers.parse(phone_str, self.default_region)
        except phonenumbers.NumberParseException as e:
            raise ValueError(f"号码解析失败: {str(e)}") from e

    def validate(self, phone_str: str) -> bool:
        """
        验证电话号码有效性
        :return: True/False
        """
        try:
            num = self.parse(phone_str)
            return phonenumbers.is_valid_number(num)
        except ValueError:
            return False

    def format_number(self, phone_str: str, fmt=phonenumbers.PhoneNumberFormat.E164) -> str:
        """
        格式化电话号码
        :param fmt: 格式类型（E164/INTERNATIONAL/NATIONAL）
        :return: 格式化后的字符串
        """
        try:
            num = self.parse(phone_str)
            return phonenumbers.format_number(num, fmt)
        except ValueError:
            return "无效号码"

    @staticmethod
    def get_location_info(self, phone_str: str, lang="zh") -> dict:
        """
        获取归属地、运营商信息
        :param self:
        :param phone_str:
        :param lang: 语言代码（zh/zh_TW/en等）
        :return: 包含归属地、运营商、时区的字典
        """
        try:
            num = self.parse(phone_str)
            return {
                "归属地": geocoder.description_for_number(num, lang),
                "运营商": carrier.name_for_number(num, lang),
                #"时区": timezone.time_zones_for_number(num),
                "类型": self._get_number_type(num)
            }
        except ValueError:
            return {"错误": "无效号码"}

    def batch_validate(self, phone_list: list) -> dict:
        """
        批量验证电话号码
        :return: {号码: 有效性} 的字典
        """
        results = {}
        for num in phone_list:
            results[num] = self.validate(num)
        return results

    @staticmethod
    def _get_number_type(num: phonenumbers.PhoneNumber) -> str:
        """获取号码类型（中文描述）"""
        type_map = {
            PhoneNumberType.MOBILE: "手机号",
            PhoneNumberType.FIXED_LINE: "固定电话",
            PhoneNumberType.VOIP: "网络电话",
            PhoneNumberType.TOLL_FREE: "免费电话"
        }
        return type_map.get(phonenumbers.number_type(num), "未知类型")


# test
if __name__ == "__main__":
    util = PhoneNumberUtils()

    # 验证
    phone = "15872394334"
    print(f"有效性: {util.validate(phone)}")
    print(util.get_location_info(phone))