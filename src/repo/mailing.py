from src.repo.base import BaseRepo
from src.schemas import Mailing, MailingCreate, MailingUpdate


class MailingRepo(BaseRepo[Mailing, MailingCreate, MailingUpdate]):
    pass


mailing = MailingRepo(Mailing, 'api', 'mailing')
