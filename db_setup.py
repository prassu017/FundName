from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# Initialize database connection
engine = create_engine('sqlite:///funds.db')
Base = declarative_base()

# Define Fund table
class Fund(Base):
    __tablename__ = 'funds'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)

# Create the table
Base.metadata.create_all(engine)

# Session for database transactions
Session = sessionmaker(bind=engine)
session = Session()
