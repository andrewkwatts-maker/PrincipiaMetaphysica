"""
Dependency Resolver for Principia Metaphysica v20
==================================================
Provides recursive parameter resolution with topological sorting.

This module implements a directed acyclic graph (DAG) for managing parameter
dependencies, enabling automatic computation of derived values in the correct
topological order.

Architecture:
    Level 0: Ten Pillar Seeds (hardcoded in FormulasRegistry)
    Level 1: Direct derivations (b3, chi_eff, k_gimel)
    Level 2: Physics constants (alpha_em, G_F, v_higgs)
    Level 3: Predictions (H0, w0, masses)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from typing import Dict, List, Set, Any, Callable, Optional, Tuple
from collections import defaultdict
import warnings


class CycleDetectedError(Exception):
    """Raised when a circular dependency is detected in the graph."""

    def __init__(self, cycle_path: List[str]):
        self.cycle_path = cycle_path
        cycle_str = " -> ".join(cycle_path)
        super().__init__(f"Circular dependency detected: {cycle_str}")


class MissingComputeFunctionError(Exception):
    """Raised when a parameter has no compute function and no base value."""

    def __init__(self, param: str):
        self.param = param
        super().__init__(f"No compute function registered for '{param}'")


class DependencyGraph:
    """
    Directed acyclic graph for parameter dependencies.

    Tracks which parameters depend on which other parameters,
    enabling topological sorting for correct computation order.

    Example:
        >>> graph = DependencyGraph()
        >>> graph.register("gravity.G_N", depends_on=["gravity.M_planck"])
        >>> graph.register("gravity.M_planck", depends_on=["geometry.k_gimel"])
        >>> graph.get_dependencies("gravity.G_N")
        ['gravity.M_planck']
    """

    def __init__(self):
        """Initialize an empty dependency graph."""
        self._dependencies: Dict[str, List[str]] = {}
        self._reverse_deps: Dict[str, List[str]] = defaultdict(list)
        self._computers: Dict[str, Callable] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}

    def register(self, param: str, depends_on: List[str] = None,
                 compute_fn: Optional[Callable] = None,
                 metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Register a parameter with its dependencies.

        Args:
            param: Parameter path (e.g., "geometry.elder_kads")
            depends_on: List of parameter paths this parameter depends on
            compute_fn: Optional function to compute this parameter.
                       Signature: fn(dep_values: Dict[str, Any]) -> Any
            metadata: Optional metadata about the parameter (level, description, etc.)

        Raises:
            CycleDetectedError: If adding this parameter would create a cycle
        """
        if depends_on is None:
            depends_on = []

        # Store dependencies
        self._dependencies[param] = depends_on

        # Update reverse dependency mapping
        for dep in depends_on:
            if param not in self._reverse_deps[dep]:
                self._reverse_deps[dep].append(param)

        # Store compute function
        if compute_fn is not None:
            self._computers[param] = compute_fn

        # Store metadata
        if metadata is not None:
            self._metadata[param] = metadata

        # Check for cycles after registration
        cycle = self.detect_cycle(param)
        if cycle:
            # Rollback the registration
            del self._dependencies[param]
            for dep in depends_on:
                self._reverse_deps[dep].remove(param)
            if compute_fn is not None:
                del self._computers[param]
            if metadata is not None:
                del self._metadata[param]
            raise CycleDetectedError(cycle)

    def unregister(self, param: str) -> None:
        """
        Remove a parameter from the graph.

        Args:
            param: Parameter path to remove
        """
        if param in self._dependencies:
            # Remove from reverse deps
            for dep in self._dependencies[param]:
                if param in self._reverse_deps[dep]:
                    self._reverse_deps[dep].remove(param)
            del self._dependencies[param]

        if param in self._computers:
            del self._computers[param]

        if param in self._metadata:
            del self._metadata[param]

        # Also remove from reverse deps if it's a dependency
        if param in self._reverse_deps:
            del self._reverse_deps[param]

    def has_param(self, param: str) -> bool:
        """Check if a parameter is registered in the graph."""
        return param in self._dependencies

    def get_dependencies(self, param: str) -> List[str]:
        """
        Get direct dependencies of a parameter.

        Args:
            param: Parameter path

        Returns:
            List of parameter paths that this parameter depends on
        """
        return self._dependencies.get(param, [])

    def get_dependents(self, param: str) -> List[str]:
        """
        Get parameters that depend on this one.

        Args:
            param: Parameter path

        Returns:
            List of parameter paths that depend on this parameter
        """
        return self._reverse_deps.get(param, [])

    def get_all_dependencies(self, param: str) -> Set[str]:
        """
        Get all transitive dependencies of a parameter (recursive).

        Args:
            param: Parameter path

        Returns:
            Set of all parameter paths that this parameter directly or
            indirectly depends on
        """
        all_deps = set()
        to_visit = list(self.get_dependencies(param))

        while to_visit:
            dep = to_visit.pop()
            if dep not in all_deps:
                all_deps.add(dep)
                to_visit.extend(self.get_dependencies(dep))

        return all_deps

    def get_compute_function(self, param: str) -> Optional[Callable]:
        """Get the compute function for a parameter."""
        return self._computers.get(param)

    def get_metadata(self, param: str) -> Dict[str, Any]:
        """Get metadata for a parameter."""
        return self._metadata.get(param, {})

    def detect_cycle(self, param: str, visited: Set[str] = None,
                     path: Set[str] = None) -> Optional[List[str]]:
        """
        Detect if the graph contains a cycle starting from this parameter.

        Args:
            param: Parameter to start cycle detection from
            visited: Set of already visited nodes (for internal recursion)
            path: Current path in DFS (for internal recursion)

        Returns:
            List representing the cycle path if a cycle exists, None otherwise
        """
        if visited is None:
            visited = set()
        if path is None:
            path = set()

        visited.add(param)
        path.add(param)

        for dep in self.get_dependencies(param):
            if dep in path:
                # Found cycle - reconstruct path
                cycle = [param, dep]
                return cycle
            if dep not in visited:
                cycle = self.detect_cycle(dep, visited, path)
                if cycle:
                    if cycle[0] != cycle[-1]:
                        cycle.insert(0, param)
                    return cycle

        path.remove(param)
        return None

    def topological_sort(self) -> List[str]:
        """
        Return parameters in dependency order (roots first).

        Parameters with no dependencies come first, followed by
        parameters that depend only on those, etc.

        Returns:
            List of parameter paths in topological order
        """
        visited = set()
        result = []

        def visit(param: str):
            if param in visited:
                return
            visited.add(param)
            for dep in self.get_dependencies(param):
                visit(dep)
            result.append(param)

        for param in self._dependencies:
            visit(param)

        return result

    def get_computation_order(self, target: str) -> List[str]:
        """
        Get the order in which parameters must be computed to resolve target.

        Args:
            target: The parameter we want to compute

        Returns:
            List of parameters in the order they must be computed,
            ending with target
        """
        if target not in self._dependencies:
            return [target]

        visited = set()
        result = []

        def visit(param: str):
            if param in visited:
                return
            visited.add(param)
            for dep in self.get_dependencies(param):
                visit(dep)
            result.append(param)

        visit(target)
        return result

    def get_level(self, param: str) -> int:
        """
        Get the dependency level of a parameter (0 = no dependencies).

        Level 0: No dependencies (seeds/base values)
        Level 1: Depends only on Level 0
        Level 2: Depends on Level 1 or below
        etc.

        Args:
            param: Parameter path

        Returns:
            Integer level (0 = root/seed)
        """
        deps = self.get_dependencies(param)
        if not deps:
            return 0
        return 1 + max(self.get_level(dep) for dep in deps)

    def get_params_at_level(self, level: int) -> List[str]:
        """
        Get all parameters at a specific dependency level.

        Args:
            level: The dependency level (0 = roots)

        Returns:
            List of parameter paths at that level
        """
        return [p for p in self._dependencies if self.get_level(p) == level]

    def export_graph(self) -> Dict[str, Any]:
        """
        Export the graph structure for debugging/visualization.

        Returns:
            Dictionary with nodes, edges, and metadata
        """
        nodes = []
        edges = []

        for param in self._dependencies:
            nodes.append({
                'id': param,
                'level': self.get_level(param),
                'has_compute': param in self._computers,
                'metadata': self._metadata.get(param, {})
            })
            for dep in self._dependencies[param]:
                edges.append({'from': dep, 'to': param})

        return {
            'nodes': nodes,
            'edges': edges,
            'topological_order': self.topological_sort()
        }


