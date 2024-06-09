start = Добро пожаловать, { $name }!

api-danbooru_post =
    { $tags ->
        <b>Tags</b>: { $tags }
    }
    { $score ->
        <b>Score</b>: { $score }
    }
    { $url ->
        <b>Url</b>: { $url }
    }
    { $rating ->
        <b>Rating</b>: { $rating }
    }