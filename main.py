from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from random import randint

frys = ["香菇","菠菜","蒜苗","胡萝卜","空心菜","地瓜叶","花菜","茄子","南瓜","鸡蛋(韭菜炒鸡蛋，西红柿炒鸡蛋)"]
example_foods = ["早饭", "中饭", "晚饭"]
meals = ["KFC","麦当劳","馍馍","自选菜（比如老乡鸡）","火锅","麻辣烫","冒菜","钵钵鸡","沙县小吃","鸡公煲","牛肉饭","咖喱饭","炒饭","炒米粉","炒面","盖浇饭","酸菜鱼","生煎包","卤肉饭","饺子/馄饨","泡面(还是吃点健康的吧)","一饭一菜","川菜","东北菜","干锅","土豆粉","米粉/米线","兰州拉面"]
front_str = [
    "今天尝尝",
    "这一顿试试"
]

@register("meal", "YourName", "一个简单的 是啊，吃什么 插件", "0.1.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    # async def initialize(self):
    #     """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 meal。注册成功后，发送 `/meal` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("meal", alias={'吃什么'})
    async def meal(self, event: AstrMessageEvent):
        """这是一个 是啊，吃什么 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        yield event.plain_result(f"{front_str[randint(0,len(front_str)-1)]}{meals[randint(0,len(meals)-1)]}吧") # 发送一条纯文本消息

    @filter.command("fry", alias={'炒什么'})
    async def fry(self, event: AstrMessageEvent):
        """这是一个 是啊，炒什么 指令"""
        message_chain = event.get_messages()
        logger.info(message_chain)
        yield event.plain_result(f"炒{frys[randint(0,len(frys)-1)]}")

    # async def terminate(self):
    #     """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
