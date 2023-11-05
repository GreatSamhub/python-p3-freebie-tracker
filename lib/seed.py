from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev, Freebie

engine = create_engine("sqlite:///freebies.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Clear the existing data
session.query(Company).delete()
session.query(Dev).delete()
session.query(Freebie).delete()
session.commit()

# Sample data
company1 = Company(name="Company A", founding_year=1990)
company2 = Company(name="Company B", founding_year=2000)
company3 = Company(name="Company C", founding_year=2010)

dev1 = Dev(name="Dev 1")
dev2 = Dev(name="Dev 2")
dev3 = Dev(name="Dev 3")

# Create Freebie instances and associate them with Dev and Company
freebie1 = Freebie(item="T-shirt", value=10)
freebie1.dev = dev1
freebie1.company = company1

freebie2 = Freebie(item="Sticker", value=2)
freebie2.dev = dev2
freebie2.company = company2

freebie3 = Freebie(item="Mug", value=5)
freebie3.dev = dev1
freebie3.company = company3

freebie4 = Freebie(item="T-shirt", value=15)
freebie4.dev = dev3
freebie4.company = company2

# Add and commit the sample data
session.add_all([company1, company2, company3, dev1, dev2, dev3, freebie1, freebie2, freebie3, freebie4])
session.commit()

# Print the Freebie instances
for freebie in session.query(Freebie).all():
    print(freebie)
