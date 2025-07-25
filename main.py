import discord
import os
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
from discord.utils import get
from datetime import datetime
import re

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

AUTO_ROLE_ID = 1396072475053265008
WELCOME_CHANNEL_ID = 1396082261245296700

COMMAND_ROLES = {
    "rules": 1396075460294737941,    
    "guide": 1396075460294737941,    
    "ranks": 1396075460294737941,    
    "news": 1396075460294737941,     
    "events": 1396075460294737941,   
    "fpl_application": 1396075460294737941  
}

def has_command_role(interaction: discord.Interaction, command_name: str) -> bool:
    required_role_id = COMMAND_ROLES.get(command_name)
    if not required_role_id:
        return False
    
    return any(role.id == required_role_id for role in interaction.user.roles)

RULES = {
    "ru": {
        "title": "📜 Официальные правила сервера RankPush",
        "description": (
            "Добро пожаловать на RankPush! Перед началом игры обязательно ознакомьтесь с правилами. "
            "Нарушение данных правил влечёт дисциплинарные меры вплоть до блокировки."
        ),
        "fields": [
            ("⚖️ 1. Общие нормы поведения",
             "Уважайте всех участников. Запрещены любые формы оскорблений, провокаций и дискриминации."),
            ("❌ 2. Использование запрещённого ПО",
             "Читы, скрипты и стороннее ПО строго запрещены. Моментальный пожизненный бан без предупреждений."),
            ("❌ 3. VPN и обход блокировок",
             "Использование VPN или прокси для входа на сервер запрещено и карается мутом или киком."),
            ("⚠️ 4. Эксплуатация багов и уязвимостей",
             "Любое намеренное использование багов — строго запрещено. За первое нарушение — предупреждение, далее — временные блокировки."),
            ("🚫 5. Запрет на политические и конфликтные темы",
             "Обсуждение политики, войны и иных конфликтных тем запрещено. Наказание — мут на 24 часа."),
            ("🔥 6. Токсичность и токсичное поведение",
             "Оскорбления, троллинг, провокации и токсичность запрещены. Последствия — от предупреждения до бана."),
            ("💬 7. Спам и флуд",
             "Запрещён массовый спам, флуд и повторяющиеся сообщения. Наказание — мут на 2 часа."),
            ("🔞 8. Новые аккаунты и активность",
             "Аккаунты Discord младше 6 месяцев должны иметь минимум 400 игр на Faceit для допуска."),
            ("🎮 9. Организация матчей",
             "Хостинг матчей осуществляет капитан первой команды. Пароль для Faceit — **0171**."),
            ("📢 10. Коммуникация и голосовые каналы",
             "В голосовых каналах запрещены крики, оскорбления и агрессивное поведение."),
            ("🤖 11. Использование ботов",
             "Используйте ботов согласно инструкциям. Злоупотребление и спам ботами запрещены."),
            ("🚫 12. Реклама и ссылки",
             "Любая реклама без одобрения администрации запрещена."),
            ("🔒 13. Конфиденциальность",
             "Запрещено разглашать личные данные других участников без их согласия."),
            ("📋 14. Ответственность администрации",
             "Администрация сервера имеет право принимать решения по модерации и блокировкам. Решения являются окончательными.")
        ],
        "footer": "Спасибо за соблюдение правил и поддержку профессиональной атмосферы на RankPush!"
    },
    "en": {
        "title": "📜 Official RankPush Server Rules",
        "description": (
            "Welcome to RankPush! Please read the rules carefully before playing. "
            "Violations will result in disciplinary actions, including bans."
        ),
        "fields": [
            ("⚖️ 1. General Conduct",
             "Respect all members. Any form of insults, provocation, or discrimination is forbidden."),
            ("❌ 2. Use of Forbidden Software",
             "Cheats, scripts, and third-party software are strictly prohibited. Immediate permanent ban without warnings."),
            ("❌ 3. VPN and Bypass Methods",
             "Using VPN or proxies to access the server is prohibited and may result in mute or kick."),
            ("⚠️ 4. Exploiting Bugs and Vulnerabilities",
             "Intentional exploitation of bugs is forbidden. First offense — warning; subsequent offenses — temporary bans."),
            ("🚫 5. No Politics or Conflict Topics",
             "Discussion of politics, war, or other conflict topics is banned. Penalty — 24-hour mute."),
            ("🔥 6. Toxicity and Harassment",
             "Insults, trolling, provocations, and toxic behavior are banned. Consequences range from warnings to bans."),
            ("💬 7. Spam and Flood",
             "Excessive spam, flooding, and repetitive messages are forbidden. Penalty — 2-hour mute."),
            ("🔞 8. New Accounts and Activity",
             "Discord accounts younger than 6 months must have at least 400 Faceit matches to be allowed."),
            ("🎮 9. Match Organization",
             "Matches are hosted by the captain of the first team. Faceit password is **0171**."),
            ("📢 10. Communication and Voice Channels",
             "No shouting, insults, or aggressive behavior in voice channels."),
            ("🤖 11. Bot Usage",
             "Use bots according to instructions. Bot abuse and spam are forbidden."),
            ("🚫 12. Advertising and Links",
             "Advertising without admin approval is prohibited."),
            ("🔒 13. Privacy",
             "Do not share personal data of other members without consent."),
            ("📋 14. Administration Responsibility",
             "Server admins have the right to moderate and ban. Decisions are final.")
        ],
        "footer": "Thank you for following the rules and supporting a professional environment at RankPush!"
    }
}


