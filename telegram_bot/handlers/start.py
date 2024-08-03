from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

async def start_command(message: Message):
    await message.answer("Добро пожаловать в FlowerDelivery бот!")

def register_handlers(dp: Dispatcher):
    dp.message.register(start_command, Command(commands=["start"]))
