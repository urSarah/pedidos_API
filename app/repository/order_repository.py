from models import ItemsOrder, Order


class OrderRepository:
    def get_by_Id(self,session,orderId):
        return session.query(Order).filter(Order.id == orderId).first()
    
    def create(self, session, current_user):
        new_order = Order(userId=current_user)

        session.add(new_order)
        self.update(session)

        return new_order
    
    def list_all(self, session):
        return session.query(Order).all()
    
    def add_item(self, session, order_id, item_schema):
        order_item = ItemsOrder(
            orderId=order_id,
            quantidade=item_schema.quantidade,
            sabor=item_schema.sabor,
            tamanho=item_schema.tamanho,
            preco_unitario=item_schema.preco_unitario
        )

        session.add(order_item)
        self.update(session)

    def update(self, session):
        session.commit()