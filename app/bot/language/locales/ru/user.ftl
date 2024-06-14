start = Добро пожаловать, { $name }!

post-danbooru = { $tags ->
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
