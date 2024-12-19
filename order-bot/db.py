from sqlalchemy.exc import SQLAlchemyError
from models import Signal, AsyncSessionLocal

async def save_signal_to_db(order_result):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            try:
                signal = Signal(
                    type=order_result['type'],
                    symbol=order_result['symbol'],
                    entry=order_result['entry'],
                    stop_loss=order_result['stop_loss'],
                    take_profit=order_result['take_profit'],
                    open_price=order_result['open_price'],
                    close_price=order_result['close_price'],
                    timestamp=order_result['timestamp'],
                    realized_pnl=order_result['realized_pnl'],
                )
                session.add(signal)
                await session.commit()
                print("Signal saved successfully")
            except SQLAlchemyError as e:
                print(f"Failed to save signal to DB: {e}")
                await session.rollback()
