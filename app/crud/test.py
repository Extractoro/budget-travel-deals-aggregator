from sqlalchemy.orm import Session


def get_test(db: Session):
    return {'message': "test", 'db': db}
