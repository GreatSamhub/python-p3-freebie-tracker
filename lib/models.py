from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    def freebies(self):
        return self.freebies

    def devs(self):
        return [freebie.dev for freebie in self.freebies]

    def give_freebie(self, session, dev, item, value):
        freebie = Freebie(dev=dev, item=item, value=value)
        session.add(freebie)
        session.commit()

    @classmethod
    def oldest_company(self):
        return session.query(Company).order_by(Company.founding_year).first()

    def __repr__(self):
        return f'<Company {self.name}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    def freebies(self):
        return self.freebies

    def companies(self):
        return [freebie.company for freebie in self.freebies]

    def received_freebie(self,item):
        for freebie in self.freebies:
            if freebie.item == item:
                return True
            return False

    def give_freebie(self, session, other_dev, freebie):
        if freebie.dev == self:
            freebie.dev = other_dev
            session.commit()

    def __repr__(self):
        return f'<Dev {self.name}>'

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item = Column(String())
    value = Column(Integer())
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))

    @property
    def _dev(self):
        return self._dev

    @property
    def _company(self):
        return self._company

    def print_details(self):
        return f"{self._dev.name} owns a {self.item} from {self._company.name} with a value of {self.value}"

    def __repr__(self):
        return f'<Freebie {self.item}>'

engine = create_engine("sqlite:///freebies.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

