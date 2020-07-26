from marshmallow import fields
from projects import ma
from projects.models import Pedidos


class PedidosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pedidos
        load_instance = True


pedidos_schema = PedidosSchema()
