from .component import ApplicationComponent
import telegram as tg
import telegram.ext as tge

class SearchByNameComponent(ApplicationComponent):
    def __init__(self, context):
        super().__init__(context)
        self.add_handler(tge.MessageHandler(tge.filters.Text(['Поиск по названию']), self.wrap_callback(self.find_by_name)), 0)
        self.add_handler(tge.MessageHandler(tge.filters.TEXT, self.wrap_callback(self.find_by_name_query)), 1)

    async def find_by_name(self, update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
        print('find_by_name')
        user_state = self._context.get_user_state(update.effective_user.id) #type: ignore
        print(user_state.current_action)
        if user_state.current_action != '':
            return
        user_state.current_action = 'find_by_name__query'
        await update.message.reply_text('Кого ищем?') #type: ignore
        print(user_state.current_action)
        raise tge.ApplicationHandlerStop()
    
    async def find_by_name_query(self, update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
        print('find_by_name_query')
        user_state = self._context.get_user_state(update.effective_user.id) #type: ignore
        print(user_state.current_action)
        if user_state.current_action != 'find_by_name__query':
            return
        #user_state.current_action = 'find_by_name__list'
        #user_state.dynamic_state['find_by_name__text'] = update.message.text #type: ignore
        user_state.current_action = ''
        async with self._context.database.cursor() as cur:
            search_text = f'%{update.message.text}%'
            result = await cur.execute("SELECT name, name_translated FROM creatures WHERE name LIKE ? OR name_translated LIKE ? ORDER BY name_translated LIMIT 10", (search_text, search_text))
            await update.message.reply_text("\n".join([f'{x[1]} [{x[0]}]' for x in await result.fetchall()]))