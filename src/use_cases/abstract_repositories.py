from abc import ABCMeta, abstractmethod


class AbstractStorage(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, *, data): pass
    
    @abstractmethod
    async def update(self, *, row_id: str, data): pass
    
    @abstractmethod
    async def read(self, *, row_id: str | None): pass
    
    @abstractmethod
    async def delete(self, *, row_id: str): pass
