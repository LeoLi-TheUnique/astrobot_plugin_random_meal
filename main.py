from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
import astrbot.api.message_components as comp
from astrbot.api import logger
from random import randint, choice, random, sample
from datetime import datetime
import math

frys = ["香菇","菠菜","蒜苗","胡萝卜","空心菜","地瓜叶","花菜","茄子","南瓜","鸡蛋(韭菜炒鸡蛋，西红柿炒鸡蛋)", "土豆丝", "四季豆"]
example_foods = ["早饭", "中饭", "晚饭"]
# 西式快餐
meals_western_fastfood = ["KFC", "麦当劳", "披萨"]

# 中式快餐/简餐
meals_chinese_fastfood = [
    "沙县小吃",
    "自选菜（比如老乡鸡）",
    "一饭一菜套餐",
    "卤肉饭",
    "猪脚饭",
    "牛肉饭",
    "咖喱饭",
    "鸡公煲",
    "酸菜鱼",
    "盖浇饭"
]

# 粉面/主食类
meals_main = [
    "兰州拉面",
    "乌冬面",
    "炒面",
    "炒米粉",
    "米粉",
    "土豆粉",
    "拌粉",
    "江西小炒",
    "炒饭",
    "炒饼"
]

# 小吃/点心类
meals_snacks = ["生煎包", "饺子", "烧麦", "肠粉", "馍馍"]

# 汤锅/麻辣类
meals_spicy = ["火锅", "麻辣烫", "冒菜", "钵钵鸡", "干锅"]

# 即食/速食
meals_instant = ["泡面(还是吃点健康的吧)"]

meals = meals_western_fastfood + meals_chinese_fastfood + meals_main + meals_snacks + meals_spicy + meals_instant

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
qq_id = {}

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
            yield event.plain_result("功能一览\n输入 /吃什么 触发主功能\n输入 /吃什么 菜单 查看正在开发的功能\n输入 /meal 帮助 查看帮助文档")
        else:
            yield event.plain_result("没有这个参数哦\n输入参数help可以查看帮助")

    @filter.command("fry", alias={'炒什么'})
    async def fry(self, event: AstrMessageEvent, n="1"):
        """这是一个 是啊，炒什么 指令"""
        message_chain = event.get_messages()
        logger.info(message_chain)
        try:
            n = int(n)
        except ValueError:
            yield event.plain_result("请输入一个整数哦")
            return
        if int(n) > 10:
            yield event.plain_result("菜炒的太多会吃不完哦~\n建议炒10份以下的菜")
            return
        elif int(n) <= 0:
            yield event.plain_result("你到底炒不炒😠")
            return
        wait_for_fry = sample(frys, k=int(n))
        str = f"炒{wait_for_fry[0]}"
        for fryed in wait_for_fry[1:]:
            str += f"，炒{fryed}"
        chain = [
            comp.Plain(str),           # 炒xx \n [图片]
            comp.Image.fromFileSystem(f"C:\\Users\\leoli\\.astrbot\\data\\plugins\\astrobot_plugin_random_meal\\assets\\{img_path[randint(0, len(img_path)-1)]}")
        ]
        yield event.chain_result(chain)

    @filter.command("choice", alias={'选什么'})
    async def choice(self, event: AstrMessageEvent, option1: str, option2: str, n: int=1000):
        """这是一个 是啊，选什么 指令"""
        message_chain = event.get_messages()
        logger.info(message_chain)
        options = [option1, option2]
        if n > 10000000:
            yield event.plain_result("根据大数定理，再往上增加次数会很大概率会出现50\\% 50\\%")
            return
        n1 = 0
        n2 = 0

        for i in range(n): 
            choice_result = choice(options)
            if choice_result == option1:
                n1 += 1
            elif choice_result == option2:
                n2 += 1
            else:
                n3 += 1
        result = f"{option1}\n{int((math.ceil(n1/n*100)-30)*1.34) * '·'}\n{n1/n*100:.4f}%\n\n{option2}\n{int((math.ceil(n2/n*100)-30)*1.34) * '·'}\n{n2/n*100:.4f}%\n\n共进行了{n}次选择"
        
        yield event.plain_result(f"{result}")
    
    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("test")
    async def test(self, event: AstrMessageEvent):
        """这是一个测试函数，未注册为指令，可以被插件内其他函数调用。"""
        message_chain = event.get_messages()
        logger.info(message_chain)
        sender = event.message_obj.sender.user_id
        group_id = event.message_obj.group_id
        self_id = event.message_obj.self_id
        session_id = event.message_obj.session_id
        message_id = event.message_obj.message_id
        if sender in qq_id:
            qq_id[sender] += 1
            yield event.plain_result(f"sender: {sender}\n你已经调用过这个测试函数了哦\n调用次数：{qq_id[sender]}\n\ngroup_id: {group_id}\nself_id: {self_id}\nsession_id: {session_id}\nmessage_id: {message_id}")
        else:
            qq_id.update({sender: 1})
            yield event.plain_result(f"sender: {sender}\n这是你第一次调用这个测试函数哦\n调用次数：1\n\ngroup_id: {group_id}\nself_id: {self_id}\nsession_id: {session_id}\nmessage_id: {message_id}")
        # yield event.plain_result(f"sender: {sender}\ngroup_id: {group_id}\nself_id: {self_id}\nsession_id: {session_id}\nmessage_id: {message_id}")


    # async def terminate(self):
    #     """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
