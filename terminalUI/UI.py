from rich import print
from rich.console import Console
class UI: 
    def __init__(self):
        self.console = Console()
        self.user_text_style = "bold magenta"
        self.assistant_text_style = "bold green"
        self.tool_call_style = "red"
        self.tool_response_style = "blue"

    def _get_user_input(self): 
        # self.console.print("[YOU]", text, style=self.user_text_style)
        return self.console.input("[bold purple][YOU][/] ")

    def _print_assistant_text(self,text):
        self.console.print("[ASSISTANT]", text, style=self.assistant_text_style)

    def _print_tool_call(self, tool_name, params): 
        self.console.print(f"[USING {tool_name}]", params , style=self.tool_call_style)

    def _print_tool_reponse(self, tool_name, response):
        self.console.print(f"[DONE {tool_name}]", response, style=self.tool_response_style)
