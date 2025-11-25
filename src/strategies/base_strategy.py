"""
Base Strategy Pattern Implementation for BI Dashboard
This defines the interface that all strategies must implement
"""
from abc import ABC, abstractmethod
import pandas as pd
from typing import Any, Dict

class DataProcessingStrategy(ABC):
    """Abstract base class for data processing strategies"""
    
    @abstractmethod
    def process(self, data: pd.DataFrame) -> Any:
        """
        Process the data according to the strategy
        
        Args:
            data: Input DataFrame
            
        Returns:
            Processed result (format depends on strategy)
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Return a description of what this strategy does"""
        pass


class VisualizationStrategy(ABC):
    """Abstract base class for visualization strategies"""
    
    @abstractmethod
    def create_visualization(self, data: pd.DataFrame, **kwargs) -> Any:
        """
        Create a visualization from the data
        
        Args:
            data: Input DataFrame
            **kwargs: Additional parameters for customization
            
        Returns:
            Visualization object (Plotly figure, matplotlib figure, etc.)
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of this visualization type"""
        pass
    
    @abstractmethod
    def get_required_columns(self) -> list:
        """Return list of column types required for this visualization"""
        pass