GUIDE = {
    "uk": {
        "title": "🧠 Гайд по Faceit-серверу RankPush",
        "description": (
            "Приветствую вас на Faceit!\n"
            "Сейчас вы узнаете, как играть с новым ботом пошагово."
        ),
        "fields": [
            ("🎧 1. Зайди в войс и чат", "Например, вы зашли в voice **2v2**, тогда у вас появится чат **2v2**."),
            ("🔘 2. Нажмите 'Join Queue'", "В чате нажмите кнопку **Join Queue** и ожидайте других игроков."),
            ("👥 3. Когда собрались игроки", "После того как нужное количество игроков в очереди — выбирается режим распределения команд."),
            ("🎯 4. Режимы команд", (
                "**Balanced** — команды распределяются по сбалансированному ELO.\n"
                "**2 top rated players** — выбираются 2 капитана с самым высоким ELO, и они по очереди выбирают игроков."
            )),
            ("🚪 5. Отмена очереди", "Если вы передумали — нажмите **Leave Queue**."),
            ("🔄 6. Повторная игра", "После окончания игры можно нажать **Requeue** — и вы снова в очереди."),
            ("🎙 7. Общение в войсе", "Ведите себя уважительно, не кричите, не перебивайте других игроков."),
            ("🆘 8. Возникли проблемы?", "Обратитесь в чат **#support** или напишите модератору."),
            ("🌟 Советы новичкам", (
                "- Не бойся спрашивать.\n"
                "- Следи за очередью в чате.\n"
                "- Соблюдай правила, будь вежливым и играй в удовольствие 🎮"
            ))
        ],
        "footer": "Спасибо за внимание, удачных вам игр!"
    },
    "en": {
        "title": "🧠 Faceit Bot Guide (RankPush)",
        "description": (
            "Welcome to Faceit!\n"
            "Here’s a simple step-by-step guide on how to play using the new bot:"
        ),
        "fields": [
            ("🎧 1. Join Voice & Chat", "Example: join the **2v2 voice** channel and you'll see the **2v2 chat** appear."),
            ("🔘 2. Click 'Join Queue'", "Press the **Join Queue** button and wait for other players."),
            ("👥 3. Queue fills up", "Once the right number of players has joined, you’ll select a **team selection mode**."),
            ("🎯 4. Team Modes", (
                "**Balanced** — teams are auto-distributed evenly by ELO.\n"
                "**2 top rated players** — top 2 ELO players become captains and pick teams in turns."
            )),
            ("🚪 5. Leaving the queue", "Click **Leave Queue** if you want to exit."),
            ("🔄 6. Replay", "Press **Requeue** after the match to play again."),
            ("🎙 7. Voice chat behavior", "Be respectful, avoid yelling or interrupting others."),
            ("🆘 8. Need help?", "Ask in **#support** or contact a moderator."),
            ("🌟 Tips for newcomers", (
                "- Don’t be afraid to ask.\n"
                "- Watch the chat queue.\n"
                "- Follow rules, be friendly, and enjoy the game 🎮"
            ))
        ],
        "footer": "Thanks for your attention and good luck!"
    }
}

