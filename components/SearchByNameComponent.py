from .component import ApplicationComponent
import telegram as tg
import telegram.ext as tge
import math
from .CreatureCard import get_creature_card_data, create_card_markup

class SearchByNameComponent(ApplicationComponent):
    def __init__(self, context):
        super().__init__(context)
        self.add_handler(tge.MessageHandler(tge.filters.Text(['Поиск по названию']), self.wrap_callback(self.find_by_name)), 0)
        self.add_handler(tge.MessageHandler(tge.filters.Text(['Назад']), self.wrap_callback(self.back_to_list)), 1)
        self.add_handler(tge.MessageHandler(tge.filters.Text(['Вперёд', 'Назад']), self.wrap_callback(self.find_by_name_list)), 2)
        self.add_handler(tge.MessageHandler(tge.filters.TEXT, self.wrap_callback(self.open_list_item)), 3)
        self.add_handler(tge.MessageHandler(tge.filters.TEXT, self.wrap_callback(self.find_by_name_query)), 4)

    async def find_by_name(self, update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
        user_state = self._context.get_user_state(update.effective_user.id) #type: ignore
        if user_state.current_action != '':
            return
        user_state.current_action = 'find_by_name__query'
        user_state.last_markup = None
        await update.message.reply_text('Кого ищем?') #type: ignore
        raise tge.ApplicationHandlerStop()
    
    async def find_by_name_list(self, update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
        user_state = self._context.get_user_state(update.effective_user.id) #type: ignore
        if user_state.current_action != 'find_by_name__list':
            return
        user_state.dynamic_state['find_by_name__page'] = (
            user_state.dynamic_state['find_by_name__page']
            + (1 if update.message.text == 'Вперёд' else -1)
        )
        async with self._context.database.cursor() as cur:
            search_text = f'%{user_state.dynamic_state['find_by_name__text']}%'
            result = await cur.execute(
                "SELECT name, name_translated, id FROM creatures WHERE name LIKE ? OR name_translated LIKE ? ORDER BY name_translated LIMIT 10 OFFSET ?",
                (search_text, search_text, user_state.dynamic_state['find_by_name__page']*10)
            )
            rows = list(await result.fetchall())
            markup = [[f'{i+1}. {x['name_translated']} [{x['name']}]'] for i, x in enumerate(rows)]
            user_state.dynamic_state['find_by_name__items'] = [x['id'] for x in rows]
            if user_state.dynamic_state['find_by_name__page'] > 0:
                markup.append(['Назад'])
            if user_state.dynamic_state['find_by_name__page'] < user_state.dynamic_state['find_by_name__total_pages'] - 1:
                markup.append(['Вперёд'])
            markup.append(['Главное меню'])
            user_state.last_markup = tg.ReplyKeyboardMarkup(markup, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text(
                f"Страница {user_state.dynamic_state['find_by_name__page'] + 1}/{user_state.dynamic_state['find_by_name__total_pages']}\n",
                reply_markup=user_state.last_markup
            )
            
        raise tge.ApplicationHandlerStop()
    
    async def open_list_item(self, update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
        try:
            user_state = self._context.get_user_state(update.effective_user.id) #type: ignore
            text : str = update.message.text
            if '.' not in text:
                return
            num = text.split('.')[0]
            num = int(num) - 1
            if num < 0 or num > 9:
                return
            id = user_state.dynamic_state['find_by_name__items'][num]
            user_state.last_markup = tg.ReplyKeyboardMarkup([
                ['Назад'],
                ['Главное меню']
            ], resize_keyboard=True, one_time_keyboard=True)
            user_state.current_action = 'find_by_name__card'
            async with self._context.database.cursor() as cur:
                data = await get_creature_card_data(id, cur)
                await update.message.reply_text(create_card_markup(data), reply_markup=user_state.last_markup)
            raise tge.ApplicationHandlerStop()
        except ValueError:
            return
    
    async def back_to_list(self, update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
        user_state = self._context.get_user_state(update.effective_user.id) #type: ignore
        if user_state.current_action != 'find_by_name__card':
            return
        user_state.current_action = 'find_by_name__list'
        async with self._context.database.cursor() as cur:
            search_text = f'%{user_state.dynamic_state['find_by_name__text']}%'
            result = await cur.execute(
                "SELECT name, name_translated, id FROM creatures WHERE name LIKE ? OR name_translated LIKE ? ORDER BY name_translated LIMIT 10 OFFSET ?",
                (search_text, search_text, user_state.dynamic_state['find_by_name__page']*10)
            )
            rows = list(await result.fetchall())
            markup = [[f'{i+1}. {x['name_translated']} [{x['name']}]'] for i, x in enumerate(rows)]
            user_state.dynamic_state['find_by_name__items'] = [x['id'] for x in rows]
            if user_state.dynamic_state['find_by_name__page'] > 0:
                markup.append(['Назад'])
            if user_state.dynamic_state['find_by_name__page'] < user_state.dynamic_state['find_by_name__total_pages'] - 1:
                markup.append(['Вперёд'])
            markup.append(['Главное меню'])
            user_state.last_markup = tg.ReplyKeyboardMarkup(markup, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text(
                f"Страница {user_state.dynamic_state['find_by_name__page'] + 1}/{user_state.dynamic_state['find_by_name__total_pages']}\n",
                reply_markup=user_state.last_markup
            )
        raise tge.ApplicationHandlerStop()

    async def find_by_name_query(self, update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
        user_state = self._context.get_user_state(update.effective_user.id) #type: ignore
        if user_state.current_action != 'find_by_name__query':
            return
        async with self._context.database.cursor() as cur:
            search_text = f'%{update.message.text}%'
            result = await cur.execute(
                "SELECT COUNT(*) FROM creatures WHERE name LIKE ? OR name_translated LIKE ? ORDER BY name_translated",
                (search_text, search_text)
            )
            pages = math.ceil((await result.fetchone())[0] / 10) #type: ignore
            if pages == 0:
                user_state.last_markup = tg.ReplyKeyboardMarkup([
                    ['Главное меню']
                ], resize_keyboard=True, one_time_keyboard=True)
                await update.message.reply_text('Ничего не нашлось', reply_markup=user_state.last_markup)
                user_state.current_action = ''
                return

            user_state.dynamic_state['find_by_name__total_pages'] = pages
            user_state.current_action = 'find_by_name__list'
            user_state.dynamic_state['find_by_name__text'] = update.message.text #type: ignore
            user_state.dynamic_state['find_by_name__page'] = 0
            result = await cur.execute(
                "SELECT name, name_translated, id FROM creatures WHERE name LIKE ? OR name_translated LIKE ? ORDER BY name_translated LIMIT 10",
                (search_text, search_text)
            )
            rows = list(await result.fetchall())
            markup = [[f'{i+1}. {x['name_translated']} [{x['name']}]'] for i, x in enumerate(rows)]
            user_state.dynamic_state['find_by_name__items'] = [x['id'] for x in rows]
            if user_state.dynamic_state['find_by_name__total_pages'] > 1:
                markup.append(['Вперёд'])
            markup.append(['Главное меню'])
            user_state.last_markup = tg.ReplyKeyboardMarkup(markup, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text(
                f"Страница {user_state.dynamic_state['find_by_name__page'] + 1}/{user_state.dynamic_state['find_by_name__total_pages']}",
                reply_markup=user_state.last_markup
            )
        raise tge.ApplicationHandlerStop()