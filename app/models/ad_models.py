from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models.client_models import Client
from app.models.community_models import Community

class Ad(db.Model):
    __tablename__ = 'ads'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    client_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Client.id, ondelete="CASCADE"),
                                               index=True)
    type: so.Mapped[str] = so.mapped_column(sa.String(6), default='cl', nullable=False)
    community: so.Mapped[str] = so.mapped_column(sa.String(24), nullable=False)
    text: so.Mapped[str] = so.mapped_column(nullable=True)
    note: so.Mapped[str] = so.mapped_column(nullable=True)
    start_date: so.Mapped[datetime] = so.mapped_column(nullable=False)
    end_date: so.Mapped[datetime] = so.mapped_column(nullable=False)
    monthly_freq: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False, default=1.0)

    client: so.Mapped[Client] = so.relationship(back_populates='ads')

    def date_from_m_y(self, month, year):
        return datetime.strptime(str(year*10000+month*100+1),'%Y%m%d')
    
    def set_start_date(self, month, year):
        self.start_date = self.date_from_m_y(month, year)

    def set_end_date(self, month, year):
        self.end_date = self.date_from_m_y(month, year)

    def __repr__(self):
        return '<Ad {}>'.format(self.username)