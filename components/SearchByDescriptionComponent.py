from .component import ApplicationComponent
import telegram as tg
import telegram.ext as tge
from .CreatureCard import get_creature_card_data, create_card_markup

class SearchByDescriptionComponent(ApplicationComponent):
    def __init__(self, context):
        super().__init__(context)
        self.add_handler(tge.MessageHandler(tge.filters.Text(['Поиск по запросу']), self.wrap_callback(self.find_by_description)), 5)
        self.add_handler(tge.MessageHandler(tge.filters.TEXT, self.wrap_callback(self.find_by_description_query)), 6)
        self.add_handler(tge.MessageHandler(tge.filters.TEXT, self.wrap_callback(self.open_list_item)), 7)
        self.add_handler(tge.MessageHandler(tge.filters.Text(['Назад']), self.wrap_callback(self.back_to_list)), 8)

    async def find_by_description(self, update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
        user_state = self._context.get_user_state(update.effective_user.id) #type: ignore
        if user_state.current_action != '':
            return
        user_state.current_action = 'find_by_description__query'
        await update.message.reply_text('Что ищем?')
        raise tge.ApplicationHandlerStop()

    async def find_by_description_query(self, update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
        user_state = self._context.get_user_state(update.effective_user.id) #type: ignore
        if user_state.current_action != 'find_by_description__query':
            return
        #Текст запроса
        text = update.message.text
        #Сформировать список айдишников
        options = [1, 2, 3]
        user_state.dynamic_state['find_by_description__items'] = options
        async with self._context.database.cursor() as cur:
            result = await cur.execute(
                f"SELECT name, name_translated, id FROM creatures WHERE id IN ({','.join(['?']*len(options))})",
                options
            )
            rows = sorted(await result.fetchall(), key=lambda x: options.index(x['id']))
            markup = [[f'{i+1}. {x['name_translated']} [{x['name']}]'] for i, x in enumerate(rows)]
            markup.append(['Главное меню'])
            user_state.last_markup = tg.ReplyKeyboardMarkup(markup, resize_keyboard=True, one_time_keyboard=True)
            user_state.current_action = 'find_by_description__list'
            await update.message.reply_text('Про кого-то поподробнее?', reply_markup=user_state.last_markup)
        raise tge.ApplicationHandlerStop()
    
    async def open_list_item(self, update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
        user_state = self._context.get_user_state(update.effective_user.id) #type: ignore
        if user_state.current_action != 'find_by_description__list':
            return
        try:
            text : str = update.message.text
            if '.' not in text:
                return
            num = text.split('.')[0]
            num = int(num) - 1
            if num < 0 or num > 9:
                return
            id = user_state.dynamic_state['find_by_description__items'][num]
            user_state.last_markup = tg.ReplyKeyboardMarkup([
                ['Назад'],
                ['Главное меню']
            ], resize_keyboard=True, one_time_keyboard=True)
            user_state.current_action = 'find_by_description__card'
            async with self._context.database.cursor() as cur:
                data = await get_creature_card_data(id, cur)
                await update.message.reply_text(create_card_markup(data), reply_markup=user_state.last_markup)
            raise tge.ApplicationHandlerStop()
        except ValueError:
            return
        
    async def back_to_list(self, update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
        user_state = self._context.get_user_state(update.effective_user.id) #type: ignore
        if user_state.current_action != 'find_by_description__card':
            return
        options = user_state.dynamic_state['find_by_description__items']
        async with self._context.database.cursor() as cur:
            result = await cur.execute(
                f"SELECT name, name_translated, id FROM creatures WHERE id IN ({','.join(['?']*len(options))})",
                options
            )
            rows = sorted(await result.fetchall(), key=lambda x: options.index(x['id']))
            markup = [[f'{i+1}. {x['name_translated']} [{x['name']}]'] for i, x in enumerate(rows)]
            markup.append(['Главное меню'])
            user_state.last_markup = tg.ReplyKeyboardMarkup(markup, resize_keyboard=True, one_time_keyboard=True)
            user_state.current_action = 'find_by_description__list'
            await update.message.reply_text('Про кого-то поподробнее?', reply_markup=user_state.last_markup)
        raise tge.ApplicationHandlerStop()