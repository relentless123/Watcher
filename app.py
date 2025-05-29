import re
import gradio as gr
import sys
import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime


from src.Agents.agents import qa_agent 
from browser_use import Browser, Agent as BrowserAgent
from src.Utilities.utils import controller 
from langchain_google_genai import ChatGoogleGenerativeAI



from src.Prompts.browser_prompts import (
    generate_browser_task
)

# Load environment variables
load_dotenv()

# Handle Windows asyncio policy
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Dictionary mapping framework names to their generation functions


async def moderate_content(input_url: str):
    print("!!!", os.environ.get("GOOGLE_API_KEY"))
    try:
        browser = Browser()
        async with await browser.new_context() as context:
            browser_agent = BrowserAgent(
                task=generate_browser_task(input_url),
                llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=os.environ.get("GOOGLE_API_KEY")),
                browser=browser,
                controller=controller)
            history = await browser_agent.run()
       
            return str(history.extracted_content()[-1])
    except Exception as e: 
        error_message = f"Error generating scenarios: {str(e)}"
        return error_message


def create_interface():
    # Custom CSS for scrollable textboxes
    custom_css = """
    .scrollable-textbox {
        max-height: 400px;
        overflow-y: auto;
    }
    .scrollable-textbox textarea {
        height: 400px !important;
    }
    .code-component {
        width: 100% !important;
        max-width: 100% !important;
    }
    .code-component textarea {
        width: 100% !important;
    }

    footer {visibility: hidden}
    """
    

    with gr.Blocks(title="Watcher", theme=gr.themes.Soft(), css=custom_css) as demo:
        gr.Markdown("# WATCHER")
        gr.Markdown("Agentic Content Moderator")
        
        with gr.Tab("Gherkin Generation"):
            with gr.Column():
                  
                url_input = gr.Textbox(
                    label="URL",
                    placeholder="Enter the URL to be moderated",
                    lines=5
                )
                
                execute_btn = gr.Button(value = "Start Moderation")
                

                output1 = gr.Code(
                    label="Problematic Content",
                    interactive=True,
                    language = 'markdown',
                    lines=5,
                    max_lines=10,
                )

        
        execute_btn.click (fn=moderate_content,
            inputs=[url_input],
            outputs=[output1])
        
    return demo

if __name__ == "__main__":
    demo = create_interface()
    #demo.launch()
    demo.launch(server_name="0.0.0.0")
