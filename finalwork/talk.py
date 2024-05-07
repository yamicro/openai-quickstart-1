import string
from zhipuai import ZhipuAI
import json


# 创建智普AI客户端
client = ZhipuAI(api_key="f916a1426f7a6bec9917e62564eb2e44.YCjKxRRZ0fjlzwlt")

# 分析对话双方的性格


def extract_character_personalities_as_string(content_list):
    # 将列表中的字符串连接起来
    text = ''.join(content_list)

    # 根据特定的格式处理文本，提取出每个角色的性格描述，并构建一个字符串
    character_personalities_string = ""
    current_character = None
    for part in text.split('（'):
        if '）：' in part:
            character_name, personality_part = part.split('）：')
            character_personalities_string += f"{character_name.strip()}的性格描述：{personality_part}\n"
            current_character = None
        elif current_character is not None:
            character_personalities_string += part
        else:
            current_character = part.strip()

    print(character_personalities_string)
    # 返回提取出的性格描述字符串
    return character_personalities_string


def analyze_personality(dialogue):
    messages = [{"role": "user", "content": msg} for msg in dialogue]
    response = client.chat.completions.create(
        model="glm-4",
        messages=messages,
        top_p=0.7,
        temperature=0.95,
        max_tokens=1024,
        stream=True,
    )
    personalities = []
    # print(response)
    for trunk in response:

        # if isinstance(trunk, ChatCompletionChunk):
        # 如果 trunk 是 ChatCompletionChunk 类型的对象
        content = trunk.choices[0].delta.content
        personalities.append(content)
        # 提取内容并拼接成文本
        # 这里假设每个 ChatCompletionChunk 只有一个 choice，并且我们只关心其中的 content
        # else:
        #     # 如果 trunk 是元组类型
        #     content = trunk[0]
    print(personalities)
    character_traits_string = ''.join(personalities)
    print(character_traits_string)
    return character_traits_string


# 使用性格生成多轮对话
def generate_dialogue(personalities):
    msgs = personalities.split('\n')
    msgs.append("请根据这两个角色的性格生成对话。注意不需要场景，只需要对话。按照如下格式形成对话：\t角色甲：对话内容\t角色乙：对话内容\t角色甲：对话内容\t角色乙：对话内容\t……\t,请注意角色甲、角色乙只是代号，不要出现在对话中。")

    messages = [{"role": "user", "content": msg} for msg in msgs]
    # print(messages)
    dialogue = []
    for _ in range(5):  # 5轮对话
        response = client.chat.completions.create(
            model="glm-4",
            messages=messages,
            top_p=0.7,
            temperature=0.95,
            max_tokens=1024,
            stream=True,
        )
        for trunk in response:
        
            content = trunk.choices[0].delta.content
            dialogue.append(content)
    talk_string = ''.join(dialogue)
    print(talk_string)
    return talk_string

# def generate_dialogue(personalities):
#     # 将personalities 按空格切分
#     msgs = personalities.split('\n')
#     msgs.append("请根据这两个角色的性格生成对话。")

#     messages = [{"role": "user", "content": msg} for msg in msgs]  # 将每个性格描述封装成字典
#     response = client.chat.completions.create(
#         model="glm-4",
#         messages=messages,
#         top_p=0.7,
#         temperature=0.95,
#         max_tokens=1024,
#         stream=True,
#     )
#     dialogue = ""
#     for trunk in response:
#         content = trunk.choices[0].delta.content
#         num = 0
#         for s in content:
#             if s == "\n":
#                 num += 1
#         if num > 1:
#             # 如果 lines 列表中的元素数量大于 1，说明存在连续的换行符，即换行
#             dialogue += content   # 将 lines 中的每行拼接成一个字符串，并在前面添加换行符
#         else:
#             # 否则，不换行，去除 content 中的回车符后拼接
#             dialogue += content.replace("\n", "") + " "  # 将 content 中的回车符替换为空，并在末尾添加空格
#     return dialogue


# 示例对话
# dialogue = [
#     "方鸿渐：“我爱你是真的，但是我不能接受你的求婚。”",
#     "唐晓芙：“为什么？你怕我拖累你吗？”",
#     "方鸿渐：“不是，我是怕我自己。我已经习惯了一个人的生活，我不想改变。”",
#     "唐晓芙：“那么你为什么还要来招惹我？”",
#     "方鸿渐：“我不知道，也许是我自私吧。我觉得我们这样挺好的，我不想失去。”",
#     "唐晓芙：“你真的爱我吗？”",
#     "方鸿渐：“爱，但是我也爱我的自由。”",
#     "唐晓芙：“那你到底要我怎么样？”",
#     "方鸿渐：“我不知道，我真的不知道。”",
#     "请根据上面的对话，分析方鸿渐和唐晓芙的性格，分别用三个词说明。同时输出格式类似于：人物甲：大方、可爱、善良。 \n ：大方、可爱、善良。",
# ]

def read_dialogue_from_markdown(file_path):
    dialogue = []
    with open(file_path, "r", encoding="utf-8") as file:
        is_dialogue_section = False
        for line in file:
            line = line.strip()
            if line == "```":  # 开始或结束对话部分
                is_dialogue_section = not is_dialogue_section
            elif is_dialogue_section and line:  # 在对话部分且不为空行时
                dialogue.append(line)
    return dialogue

# 示例对话所在的Markdown文件路径
markdown_file_path = "novel.md"

# 从Markdown文件中提取对话内容
dialogue = read_dialogue_from_markdown(markdown_file_path)

# 输出对话内容
print(dialogue)
dialogue.append("请根据上面的对话，分析方鸿渐和唐晓芙的性格，分别用三个词说明。同时输出格式类似于：人物甲：大方、可爱、善良。 \n ：大方、可爱、善良。",)
# 分析对话双方的性格
personalities = analyze_personality(dialogue)
print(personalities)
# 使用性格生成多轮对话
generated_dialogue = generate_dialogue(personalities)

# 输出生成的对话
# for line in generated_dialogue:
#     print(line)
output_file = "generated_dialogue.txt"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(generated_dialogue)

print(f"对话已保存到文件 {output_file}")
