from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Learning Portal</title>

<style>
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                 Arial, sans-serif;
    background: white;
    color: #222;
}

#loading {
    position: fixed;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: white;
    color: #777;
    font-size: 15px;
    z-index: 9999;
}

#main {
    display: none;
}

.notice {
    padding: 10px 15px;
    text-align: center;
    font-size: 13px;
    color: #777;
    background: #f6f6f6;
    border-bottom: 1px solid #eee;
}

.container {
    width: min(100% - 30px, 1000px);
    margin: auto;
    padding: 25px 0 50px;
}

.site-name {
    margin-bottom: 25px;
    font-size: 15px;
    color: #666;
}

h1 {
    margin: 0 0 25px;
    font-size: clamp(25px, 5vw, 38px);
    line-height: 1.3;
}

h2 {
    margin-top: 30px;
    font-size: 20px;
    line-height: 1.5;
}

.description {
    font-size: 16px;
    line-height: 1.8;
    color: #444;
}

.browser {
    margin-top: 35px;
    overflow: hidden;
    border: 1px solid #ddd;
    border-radius: 12px;
    background: white;
    box-shadow: 0 3px 15px rgba(0,0,0,.08);
}

.toolbar {
    display: flex;
    gap: 8px;
    padding: 10px;
    background: #f2f2f2;
    border-bottom: 1px solid #ddd;
}

#url {
    flex: 1;
    min-width: 0;
    height: 42px;
    padding: 0 12px;
    border: 1px solid #ccc;
    border-radius: 7px;
    background: white;
    font-size: 15px;
}

button {
    min-width: 85px;
    height: 42px;
    padding: 0 14px;
    border: none;
    border-radius: 7px;
    background: #333;
    color: white;
    font-size: 14px;
}

.open-new {
    background: #666;
}

#viewer {
    display: block;
    width: 100%;
    height: 650px;
    border: none;
    background: white;
}

#message {
    padding: 12px 15px;
    margin: 0;
    font-size: 13px;
    line-height: 1.6;
    color: #666;
    background: #fafafa;
    border-top: 1px solid #eee;
    display: none;
}

@media (max-width: 600px) {
    .toolbar {
        flex-wrap: wrap;
    }

    #url {
        width: 100%;
        flex-basis: 100%;
    }

    button {
        flex: 1;
    }

    #viewer {
        height: 70vh;
        min-height: 450px;
    }
}
</style>
</head>

<body>

<div id="loading">
    Loading...
</div>

<div id="main">

    <div class="notice">
        Learning Portal
    </div>

    <div class="container">

        <div class="site-name">
            Learning Portal
        </div>

        <h1>
            Schoolwork: ELA, Science, History,
            Math, Literature, Social Studies,
            and Writing
        </h1>

        <h2>
            Educational resources for learning
            and studying.
        </h2>

        <p class="description">
            Research historical events.
            Analyze scientific experiments.
            Study mathematics and literature.
            Explore educational resources from around the web.
        </p>

        <div class="browser">

            <div class="toolbar">

                <input
                    id="url"
                    type="url"
                    inputmode="url"
                    autocomplete="url"
                    placeholder="https://example.com"
                >

                <button onclick="openInside()">
                    開く
                </button>

                <button
                    class="open-new"
                    onclick="openNewTab()"
                >
                    新しいタブ
                </button>

            </div>

            <iframe
                id="viewer"
                title="Website viewer"
                referrerpolicy="no-referrer">
            </iframe>

            <p id="message"></p>

        </div>

    </div>
</div>

<script>

window.addEventListener("load", function() {

    setTimeout(function() {

        document.getElementById("loading").style.display = "none";
        document.getElementById("main").style.display = "block";

    }, 900);

});


function getURL() {

    let input =
        document.getElementById("url").value.trim();

    if (!input) {

        showMessage("URLを入力してください。");
        return null;

    }

    if (
        !input.startsWith("http://") &&
        !input.startsWith("https://")
    ) {
        input = "https://" + input;
    }

    try {

        const parsed = new URL(input);

        if (
            parsed.protocol !== "http:" &&
            parsed.protocol !== "https:"
        ) {
            throw new Error();
        }

        return parsed.href;

    } catch {

        showMessage("正しいURLを入力してください。");
        return null;

    }
}


function openInside() {

    const url = getURL();

    if (!url) return;

    document.getElementById("viewer").src = url;

    hideMessage();

}


function openNewTab() {

    const url = getURL();

    if (!url) return;

    window.open(
        url,
        "_blank",
        "noopener,noreferrer"
    );

}


function showMessage(text) {

    const message =
        document.getElementById("message");

    message.textContent = text;
    message.style.display = "block";

}


function hideMessage() {

    document.getElementById("message").style.display = "none";

}


document.getElementById("url").addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {
            openInside();
        }

    }
);

</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
