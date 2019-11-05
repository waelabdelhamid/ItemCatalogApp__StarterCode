from models import Base, Catalog, CatalogItem, User
from sqlalchemy import asc, create_engine, desc
from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite:///catalogitems.db')
engine = create_engine("postgresql+psycopg2://catalog:ccatalog@localhost/catalog")
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user if you are not login yet
# User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
#             picture='https://pbs.twimg.com/profile_images/2671170543/
#             18debd694829ed78203a5a36dd364160_400x400.png')
# session.add(User1)
# session.commit()

# Query first user if you are already login
User1 = session.query(User).order_by(
    asc(User.created_at)).first()

# Catalog for Soccer
catalog1 = Catalog(user_id=1, name="Soccer")

session.add(catalog1)
session.commit()

# Catalog for Basketball
catalog1 = Catalog(user_id=1, name="Basketball")

session.add(catalog1)
session.commit()

# Catalog for Thyme for Baseball
catalog1 = Catalog(user_id=1, name="Baseball")

session.add(catalog1)
session.commit()

# Catalog for Frisbee
catalog1 = Catalog(user_id=1, name="Frisbee")

session.add(catalog1)
session.commit()

# Catalog for Snowboarding
catalog1 = Catalog(user_id=1, name="Snowboarding")

session.add(catalog1)
session.commit()

# Catalog for Rock Climbing
catalog1 = Catalog(user_id=1, name="Rock Climbing")

session.add(catalog1)
session.commit()

# Catalog for Foosball
catalog1 = Catalog(user_id=1, name="Foosball")

session.add(catalog1)
session.commit()

# Catalog for Skating
catalog1 = Catalog(user_id=1, name="Skating")

session.add(catalog1)
session.commit()

# Catalog for Hoskey
catalog1 = Catalog(user_id=1, name="Hoskey")

session.add(catalog1)
session.commit()


print "added catalogs!"
