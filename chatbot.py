from typing import List, Dict, Optional
from dataclasses import dataclass, field
import json
import openai
from .retriever import RAGRetriever, RetrievedContext

@dataclass
class Message:
    """Enhanced message class with metadata."""
    role: str
    content: str
    metadata: Dict = field(default_factory=dict)

class Conversation:
    """Enhanced conversation manager with context tracking."""
    def __init__(self, max_history: int = 10):
        self.messages: List[Message] = []
        self.max_history = max_history
        self.context_history: List[Dict] = []  # Track retrieved contexts

    def add_message(self, role: str, content: str, metadata: Dict = None):
        """Add message with metadata and maintain history limit."""
        self.messages.append(Message(role=role, content=content, metadata=metadata or {}))
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]

    def add_context(self, contexts: List[RetrievedContext]):
        """Track retrieved contexts for conversation."""
        context_info = {
            'turn': len(self.messages),
            'contexts': [
                {
                    'content': ctx.content,
                    'metadata': ctx.metadata,
                    'score': ctx.relevance_score,
                    'type': ctx.source_type
                }
                for ctx in contexts
            ]
        }
        self.context_history.append(context_info)

    def get_recent_contexts(self, turns: int = 2) -> List[Dict]:
        """Get contexts from recent conversation turns."""
        return self.context_history[-turns:]

class CPChatbot:
    def __init__(
        self,
        retriever: RAGRetriever,
        system_message: str,
        openai_api_key: str,
        model: str = "gpt-4",
        max_context_length: int = 2000,
        temperature: float = 0.7
    ):
        """Initialize enhanced chatbot with LLM integration."""
        self.retriever = retriever
        self.system_message = system_message
        self.conversation = Conversation()
        self.max_context_length = max_context_length
        
        # LLM configuration
        openai.api_key = openai_api_key
        self.model = model
        self.temperature = temperature
        
        # Add system message
        self.conversation.add_message("system", system_message)

    def _format_prompt(self, query: str, contexts: List[RetrievedContext]) -> str:
        """Format sophisticated prompt with context integration."""
        # Get recent contexts
        recent_contexts = self.conversation.get_recent_contexts()
        
        # Format current contexts
        current_contexts = "\n\n".join([
            f"[Context {i+1}] ({ctx.source_type}, confidence: {ctx.confidence:.2f})\n"
            f"Problem: {ctx.metadata.get('problem_id', 'N/A')}\n"
            f"Difficulty: {ctx.metadata.get('difficulty', 'N/A')}\n"
            f"Tags: {', '.join(ctx.metadata.get('tags', []))}\n"
            f"Content: {ctx.content}"
            for i, ctx in enumerate(contexts)
        ])
        
        # Format conversation history
        history = "\n".join([
            f"{msg.role}: {msg.content}"
            for msg in self.conversation.messages[1:]  # Skip system message
        ])
        
        # Create comprehensive prompt
        prompt = (
            f"Previous Conversation:\n{history}\n\n"
            f"Retrieved Contexts:\n{current_contexts}\n\n"
            f"Current Query: {query}\n\n"
            "Instructions:\n"
            "1. Analyze the problem and contexts thoroughly\n"
            "2. Provide a clear, structured explanation\n"
            "3. Focus on problem-solving approach and concepts\n"
            "4. Reference specific parts of the editorial when relevant\n"
            "5. If code examples are needed, provide high-level pseudocode only\n"
            "6. Acknowledge any ambiguities or alternative approaches\n"
        )
        
        return prompt

    def _generate_response(self, prompt: str) -> str:
        """Generate response using OpenAI's GPT model."""
        messages = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": prompt}
        ]
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=1000,
            n=1,
            stop=None
        )
        
        return response.choices[0].message.content

    def chat(self, query: str) -> str:
        """Process query and generate detailed response."""
        # Add user message
        self.conversation.add_message("user", query)
        
        # Retrieve relevant contexts
        contexts = self.retriever.retrieve(query)
        self.conversation.add_context(contexts)
        
        # Format prompt
        prompt = self._format_prompt(query, contexts)
        
        # Generate response
        response = self._generate_response(prompt)
        
        # Add assistant response
        self.conversation.add_message(
            "assistant",
            response,
            metadata={"contexts_used": len(contexts)}
        )
        
        return response

    def get_conversation_history(self) -> List[Dict]:
        """Get detailed conversation history with metadata."""
        return [
            {
                "role": msg.role,
                "content": msg.content,
                "metadata": msg.metadata,
                "turn": i
            }
            for i, msg in enumerate(self.conversation.messages)
        ]

    def save_state(self, path: str):
        """Save complete conversation state."""
        state = {
            "messages": self.get_conversation_history(),
            "context_history": self.conversation.context_history
        }
        
        with open(path, 'w') as f:
            json.dump(state, f, indent=2)

    def load_state(self, path: str):
        """Load complete conversation state."""
        with open(path, 'r') as f:
            state = json.load(f)
            
        # Reset conversation
        self.conversation = Conversation()
        
        # Restore messages
        for msg in state["messages"]:
            self.conversation.add_message(
                msg["role"],
                msg["content"],
                msg.get("metadata", {})
            )
            
        # Restore context history
        self.conversation.context_history = state["context_history"]

    def generate_code_solution(self, problem_id: str) -> str:
        """Generate pseudocode solution for a problem."""
        # Retrieve problem and editorial contexts
        contexts = self.retriever.retrieve(f"problem {problem_id} solution", k=2)
        
        # Format specialized prompt for code generation
        prompt = (
            f"Generate a pseudocode solution for problem {problem_id}.\n\n"
            "Problem context:\n"
            f"{contexts[0].content if contexts else 'Not found'}\n\n"
            "Editorial approach:\n"
            f"{contexts[1].content if len(contexts) > 1 else 'Not found'}\n\n"
            "Instructions:\n"
            "1. Provide a high-level pseudocode solution\n"
            "2. Include time and space complexity analysis\n"
            "3. Explain key algorithms and data structures used\n"
            "4. Note any important edge cases\n"
        )
        
        return self._generate_response(prompt)
