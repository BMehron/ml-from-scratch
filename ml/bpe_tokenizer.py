from collections import defaultdict
from typing import List
import heapq

class ByteLevelBPETokenizer:
    def __init__(self, train_texts: List[str], max_vocab_size=1000):
        self.vocab = list(range(256)) # Base vocab consists from bytes.
        self.rules = []
        self.max_vocab_size = max_vocab_size
    
        self.__build_vocab__(train_texts)

    def __build_vocab__(self, train_texts: str | List[str]):
        # 1. Convert string texts into sequences of bytes.
        if isinstance(train_texts, str):
            train_texts = [train_texts]

        train_texts = [list(map(str, list(text.encode("utf-8")))) for text in train_texts] # Encode texts into sequnce of bytes. O(|train_texts|)
        freq_counter = defaultdict(int) # pair : (frequency, list[indexis where they occur])

        # 2. Create a sparse counter dict for each pair of consecutive tokens and list of indexes where they occur.
        for i, text in enumerate(train_texts): 
            for j in range(1, len(text)):   # Overall O(|train_texts|)
                pair = (text[j-1], text[j])
                freq_counter[pair] += 1
        
        # 3. Create a heap from this frequencies.
        heap = [(-freq_counter[pair], pair) for pair in freq_counter]
        heapq.heapify(heap)

        # 4. While size of vocab is less than max_vocab_size:
        while heap and len(self.vocab) < self.max_vocab_size:
            # 5. Take the most frequent pair. Put it in the rules.
            freq, merge_pair = heapq.heappop(heap)
            merged_token = merge_pair[0] + "+" + merge_pair[1]
            if merge_pair not in freq_counter or freq_counter[merge_pair] != -freq:
                continue # This pair is from earlier stages
            
            self.vocab.append(merged_token)
            self.rules.append(merge_pair)
            # 6. Merge them in all texts. Update counters in their neighbouhoods and the heap.
            for text in train_texts:
                i = 0
                while i < len(text) - 1:
                    if (text[i], text[i+1]) == merge_pair:
                        text[i:i+2] = [merged_token]
                        if i > 0:
                            prev_token = text[i-1]

                            freq_counter[(prev_token, merge_pair[0])] -= 1
                            if freq_counter[(prev_token, merge_pair[0])] == 0:
                                del freq_counter[(prev_token, merge_pair[0])]
                            else:
                                heapq.heappush(heap, (-freq_counter[(prev_token, merge_pair[0])], (prev_token, merge_pair[0])))

                            freq_counter[(prev_token, merged_token)] += 1
                            heapq.heappush(heap, (-freq_counter[(prev_token, merged_token)], (prev_token, merged_token)))

                        if i + 1 < len(text):
                            next_token = text[i+1]

                            freq_counter[(merge_pair[1], next_token)] -= 1
                            if freq_counter[(merge_pair[1], next_token)] == 0:
                                del freq_counter[(merge_pair[1], next_token)]
                            else:
                                heapq.heappush(heap, (-freq_counter[(merge_pair[1], next_token)], (merge_pair[1], next_token)))

                            freq_counter[(merged_token, next_token)] += 1
                            heapq.heappush(heap, (-freq_counter[(merged_token, next_token)], (merged_token, next_token)))
                    else:
                        i += 1

            del freq_counter[merge_pair]

        if not heap:
            print("We can't merge further!")

    
    def encode(self, encode_texts: str | List[str]):
        if isinstance(encode_texts, str):
            encode_texts = [encode_texts]

        encode_texts = [list(map(str, list(text.encode("utf-8")))) for text in encode_texts]
        print(encode_texts)
        for merge_pair in self.rules:
            merged_token = merge_pair[0] + '+' + merge_pair[1]
            for text in encode_texts:
                i = 0
                while i < len(text)-1:
                    if (text[i], text[i+1]) == merge_pair:
                        text[i:i+2] = [merged_token]
                    else:
                        i += 1
    
        encoded_texts = [
            [bytes(map(int, token.split("+"))) for token in text]
            for text in encode_texts
        ]
        return encoded_texts


import random

# from ml.bpe_tokenizer import ByteLevelBPETokenizer


