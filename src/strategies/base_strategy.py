"""
Base Strategy Pattern Implementation
"""
from abc import ABC, abstractmethod
import pandas as pd
from typing import Any

class DataProcessingStrategy(ABC):
    @abstractmethod
    def process(self, data: pd.DataFrame) -> Any:
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        pass

class VisualizationStrategy(ABC):
    @abstractmethod
    def create_visualization(self, data: pd.DataFrame, **kwargs) -> Any:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass
    
    @abstractmethod
    def get_required_columns(self) -> list:
        pass