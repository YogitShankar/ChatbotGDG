from langchain_core.prompts import ChatPromptTemplate
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import LLMChain

class CPChatbot:
    def __init__(self, retriever, system_message):
        self.retriever = retriever.retriever
        self.system_message = system_message
        model_id= "distilbert/distilgpt2"
        tokenizer = AutoTokenizer.from_pretrained(model_id,device_map = "auto")
        model = AutoModelForCausalLM.from_pretrained(model_id, device_map = "auto")
        hf_pipeline = pipeline(
            "text-generation", model=model, tokenizer=tokenizer, max_new_tokens = 2048
        )
        self.llm = HuggingFacePipeline(pipeline=hf_pipeline)
        template = """
          You are a competitive programming chatbot. Help out the user with the context provided below:
          {context}

          Using the above context, if relevant, answer the following query:
          {question}
        """
        self.prompt = ChatPromptTemplate.from_template(template)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",  # Key used to store the chat history
            return_messages=True        # Set to True to return the full messages
        )
        self.question_generator_chain = LLMChain(llm=self.llm, prompt=self.prompt)
        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm,                  # Your language model (e.g., OpenAI's GPT model)
            retriever=self.retriever,  # Your retriever
            memory=self.memory,
            chain_type="stuff",
            condense_question_prompt=self.prompt,
            # chain_type_kwargs={"prompt": self.prompt},
            return_source_documents=False# The memory that will store the conversation history
        )
        # self.qa.chain.set_prompt(custom_prompt)
    def chat(self, query):
        print(f"System Message: {self.system_message}")
        results = self.qa.run(query)
        print(results)
        return "Response constructed from retrieved documents."