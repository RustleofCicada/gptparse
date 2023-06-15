import openai
import argparse
import gptparse

openai.api_key = YOUR_API_KEY
API_VERSION = 'gpt-3.5-turbo-0613'

available_people = ["Robert", "Mike", "Jane", "Kate", "Marry", "Elon"]

def greet(greeting: str = 'Hi', people: list[str] = available_people) -> None:
    for person in people:
        print(f'{greeting} {person}!')

greet_parser = argparse.ArgumentParser(
    prog = "greet",
    description="Greets a list of people individually")
greet_parser.add_argument("greeting", type=str, help="Greeting string")
greet_parser.add_argument("people", nargs="+", help="List of people", choices=available_people)

try:
    while True:
        user_input = input("Provide instruction for GPT: ")
        completition = openai.ChatCompletion.create(
            model = API_VERSION,
            messages = [{"role": "user", "content": user_input}],
            functions = gptparse.from_parsers([greet_parser]),
            function_call = "auto"
        )
        
        prog, kwargs = gptparse.get_arguments(completition)
        if prog == "greet": greet(**kwargs)
    
except KeyboardInterrupt:
    pass
