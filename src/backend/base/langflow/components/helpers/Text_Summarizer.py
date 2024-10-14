from langflow.custom import Component
from langflow.io import MultilineInput, Output
from langflow.schema.message import Message
from openai import OpenAI
import os


class TextSummarizerComponent(Component):
    display_name = "Text Summarizer"
    description = "Summarizes the given text."
    icon = "align-left"
    name = "TextSummarizer"
    
    inputs = [
        MultilineInput(
            name="input_message",
            display_name="Extracted Message",
            info="Provide the extracted message to summarize."
        ),
    ]

    outputs = [
        Output(display_name="Summarized Text", name="summarized_text", method="build_output"),
    ]

    async def build_output(self) -> Message:
        """Takes input message and returns a summarized version as a Message."""
        if not self.input_message:
            raise ValueError("Please, provide a message to summarize.")
        
        # Call the OpenAI API to summarize the text
        summarized_text = await self.summarize_text(self.input_message)
    
        return Message(text=summarized_text)

    async def summarize_text(self, text) -> str:
        """Uses OpenAI's API to summarize the provided text."""
        try:
            client = OpenAI()
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error summarizing text: {str(e)}"
