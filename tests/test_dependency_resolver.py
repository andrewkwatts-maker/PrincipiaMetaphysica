"""
Unit Tests for DependencyGraph - Topological Dependency Resolution
=================================================================
Tests the DAG-based parameter dependency system that ensures
simulations execute in the correct topological order.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "simulations"))

from simulations.core.dependency_resolver import (
    DependencyGraph,
    CycleDetectedError,
    MissingComputeFunctionError,
)


@pytest.fixture
def graph():
    """Create a fresh DependencyGraph."""
    return DependencyGraph()


class TestRegistration:
    """Tests for parameter registration."""

    def test_register_parameter(self, graph):
        """Can register a parameter with no dependencies."""
        graph.register("seed.b3")
        assert graph.has_param("seed.b3")

    def test_register_with_dependencies(self, graph):
        """Can register a parameter with dependencies."""
        graph.register("seed.b3")
        graph.register("physics.alpha", depends_on=["seed.b3"])
        assert graph.get_dependencies("physics.alpha") == ["seed.b3"]

    def test_unregister_parameter(self, graph):
        """Can unregister a parameter."""
        graph.register("seed.b3")
        graph.unregister("seed.b3")
        assert not graph.has_param("seed.b3")

    def test_register_with_compute_fn(self, graph):
        """Can register a parameter with a compute function."""
        graph.register("seed.b3")
        graph.register(
            "derived.chi",
            depends_on=["seed.b3"],
            compute_fn=lambda deps: deps["seed.b3"] * 2,
        )
        assert graph.has_param("derived.chi")


class TestDependencyQueries:
    """Tests for querying dependencies."""

    def test_get_dependencies(self, graph):
        """get_dependencies returns direct dependencies."""
        graph.register("A")
        graph.register("B", depends_on=["A"])
        assert graph.get_dependencies("B") == ["A"]

    def test_get_dependents(self, graph):
        """get_dependents returns reverse dependencies."""
        graph.register("A")
        graph.register("B", depends_on=["A"])
        assert "B" in graph.get_dependents("A")

    def test_get_all_dependencies_transitive(self, graph):
        """get_all_dependencies returns transitive closure."""
        graph.register("A")
        graph.register("B", depends_on=["A"])
        graph.register("C", depends_on=["B"])
        all_deps = graph.get_all_dependencies("C")
        assert "A" in all_deps
        assert "B" in all_deps

    def test_no_dependencies_returns_empty(self, graph):
        """Parameter with no deps returns empty list."""
        graph.register("seed")
        assert graph.get_dependencies("seed") == []


class TestCycleDetection:
    """Tests for circular dependency detection."""

    def test_detect_cycle_manual(self):
        """Manually injected cycle is detected by detect_cycle()."""
        graph = DependencyGraph()
        graph.register("A")
        graph.register("B", depends_on=["A"])
        # Manually inject a back-edge to create A -> B -> A
        graph._dependencies["A"] = ["B"]
        cycle = graph.detect_cycle("A")
        assert cycle is not None

    def test_no_cycle_returns_none(self, graph):
        """Acyclic graph returns None from detect_cycle."""
        graph.register("A")
        graph.register("B", depends_on=["A"])
        graph.register("C", depends_on=["B"])
        assert graph.detect_cycle("C") is None


class TestTopologicalSort:
    """Tests for topological sorting."""

    def test_linear_chain(self, graph):
        """Linear chain A -> B -> C sorts correctly."""
        graph.register("A")
        graph.register("B", depends_on=["A"])
        graph.register("C", depends_on=["B"])
        order = graph.topological_sort()
        assert order.index("A") < order.index("B") < order.index("C")

    def test_diamond_dependency(self, graph):
        """Diamond pattern: D depends on B and C, both depend on A."""
        graph.register("A")
        graph.register("B", depends_on=["A"])
        graph.register("C", depends_on=["A"])
        graph.register("D", depends_on=["B", "C"])
        order = graph.topological_sort()
        assert order.index("A") < order.index("B")
        assert order.index("A") < order.index("C")
        assert order.index("B") < order.index("D")
        assert order.index("C") < order.index("D")

    def test_empty_graph_sorts(self, graph):
        """Empty graph returns empty sort."""
        order = graph.topological_sort()
        assert order == []

    def test_single_node(self, graph):
        """Single node sorts to itself."""
        graph.register("only")
        order = graph.topological_sort()
        assert order == ["only"]


class TestComputeFunctions:
    """Tests for compute function storage and retrieval."""

    def test_compute_fn_stored(self, graph):
        """Compute functions are stored when registered."""
        fn = lambda deps: 24
        graph.register("b3", compute_fn=fn)
        assert "b3" in graph._computers
        assert graph._computers["b3"] is fn

    def test_compute_fn_chain(self, graph):
        """Compute functions can depend on other computed values."""
        graph.register("b3", compute_fn=lambda deps: 24)
        graph.register(
            "double",
            depends_on=["b3"],
            compute_fn=lambda deps: deps["b3"] * 2,
        )
        # Verify the chain is set up correctly
        assert graph.get_dependencies("double") == ["b3"]
        assert "double" in graph._computers
