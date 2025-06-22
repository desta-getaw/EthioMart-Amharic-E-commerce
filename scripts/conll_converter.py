import re
from typing import List, Dict, Tuple

class CONLLConverter:
    def __init__(self):
        self.entity_types = {
            'PRODUCT': ['B-PRODUCT', 'I-PRODUCT'],
            'PRICE': ['B-PRICE', 'I-PRICE'],
            'LOC': ['B-LOC', 'I-LOC']
        }

    def preprocess_text(self, text: str) -> List[str]:
        """Split text into tokens while preserving special patterns."""
        tokens = []
        for word in text.split():
            price_match = re.match(r'(\d+)(ብር|br|birr)', word, re.IGNORECASE)
            if price_match:
                tokens.extend([price_match.group(1), price_match.group(2)])
            else:
                tokens.append(word)
        return tokens

    def label_entities(self, message: str) -> List[Tuple[str, str]]:
        """Label entities in a single message."""
        tokens = self.preprocess_text(message)
        labels = ['O'] * len(tokens)

        # Product labeling (by keyword match)
        for i, token in enumerate(tokens):
            if token in ['B-PRODUCT', 'I-PRODUCT']:
                labels[i] = token

        # Price labeling
        price_patterns = [
            (r'\bዋጋ[:-]?\s*(\d+)', 'B-PRICE'),
            (r'(\d+)\s*ብር', 'I-PRICE'),
            (r'\bprice[:-]?\s*(\d+)', 'B-PRICE')
        ]
        for i in range(len(tokens)):
            for pattern, label in price_patterns:
                if re.search(pattern, tokens[i], re.IGNORECASE):
                    labels[i] = label
                    if label == 'B-PRICE' and i + 1 < len(tokens) and tokens[i+1].isdigit():
                        labels[i+1] = 'I-PRICE'
                        if i + 2 < len(tokens) and tokens[i+2] in ['ብር', 'birr', 'br']:
                            labels[i+2] = 'I-PRICE'

        # Location labeling
        loc_keywords = ['I-LOC', 'ለቡ', 'መገናኛ', 'አድራሻ']
        for i, token in enumerate(tokens):
            if token in loc_keywords:
                labels[i] = 'I-LOC'
                if token == 'አድራሻ':
                    j = i + 1
                    while j < len(tokens) and j < i + 5:
                        if tokens[j] not in ['ቁ.', 'ቁጥር.', 'SL-05A']:
                            labels[j] = 'I-LOC'
                        j += 1

        return list(zip(tokens, labels))

    def convert_to_conll(self, messages: List[str]) -> str:
        """Convert list of messages to CONLL format."""
        conll_lines = []
        for message in messages:
            labeled_tokens = self.label_entities(message)
            for token, label in labeled_tokens:
                conll_lines.append(f"{token} {label}")
            conll_lines.append("")
        return "\n".join(conll_lines)

    def save_to_file(self, conll_data: str, filepath: str):
        """Save CONLL data to file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(conll_data)

def process_dataset(input_file: str, output_file: str):
    """Process dataset from input file to CONLL output."""
    converter = CONLLConverter()
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    messages = [msg.strip() for msg in content.split('\n\n') if msg.strip()]
    messages_to_process = messages[:50]
    conll_data = converter.convert_to_conll(messages_to_process)
    converter.save_to_file(conll_data, output_file)
    print(f"Successfully processed {len(messages_to_process)} messages to {output_file}")

if __name__ == "__main__":
    input_file = "labeled_telegram_product_price_location.txt"
    output_file = "labeled_data.conll"
    process_dataset(input_file, output_file)