def decode_batch(encoded_texts):
    """Decode encoded_texts returned by encode() by joining bytes tokens."""
    return [b"".join(tokens).decode("utf-8") for tokens in encoded_texts]


def assert_rules_consistent(tok):
    """Rules are pairs of strings; merged token string should exist in vocab for each rule."""
    merged = {a + "+" + b for (a, b) in tok.rules}
    vocab_str = {v for v in tok.vocab if isinstance(v, str)}
    assert merged.issubset(vocab_str)

# Add these tests below your class (same file) or in a separate test file.
# Run: python -m pytest -q ml/bpe_tokenizer.py

def test_overlap_repeated_single_char_ascii_roundtrip():
    # Overlap-heavy: "aaaaaa" has many overlapping ("a","a") pairs.
    texts = ["a" * 200, "a" * 199, "a" * 50]
    tok = ByteLevelBPETokenizer(texts, max_vocab_size=400)

    enc = tok.encode(texts)
    assert decode_batch(enc) == texts


def test_alternating_pattern_overlap_roundtrip():
    # Overlap-heavy alternating pattern: many "ab" pairs with overlaps.
    texts = [("ab" * 150), ("ba" * 150), ("abababa" * 40)]
    tok = ByteLevelBPETokenizer(texts, max_vocab_size=450)

    enc = tok.encode(texts)
    assert decode_batch(enc) == texts


def test_mixed_overlap_with_spaces_and_punct_roundtrip():
    # Stress boundaries and repeated short patterns + punctuation.
    base = ("hello, hello! hello? " * 120).strip()
    texts = [base, base.replace(" ", "  "), base.replace("hello", "hellO")]
    tok = ByteLevelBPETokenizer(texts, max_vocab_size=600)

    enc = tok.encode(texts)
    assert decode_batch(enc) == texts


def test_unicode_overlap_roundtrip():
    # Unicode where UTF-8 uses multiple bytes; repeats create overlaps at byte level too.
    texts = [
        ("café " * 200).strip(),
        ("naïve " * 150).strip(),
        ("你好你好你好" * 80),
        ("🚀🚀🚀" * 100),
    ]
    tok = ByteLevelBPETokenizer(texts, max_vocab_size=700)

    enc = tok.encode(texts)
    assert decode_batch(enc) == texts


def test_train_does_not_crash_from_stale_heap_entries():
    # This test is specifically aimed at catching KeyError from stale heap entries.
    # It doesn't assert exact merges, just that training completes and encoding works.
    texts = [
        "a" * 300,
        "ab" * 200,
        "abc" * 150,
        ("the quick brown fox jumps over the lazy dog. " * 50).strip(),
    ]
    tok = ByteLevelBPETokenizer(texts, max_vocab_size=800)
    enc = tok.encode(texts)
    assert decode_batch(enc) == texts


def test_vocab_and_rules_invariants_hold():
    texts = ["abababab" * 50, "aaaaaa" * 50, "xyzxyzxyz" * 50]
    tok = ByteLevelBPETokenizer(texts, max_vocab_size=500)

    # Invariant: base vocab (256 ints) + one vocab entry per rule
    assert len(tok.vocab) == 256 + len(tok.rules)
    assert len(tok.vocab) <= 500

    # Each rule should have corresponding merged token in vocab (as a string)
    merged_tokens = {a + "+" + b for (a, b) in tok.rules}
    vocab_strings = {v for v in tok.vocab if isinstance(v, str)}
    assert merged_tokens.issubset(vocab_strings)



def test_medium_diverse_corpus_roundtrip_and_some_merges():
    texts = [
        "Deep learning models learn representations from data.",
        "Byte-level BPE tokenizes a stream of bytes, not words.",
        "Numbers: 1234567890, punctuation: !?.,;:-_()[]{}",
        "Newlines\nand\ttabs\tare bytes too.",
        "Repeated repeated repeated repeated repeated words words words.",
        "café naïve façade coöperate",
        "こんにちは世界",
        "你好，世界",
        "Привет мир",
        "🚀✨🔥💡 — emojis and symbols",
        "mix: English 中文 café 🚀 end",
        "James Bond is from England."
    ] * 50  # scale up

    tok = ByteLevelBPETokenizer(texts, max_vocab_size=500)

    # Should typically reach max vocab size
    assert len(tok.vocab) == 500
    assert len(tok.rules) == 500 - 256
    assert_rules_consistent(tok)

    encoded = tok.encode(texts)
    assert decode_batch(encoded) == texts


