# -*- coding: utf-8 -*-
"""Клавиатуры (кнопки) бота Union Auto."""

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
import config as c


def ikb(rows) -> InlineKeyboardMarkup:
    """rows = [[(текст, callback_data | ('url', ссылка))], ...]"""
    kb = []
    for row in rows:
        line = []
        for text, data in row:
            if isinstance(data, tuple) and data[0] == "url":
                line.append(InlineKeyboardButton(text=text, url=data[1]))
            else:
                line.append(InlineKeyboardButton(text=text, callback_data=data))
        kb.append(line)
    return InlineKeyboardMarkup(inline_keyboard=kb)


BACK = [("⬅️ В главное меню", "menu")]


def main_menu() -> InlineKeyboardMarkup:
    return ikb([
        [("🏢 О компании", "about")],
        [("🚗 Что мы возим", "cats"), ("🛣 Как проходит покупка", "path")],
        [("🎁 Акции и спецпредложения", "promo")],
        [("💳 Автокредит и лизинг", "finance")],
        [("🚘 В наличии сейчас", "stock"), ("📸 Уже привезли", "brought")],
        [("⭐️ Отзывы", "reviews"), ("❓ Частые вопросы", "faq")],
        [("📍 Контакты и адрес", "contacts"), ("🌐 Соцсети", "social")],
        [("✍️ Бесплатный подбор", "request")],
        [("💬 Написать менеджеру", ("url", f"https://t.me/{c.ADMIN_USERNAME}"))],
    ])


def cats_menu() -> InlineKeyboardMarkup:
    return ikb([
        [("🚙 Легковые автомобили", "cars")],
        [("🚛 Грузовики и коммерческий", "trucks")],
        [("🏗 Спецтехника", "machinery")],
        BACK,
    ])


def path_menu() -> InlineKeyboardMarkup:
    return ikb([
        [("🚙 Легковые авто", "path_cars")],
        [("🚛 Грузовики и спецтехника", "path_trucks")],
        BACK,
    ])


def promo_menu() -> InlineKeyboardMarkup:
    return ikb([
        [("🎖 −50% на комиссию: СВО, многодетные, инвалидность", "promo_social")],
        [("👥 Реферальная программа 20 000 ₽", "promo_ref")],
        [("🎁 Бонусы клиентам", "promo_bonus")],
        [("💳 Автокредит и лизинг", "finance")],
        BACK,
    ])


def inner(*, back_to: str = "menu", extra=None) -> InlineKeyboardMarkup:
    rows = list(extra or [])
    rows.append([("✍️ Бесплатный подбор", "request")])
    rows.append([("💬 Написать менеджеру", ("url", f"https://t.me/{c.ADMIN_USERNAME}"))])
    rows.append([("⬅️ Назад", back_to)])
    return ikb(rows)


def contacts_kb() -> InlineKeyboardMarkup:
    return ikb([
        [("🗺 Открыть на карте (2ГИС)", ("url", c.MAP_2GIS))],
        [("💬 Написать в Telegram", ("url", f"https://t.me/{c.ADMIN_USERNAME}"))],
        [("🟢 WhatsApp", ("url", c.WHATSAPP))],
        [("🔵 MAX", ("url", c.MAX_MESSENGER))],
        [("🌐 Сайт", ("url", c.SITE))],
        BACK,
    ])


def social_kb() -> InlineKeyboardMarkup:
    return ikb([
        [("📣 Telegram-канал", ("url", c.TG_CHANNEL))],
        [("📸 Instagram", ("url", c.INSTAGRAM)), ("🔷 ВКонтакте", ("url", c.VK))],
        [("▶️ YouTube", ("url", c.YOUTUBE)), ("🎬 RUTUBE", ("url", c.RUTUBE))],
        [("🔵 MAX", ("url", c.MAX_MESSENGER)), ("🌐 Сайт", ("url", c.SITE))],
        BACK,
    ])


def phone_request_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Отправить мой номер", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