class DependencyResolver:
    """
    Resolves parameter values with automatic dependency resolution.

    When a parameter is requested:
    1. Check if already computed (cached)
    2. If not, resolve all dependencies first
    3. Compute this parameter using its compute function
    4. Cache and return the result

    Example:
        >>> graph = DependencyGraph()
        >>> graph.register("a", depends_on=[], compute_fn=lambda deps: 10)
        >>> graph.register("b", depends_on=["a"], compute_fn=lambda deps: deps["a"] * 2)
        >>> resolver = DependencyResolver(graph)
        >>> resolver.resolve("b")
        20
    """

    def __init__(self, graph: DependencyGraph):
        """
        Initialize the resolver with a dependency graph.

        Args:
            graph: DependencyGraph instance defining dependencies
        """
        self.graph = graph
        self._cache: Dict[str, Any] = {}
        self._computing: Set[str] = set()  # For runtime cycle detection
        self._computation_log: List[Tuple[str, str]] = []  # (param, status)

    def resolve(self, param: str, base_values: Dict[str, Any] = None) -> Any:
        """
        Resolve a parameter value, computing dependencies as needed.

        This method recursively resolves all dependencies before computing
        the requested parameter. Values are cached for efficiency.

        Args:
            param: Parameter path to resolve
            base_values: Pre-set values (Level 0 seeds) that override computation

        Returns:
            Computed parameter value

        Raises:
            CycleDetectedError: If circular dependency is detected at runtime
            MissingComputeFunctionError: If no compute function exists
            KeyError: If parameter is not in graph and not in base_values
        """
        if base_values is None:
            base_values = {}

        # Check cache first
        if param in self._cache:
            self._computation_log.append((param, 'cached'))
            return self._cache[param]

        # Check base values (Level 0 seeds)
        if param in base_values:
            self._cache[param] = base_values[param]
            self._computation_log.append((param, 'base_value'))
            return base_values[param]

        # Runtime cycle detection
        if param in self._computing:
            # Build cycle path from current computation stack
            cycle_path = list(self._computing) + [param]
            raise CycleDetectedError(cycle_path)

        # Check if parameter is registered
        if not self.graph.has_param(param):
            raise KeyError(f"Parameter '{param}' not registered in dependency graph")

        self._computing.add(param)

        try:
            # Resolve all dependencies first
            deps = self.graph.get_dependencies(param)
            dep_values = {}
            for dep in deps:
                dep_values[dep] = self.resolve(dep, base_values)

            # Get compute function
            compute_fn = self.graph.get_compute_function(param)
            if compute_fn is None:
                raise MissingComputeFunctionError(param)

            # Compute this parameter
            value = compute_fn(dep_values)

            # Cache the result
            self._cache[param] = value
            self._computation_log.append((param, 'computed'))

            return value

        finally:
            self._computing.remove(param)

    def resolve_all(self, params: List[str], base_values: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Resolve multiple parameters at once.

        Args:
            params: List of parameter paths to resolve
            base_values: Pre-set values for base parameters

        Returns:
            Dictionary mapping parameter paths to their resolved values
        """
        results = {}
        for param in params:
            results[param] = self.resolve(param, base_values)
        return results

    def try_resolve(self, param: str, base_values: Dict[str, Any] = None,
                    default: Any = None) -> Any:
        """
        Try to resolve a parameter, returning default on failure.

        Args:
            param: Parameter path to resolve
            base_values: Pre-set values for base parameters
            default: Value to return if resolution fails

        Returns:
            Resolved value or default
        """
        try:
            return self.resolve(param, base_values)
        except (KeyError, MissingComputeFunctionError, CycleDetectedError):
            return default

    def invalidate(self, param: str) -> Set[str]:
        """
        Invalidate a cached value and all dependents.

        When a base value changes, all derived values must be recomputed.
        This method clears the cache for the specified parameter and
        recursively invalidates all parameters that depend on it.

        Args:
            param: Parameter path to invalidate

        Returns:
            Set of all invalidated parameter paths
        """
        invalidated = set()

        def _invalidate_recursive(p: str):
            if p in self._cache:
                del self._cache[p]
                invalidated.add(p)

            for dependent in self.graph.get_dependents(p):
                _invalidate_recursive(dependent)

        _invalidate_recursive(param)
        return invalidated

    def clear_cache(self) -> None:
        """Clear all cached values."""
        self._cache.clear()
        self._computation_log.clear()

    def get_cached_value(self, param: str) -> Optional[Any]:
        """
        Get a cached value without triggering computation.

        Args:
            param: Parameter path

        Returns:
            Cached value or None if not cached
        """
        return self._cache.get(param)

    def is_cached(self, param: str) -> bool:
        """Check if a parameter value is cached."""
        return param in self._cache

    def get_computation_log(self) -> List[Tuple[str, str]]:
        """
        Get the log of computations performed.

        Returns:
            List of (param, status) tuples where status is one of:
            'cached', 'base_value', 'computed'
        """
        return list(self._computation_log)

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the cache.

        Returns:
            Dictionary with cache statistics
        """
        computed_count = sum(1 for _, s in self._computation_log if s == 'computed')
        cached_count = sum(1 for _, s in self._computation_log if s == 'cached')
        base_count = sum(1 for _, s in self._computation_log if s == 'base_value')

        return {
            'cached_values': len(self._cache),
            'total_lookups': len(self._computation_log),
            'computed': computed_count,
            'cache_hits': cached_count,
            'base_values': base_count,
            'hit_rate': cached_count / len(self._computation_log) if self._computation_log else 0.0
        }


# ===========================================================================
# Pre-defined Dependency Graph for PM v20
# ===========================================================================

def build_pm_dependency_graph() -> DependencyGraph:
    """
    Build the standard PM v20 dependency graph.

    This function constructs the complete dependency graph for the
    Principia Metaphysica framework, defining how parameters derive
    from each other.

    Level 0: Ten Pillar Seeds (hardcoded in FormulasRegistry)
    Level 1: Direct derivations (b3, chi_eff, k_gimel)
    Level 2: Physics constants (alpha_em, G_F, v_higgs)
    Level 3: Predictions (H0, w0, masses)

    Returns:
        Configured DependencyGraph instance
    """
    graph = DependencyGraph()

    # =========================================================================
    # Level 0: Seeds (no dependencies - values come from FormulasRegistry)
    # =========================================================================
    # These are the Ten Pillar Seeds - they have no compute functions
    # because their values are provided as base_values during resolution

    # Core topological invariants
    graph.register("seeds.elder_kads", depends_on=[],
                   metadata={'level': 0, 'description': 'Dimensional parameter b3 = 24'})
    graph.register("seeds.mephorash_chi", depends_on=[],
                   metadata={'level': 0, 'description': 'Effective chi = 144'})
    graph.register("seeds.logos_joint", depends_on=[],
                   metadata={'level': 0, 'description': 'The Christ Constant = 153'})
    graph.register("seeds.visible_gates", depends_on=[],
                   metadata={'level': 0, 'description': 'Visible Gates = 135'})
    graph.register("seeds.bulk_pressure", depends_on=[],
                   metadata={'level': 0, 'description': 'O\'Dowd Bulk Pressure = 163'})
    graph.register("seeds.logic_closure", depends_on=[],
                   metadata={'level': 0, 'description': 'Logic Closure = 288'})

    # =========================================================================
    # Level 1: Direct geometric derivations
    # =========================================================================

    # k_gimel = 2 * pi / b3 (geometric coupling)
    graph.register(
        "geometry.k_gimel",
        depends_on=["seeds.elder_kads"],
        compute_fn=lambda deps: 2 * 3.141592653589793 / deps["seeds.elder_kads"],
        metadata={'level': 1, 'description': 'Gimel coupling constant'}
    )

    # V_G2 = b3^(3/2) (G2 volume factor)
    graph.register(
        "geometry.V_G2",
        depends_on=["seeds.elder_kads"],
        compute_fn=lambda deps: deps["seeds.elder_kads"] ** 1.5,
        metadata={'level': 1, 'description': 'G2 volume factor'}
    )

    # chi_ratio = 1 / chi_eff (Reid invariant)
    graph.register(
        "geometry.chi_ratio",
        depends_on=["seeds.mephorash_chi"],
        compute_fn=lambda deps: 1.0 / deps["seeds.mephorash_chi"],
        metadata={'level': 1, 'description': 'Chi ratio (Reid invariant)'}
    )

    # =========================================================================
    # Level 2: Electroweak parameters
    # =========================================================================

    # sin^2(theta_W) derived from b3
    graph.register(
        "electroweak.sin2_theta_W",
        depends_on=["seeds.elder_kads"],
        compute_fn=lambda deps: 3.0 / (8.0 + deps["seeds.elder_kads"]),
        metadata={'level': 2, 'description': 'Weak mixing angle (sin^2 theta_W)'}
    )

    # v_higgs from chi_eff
    graph.register(
        "electroweak.v_higgs",
        depends_on=["seeds.mephorash_chi"],
        compute_fn=lambda deps: 246.22 * (72.0 / deps["seeds.mephorash_chi"]) ** 0.5,
        metadata={'level': 2, 'description': 'Higgs VEV in GeV'}
    )

    # G_F from v_higgs
    graph.register(
        "electroweak.G_F",
        depends_on=["electroweak.v_higgs"],
        compute_fn=lambda deps: 1.0 / (deps["electroweak.v_higgs"] ** 2 * 1.41421356),
        metadata={'level': 2, 'description': 'Fermi constant'}
    )

    # =========================================================================
    # Level 2: Gravity parameters
    # =========================================================================

    # M_planck from k_gimel and V_G2
    graph.register(
        "gravity.M_planck",
        depends_on=["geometry.k_gimel", "geometry.V_G2"],
        compute_fn=lambda deps: 1.22089e19 * (deps["geometry.k_gimel"] / deps["geometry.V_G2"]) ** 0.25,
        metadata={'level': 2, 'description': 'Planck mass in GeV'}
    )

    # G_N from M_planck
    graph.register(
        "gravity.G_N",
        depends_on=["gravity.M_planck"],
        compute_fn=lambda deps: 6.70883e-39 / (deps["gravity.M_planck"] / 1.22089e19) ** 2,
        metadata={'level': 2, 'description': 'Newton gravitational constant'}
    )

    # =========================================================================
    # Level 3: Cosmological predictions
    # =========================================================================

    # H0_geometric from geometric parameters
    graph.register(
        "cosmology.H0_geometric",
        depends_on=["geometry.k_gimel", "seeds.mephorash_chi", "seeds.logos_joint"],
        compute_fn=lambda deps: 71.55 * (deps["geometry.k_gimel"] * deps["seeds.mephorash_chi"] / deps["seeds.logos_joint"]) ** 0.1,
        metadata={'level': 3, 'description': 'Hubble constant from geometry'}
    )

    # w0_geometric from b3
    graph.register(
        "cosmology.w0_geometric",
        depends_on=["seeds.elder_kads"],
        compute_fn=lambda deps: -1.0 + 1.0 / deps["seeds.elder_kads"],
        metadata={'level': 3, 'description': 'Dark energy equation of state'}
    )

    # Omega_DE from w0
    graph.register(
        "cosmology.Omega_DE",
        depends_on=["cosmology.w0_geometric"],
        compute_fn=lambda deps: 0.685 * (1.0 + 0.1 * (deps["cosmology.w0_geometric"] + 1.0)),
        metadata={'level': 3, 'description': 'Dark energy density parameter'}
    )

    return graph


def build_seed_values() -> Dict[str, Any]:
    """
    Build the base seed values from FormulasRegistry constants.

    These are the Level 0 values that have no dependencies.
    They should be passed as base_values to the resolver.

    Returns:
        Dictionary mapping seed parameter paths to their values
    """
    return {
        "seeds.elder_kads": 24,
        "seeds.mephorash_chi": 72,  # chi_eff = 72 per M-theory index theorem (|chi|/24 = 72/24 = 3 generations)
        "seeds.logos_joint": 153,
        "seeds.visible_gates": 135,
        "seeds.bulk_pressure": 163,
        "seeds.logic_closure": 288,
    }


# ===========================================================================
# Convenience Functions
# ===========================================================================

def create_pm_resolver() -> Tuple[DependencyGraph, DependencyResolver]:
    """
    Create a fully configured PM dependency resolver.

    Returns:
        Tuple of (DependencyGraph, DependencyResolver) ready for use
    """
    graph = build_pm_dependency_graph()
    resolver = DependencyResolver(graph)
    return graph, resolver


def resolve_with_seeds(param: str, graph: DependencyGraph = None,
                       resolver: DependencyResolver = None) -> Any:
    """
    Convenience function to resolve a parameter with standard seeds.

    Args:
        param: Parameter path to resolve
        graph: Optional existing graph (creates new if None)
        resolver: Optional existing resolver (creates new if None)

    Returns:
        Resolved parameter value
    """
    if graph is None or resolver is None:
        graph, resolver = create_pm_resolver()

    seeds = build_seed_values()
    return resolver.resolve(param, base_values=seeds)


# ===========================================================================
# Module Exports
# ===========================================================================

__all__ = [
    'DependencyGraph',
    'DependencyResolver',
    'CycleDetectedError',
    'MissingComputeFunctionError',
    'build_pm_dependency_graph',
    'build_seed_values',
    'create_pm_resolver',
    'resolve_with_seeds',
]
