import os
import unittest
import langchain
from src.chatbot.fx_cache import FxOpenAI
from langchain.llms import OpenAI
from langchain.cache import InMemoryCache
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.cache import GPTCache
from src.chatbot.fx_cache import init_gptcache

load_dotenv()

class Test(unittest.TestCase):

    def test_llm_openai(self):

        # 开启缓存
        # langchain.llm_cache = InMemoryCache()

        langchain.llm_cache = GPTCache(init_gptcache)

        os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
        # llm = OpenAI(model_name="text-davinci-002", n=2, best_of=2)

        llm = FxOpenAI(model_name="text-davinci-002", n=2, best_of=2)

        result = llm("Tell me a joke")
        print(f"result={result}")

        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()
