from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
import astrbot.api.message_components as comp
from astrbot.api import logger
from random import randint, choice, random
from datetime import datetime

frys = ["香菇","菠菜","蒜苗","胡萝卜","空心菜","地瓜叶","花菜","茄子","南瓜","鸡蛋(韭菜炒鸡蛋，西红柿炒鸡蛋)", "土豆丝", "四季豆"]
example_foods = ["早饭", "中饭", "晚饭"]
meals = ["KFC","麦当劳","馍馍","自选菜（比如老乡鸡）","火锅","麻辣烫","冒菜","钵钵鸡","沙县小吃","鸡公煲","牛肉饭","咖喱饭",
         "乌冬面","炒饭","炒米粉","炒面","盖浇饭","酸菜鱼","生煎包","卤肉饭","饺子","泡面(还是吃点健康的吧)",
         "一饭一菜套餐","干锅","土豆粉","米粉","兰州拉面","披萨","肠粉","江西小炒","拌粉","炒饼","猪脚饭"
         ]
human_templates = [
    # 今天尝尝 + 后缀
    "今天尝尝{}吧",
    "今天尝尝{}怎么样？",
    "今天尝尝{}？",
    "今天尝尝{}！",

    # 这一顿试试 + 后缀
    "这一顿试试{}吧",
    "这一顿试试{}怎么样？",
    "这一顿试试{}？",
    "这一顿试试{}！",

    # 试试 + 后缀
    "试试{}吧",
    "试试{}怎么样？",
    "试试{}？",
    "试试{}！",

    # 了解一下 + 后缀
    "了解一下{}吧",
    "了解一下{}怎么样？",
    "了解一下{}？",
    "了解一下{}！",

    # 吃点 + 后缀
    "吃点{}吧",
    "吃点{}怎么样？",
    "吃点{}？",
    "吃点{}！",

    # 来点 + 后缀
    "来点{}吧",
    "来点{}怎么样？",
    "来点{}？",
    "来点{}！",

    # 吃吃 + 后缀
    "吃吃{}吧",
    "吃吃{}怎么样？",
    "吃吃{}？",
    "吃吃{}！",

    # 空前缀 + 所有后缀
    "{}吧",
    "{}怎么样？",
    "{}？",
    "{}尝尝",
    "{}吃吃！",
    "{}！",

    # 额外添加的常用表达
    "不妨试试{}吧",
    "不妨试试{}怎么样？",
    "推荐你{}尝尝",
    "一定要试{}！",
]
kfc_not_human = ["友情提醒，今天是星期四", "KFC Crazy Thursday", ":(\n\n在调用插件的处理函数 meal 时出现异常：KFC Crazy Thursday need ￥50", "前面忘了，后面忘了，最后今天疯狂星期四"]
human_length = len(human_templates)
kfc_length = len(kfc_not_human)
total_length = human_length + kfc_length
img_path = ["开始炒.jpg", "炒好了.jpg"]
nowtime = datetime.now()

@register("meal", "spica", "一个简单的 是啊，吃什么 插件", "0.4.5")
class RandMeal(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    # async def initialize(self):
    #     """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 meal。注册成功后，发送 `/meal` 就会触发这个指令，并回复一个随机的吃什么建议。alias 参数可以设置指令的别名，用户发送别名也会触发这个指令。
    @filter.command("meal", alias={'吃什么', '吃什麽'})
    async def random_meal(self, event: AstrMessageEvent, msg_arg: str=""):
        """这是一个 是啊，吃什么 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        # user_name = event.get_sender_name()
        # message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        if msg_arg == "菜单":
            yield event.plain_result("菜单功能开发中！")
        elif msg_arg == "":
            if nowtime.weekday() == 3 and random() < 0.4: # 疯狂星期四 kfc概率0.4
                i = randint(0, total_length-1)
                if random() <= 0.5:
                    meal = meals[0]
                    sentense = choice(human_templates).format(meal)
                else:
                    sentense = choice(kfc_not_human)
            else:
                meal = meals[randint(0,len(meals)-1)]
                sentense = choice(human_templates).format(meal)
            yield event.plain_result(sentense) # 发送一条纯文本消息
            # yield event.plain_result(str(msg_arg=="")) # 发送一条纯文本消息
        elif msg_arg == "帮助" or msg_arg == "help":
            yield event.plain_result("功能一览\n输入 /meal 触发主功能\n输入 /meal 目录 查看正在开发的功能\n输入 /meal 帮助 查看帮助文档")
        else:
            yield event.plain_result("没有这个参数哦\n输入参数help可以查看帮助")

    @filter.command("fry", alias={'炒什么'})
    async def fry(self, event: AstrMessageEvent, n=1):
        """这是一个 是啊，炒什么 指令"""
        message_chain = event.get_messages()
        logger.info(message_chain)

        chain = [
            comp.Plain(f"炒{frys[randint(0,len(frys)-1)]}"),           # 炒xx \n [图片]
            comp.Image.fromFileSystem(f"C:\\Users\\leoli\\.astrbot\\data\\plugins\\astrobot_plugin_random_meal\\assets\\{img_path[randint(0, len(img_path)-1)]}")
        ]
        for i in range(n-1):
            chain.insert(0, comp.Plain(f"炒{frys[randint(0,len(frys)-1)]}"))
        yield event.chain_result(chain)

    # async def terminate(self):
    #     """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