RANKS = {
    "uk": {
        "title": "🏆 Система уровней RankPush",
        "description": (
            "На нашем сервере действует система уровней — играй чаще, показывай результат, и ты поднимешься вверх!\n\n"
            "Каждый уровень отражает твой вклад и активность. Повышайся, чтобы получить уважение, доступ к привилегиям и крутые роли!"
        ),
        "fields": [
            ("🥉 Level 1 — Новичок", "👤 Требуется: **0+ ELO**\nТы только начал путь — впереди большие матчи!"),
            ("🥈 Level 2 — Игрок", "🎯 Требуется: **100+ ELO**\nНабрал первые победы, продолжаем подниматься."),
            ("🥈 Level 3 — Активист", "⚔️ Требуется: **200+ ELO**\nСтабильный игрок, уже чувствуешь Faceit-движ."),
            ("🥇 Level 4 — Стример", "📺 Требуется: **350+ ELO**\nИграешь красиво — пора делиться хайлайтами."),
            ("🥇 Level 5 — Надежный", "🛡️ Требуется: **450+ ELO**\nКоманды уважают тебя, часто берут в стак."),
            ("🏅 Level 6 — Полупро", "🔥 Требуется: **600+ ELO**\nИграешь на уровне. Готов к серьёзным боям."),
            ("🏅 Level 7 — Капитан", "🧠 Требуется: **800+ ELO**\nУмеешь лидировать, грамотно собираешь состав."),
            ("🎖️ Level 8 — Легенда", "🌟 Требуется: **1000+ ELO**\nИмя твоё уже известно в каналах. Играют с уважением."),
            ("🎖️ Level 9 — Элита", "💎 Требуется: **1300+ ELO**\nВысший класс. Лучшие хотят в твою команду."),
            ("👑 Level 10 — Грандмастер", 
 "🏆 Требуется: **2000+ ELO**\n"
 "Абсолют. Ты — икона RankPush.\n"
 "Если продолжишь в том же духе — следующим шагом может стать **FPL-C** или даже **FPL**. "
 "Твоя карьера только начинается!")
        ],
        "footer": "Набирай ELO, прокачивай левел и становись легендой нашего сервера!"
    },
    "en": {
        "title": "🏆 RankPush Level System",
        "description": (
            "Our server uses a progressive level system — the more you play and win, the higher you climb!\n\n"
            "Each level reflects your experience and commitment. Unlock recognition, access special roles, and show your worth!"
        ),
        "fields": [
            ("🥉 Level 1 — Newcomer", "👤 Required: **0+ ELO**\nJust getting started — the journey begins!"),
            ("🥈 Level 2 — Player", "🎯 Required: **100+ ELO**\nYou've gained some wins. Keep pushing!"),
            ("🥈 Level 3 — Active", "⚔️ Required: **200+ ELO**\nYou're becoming consistent. Great job!"),
            ("🥇 Level 4 — Streamer", "📺 Required: **350+ ELO**\nYou play well — start showing your skills!"),
            ("🥇 Level 5 — Trusted", "🛡️ Required: **450+ ELO**\nTeams trust you. You're always welcome."),
            ("🏅 Level 6 — Semi-Pro", "🔥 Required: **600+ ELO**\nSolid skills. Ready for real challenges."),
            ("🏅 Level 7 — Captain", "🧠 Required: **800+ ELO**\nYou lead the team and make smart picks."),
            ("🎖️ Level 8 — Legend", "🌟 Required: **1000+ ELO**\nYour name is known. People respect your game."),
            ("🎖️ Level 9 — Elite", "💎 Required: **1300+ ELO**\nTop-tier player. Everyone wants you on their team."),
            ("👑 Level 10 — Grandmaster", 
 "🏆 Required: **2000+ ELO**\n"
 "The pinnacle. You are the icon of RankPush.\n"
 "Keep grinding — your next step might be **FPL-C** or even **FPL**. "
 "Your career is just beginning!")
        ],
        "footer": "Grind ELO, level up, and become a true server legend!"
    }
}




