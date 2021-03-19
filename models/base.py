from sqlalchemy import Column, Integer


class Base:
    id = Column(Integer, primary_key=True)

    def save(self, commit=False):
        self.session.add(self)
        if commit:
            self.session.commit()

    def delete(self, commit=False):
        self.session.delete(self)
        if commit:
            self.session.commit()

    def __repr__(self):
        if hasattr(self, 'nome'):
            return self.nome
        return super.__repr__()
