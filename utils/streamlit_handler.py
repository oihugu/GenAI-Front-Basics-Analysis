from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.schema import AgentAction, AgentFinish, LLMResult
from langchain.callbacks.base import BaseCallbackHandler
from typing import Any, Dict, List, Union
import streamlit

class MyCustomHandler(BaseCallbackHandler):

    def __init__(self, BaseCallbackHandler, st) -> None:
        BaseCallbackHandler.__init__(self)
        self.st = st

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        #on_llm_start {'lc': 1, 'type': 'constructor', 'id': ['langchain', 'llms', 'google_palm', 'GooglePalm'], 'kwargs': {}}
        #print(f"on_llm_start {serialized}")
        #self.st.write(f"on_llm_start")
        pass

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        print(f"on_new_token {token}")

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when LLM errors."""


    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        action = response.generations[0][0].text
        if "Final Answer:" in action:
            self.st.write(action.split("Final Answer:")[-1])
        else:
            with self.st.expander(":thinking_face: Action"):
                self.st.write(action)

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        #on_tool_start {'name': 'Search Answer', 'description': 'useful for when you need to ask with recent information'}
        # print(f"on_tool_start {serialized}")
        print(f"on_tool_start")

    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        """Run when tool ends running."""
        print("on_tool_end")

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        #on_agent_action tool='Search Answer' tool_input='oi' log="I don't know what oi means\nAction: Search Answer\nAction Input: oi"
        #print(f"on_agent_action {action}")
        print(f"on_agent_action")