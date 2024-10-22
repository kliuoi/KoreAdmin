from enum import Enum
from pydantic import BaseModel


# 使用枚举类定义自定义状态码, 效率更高
class CustomCodeBase(Enum):
    """自定义状态码基类"""

    @property
    def code(self):
        """
        获取状态码
        """
        return self.value[0]

    @property
    def msg(self):
        """
        获取状态码信息
        """
        return self.value[1]


class CustomResponseCode(CustomCodeBase):
    """自定义响应状态码"""

    HTTP_200 = (200, "请求成功")
    HTTP_201 = (201, "新建请求成功")
    HTTP_202 = (202, "请求已接受，但处理尚未完成")
    HTTP_204 = (204, "请求成功，但没有返回内容")
    HTTP_400 = (400, "请求错误")
    HTTP_401 = (401, "未经授权")
    HTTP_403 = (403, "禁止访问")
    HTTP_404 = (404, "请求的资源不存在")
    HTTP_410 = (410, "请求的资源已永久删除")
    HTTP_422 = (422, "请求参数非法")
    HTTP_425 = (425, "无法执行请求，由于服务器无法满足要求")
    HTTP_429 = (429, "请求过多，服务器限制")
    HTTP_500 = (500, "服务器内部错误")
    HTTP_502 = (502, "网关错误")
    HTTP_503 = (503, "服务器暂时无法处理请求")
    HTTP_504 = (504, "网关超时")

    # 自定义错误状态码
    CAPTCHA_ERROR = (40001, "验证码错误")


class CustomResponse(BaseModel):
    """
    提供开放式响应状态码，而不是枚举，如果你想自定义响应信息，这可能很有用
    """

    code: int
    msg: str


