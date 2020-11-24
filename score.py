#!/usr/bin/env python
"""Computes WER on a fairseq prediction file."""

import argparse

from typing import Iterable, List, Optional, Tuple


# fairseq-generate parsing.


LOG_STATEMENT = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} | INFO"


Sequence = List[str]


def _output(path: str) -> Iterable[Tuple[Sequence, Sequence, Sequence, float]]:
    """Generates source, target, hypothesis, and posterior score tuples."""
    # This is sort of overkill but I already had it lying around.
    with open(path, "r") as generate:
        while True:
            try:
                line = next(generate)
            except StopIteration:
                return
            if line.startswith("Generate"):
                return
            # The format is:
            # S: "source"
            # T: "target"
            # H: score <tab> "hypothesis"
            # D: score <tab> "detokenized hypothesis"
            # P: positional scores per token.
            # We extract S, T, H, and H's score.
            assert line.startswith("S-"), line
            (_, source_str) = line.split("\t", 1)
            source = source_str.split()
            line = next(generate)
            assert line.startswith("T-"), line
            (_, target_str) = line.split("\t", 1)
            target = target_str.split()
            line = next(generate)
            assert line.startswith("H-"), line
            (_, score_str, hypothesis_str) = line.split("\t", 2)
            score = float(score_str)
            hypothesis = hypothesis_str.split()
            # TODO: I think there can be multiple hypotheses per S/T pair, but
            # this is not yet supported.
            yield (source, target, hypothesis, score)
            # Skips over the next two.
            line = next(generate)
            line = next(generate)


def main(args: argparse.Namespace) -> None:
    correct = 0
    incorrect = 0
    for (_, target, hypothesis, _) in _output(args.src):
        if target == hypothesis:    
            correct += 1
        else:
            incorrect += 1
    WER = incorrect / (correct + incorrect)
    print(f"WER:\t{WER * 100:.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("src", help="source file path")
    main(parser.parse_args())
    main
