#!/usr/bin/env python3
"""
Principia Metaphysica - Structured Simulation Runner
=====================================================

Reads simulation_structure.json and executes simulations in order,
chaining outputs from one phase to inputs of the next.

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import json
import importlib.util
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

STRUCTURE_FILE = "simulation_structure.json"
OUTPUT_FILE = "theory_output.json"


class SimulationContext:
    """Maintains state across simulation phases."""

    def __init__(self):
        self.params: Dict[str, Any] = {}
        self.results: Dict[str, Any] = {}
        self.phase_outputs: Dict[str, List[str]] = {}

    def get_param(self, path: str) -> Optional[Any]:
        """Get a parameter by dotted path (e.g., 'topology.B3')."""
        parts = path.split('.')
        current = self.params
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current

    def set_param(self, path: str, value: Any):
        """Set a parameter by dotted path."""
        parts = path.split('.')
        current = self.params
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value

    def validate_inputs(self, sim_inputs: List[str]) -> tuple[bool, List[str]]:
        """Check if all required inputs are available."""
        missing = []
        for input_path in sim_inputs:
            if self.get_param(input_path) is None:
                missing.append(input_path)
        return len(missing) == 0, missing


def load_structure() -> Dict:
    """Load simulation structure from JSON."""
    with open(STRUCTURE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_simulation_module(file_path: str):
    """Dynamically load a simulation module."""
    path = Path(file_path)
    if not path.exists():
        return None

    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        return None

    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    return module


def run_phase(phase: Dict, context: SimulationContext) -> bool:
    """Execute all simulations in a phase."""
    phase_name = phase['name']
    print(f"\n{'=' * 70}")
    print(f" {phase_name}")
    print(f"{'=' * 70}")

    for sim in phase['simulations']:
        sim_name = sim['name']
        sim_file = sim['file']
        sim_inputs = sim.get('inputs', [])
        sim_outputs = sim.get('outputs', [])

        print(f"\n  Running: {sim_name}")

        # Validate inputs
        valid, missing = context.validate_inputs(sim_inputs)
        if not valid:
            print(f"    SKIP: Missing inputs: {missing}")
            continue

        # Load and run simulation
        try:
            module = load_simulation_module(sim_file)
            if module is None:
                print(f"    SKIP: Could not load {sim_file}")
                continue

            # Look for main() or run() function
            if hasattr(module, 'main'):
                result = module.main()
            elif hasattr(module, 'run'):
                result = module.run()
            else:
                print(f"    SKIP: No main() or run() function")
                continue

            # Extract outputs
            if isinstance(result, dict):
                for output_path in sim_outputs:
                    parts = output_path.split('.')
                    if len(parts) >= 2:
                        category, param = parts[0], parts[1]
                        if category in result and param in result[category]:
                            context.set_param(output_path, result[category][param])
                            print(f"    Output: {output_path} = {result[category][param]}")

            print(f"    DONE: {sim_name}")

        except Exception as e:
            print(f"    ERROR: {e}")
            continue

    return True


def main():
    print("=" * 70)
    print(" PRINCIPIA METAPHYSICA - STRUCTURED SIMULATION RUNNER")
    print("=" * 70)

    # Load structure
    print(f"\nLoading {STRUCTURE_FILE}...")
    structure = load_structure()

    print(f"  Found {len(structure['phases'])} phases")
    print(f"  Mode: {structure['metadata']['execution_mode']}")

    # Initialize context
    context = SimulationContext()

    # Pre-load config.py constants
    try:
        from config import CONSTANTS
        for category, params in CONSTANTS.items():
            for param_name, value in params.items():
                context.set_param(f"{category}.{param_name}", value)
        print(f"  Loaded constants from config.py")
    except ImportError:
        print("  WARNING: Could not load config.py constants")

    # Run phases in order
    phases = sorted(structure['phases'], key=lambda p: p['order'])
    for phase in phases:
        success = run_phase(phase, context)
        if not success and structure['metadata'].get('validation') == 'check_outputs_before_next_phase':
            print(f"\n  ABORT: Phase {phase['name']} failed validation")
            break

    # Export results
    print("\n" + "=" * 70)
    print(" EXPORTING RESULTS")
    print("=" * 70)

    output = {
        'parameters': context.params,
        'simulation_results': context.results,
        'phase_outputs': context.phase_outputs
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n  Saved: {OUTPUT_FILE}")

    print("\n" + "=" * 70)
    print(" STRUCTURED SIMULATION COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    main()
