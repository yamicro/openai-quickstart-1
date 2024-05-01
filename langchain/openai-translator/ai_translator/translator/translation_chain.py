from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.memory import ConversationBufferMemory
from utils import LOG

class TranslationChain:
    def __init__(self, model_name: str = "gpt-3.5-turbo", verbose: bool = True):
        # 翻译任务指令始终由 System 角色承担
        system_message = "You are a translation expert, proficient in various languages. \nTranslates {source_language} to {target_language}."
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)

        # 待翻译文本由 Human 角色输入
        human_message_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_message_template)

        # 使用 System 和 Human 角色的提示模板构造 ChatPromptTemplate
        chat_prompt_template = ChatPromptTemplate.from_messages(
            [system_message_prompt, MessagesPlaceholder(variable_name="chat_history"), human_message_prompt]
        )

        # 初始化 ChatOpenAI 实例
        llm = ChatOpenAI(
            model_name=model_name,
            temperature=0,
            verbose=verbose,
            api_key="your_zhipuai_api_key",
            api_base="https://open.bigmodel.cn/api/paas/v4/"
        )

        # 创建 ConversationBufferMemory 实例
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # 创建 LLMChain 实例
        self.chain = LLMChain(llm=llm, prompt=chat_prompt_template, verbose=verbose, memory=memory)

    def run(self, text: str, source_language: str, target_language: str) -> (str, bool):
        try:
            # 构建完整的翻译提示信息
            result = self.chain.run({
                "text": text,
                "source_language": source_language,
                "target_language": target_language,
            })
            
            return result, True
        except Exception as e:
            LOG.error(f"An error occurred during translation: {e}")
            return "", False
