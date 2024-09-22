from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator


def translator_hub() -> TranslatorHub:
    t_hub: TranslatorHub = TranslatorHub(
        locales_map={
            'ru': ('ru',)
        },
        translators=[
            FluentTranslator(
                locale='ru',
                translator=FluentBundle.from_files(
                    locale='ru-RU',
                    filenames=[
                        "app/bot/language/locales/ru/user.ftl",
                        "app/bot/language/locales/ru/admin.ftl",
                        "app/bot/language/locales/ru/error.ftl"
                    ],
                    use_isolating=False
                )
            )
        ],
        root_locale='ru'
    )
    return t_hub
