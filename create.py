from db_connect import Bird, Session

with Session() as session:
  bird = Bird(name='Penguin')
  session.add(bird)
  session.commit()