class StandardResponseCode:
    """标准响应状态码"""

    """
    HTTP codes
    See HTTP Status Code Registry:
    https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml

    And RFC 2324 - https://tools.ietf.org/html/rfc2324
    """
    HTTP_100 = 100  # CONTINUE: 继续
    HTTP_101 = 101  # SWITCHING_PROTOCOLS: 协议切换
    HTTP_102 = 102  # PROCESSING: 处理中
    HTTP_103 = 103  # EARLY_HINTS: 提示信息
    HTTP_200 = 200  # OK: 请求成功
    HTTP_201 = 201  # CREATED: 已创建
    HTTP_202 = 202  # ACCEPTED: 已接受
    HTTP_203 = 203  # NON_AUTHORITATIVE_INFORMATION: 非权威信息
    HTTP_204 = 204  # NO_CONTENT: 无内容
    HTTP_205 = 205  # RESET_CONTENT: 重置内容
    HTTP_206 = 206  # PARTIAL_CONTENT: 部分内容
    HTTP_207 = 207  # MULTI_STATUS: 多状态
    HTTP_208 = 208  # ALREADY_REPORTED: 已报告
    HTTP_226 = 226  # IM_USED: 使用了
    HTTP_300 = 300  # MULTIPLE_CHOICES: 多种选择
    HTTP_301 = 301  # MOVED_PERMANENTLY: 永久移动
    HTTP_302 = 302  # FOUND: 临时移动
    HTTP_303 = 303  # SEE_OTHER: 查看其他位置
    HTTP_304 = 304  # NOT_MODIFIED: 未修改
    HTTP_305 = 305  # USE_PROXY: 使用代理
    HTTP_307 = 307  # TEMPORARY_REDIRECT: 临时重定向
    HTTP_308 = 308  # PERMANENT_REDIRECT: 永久重定向
    HTTP_400 = 400  # BAD_REQUEST: 请求错误
    HTTP_401 = 401  # UNAUTHORIZED: 未授权
    HTTP_402 = 402  # PAYMENT_REQUIRED: 需要付款
    HTTP_403 = 403  # FORBIDDEN: 禁止访问
    HTTP_404 = 404  # NOT_FOUND: 未找到
    HTTP_405 = 405  # METHOD_NOT_ALLOWED: 方法不允许
    HTTP_406 = 406  # NOT_ACCEPTABLE: 不可接受
    HTTP_407 = 407  # PROXY_AUTHENTICATION_REQUIRED: 需要代理身份验证
    HTTP_408 = 408  # REQUEST_TIMEOUT: 请求超时
    HTTP_409 = 409  # CONFLICT: 冲突
    HTTP_410 = 410  # GONE: 已删除
    HTTP_411 = 411  # LENGTH_REQUIRED: 需要内容长度
    HTTP_412 = 412  # PRECONDITION_FAILED: 先决条件失败
    HTTP_413 = 413  # REQUEST_ENTITY_TOO_LARGE: 请求实体过大
    HTTP_414 = 414  # REQUEST_URI_TOO_LONG: 请求 URI 过长
    HTTP_415 = 415  # UNSUPPORTED_MEDIA_TYPE: 不支持的媒体类型
    HTTP_416 = 416  # REQUESTED_RANGE_NOT_SATISFIABLE: 请求范围不符合要求
    HTTP_417 = 417  # EXPECTATION_FAILED: 期望失败
    HTTP_418 = 418  # UNUSED: 闲置
    HTTP_421 = 421  # MISDIRECTED_REQUEST: 被错导的请求
    HTTP_422 = 422  # UNPROCESSABLE_CONTENT: 无法处理的实体
    HTTP_423 = 423  # LOCKED: 已锁定
    HTTP_424 = 424  # FAILED_DEPENDENCY: 依赖失败
    HTTP_425 = 425  # TOO_EARLY: 太早
    HTTP_426 = 426  # UPGRADE_REQUIRED: 需要升级
    HTTP_427 = 427  # UNASSIGNED: 未分配
    HTTP_428 = 428  # PRECONDITION_REQUIRED: 需要先决条件
    HTTP_429 = 429  # TOO_MANY_REQUESTS: 请求过多
    HTTP_430 = 430  # Unassigned: 未分配
    HTTP_431 = 431  # REQUEST_HEADER_FIELDS_TOO_LARGE: 请求头字段太大
    HTTP_451 = 451  # UNAVAILABLE_FOR_LEGAL_REASONS: 由于法律原因不可用
    HTTP_500 = 500  # INTERNAL_SERVER_ERROR: 服务器内部错误
    HTTP_501 = 501  # NOT_IMPLEMENTED: 未实现
    HTTP_502 = 502  # BAD_GATEWAY: 错误的网关
    HTTP_503 = 503  # SERVICE_UNAVAILABLE: 服务不可用
    HTTP_504 = 504  # GATEWAY_TIMEOUT: 网关超时
    HTTP_505 = 505  # HTTP_VERSION_NOT_SUPPORTED: HTTP 版本不支持
    HTTP_506 = 506  # VARIANT_ALSO_NEGOTIATES: 变体也会协商
    HTTP_507 = 507  # INSUFFICIENT_STORAGE: 存储空间不足
    HTTP_508 = 508  # LOOP_DETECTED: 检测到循环
    HTTP_509 = 509  # UNASSIGNED: 未分配
    HTTP_510 = 510  # NOT_EXTENDED: 未扩展
    HTTP_511 = 511  # NETWORK_AUTHENTICATION_REQUIRED: 需要网络身份验证

    """
    WebSocket codes
    https://www.iana.org/assignments/websocket/websocket.xml#close-code-number
    https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent
    """
    WS_1000 = 1000  # NORMAL_CLOSURE: 正常闭合
    WS_1001 = 1001  # GOING_AWAY: 正在离开
    WS_1002 = 1002  # PROTOCOL_ERROR: 协议错误
    WS_1003 = 1003  # UNSUPPORTED_DATA: 不支持的数据类型
    WS_1005 = 1005  # NO_STATUS_RCVD: 没有接收到状态
    WS_1006 = 1006  # ABNORMAL_CLOSURE: 异常关闭
    WS_1007 = 1007  # INVALID_FRAME_PAYLOAD_DATA: 无效的帧负载数据
    WS_1008 = 1008  # POLICY_VIOLATION: 策略违规
    WS_1009 = 1009  # MESSAGE_TOO_BIG: 消息太大
    WS_1010 = 1010  # MANDATORY_EXT: 必需的扩展
    WS_1011 = 1011  # INTERNAL_ERROR: 内部错误
    WS_1012 = 1012  # SERVICE_RESTART: 服务重启
    WS_1013 = 1013  # TRY_AGAIN_LATER: 请稍后重试
    WS_1014 = 1014  # BAD_GATEWAY: 错误的网关
    WS_1015 = 1015  # TLS_HANDSHAKE: TLS握手错误
    WS_3000 = 3000  # UNAUTHORIZED: 未经授权
    WS_3003 = 3003  # FORBIDDEN: 禁止访问


