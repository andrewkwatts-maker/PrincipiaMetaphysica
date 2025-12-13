"""
Simulation Base Classes and Registry
=====================================

SOLID Principles Applied:
- Single Responsibility: SimulationBase only defines interface
- Open/Closed: New simulations extend base without modifying it
- Liskov Substitution: All simulations can be used interchangeably
- Interface Segregation: Minimal interface requirements
- Dependency Inversion: Depends on abstractions (ConfigProvider)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Type, Callable
from datetime import datetime
import numpy as np


@dataclass
class SimulationResult:
    """
    Standardized container for simulation results.

    Provides consistent structure for all simulation outputs.
    """
    # Identification
    name: str
    version: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    # Results
    data: Dict[str, Any] = field(default_factory=dict)
    status: str = "completed"
    error: Optional[str] = None

    # Metadata
    parameters_used: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'version': self.version,
            'timestamp': self.timestamp,
            'data': self._sanitize_data(self.data),
            'status': self.status,
            'error': self.error,
            'parameters_used': self.parameters_used,
            'execution_time_ms': self.execution_time_ms,
        }

    def _sanitize_data(self, data: Any) -> Any:
        """Recursively sanitize data for JSON (handle numpy, NaN, etc.)"""
        if isinstance(data, dict):
            return {k: self._sanitize_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._sanitize_data(item) for item in data]
        elif isinstance(data, np.ndarray):
            return self._sanitize_data(data.tolist())
        elif isinstance(data, (np.integer, np.floating)):
            val = float(data)
            if np.isnan(val) or np.isinf(val):
                return None
            return val
        elif isinstance(data, float):
            if np.isnan(data) or np.isinf(data):
                return None
            return data
        elif isinstance(data, complex):
            return {'real': data.real, 'imag': data.imag}
        return data


class SimulationBase(ABC):
    """
    Abstract base class for all simulations.

    Interface Segregation: Only requires run() and metadata.
    Dependency Inversion: Receives config via constructor.

    Example Usage:
        class ProtonDecaySimulation(SimulationBase):
            name = "proton_decay"
            version = "12.7"

            def run(self, **kwargs) -> SimulationResult:
                # Implementation
                return SimulationResult(
                    name=self.name,
                    version=self.version,
                    data={'tau_p': 3.91e34}
                )
    """

    # Class-level metadata (to be overridden)
    name: str = "base_simulation"
    version: str = "1.0"
    description: str = "Base simulation class"
    dependencies: List[str] = []

    def __init__(self, config_provider=None):
        """
        Initialize with optional config provider.

        Dependency Inversion: Config is injected, not imported directly.
        """
        self._config_provider = config_provider
        self._start_time = None
        self._end_time = None

    @property
    def config(self):
        """Get configuration provider (lazy load if not provided)"""
        if self._config_provider is None:
            from .config_provider import get_config
            self._config_provider = get_config()
        return self._config_provider

    @abstractmethod
    def run(self, verbose: bool = True, **kwargs) -> SimulationResult:
        """
        Execute the simulation.

        Args:
            verbose: Whether to print progress
            **kwargs: Simulation-specific parameters

        Returns:
            SimulationResult with computed data
        """
        pass

    def validate_inputs(self, **kwargs) -> bool:
        """
        Validate input parameters before running.

        Override in subclasses for specific validation.
        """
        return True

    def pre_run(self):
        """Hook called before run() - for setup"""
        self._start_time = datetime.now()

    def post_run(self, result: SimulationResult):
        """Hook called after run() - for cleanup"""
        self._end_time = datetime.now()
        if self._start_time and self._end_time:
            delta = (self._end_time - self._start_time).total_seconds() * 1000
            result.execution_time_ms = delta

    def execute(self, verbose: bool = True, **kwargs) -> SimulationResult:
        """
        Template method for simulation execution.

        Wraps run() with pre/post hooks and error handling.
        """
        self.pre_run()

        try:
            if not self.validate_inputs(**kwargs):
                return SimulationResult(
                    name=self.name,
                    version=self.version,
                    status="failed",
                    error="Input validation failed"
                )

            result = self.run(verbose=verbose, **kwargs)
            self.post_run(result)
            return result

        except Exception as e:
            return SimulationResult(
                name=self.name,
                version=self.version,
                status="error",
                error=str(e)
            )


class SimulationRegistry:
    """
    Registry for simulation classes.

    Open/Closed Principle: New simulations can be registered
    without modifying existing code.

    Example Usage:
        # Register a simulation
        SimulationRegistry.register(ProtonDecaySimulation)

        # Get simulation by name
        sim_class = SimulationRegistry.get("proton_decay")
        sim = sim_class()
        result = sim.execute()

        # Run all registered simulations
        results = SimulationRegistry.run_all(verbose=True)
    """

    _registry: Dict[str, Type[SimulationBase]] = {}
    _order: List[str] = []

    @classmethod
    def register(cls, simulation_class: Type[SimulationBase], order: Optional[int] = None):
        """
        Register a simulation class.

        Args:
            simulation_class: The simulation class to register
            order: Optional execution order (lower = earlier)
        """
        name = simulation_class.name
        cls._registry[name] = simulation_class

        if name not in cls._order:
            if order is not None:
                cls._order.insert(order, name)
            else:
                cls._order.append(name)

    @classmethod
    def get(cls, name: str) -> Optional[Type[SimulationBase]]:
        """Get a simulation class by name"""
        return cls._registry.get(name)

    @classmethod
    def list_all(cls) -> List[str]:
        """List all registered simulation names in order"""
        return list(cls._order)

    @classmethod
    def run_all(cls, verbose: bool = True, config_provider=None, **kwargs) -> Dict[str, SimulationResult]:
        """
        Run all registered simulations in order.

        Args:
            verbose: Whether to print progress
            config_provider: Configuration provider to inject
            **kwargs: Passed to all simulations

        Returns:
            Dictionary mapping simulation names to results
        """
        results = {}

        for name in cls._order:
            sim_class = cls._registry.get(name)
            if sim_class:
                if verbose:
                    print(f"\nRunning: {name} (v{sim_class.version})...")

                sim = sim_class(config_provider=config_provider)
                result = sim.execute(verbose=verbose, **kwargs)
                results[name] = result

                if verbose:
                    status = "✓" if result.status == "completed" else "✗"
                    print(f"  {status} {name}: {result.status}")

        return results

    @classmethod
    def clear(cls):
        """Clear the registry (for testing)"""
        cls._registry.clear()
        cls._order.clear()


def register_simulation(order: Optional[int] = None):
    """
    Decorator to register a simulation class.

    Example:
        @register_simulation(order=1)
        class ProtonDecaySimulation(SimulationBase):
            name = "proton_decay"
            ...
    """
    def decorator(cls: Type[SimulationBase]) -> Type[SimulationBase]:
        SimulationRegistry.register(cls, order=order)
        return cls
    return decorator
