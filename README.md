# Hardware Sizing Calculator

Estimates the CPU, RAM, and disk space needed to run a given biometric
transaction load (verification / identification / enrollment), based on the
transaction rate and computational requirement.

## How to run

### Docker (recommended)

```bash
docker build -t hw-sizing-calc .
```

Non-interactive (arguments provided directly — no `-it` needed, works well
in scripts/CI):

```bash
docker run --rm hw-sizing-calc --tps 100 --type identification --requirement high
```

Interactive (prompts for the values):

```bash
docker run -it --rm hw-sizing-calc
```

### Locally (without Docker)

```bash
python -m src.main --tps 100 --type identification --requirement high
# or, interactively:
python -m src.main
```

### Tests

```bash
pip install pytest
python -m pytest tests/
```

## Inputs

| Flag            | Values                                        |
|-----------------|------------------------------------------------|
| `--tps`         | whole number > 0                               |
| `--type`        | `verification`, `identification`, `enrollment` |
| `--requirement` | `low`, `medium`, `high`                        |

If any flag is omitted, the missing value(s) are collected interactively.

## Design decisions

**"Number of transactions" → transactions per second.** The assignment asks
for the number of transactions, but hardware sizing is really about
sustained throughput, so the input is interpreted as a rate (TPS) rather
than a one-off count. This is what CPU/RAM actually scale with.

**Per-type resource profiles.** Each transaction type has its own
CPU/RAM/disk cost per transaction (`constants.py`), because a 1:N
identification is inherently more expensive than a 1:1 verification, and
enrollment writes more data than it computes. The concrete numbers are
estimates for the purpose of this exercise, not benchmarked values — in a
real deployment they'd come from profiling the actual biometric engine.

**Computational requirement as a multiplier.** `low/medium/high` scales the
per-transaction cost (0.7× / 1.0× / 1.5×) rather than being a separate
additive term, since it represents how demanding a single transaction is,
not extra load.

**Disk sizing assumes 30-day retention** of transaction data
(`RETENTION_DAYS`), applied as `tps × seconds/day × retention_days`. This
dominates the disk estimate and is the single biggest assumption in the
model — it's hardcoded and would need to be an input in a real tool.

**Safety margins and minimums.** All three outputs are inflated by a
margin (20-30%) and floored at a sane minimum (e.g. never recommend 0 CPU
cores), so the tool doesn't return technically-correct-but-useless numbers
at very low load.

**Both interactive and non-interactive modes.** A CLI tool that only reads
`input()` is awkward to deploy or automate — a container run without a TTY
just fails on EOF. Argument flags make the same binary usable as a
one-shot, scriptable command; interactive prompts remain as a convenience
fallback for missing values.