# 自定义验证错误信息不包含验证预期内容（也就是输入内容），受支持的预期内容字段参考以下链接
# https://github.com/pydantic/pydantic-core/blob/a5cb7382643415b716b1a7a5392914e50f726528/tests/test_errors.py#L266
# 替换预期内容字段方式，参考以下链接
# https://github.com/pydantic/pydantic/blob/caa78016433ec9b16a973f92f187a7b6bfde6cb5/docs/errors/errors.md?plain=1#L232
CUSTOM_VALIDATION_ERROR_MESSAGES = {
    "arguments_type": "参数类型输入错误",
    "assertion_error": "断言执行错误",
    "bool_parsing": "布尔值输入解析错误",
    "bool_type": "布尔值类型输入错误",
    "bytes_too_long": "字节长度输入过长",
    "bytes_too_short": "字节长度输入过短",
    "bytes_type": "字节类型输入错误",
    "callable_type": "可调用对象类型输入错误",
    "dataclass_exact_type": "数据类实例类型输入错误",
    "dataclass_type": "数据类类型输入错误",
    "date_from_datetime_inexact": "日期分量输入非零",
    "date_from_datetime_parsing": "日期输入解析错误",
    "date_future": "日期输入非将来时",
    "date_parsing": "日期输入验证错误",
    "date_past": "日期输入非过去时",
    "date_type": "日期类型输入错误",
    "datetime_future": "日期时间输入非将来时间",
    "datetime_object_invalid": "日期时间输入对象无效",
    "datetime_parsing": "日期时间输入解析错误",
    "datetime_past": "日期时间输入非过去时间",
    "datetime_type": "日期时间类型输入错误",
    "decimal_max_digits": "小数位数输入过多",
    "decimal_max_places": "小数位数输入错误",
    "decimal_parsing": "小数输入解析错误",
    "decimal_type": "小数类型输入错误",
    "decimal_whole_digits": "小数位数输入错误",
    "dict_type": "字典类型输入错误",
    "enum": "枚举成员输入错误，允许 {expected}",
    "extra_forbidden": "禁止额外字段输入",
    "finite_number": "有限值输入错误",
    "float_parsing": "浮点数输入解析错误",
    "float_type": "浮点数类型输入错误",
    "frozen_field": "冻结字段输入错误",
    "frozen_instance": "冻结实例禁止修改",
    "frozen_set_type": "冻结类型禁止输入",
    "get_attribute_error": "获取属性错误",
    "greater_than": "输入值过大",
    "greater_than_equal": "输入值过大或相等",
    "int_from_float": "整数类型输入错误",
    "int_parsing": "整数输入解析错误",
    "int_parsing_size": "整数输入解析长度错误",
    "int_type": "整数类型输入错误",
    "invalid_key": "输入无效键值",
    "is_instance_of": "类型实例输入错误",
    "is_subclass_of": "类型子类输入错误",
    "iterable_type": "可迭代类型输入错误",
    "iteration_error": "迭代值输入错误",
    "json_invalid": "JSON 参数或格式输入错误",
    "json_type": "JSON 类型输入错误",
    "less_than": "输入值过小",
    "less_than_equal": "输入值过小或相等",
    "list_type": "列表类型输入错误",
    "literal_error": "字面值输入错误",
    "mapping_type": "映射类型输入错误",
    "missing": "缺少必填字段",
    "missing_argument": "缺少参数",
    "missing_keyword_only_argument": "缺少关键字参数",
    "missing_positional_only_argument": "缺少位置参数",
    "model_attributes_type": "模型属性类型输入错误",
    "model_type": "模型实例输入错误",
    "multiple_argument_values": "参数值输入过多",
    "multiple_of": "输入值非倍数",
    "no_such_attribute": "分配无效属性值",
    "none_required": "输入值必须为 None",
    "recursion_loop": "输入循环赋值",
    "set_type": "集合类型输入错误",
    "string_pattern_mismatch": "字符串约束模式输入不匹配",
    "string_sub_type": "字符串子类型（非严格实例）输入错误",
    "string_too_long": "字符串输入过长",
    "string_too_short": "字符串输入过短",
    "string_type": "字符串类型输入错误",
    "string_unicode": "字符串输入非 Unicode",
    "time_delta_parsing": "时间差输入解析错误",
    "time_delta_type": "时间差类型输入错误",
    "time_parsing": "时间输入解析错误",
    "time_type": "时间类型输入错误",
    "timezone_aware": "缺少时区输入信息",
    "timezone_naive": "禁止时区输入信息",
    "too_long": "输入过长",
    "too_short": "输入过短",
    "tuple_type": "元组类型输入错误",
    "unexpected_keyword_argument": "输入意外关键字参数",
    "unexpected_positional_argument": "输入意外位置参数",
    "union_tag_invalid": "联合类型字面值输入错误",
    "union_tag_not_found": "联合类型参数输入未找到",
    "url_parsing": "URL 输入解析错误",
    "url_scheme": "URL 输入方案错误",
    "url_syntax_violation": "URL 输入语法错误",
    "url_too_long": "URL 输入过长",
    "url_type": "URL 类型输入错误",
    "uuid_parsing": "UUID 输入解析错误",
    "uuid_type": "UUID 类型输入错误",
    "uuid_version": "UUID 版本类型输入错误",
    "value_error": "值输入错误",
}

