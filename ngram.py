import random
import re
from collections import defaultdict

class NgramModel:
    def __init__(self, n=5):
        self.max_n = n
        self.models = {}
        for i in range(1, self.max_n + 1):
            self.models[i] = defaultdict(list)

    def train(self, text):
        tokens = re.findall(r"[\w']+|[.,!?;]", text)
        
        for n in range(1, self.max_n + 1):
            for i in range(len(tokens) - n + 1):
                context = tuple(tokens[i : i + n - 1])
                next_word = tokens[i + n - 1]
                self.models[n][context].append(next_word)

    def predict_next(self, current_history):
        for n in range(self.max_n, 0, -1):
            required_context_len = n - 1
            
            if len(current_history) < required_context_len:
                continue
                
            if required_context_len == 0:
                context = () 
            else:
                context = tuple(current_history[-required_context_len:])
            
            possible_words = self.models[n].get(context)
            
            if possible_words: 
                return random.choice(possible_words)
 
        return "."

    def generate(self, seed_text, length=30):
        tokens = re.findall(r"[\w']+|[.,!?;]", seed_text)
        output = list(tokens)
        
        for _ in range(length):
            next_word = self.predict_next(output)
            output.append(next_word)
            
        return " ".join(output).replace(" .", ".").replace(" ,", ",")


corpus_text = open("sherlockholmes.txt",encoding="utf-8").read()
model = NgramModel(n=5)
model.train(corpus_text)

print("Input: The day was very crazy")
print(f"Output: {model.generate("The day was very crazy")}")


print("\nInput: she has turned all the")
print(f"Output: {model.generate("she has turned all the")}")

print("\nInput: We had reached Baker Street")
print(f"Output: {model.generate("We had reached Baker Street")}")