ALLOWED_ROLE_IDS = [1396075460294737941]  

NEWS_CHANNEL_ID = 1396077313237585990

BASE_NEWS = {
    "en": {
        "title": "📢 Announcements & News",
        "description": (
            "This section features the **latest updates**, bot improvements, tournaments, "
            "and important Faceit community news.\n"
            "⚠️ Each announcement appears as a **separate embed** message."
        ),
        "fields": [],
        "footer": "🔔 Stay tuned for updates — don’t miss anything!"
    },
    "uk": {
        "title": "📢 Объявления и новости",
        "description": (
            "Здесь публикуются **последние обновления**, улучшения бота, турниры "
            "и важные новости нашего Faceit-сообщества.\n"
            "⚠️ Каждое новое объявление публикуется как **отдельный эмбед**."
        ),
        "fields": [],
        "footer": "🔔 Следите за обновлениями, чтобы ничего не пропустить!"
    }
}


NEWS_ITEMS = []

class NewsModal(Modal, title='Опублікувати новину'):
    news_title = TextInput(label='Заголовок новини', style=discord.TextStyle.short)
    news_content = TextInput(label='Зміст новини', style=discord.TextStyle.long)
    news_image = TextInput(label='Посилання на зображення (необов\'язково)', style=discord.TextStyle.short, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        news_embed = {
            "timestamp": datetime.now().isoformat(),
            "uk": {
                "title": str(self.news_title),
                "description": str(self.news_content),
                "image": str(self.news_image) if self.news_image.value else None
            },
            "en": {
                "title": str(self.news_title),
                "description": str(self.news_content),
                "image": str(self.news_image) if self.news_image.value else None
            }
        }
        
        NEWS_ITEMS.insert(0, news_embed)
        
        if len(NEWS_ITEMS) > 20:
            NEWS_ITEMS.pop()
        
        channel = bot.get_channel(NEWS_CHANNEL_ID)
        if channel:
            if not hasattr(bot, 'main_news_message'):
                main_embed = discord.Embed(
                    title=BASE_NEWS["uk"]["title"],
                    description=BASE_NEWS["uk"]["description"],
                    color=discord.Color.gold()
                )
                main_embed.set_footer(text=BASE_NEWS["uk"]["footer"])
                bot.main_news_message = await channel.send(embed=main_embed)
            
            embed = discord.Embed(
                title=news_embed["uk"]["title"],
                description=news_embed["uk"]["description"],
                color=discord.Color.green(),
                timestamp=datetime.fromisoformat(news_embed["timestamp"])
            )
            
            if news_embed["uk"]["image"]:
                embed.set_image(url=news_embed["uk"]["image"])
            
            await channel.send(embed=embed)
        
        await interaction.response.send_message("✅ Новину успішно опубліковано!", ephemeral=True)

@bot.tree.command(name="news", description="Опублікувати новину")
@commands.has_permissions(administrator=True)
async def news(interaction: discord.Interaction):
    if not has_command_role(interaction, "rules"):
        return await interaction.response.send_message(
            "⛔ У вас немає ролі, необхідної для цієї команди!",
            ephemeral=True
        )
    
    modal = NewsModal()
    await interaction.response.send_modal(modal)

@bot.tree.command(name="shownews", description="Показати останні новини")
async def shownews(interaction: discord.Interaction, count: int = 5):
    if not has_command_role(interaction, "rules"):
        return await interaction.response.send_message(
            "⛔ У вас немає ролі, необхідної для цієї команди!",
            ephemeral=True
        )
    
    count = max(1, min(count, 10))
    
    main_embed = discord.Embed(
        title=BASE_NEWS["uk"]["title"],
        description=BASE_NEWS["uk"]["description"],
        color=discord.Color.gold()
    )
    main_embed.set_footer(text=BASE_NEWS["uk"]["footer"])
    
    await interaction.response.send_message(embed=main_embed)
    
    for news_item in NEWS_ITEMS[:count]:
        embed = discord.Embed(
            title=news_item["uk"]["title"],
            description=news_item["uk"]["description"],
            color=discord.Color.green(),
            timestamp=datetime.fromisoformat(news_item["timestamp"])
        )
        
        if news_item["uk"]["image"]:
            embed.set_image(url=news_item["uk"]["image"])
        
        await interaction.followup.send(embed=embed)

EVENTS_CHANNEL_ID = 1396077442765950976

BASE_EVENTS = {
    "en": {
        "title": "🗓️ Upcoming Events",
        "description": (
            "Here you'll find all upcoming **events**, **tournaments**, and server activities.\n"
            "📌 Each event is posted as a separate message with all the details: time, format, prizes, and how to join."
        ),
        "footer": "✅ Don’t miss out — register and play with us!"
    },
    "uk": {
        "title": "🗓️ Предстоящие события",
        "description": (
            "Здесь публикуются все запланированные **ивенты**, **турниры** и активности сервера.\n"
            "📌 Каждое событие — отдельное сообщение с подробностями: время, формат, призы и условия участия."
        ),
        "footer": "✅ Не упусти шанс — регистрируйся и участвуй вместе с нами!"
    }
}


EVENTS_ITEMS = []

class EventModal(Modal, title='Створити подію'):
    event_name = TextInput(label='Назва події', style=discord.TextStyle.short)
    event_description = TextInput(label='Опис події', style=discord.TextStyle.long)
    event_date = TextInput(label='Дата (ДД.ММ.РРРР)', style=discord.TextStyle.short)
    event_time = TextInput(label='Час (ГГ:ХХ)', style=discord.TextStyle.short)
    event_image = TextInput(label='Посилання на зображення (необов\'язково)', style=discord.TextStyle.short, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            day, month, year = map(int, str(self.event_date).split('.'))
            hour, minute = map(int, str(self.event_time).split(':'))
            event_datetime = datetime(year, month, day, hour, minute)
            
            event_embed = {
                "timestamp": event_datetime.isoformat(),
                "uk": {
                    "title": str(self.event_name),
                    "description": str(self.event_description),
                    "date": f"{day:02d}.{month:02d}.{year}",
                    "time": f"{hour:02d}:{minute:02d}",
                    "image": str(self.event_image) if self.event_image.value else None
                },
                "en": {
                    "title": str(self.event_name),
                    "description": str(self.event_description),
                    "date": f"{day:02d}.{month:02d}.{year}",
                    "time": f"{hour:02d}:{minute:02d}",
                    "image": str(self.event_image) if self.event_image.value else None
                }
            }
            
            EVENTS_ITEMS.append(event_embed)
            EVENTS_ITEMS.sort(key=lambda x: x["timestamp"])
            
            if len(EVENTS_ITEMS) > 30:
                EVENTS_ITEMS.pop(0)
            
            channel = bot.get_channel(EVENTS_CHANNEL_ID)
            if channel:
                if not hasattr(bot, 'main_events_message'):
                    main_embed = discord.Embed(
                        title=BASE_EVENTS["uk"]["title"],
                        description=BASE_EVENTS["uk"]["description"],
                        color=discord.Color.blurple()
                    )
                    main_embed.set_footer(text=BASE_EVENTS["uk"]["footer"])
                    bot.main_events_message = await channel.send(embed=main_embed)
                
                embed = discord.Embed(
                    title=event_embed["uk"]["title"],
                    description=event_embed["uk"]["description"],
                    color=discord.Color.green()
                )
                embed.add_field(name="📅 Дата", value=event_embed["uk"]["date"], inline=True)
                embed.add_field(name="🕒 Час", value=event_embed["uk"]["time"], inline=True)
                
                if event_embed["uk"]["image"]:
                    embed.set_image(url=event_embed["uk"]["image"])
                
                await channel.send(embed=embed)
            
            await interaction.response.send_message("✅ Подію успішно створено!", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Невірний формат дати або часу! Використовуйте ДД.ММ.РРРР для дати та ГГ:ХХ для часу.", ephemeral=True)

@bot.tree.command(name="event", description="Створити нову подію")
@commands.has_permissions(administrator=True)
async def event(interaction: discord.Interaction):
    if not has_command_role(interaction, "rules"):
        return await interaction.response.send_message(
            "⛔ У вас немає ролі, необхідної для цієї команди!",
            ephemeral=True
        )
    
    modal = EventModal()
    await interaction.response.send_modal(modal)

@bot.tree.command(name="events", description="Показати майбутні події")
async def events(interaction: discord.Interaction, count: int = 10):
    if not has_command_role(interaction, "rules"):
        return await interaction.response.send_message(
            "⛔ У вас немає ролі, необхідної для цієї команди!",
            ephemeral=True
        )

    now = datetime.now()
    upcoming_events = [e for e in EVENTS_ITEMS if datetime.fromisoformat(e["timestamp"]) > now]
    
    count = max(1, min(count, 10))
    
    main_embed = discord.Embed(
        title=BASE_EVENTS["uk"]["title"],
        description=BASE_EVENTS["uk"]["description"],
        color=discord.Color.blurple()
    )
    main_embed.set_footer(text=BASE_EVENTS["uk"]["footer"])
    
    await interaction.response.send_message(embed=main_embed)
    
    for event_item in upcoming_events[:count]:
        embed = discord.Embed(
            title=event_item["uk"]["title"],
            description=event_item["uk"]["description"],
            color=discord.Color.green()
        )
        embed.add_field(name="📅 Дата", value=event_item["uk"]["date"], inline=True)
        embed.add_field(name="🕒 Час", value=event_item["uk"]["time"], inline=True)
        
        if event_item["uk"]["image"]:
            embed.set_image(url=event_item["uk"]["image"])
        
        await interaction.followup.send(embed=embed)

class LanguageView(View):
    def __init__(self, content_type):
        super().__init__(timeout=None)
        self.content_type = content_type
        
        uk_button = Button(label="Русский", style=discord.ButtonStyle.primary, custom_id=f"lang_uk_{content_type}")
        en_button = Button(label="English", style=discord.ButtonStyle.primary, custom_id=f"lang_en_{content_type}")
        
        uk_button.callback = self.language_callback
        en_button.callback = self.language_callback
        
        self.add_item(uk_button)
        self.add_item(en_button)
    
    async def language_callback(self, interaction: discord.Interaction):
        lang, content_type = interaction.data["custom_id"].split("_")[1:]
        
        if content_type == "rules":
            content = RULES
        elif content_type == "guide":
            content = GUIDE
        elif content_type == "ranks":
            content = RANKS
        elif content_type == "news":
            content = NEWS_ITEMS
        else:
            content = EVENTS_ITEMS
        
        embed = discord.Embed(
            title=content[lang]["title"],
            description=content[lang]["description"],
            color=discord.Color.gold() if content_type == "news" else discord.Color.blue()
        )
        
        for field_title, field_text in content[lang]["fields"][:1000]:  
            embed.add_field(name=field_title, value=field_text, inline=False)
        
        embed.set_footer(text=content[lang]["footer"])
        
        await interaction.response.edit_message(embed=embed, view=self)

@bot.event
async def on_ready():
    print(f"Бот {bot.user} готовий до роботи!")
    bot.add_view(LanguageView("rules"))
    bot.add_view(LanguageView("guide"))
    bot.add_view(LanguageView("ranks"))
    try:
        synced = await bot.tree.sync()
        print(f"Синхронізовано {len(synced)} команд")
    except Exception as e:
        print(f"Помилка синхронізації: {e}")

@bot.event
async def on_member_join(member):
    role = get(member.guild.roles, id=AUTO_ROLE_ID)
    if role:
        try:
            await member.add_roles(role)
            channel = bot.get_channel(WELCOME_CHANNEL_ID)
            if channel:
                embed = discord.Embed(
                    title=f"Ласкаво просимо, {member.name}!",
                    description=f"Вам видано роль {role.mention}",
                    color=discord.Color.green()
                )
                await channel.send(embed=embed)
        except Exception as e:
            print(f"Помилка: {e}")

@bot.tree.command(name="rules", description="Показати правила серверу")
async def rules(interaction: discord.Interaction):
    if not has_command_role(interaction, "rules"):
        return await interaction.response.send_message(
            "⛔ У вас немає ролі, необхідної для цієї команди!",
            ephemeral=True
        )
    
    embed = discord.Embed(
        title=RULES["uk"]["title"],
        description=RULES["uk"]["description"],
        color=discord.Color.blue()
    )
    
    for field_title, field_text in RULES["uk"]["fields"]:
        embed.add_field(name=field_title, value=field_text, inline=False)
    
    embed.set_footer(text=RULES["uk"]["footer"])
    
    await interaction.response.send_message(embed=embed, view=LanguageView("rules"))

@bot.tree.command(name="guide", description="Як користуватись сервером")
async def guide(interaction: discord.Interaction):
    if not has_command_role(interaction, "rules"):
        return await interaction.response.send_message(
            "⛔ У вас немає ролі, необхідної для цієї команди!",
            ephemeral=True
        )
    
    embed = discord.Embed(
        title=GUIDE["uk"]["title"],
        description=GUIDE["uk"]["description"],
        color=discord.Color.blue()
    )
    
    for field_title, field_text in GUIDE["uk"]["fields"]:
        embed.add_field(name=field_title, value=field_text, inline=False)
    
    embed.set_footer(text=GUIDE["uk"]["footer"])
    
    await interaction.response.send_message(embed=embed, view=LanguageView("guide"))

@bot.tree.command(name="ranks", description="Система рангів серверу")
async def ranks(interaction: discord.Interaction):
    if not has_command_role(interaction, "rules"):
        return await interaction.response.send_message(
            "⛔ У вас немає ролі, необхідної для цієї команди!",
            ephemeral=True
        )
    
    embed = discord.Embed(
        title=RANKS["uk"]["title"],
        description=RANKS["uk"]["description"],
        color=discord.Color.blue()
    )
    
    for field_title, field_text in RANKS["uk"]["fields"]:
        embed.add_field(name=field_title, value=field_text, inline=False)
    
    embed.set_footer(text=RANKS["uk"]["footer"])
    
    await interaction.response.send_message(embed=embed, view=LanguageView("ranks"))

@bot.command()
@commands.has_permissions(administrator=True)
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("✅ Команди синхронізовано!")

bot.run(os.getenv("TOKEN"))
