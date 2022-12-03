from src.repo.base import BaseRepo
from src.schemas import Client, ClientCreate, ClientUpdate


class ClientRepo(BaseRepo[Client, ClientCreate, ClientUpdate]):
    pass


client = ClientRepo(Client, 'api', 'client')
