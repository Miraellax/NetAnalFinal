from .component import ApplicationComponent
import telegram as tg
import telegram.ext as tge

class MainMenuComponent(ApplicationComponent):
    def __init__(self, context):
        super().__init__(context)
        self.add_handler(tge.CommandHandler('start', self.wrap_callback(self.open_menu)), -1)
        self.add_handler(tge.MessageHandler(tge.filters.Text(['Главное меню']), self.wrap_callback(self.open_menu)), 0)
        self.add_handler(tge.MessageHandler(tge.filters.TEXT, self.wrap_callback(self.unknown_command_in_state)), 1000)

        self.user_menu_markup = tg.ReplyKeyboardMarkup([
            [tg.KeyboardButton('Поиск по названию')]
        ], resize_keyboard=True, one_time_keyboard=True)

        self.admin_menu_markup = tg.ReplyKeyboardMarkup([
            [tg.KeyboardButton('Поиск по названию')]
        ], resize_keyboard=True, one_time_keyboard=True)

    async def open_menu(self, update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
        user_state = self._context.get_user_state(update.effective_user.id) #type: ignore
        user_state.current_action = ''
        async with self._context.database.cursor() as cur:
            is_admin = await (await cur.execute("SELECT * FROM admins WHERE userid = ?", (update.effective_user.id,))).fetchone() is not None #type: ignore
        user_state.last_markup = self.admin_menu_markup if is_admin else self.user_menu_markup
        await update.message.reply_text('Выбери действие:', reply_markup=user_state.last_markup) #type: ignore
        raise tge.ApplicationHandlerStop()

    async def unknown_command_in_state(self, update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
        user_state = self._context.get_user_state(update.effective_user.id) #type: ignore
        await update.message.reply_text('Я не понял. Попробуй ещё раз:', reply_markup=user_state.last_markup)