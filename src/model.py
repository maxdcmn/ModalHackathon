from openai import OpenAI
from typing import List, Dict, Any, Optional
import modal
from dataclasses import dataclass


@dataclass
class ModelResponse:
    """Simple class to mimic the structure expected by smolagents"""
    content: str


class VLLMModalModel:
    """
    A model class that connects to a vLLM model deployed on Modal.
    Compatible with smolagents library.
    """
    
    def __init__(
        self,
        base_url: str = "https://imjustmark--example-vllm-openai-compatible-serve.modal.run/v1",
        api_key: str = None,
        model_id: str = "neuralmagic/Meta-Llama-3.1-8B-Instruct-quantized.w4a16",
        **kwargs
    ):
        """
        Initialize the model with connection parameters.
        
        Args:
            base_url: The base URL of your Modal deployment
            api_key: The API key for authentication
            model_id: The model identifier to use
            **kwargs: Additional parameters to pass to the completion API
        """
        self.base_url = base_url
        self.api_key = api_key
        self.model_id = model_id
        self.default_params = kwargs
        
        # Initialize the OpenAI client
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def __call__(
        self, 
        messages: List[Dict[str, Any]], 
        stop_sequences: Optional[List[str]] = None,
        grammar: Optional[Any] = None,
        **kwargs
    ) -> ModelResponse:
        """
        Generate a response based on the input messages.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            stop_sequences: Optional list of strings that signal when to stop generating
            grammar: Optional grammar for constrained generation
            **kwargs: Additional parameters to override defaults
            
        Returns:
            ModelResponse object with a content attribute containing the generated text
        """
        # Combine default parameters with any overrides
        completion_args = {**self.default_params, **kwargs}
        
        # Add the model and messages
        completion_args["model"] = self.model_id
        completion_args["messages"] = messages
        
        # Add stop sequences if provided
        if stop_sequences:
            completion_args["stop"] = stop_sequences
            
        # Remove None values
        completion_args = {k: v for k, v in completion_args.items() if v is not None}
        
        # Make the API call
        response = self.client.chat.completions.create(**completion_args)
        
        # Return a ModelResponse object with the content attribute
        return ModelResponse(content=response.choices[0].message.content)