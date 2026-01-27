# Handlers package
from .start import register_start_handlers
from .chat import register_chat_handlers
from .subscription import register_subscription_handlers
from .admin import register_admin_handlers
from .vagal_assessment import get_vagal_assessment_handler


def register_all_handlers(application):
    """Регистрирует все обработчики команд."""
    register_start_handlers(application)
    register_subscription_handlers(application)
    register_admin_handlers(application)
    
    # Вагусный профиль - ConversationHandler
    application.add_handler(get_vagal_assessment_handler())
    
    register_chat_handlers(application)  # Должен быть последним (ловит все текстовые сообщения)
