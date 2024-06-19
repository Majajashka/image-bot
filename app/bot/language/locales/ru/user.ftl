start = Добро пожаловать, { $name }!

danbooru-post = { $tags ->
        [0] {""}
        *[other]{""}
                <b>Tags</b>: { $tags }
    }{ $rating ->
        [0] {""}
        *[other]{""}
                <b>Rating</b>: { $rating }
    }{ $score ->
        [0] {""}
        *[other]{""}
                <b>Score</b>: { $score }
    }{ $url ->
        [0] {""}
        *[other]{""}
                <b>Url</b>: { $url }
    }

danbooru-tags = <code>{ $tag }</code>: { $post_count }
chat_bind = Чат был успешно привязан!