def test_unicode_heavy_corpus_roundtrip():
    texts = [
        "café naïve façade coöperate",
        "こんにちは世界",
        "你好，世界",
        "Привет мир",
        "🚀✨🔥💡 — emojis and symbols",
        "mix: English 中文 café 🚀 end",
    ] * 200

    tok = ByteLevelBPETokenizer(texts, max_vocab_size=700)

    encoded = tok.encode(texts)
    assert decode_batch(encoded) == texts


def test_multiple_sources_list_of_docs_no_cross_doc_required():
    # Emulates “multiple sources”: each string is a separate stream.
    docs = []
    for i in range(200):
        docs.append(f"doc{i}: alpha beta gamma delta. " * 5)
        docs.append(f"doc{i}: ALPHA BETA GAMMA DELTA. " * 5)
        docs.append(f"doc{i}: αβγδ — unicode greek. " * 2)

    tok = ByteLevelBPETokenizer(docs, max_vocab_size=650)
    encoded = tok.encode(docs)
    assert decode_batch(encoded) == docs


def test_random_synthetic_corpus_stability_roundtrip():
    # Random-but-deterministic text to stress edge cases
    rng = random.Random(0)

    alphabet = list("abcdefghijklmnopqrstuvwxyz     .,!?;:-\n\t")
    docs = []
    for _ in range(500):
        n = rng.randint(20, 120)
        s = "".join(rng.choice(alphabet) for _ in range(n))
        # Add a few unicode symbols sometimes
        if rng.random() < 0.2:
            s += rng.choice([" café", " 你好", " 🚀", " naïve"])
        docs.append(s)

    tok = ByteLevelBPETokenizer(docs, max_vocab_size=700)

    encoded = tok.encode(docs)
    assert decode_batch(encoded) == docs


def test_vocab_size_may_stop_early_if_heap_exhausts():
    # If all docs are length 0 or 1 byte, there are no pairs -> heap empty -> no merges.
    docs = ["", "a", "🚀"]  # "🚀" is 4 bytes but single doc still has pairs; include empties
    tok = ByteLevelBPETokenizer(["", ""], max_vocab_size=300)
    assert tok.rules == []
    assert len(tok.vocab) == 256


def test_encoded_tokens_are_bytes_and_not_empty_for_nonempty_text():
    docs = ["hello world"] * 100
    tok = ByteLevelBPETokenizer(docs, max_vocab_size=400)
    enc = tok.encode(["hello world", "HELLO WORLD"])
    assert all(isinstance(t, bytes) for t in enc[0])
    assert len(enc[0]) > 0
    assert len(enc[1]) > 0



## RUN this command from the terminal: pytest ml/bpe_tokenizer.py

if __name__ == "__main__":
    train_corpus = [
        "Deep learning models learn representations from data.",
        "Byte-level BPE tokenizes a stream of bytes, not words.",
        "Numbers: 1234567890, punctuation: !?.,;:-_()[]{}",
        "Newlines\nand\ttabs\tare bytes too.",
        "Repeated repeated repeated repeated repeated words words words.",
        "café naïve façade coöperate",
        "こんにちは世界",
        "你好，世界",
        "Привет мир",
        "🚀✨🔥💡 — emojis and symbols",
        "mix: English 中文 café 🚀 end",
        "James Bond is from England.",
        "The weather very cold today, isn't it?",
        "There are trillions of starts in the universe.",
        "The",
        "low",
        "lower"
        ""
    ]

    tokenizer = ByteLevelBPETokenizer(train_corpus, max_vocab_size=500)
    print(tokenizer.vocab, tokenizer.rules)
    sentence = "Thé lower the temperature, the colder the weather."
    print(tokenizer.encode([sentence]))

