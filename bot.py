# -*- coding: utf-8 -*-
"""
Telegram-бот компании Union Auto.
Запуск:  python bot.py
Требуется: pip install -r requirements.txt  и токен в config.py
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    BotCommand,
    CallbackQuery,
    Message,
    ReplyKeyboardRemove,
)

import config as c
import keyboards as kb
import texts as t

logging.basicConfig(level=logging.INFO)
router = Router()


# ─────────────────────────── ХЕЛПЕРЫ ───────────────────────────
async def show(target, text: str, keyboard):
    """Показать раздел: правим сообщение, если пришли с кнопки."""
    if isinstance(target, CallbackQuery):
        try:
            await target.message.edit_text(
                text, reply_markup=keyboard, disable_web_page_preview=True
            )
        except Exception:
            await target.message.answer(
                text, reply_markup=keyboard, disable_web_page_preview=True
            )
        await target.answer()
    else:
        await target.answer(text, reply_markup=keyboard, disable_web_page_preview=True)


# ─────────────────────────── СТАРТ / МЕНЮ ───────────────────────────
@router.message(CommandStart())
async def cmd_start(m: Message, state: FSMContext):
    await state.clear()
    await m.answer(t.START, reply_markup=kb.main_menu(), disable_web_page_preview=True)


@router.message(Command("menu"))
async def cmd_menu(m: Message, state: FSMContext):
    await state.clear()
    await m.answer(t.MENU, reply_markup=kb.main_menu())


@router.message(Command("help"))
async def cmd_help(m: Message):
    await m.answer(t.FAQ, reply_markup=kb.main_menu(), disable_web_page_preview=True)


@router.callback_query(F.data == "menu")
async def cb_menu(q: CallbackQuery, state: FSMContext):
    await state.clear()
    await show(q, t.MENU, kb.main_menu())


# ─────────────────────────── РАЗДЕЛЫ ───────────────────────────
@router.callback_query(F.data == "about")
async def cb_about(q: CallbackQuery):
    await show(q, t.ABOUT, kb.inner(extra=[
        [("🌐 Сайт компании", ("url", c.SITE))],
        [("📣 Наш канал", ("url", c.TG_CHANNEL))],
    ]))


@router.callback_query(F.data == "cats")
async def cb_cats(q: CallbackQuery):
    await show(q, t.CATS, kb.cats_menu())


@router.callback_query(F.data == "cars")
async def cb_cars(q: CallbackQuery):
    await show(q, t.CARS, kb.inner(back_to="cats", extra=[
        [("🚘 Легковые в наличии", ("url", c.SITE_STOCK))],
        [("🛣 Как проходит покупка", "path_cars")],
    ]))


@router.callback_query(F.data == "trucks")
async def cb_trucks(q: CallbackQuery):
    await show(q, t.TRUCKS, kb.inner(back_to="cats", extra=[
        [("🚛 Смотреть в наличии", ("url", c.SITE_STOCK))],
        [("🛣 Как проходит покупка", "path_trucks")],
    ]))


@router.callback_query(F.data == "machinery")
async def cb_machinery(q: CallbackQuery):
    await show(q, t.MACHINERY, kb.inner(back_to="cats", extra=[
        [("🏗 Спецтехника в наличии", ("url", c.SITE_STOCK))],
        [("💳 Лизинг на спецтехнику", "finance")],
    ]))


@router.callback_query(F.data == "path")
async def cb_path(q: CallbackQuery):
    await show(q, t.PATH_MENU, kb.path_menu())


@router.callback_query(F.data == "path_cars")
async def cb_path_cars(q: CallbackQuery):
    await show(q, t.PATH_CARS, kb.inner(back_to="path"))


@router.callback_query(F.data == "path_trucks")
async def cb_path_trucks(q: CallbackQuery):
    await show(q, t.PATH_TRUCKS, kb.inner(back_to="path"))


@router.callback_query(F.data == "finance")
async def cb_finance(q: CallbackQuery):
    await show(q, t.FINANCE, kb.inner())


@router.callback_query(F.data == "promo")
async def cb_promo(q: CallbackQuery):
    await show(q, t.PROMO_MENU, kb.promo_menu())


@router.callback_query(F.data == "promo_social")
async def cb_promo_social(q: CallbackQuery):
    await show(q, t.PROMO_SOCIAL, kb.inner(back_to="promo"))


@router.callback_query(F.data == "promo_ref")
async def cb_promo_ref(q: CallbackQuery):
    await show(q, t.PROMO_REFERRAL, kb.inner(back_to="promo"))


@router.callback_query(F.data == "promo_bonus")
async def cb_promo_bonus(q: CallbackQuery):
    await show(q, t.PROMO_BONUS, kb.inner(back_to="promo"))


@router.callback_query(F.data == "stock")
async def cb_stock(q: CallbackQuery):
    await show(q, t.STOCK, kb.inner(extra=[
        [("🚘 Наличие на сайте", ("url", c.SITE_STOCK))],
        [("📣 #вналичии в канале", ("url", c.TG_HASHTAG_STOCK))],
    ]))


@router.callback_query(F.data == "brought")
async def cb_brought(q: CallbackQuery):
    await show(q, t.BROUGHT, kb.inner(extra=[
        [("📸 Смотреть привезённое", ("url", c.SITE_BROUGHT))],
    ]))


@router.callback_query(F.data == "reviews")
async def cb_reviews(q: CallbackQuery):
    await show(q, t.REVIEWS, kb.inner(extra=[
        [("🗺 Отзывы в 2ГИС", ("url", c.MAP_2GIS))],
        [("⭐️ Отзывы на сайте", ("url", c.SITE_REVIEWS))],
    ]))


@router.callback_query(F.data == "contacts")
async def cb_contacts(q: CallbackQuery):
    await show(q, t.CONTACTS, kb.contacts_kb())


@router.callback_query(F.data == "social")
async def cb_social(q: CallbackQuery):
    await show(q, t.SOCIAL, kb.social_kb())


@router.callback_query(F.data == "faq")
async def cb_faq(q: CallbackQuery):
    await show(q, t.FAQ, kb.inner())


# ─────────────────────────── ЗАЯВКА (FSM) ───────────────────────────
class Req(StatesGroup):
    name = State()
    phone = State()
    what = State()
    budget = State()


@router.callback_query(F.data == "request")
async def cb_request(q: CallbackQuery, state: FSMContext):
    await state.set_state(Req.name)
    await q.message.answer(t.REQUEST_START, reply_markup=ReplyKeyboardRemove())
    await q.answer()


@router.message(Command("zayavka"))
async def cmd_request(m: Message, state: FSMContext):
    await state.set_state(Req.name)
    await m.answer(t.REQUEST_START, reply_markup=ReplyKeyboardRemove())


@router.message(Req.name)
async def req_name(m: Message, state: FSMContext):
    await state.update_data(name=m.text)
    await state.set_state(Req.phone)
    await m.answer(t.REQUEST_PHONE, reply_markup=kb.phone_request_kb())


@router.message(Req.phone, F.contact)
async def req_phone_contact(m: Message, state: FSMContext):
    await state.update_data(phone=m.contact.phone_number)
    await state.set_state(Req.what)
    await m.answer(t.REQUEST_WHAT, reply_markup=ReplyKeyboardRemove())


@router.message(Req.phone)
async def req_phone_text(m: Message, state: FSMContext):
    await state.update_data(phone=m.text)
    await state.set_state(Req.what)
    await m.answer(t.REQUEST_WHAT, reply_markup=ReplyKeyboardRemove())


@router.message(Req.what)
async def req_what(m: Message, state: FSMContext):
    await state.update_data(what=m.text)
    await state.set_state(Req.budget)
    await m.answer(t.REQUEST_BUDGET)


@router.message(Req.budget)
async def req_budget(m: Message, state: FSMContext, bot: Bot):
    await state.update_data(budget=m.text)
    d = await state.get_data()
    await state.clear()

    uname = f"@{m.from_user.username}" if m.from_user.username else "—"
    card = (
        "🔔 <b>Новая заявка из Telegram-бота</b>\n\n"
        f"👤 Имя: {d.get('name')}\n"
        f"📞 Телефон: {d.get('phone')}\n"
        f"🚗 Интерес: {d.get('what')}\n"
        f"💰 Бюджет / город: {d.get('budget')}\n\n"
        f"TG: {uname} (id {m.from_user.id})"
    )
    for admin in c.ADMIN_IDS:
        try:
            await bot.send_message(admin, card)
        except Exception as e:
            logging.warning("Не отправилось админу %s: %s", admin, e)

    await m.answer(t.REQUEST_DONE, reply_markup=kb.main_menu())


# ─────────────────────────── ЛЮБОЙ ДРУГОЙ ТЕКСТ ───────────────────────────
@router.message()
async def fallback(m: Message):
    await m.answer(
        "Я бот-визитка Union Auto 🙂 Всё самое важное — в меню ниже.\n"
        f"Если нужен живой человек — напишите @{c.ADMIN_USERNAME} или позвоните {c.PHONE}.",
        reply_markup=kb.main_menu(),
    )


# ─────────────────────────── ЗАПУСК ───────────────────────────
async def main():
    bot = Bot(
        token=c.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)

    await bot.set_my_commands([
        BotCommand(command="start", description="Главное меню"),
        BotCommand(command="menu", description="Меню разделов"),
        BotCommand(command="zayavka", description="Бесплатный подбор"),
        BotCommand(command="help", description="Частые вопросы"),
    ])

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
