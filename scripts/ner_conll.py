import re
from typing import List, Tuple, Optional
import pandas as pd
from pathlib import Path

class CoNLLAnnotator:
    """
    A class to annotate messages in CoNLL format for NER tasks.
    Handles product, price, and location entities in Amharic text.
    """
    
    def __init__(self):
        # Compile regex patterns for entity recognition
        self._compile_patterns()
        
    def _compile_patterns(self):
        """Compile all regex patterns used for entity recognition"""
        # Price patterns (Amharic and English variations)
        self.price_pattern = re.compile(
            r'(ዋጋ፦?|በ|ከ|💰|🏷|💲|💵|price)[\s:]*([\d,]+)\s*(ብር|br|birr)?',
            re.IGNORECASE
        )
        
        # Location patterns (address-related terms)
        self.location_pattern = re.compile(
            r'(አድራሻ|📍|🏢|ቢሮ|ፎቅ|ሁለተኛ|ደፋር|ሞል|መገናኛ|መሰረት|address|location|floor)',
            re.IGNORECASE
        )
        
        # Product indicators
        self.product_indicator = re.compile(
            r'📌|🎯|product|item|👍'
        )
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words while preserving Amharic punctuation.
        """
        tokens = re.findall(r'[\w]+|[\w]+[^\w\s]|[\w]+[^\w\s]?', text)
        return tokens
    
    def _detect_price(self, tokens: List[str], index: int) -> Optional[Tuple[int, int]]:
        """
        Detect price entities starting at the given index.
        """
        window = ' '.join(tokens[index:index+4])
        match = self.price_pattern.search(window)
        
        if match:
            matched_text = match.group()
            matched_tokens = self.tokenize(matched_text)
            end_pos = index + len(matched_tokens)
            return (index, end_pos)
        return None
    
    def _detect_location(self, token: str) -> bool:
        """Check if token indicates a location"""
        return bool(self.location_pattern.search(token))
    
    def _detect_product(self, tokens: List[str], index: int) -> bool:
        """Check if token is part of a product name"""
        if index > 0 and self.product_indicator.search(tokens[index-1]):
            return True
        
        if len(tokens[index]) > 3 and not any(c.isdigit() for c in tokens[index]):
            if index > 0 and any(l in ['B-PRODUCT', 'I-PRODUCT'] for _, l in self.annotations[:index]):
                return True
        return False
    
    def annotate(self, text: str) -> List[Tuple[str, str]]:
        """
        Annotate text with named entities.
        """
        self.annotations = []
        tokens = self.tokenize(text)
        i = 0
        n = len(tokens)
        
        while i < n:
            current_label = 'O'
            
            price_span = self._detect_price(tokens, i)
            if price_span:
                start, end = price_span
                self.annotations.append((tokens[i], 'B-PRICE'))
                i += 1
                
                while i < end and i < n:
                    self.annotations.append((tokens[i], 'I-PRICE'))
                    i += 1
                continue
                
            if self._detect_location(tokens[i]):
                current_label = 'B-LOC' if tokens[i] in ['አድራሻ', '📍', '🏢'] else 'I-LOC'
                
            elif self._detect_product(tokens, i):
                if i > 0 and self.annotations[i-1][1] in ['B-PRODUCT', 'I-PRODUCT']:
                    current_label = 'I-PRODUCT'
                else:
                    current_label = 'B-PRODUCT'
            
            self.annotations.append((tokens[i], current_label))
            i += 1
            
        return self.annotations
    
    def to_conll(self, annotated_tokens: List[Tuple[str, str]]) -> str:
        """
        Convert annotated tokens to CoNLL format string.
        """
        return '\n'.join([f'{token}\t{label}' for token, label in annotated_tokens])


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load dataset from CSV file with proper path handling.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found at: {path.absolute()}")
    return pd.read_csv(path)


def save_annotations(annotations: List[str], output_path: str):
    """
    Save annotations to file in CoNLL format.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(annotations))