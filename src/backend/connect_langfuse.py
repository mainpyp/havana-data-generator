import os
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Any, Dict, Optional, List
from dotenv import load_dotenv


class LangfuseManager:
    def __init__(
        self,
        public_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        host: Optional[str] = None,
    ):
        """
        Initialize Langfuse client. If no keys/host are provided, use environment variables.
        """
        self.public_key = public_key or os.getenv("LANGFUSE_PUBLIC_KEY")
        self.secret_key = secret_key or os.getenv("LANGFUSE_SECRET_KEY")
        self.host = host or os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
        self.langfuse = None
        self._init_client()

    def _init_client(self):
        """Initialize the Langfuse client singleton."""
        self.langfuse = Langfuse(
            public_key=self.public_key, secret_key=self.secret_key, host=self.host
        )

    def get_secret_key(self) -> str:
        """Get the Langfuse secret key."""
        return self.langfuse.secret_key

    def get_handler(self) -> CallbackHandler:
        """Get a Langfuse CallbackHandler for LangChain tracing."""
        return CallbackHandler()

    def create_chain(
        self,
        prompt_template: str = "Tell me a joke about {topic}",
        model_name: str = "gpt-4.1-nano-2025-04-14",
    ):
        """Create a simple LangChain chain with a prompt and LLM."""
        llm = ChatOpenAI(model_name=model_name)
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | llm
        return chain

    def run_chain_with_tracing(
        self,
        chain,
        inputs: Dict[str, Any],
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        trace_name: Optional[str] = None,
    ) -> Any:
        """
        Run a LangChain chain with Langfuse tracing and optional dynamic trace attributes.
        """
        handler = self.get_handler()
        metadata = {}
        if user_id:
            metadata["langfuse_user_id"] = user_id
        if session_id:
            metadata["langfuse_session_id"] = session_id
        if tags:
            metadata["langfuse_tags"] = tags
        config = {"callbacks": [handler]}
        if metadata:
            config["metadata"] = metadata
        if trace_name:
            config["run_name"] = trace_name
        response = chain.invoke(inputs, config=config)
        return response

    def score_trace(
        self, trace_id: str, name: str, value: float, comment: Optional[str] = None
    ):
        """
        Add a score to a trace (e.g., for user feedback or evaluation).
        """
        self.langfuse.create_score(
            trace_id=trace_id,
            name=name,
            value=value,
            data_type="NUMERIC",
            comment=comment,
        )

    def flush(self):
        """
        Flush all pending events to Langfuse (important for short-lived apps).
        """
        self.langfuse.flush()

    def shutdown(self):
        """
        Shutdown the Langfuse client (optional, for short-lived apps).
        """
        self.langfuse.shutdown()


# Example usage (remove or adapt for production):
if __name__ == "__main__":
    load_dotenv()
    manager = LangfuseManager()
    chain = manager.create_chain()
    response = manager.run_chain_with_tracing(
        chain,
        {"topic": "homies"},
        user_id="user-123",
        session_id="sess-456",
        tags=["demo"],
    )
    print(response.content)
    manager.flush()
