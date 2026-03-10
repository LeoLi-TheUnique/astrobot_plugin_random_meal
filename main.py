from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from random import randint

frys = ["香菇","菠菜","蒜苗","胡萝卜","空心菜","地瓜叶","花菜","茄子","南瓜","鸡蛋(韭菜炒鸡蛋，西红柿炒鸡蛋)"]
example_foods = ["早饭", "中饭", "晚饭"]
meals = ["KFC","麦当劳","馍馍","自选菜（比如老乡鸡）","火锅","麻辣烫","冒菜","钵钵鸡","沙县小吃","鸡公煲","牛肉饭","咖喱饭","乌冬面","炒饭","炒米粉","炒面","盖浇饭","酸菜鱼","生煎包","卤肉饭","饺子","泡面(还是吃点健康的吧)","一饭一菜套餐","干锅","土豆粉","米粉","兰州拉面","披萨","肠粉","江西小炒","拌粉"]
front_strs = [
    "今天尝尝",
    "这一顿试试",
    "试试看",
    "了解一下",
    "吃点",
    "来点",
    "吃吃",
    ""
]
back_strs = [       # 都使用全宽标点符号，保持风格一致
    "怎么样？",
    "？",
    "吧",
    "尝尝",
    "吃吃！",
    "！"
]

@register("meal", "spica", "一个简单的 是啊，吃什么 插件", "0.4.0")
class RandMeal(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    # async def initialize(self):
    #     """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 meal。注册成功后，发送 `/meal` 就会触发这个指令，并回复一个随机的吃什么建议。alias 参数可以设置指令的别名，用户发送别名也会触发这个指令。
    @filter.command("meal", alias={'吃什么', '吃什麽'})
    async def meal(self, event: AstrMessageEvent):
        """这是一个 是啊，吃什么 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        # user_name = event.get_sender_name()
        # message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        meal = meals[randint(0,len(meals)-1)]
        front_str = front_strs[randint(0,len(front_strs)-1)]
        back_str = back_strs[randint(0,len(back_strs)-1)]

        # 这里是一些特殊情况的处理，主要是为了让回复的消息更自然有趣。比如当随机到的前缀和后缀组合在一起不太合适时，就进行调整。
        if back_str == "吧" and meal == "钵钵鸡":
            back_str = "！"
        if front_str == "吃吃" and back_str == "吃吃！":
            front_str = "吃点"
            back_str = "尝尝"
        if front_str == "了解一下":
            back_str = "？"
        if meal == "沙县小吃" and back_str == "吃吃！":
            back_str = "怎么样？"
        if front_str == "":
            back_str = "怎么样？"
        if meal == "泡面(还是吃点健康的吧)" and back_str == "吧":
            back_str = ""


        yield event.plain_result(f"{front_str}{meal}{back_str}") # 发送一条纯文本消息

    @filter.command("fry", alias={'炒什么'})
    async def fry(self, event: AstrMessageEvent):
        """这是一个 是啊，炒什么 指令"""
        message_chain = event.get_messages()
        logger.info(message_chain)
        yield event.plain_result(f"炒{frys[randint(0,len(frys)-1)]}")

    # async def terminate(self):
    #     """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