CUSTOM_USAGE_ERROR_MESSAGES = {
    "class-not-fully-defined": "类属性类型未完全定义",
    "custom-json-schema": "__modify_schema__ 方法在V2中已被弃用",
    "decorator-missing-field": "定义了无效字段验证器",
    "discriminator-no-field": "鉴别器字段未全部定义",
    "discriminator-alias-type": "鉴别器字段使用非字符串类型定义",
    "discriminator-needs-literal": "鉴别器字段需要使用字面值定义",
    "discriminator-alias": "鉴别器字段别名定义不一致",
    "discriminator-validator": "鉴别器字段禁止定义字段验证器",
    "model-field-overridden": "无类型定义字段禁止重写",
    "model-field-missing-annotation": "缺少字段类型定义",
    "config-both": "重复定义配置项",
    "removed-kwargs": "调用已移除的关键字配置参数",
    "invalid-for-json-schema": "存在无效的 JSON 类型",
    "base-model-instantiated": "禁止实例化基础模型",
    "undefined-annotation": "缺少类型定义",
    "schema-for-unknown-type": "未知类型定义",
    "create-model-field-definitions": "字段定义错误",
    "create-model-config-base": "配置项定义错误",
    "validator-no-fields": "字段验证器未指定字段",
    "validator-invalid-fields": "字段验证器字段定义错误",
    "validator-instance-method": "字段验证器必须为类方法",
    "model-serializer-instance-method": "序列化器必须为实例方法",
    "validator-v1-signature": "V1字段验证器错误已被弃用",
    "validator-signature": "字段验证器签名错误",
    "field-serializer-signature": "字段序列化器签名无法识别",
    "model-serializer-signature": "模型序列化器签名无法识别",
    "multiple-field-serializers": "字段序列化器重复定义",
    "invalid_annotated_type": "无效的类型定义",
    "type-adapter-config-unused": "类型适配器配置项定义错误",
    "root-model-extra": "根模型禁止定义额外字段",
}
