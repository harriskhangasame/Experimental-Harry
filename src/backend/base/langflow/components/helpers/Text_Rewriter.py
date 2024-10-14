from langflow.custom import Component
from langflow.io import MultilineInput, Output
from langflow.schema.message import Message
from openai import OpenAI
import os


class TextRewriterComponent(Component):
    display_name = "Text Rewriter"
    description = "Rewrites the given text."
    icon = "align-left"
    name = "TextRewriter"
    
    inputs = [
        MultilineInput(
            name="input_message",
            display_name="Input Message",
            info="Provide the text to rewrite."
        ),
    ]

    outputs = [
        Output(display_name="Rewritten Text", name="rewritten_text", method="build_output"),
    ]

    async def build_output(self) -> Message:
        """Takes input message and returns a rewritten version as a Message."""
        if not self.input_message:
            raise ValueError("Please, provide a message to rewrite.")
        
        # Call the OpenAI API to rewrite the text
        rewritten_text = await self.rewrite_text(self.input_message)
    
        return Message(text=rewritten_text)

    async def rewrite_text(self, text: str) -> str:
        """Uses OpenAI's API to rewrite the provided text."""
        try:
            client = OpenAI()
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Rewrite the following text:\n\n{text}"}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error rewriting text: {str(e)}"
