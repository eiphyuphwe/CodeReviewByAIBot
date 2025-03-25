# Apache License
# Version 2.0, January 2004
# Author: Eugene Tkachenko

from abc import ABC, abstractmethod
from ai.line_comment import LineComment

class AiBot(ABC):
    
    __no_response = "No critical issues found"
    __problems="errors, issues, memory leaks, possible crashes or unhandled exceptions,kotlin syntax issues"
    __chat_gpt_ask_long="""
We have an Android Jetpack project that follows the latest Google recommendations.
The code should use coroutines and must be thread safe. It should not have ANR as well.Follow idiomatic Kotlin syntax and best practices.

Could you describe briefly {problems} for the next code with given code?
Please, also, do not add intro words, just print errors in the format: "line_number : cause effect"
Line numbers should depend only on the code, not on the diffs.
If there are no {problems} just say "{no_response}".

- If you see **any optimization suggestions**, clearly write:
     `"Optimization Suggestion (line X):"`
     Follow with a short description and an optimized version of the code.
- If a **variable or function name is not meaningful**, mention:
     `"Naming Suggestion (line X): 'foo' is unclear → rename to 'userList'"`
- For **null safety problems**, write:
     `"Null Safety Issue (line X): risk of null pointer → use '?.' or '?:' or 'requireNotNull'"`
     Also include the improved code.
- For **Kotlin syntax improvements**, use:
     `"Kotlin Syntax Improvement (line X):"`
     Explain the reason and provide the improved code.
If there are no {problems} just say "{no_response}".

Code Language: Kotlin/Java
Android API Level / Jetpack Version: Latest
Architectural Pattern: MVVM

Full code of the file:

{code}

GIT DIFFS:

{diffs}
"""

    @abstractmethod
    def ai_request_diffs(self, code, diffs) -> str:
        pass

    @staticmethod
    def build_ask_text(code, diffs) -> str:
        return AiBot.__chat_gpt_ask_long.format(
            problems = AiBot.__problems,
            no_response = AiBot.__no_response,
            diffs = diffs,
            code = code,
        )

    @staticmethod
    def is_no_issues_text(source: str) -> bool:
        target = AiBot.__no_response.replace(" ", "")
        source_no_spaces = source.replace(" ", "")
        return source_no_spaces.startswith(target)
    
    @staticmethod
    def split_ai_response(input) -> list[LineComment]:
        if input is None or not input:
            return []
        
        lines = input.strip().split("\n")
        models = []

        for full_text in lines:
            number_str = ''
            number = 0
            full_text = full_text.strip()
            if len( full_text ) == 0:
                continue

            reading_number = True
            for char in full_text.strip():
                if reading_number:
                    if char.isdigit():
                        number_str += char
                    else:
                        break

            if number_str:
                number = int(number_str)

            models.append(LineComment(line = number, text = full_text))
        return models
    