from typing import Any, Callable

class state():
    
    def __init__(self, variable: Any) -> None:
        self.hook_list = []
        self.variable = variable
    
    def change(self, variable) -> None:
        self.variable = variable
        for function in self.hook_list:
            function(self.variable)
    
    def hook(self, function: Callable) -> None:
        function(self.variable)
        self.hook_list.append(function)