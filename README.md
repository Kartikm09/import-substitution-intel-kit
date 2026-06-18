# Import Substitution Intel Kit

Research toolkit for ranking import-substitution and local-manufacturing opportunities.

The idea comes from tracking products imported from China and asking: which ones could be manufactured or assembled in India with realistic capability, demand, and margin?

This repo uses public-safe CSV inputs. It does not claim live trade accuracy; it demonstrates the scoring model and research workflow.

## Quick Start

```bash
PYTHONPATH=src python3 -m import_intel.cli rank examples/import_candidates.csv
```

JSON output:

```bash
PYTHONPATH=src python3 -m import_intel.cli rank examples/import_candidates.csv --format json
```

Run tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Output

- ranked product opportunities
- substitution readiness score
- capability and complexity notes
- suggested next research actions
- caution flags for regulation, tooling, or capital intensity

## Portfolio Signal

This repo supports:

- business intelligence automation
- India manufacturing research
- import-substitution analysis
- strategic sourcing
- data scoring pipelines
- Python CLI tooling

