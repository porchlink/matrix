from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
#from app.models.ad_models import Ad


class Client(db.Model):
    __tablename__ = 'client'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash : so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    freshbooks_id : so.Mapped[int] = so.mapped_column(default=0)
    created_ts : so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))

    notes: so.WriteOnlyMapped['ClientNotes'] = so.relationship(
        back_populates='client', passive_deletes=True)
    
    ads: so.WriteOnlyMapped['Ad'] = so.relationship(
        back_populates='client', passive_deletes=True)

    def __repr__(self):
        return '<Client {}>'.format(self.name)
    
class ClientNotes(db.Model):
    __tablename__ = 'client_notes'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    client_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Client.id, ondelete="CASCADE"),
                                               index=True)

    client: so.Mapped[Client] = so.relationship(back_populates='notes')

    def __repr__(self):
        return '<Post {}>'.format(self.body)