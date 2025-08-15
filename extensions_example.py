#!/usr/bin/env python3
"""
Example extensions for the Voice Assistant
These can be added to the main VoiceAssistant class during the workshop
"""

import random
import time
import math

class VoiceAssistantExtensions:
    """Example extensions that can be added to the main voice assistant"""
    
    def __init__(self):
        # Joke database
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it had too many problems!",
        ]
        
        # Fun facts database
        self.fun_facts = [
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
            "A group of flamingos is called a 'flamboyance'.",
            "Octopuses have three hearts and blue blood.",
            "Bananas are berries, but strawberries aren't.",
            "A day on Venus is longer than its year.",
        ]

    def tell_joke(self):
        """Tell a random joke"""
        joke = random.choice(self.jokes)
        return joke

    def tell_fun_fact(self):
        """Share a random fun fact"""
        fact = random.choice(self.fun_facts)
        return f"Here's a fun fact: {fact}"

    def simple_calculator(self, expression):
        """Perform simple calculations"""
        try:
            # Replace words with operators
            expression = expression.lower()
            expression = expression.replace("plus", "+")
            expression = expression.replace("add", "+")
            expression = expression.replace("minus", "-")
            expression = expression.replace("subtract", "-")
            expression = expression.replace("times", "*")
            expression = expression.replace("multiply", "*")
            expression = expression.replace("divided by", "/")
            expression = expression.replace("divide", "/")
            
            # Remove common words
            words_to_remove = ["what", "is", "equals", "calculate"]
            for word in words_to_remove:
                expression = expression.replace(word, "")
            
            # Clean up spaces
            expression = expression.strip()
            
            # Evaluate the expression (be careful with eval in real applications!)
            result = eval(expression)
            return f"The answer is {result}"
            
        except Exception as e:
            return "Sorry, I couldn't calculate that. Try saying something like 'what is 5 plus 3'"

    def set_timer(self, duration_text):
        """Set a simple timer"""
        try:
            # Extract number from text
            words = duration_text.split()
            duration = None
            
            for word in words:
                if word.isdigit():
                    duration = int(word)
                    break
            
            if duration is None:
                return "Please specify how many seconds for the timer"
            
            if duration > 300:  # Limit to 5 minutes for workshop
                return "Timer limit is 5 minutes for this demo"
            
            # This would block in real implementation - just return message
            return f"Timer set for {duration} seconds. (In a real implementation, this would count down)"
            
        except Exception as e:
            return "Sorry, I couldn't set the timer. Try saying 'set timer for 30 seconds'"

    def flip_coin(self):
        """Flip a virtual coin"""
        result = random.choice(["Heads", "Tails"])
        return f"The coin landed on {result}!"

    def roll_dice(self, sides=6):
        """Roll a virtual dice"""
        result = random.randint(1, sides)
        return f"You rolled a {result}!"

    def generate_password(self, length=8):
        """Generate a simple password"""
        import string
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for _ in range(length))
        return f"Here's a random password: {password}"

# Example of how to integrate these into the main assistant:

def add_extensions_to_assistant():
    """
    Example code showing how to add these extensions to the main VoiceAssistant class
    This would be added to the process_command method
    """
    
    example_code = '''
    # Add this to your VoiceAssistant.__init__ method:
    self.extensions = VoiceAssistantExtensions()
    
    # Add these elif statements to your process_command method:
    
    elif "joke" in command:
        response = self.extensions.tell_joke()
        self.speak(response)
    
    elif "fun fact" in command or "fact" in command:
        response = self.extensions.tell_fun_fact()
        self.speak(response)
    
    elif "calculate" in command or "what is" in command:
        response = self.extensions.simple_calculator(command)
        self.speak(response)
    
    elif "timer" in command:
        response = self.extensions.set_timer(command)
        self.speak(response)
    
    elif "flip coin" in command or "coin flip" in command:
        response = self.extensions.flip_coin()
        self.speak(response)
    
    elif "roll dice" in command or "dice" in command:
        response = self.extensions.roll_dice()
        self.speak(response)
    
    elif "password" in command:
        response = self.extensions.generate_password()
        self.speak(response)
    '''
    
    return example_code

if __name__ == "__main__":
    # Test the extensions
    ext = VoiceAssistantExtensions()
    
    print("Testing Voice Assistant Extensions:")
    print("-" * 40)
    print("Joke:", ext.tell_joke())
    print("Fun Fact:", ext.tell_fun_fact())
    print("Calculator:", ext.simple_calculator("what is 15 plus 27"))
    print("Coin Flip:", ext.flip_coin())
    print("Dice Roll:", ext.roll_dice())
    print("Password:", ext.generate_password())
    print("-" * 40)
    print("Extensions ready to integrate!")