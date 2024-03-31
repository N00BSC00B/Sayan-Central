from fastapi import FastAPI
from starlette.responses import RedirectResponse, HTMLResponse
import json

app = FastAPI()


with open("mappings.json", "r") as f:
    url_mappings = json.load(f)


css = """

"""


def html(css, body):
    content = f"""
    <html>
        <head>
            <title>URL Forwarder</title>
            <style>
                {css}
            </style>
        </head>
        <body>
            {body}
        </body>
    </html>
    """
    return content


@app.get("/")
async def home():
    body = """
    <h1>Welcome to the URL Forwarder service!</h1>
    <p>Go to:</p>
    <ul>
    """

    for short_url, long_url in url_mappings.items():
        body += f"<li><a href='/{short_url}'>{short_url}</a> for {long_url}</li>"
    body += """
    </ul>
    """

    return HTMLResponse(content=html(css, body))


@app.get("/{short_url}")
async def redirect_to_original(short_url: str):

    if short_url in url_mappings:
        return RedirectResponse(url=url_mappings[short_url])
    else:
        body = f"""
        <h1>URL not found</h1>
        <p>URL for <strong>{short_url}</strong> not found</p>
        """
        content = html(css, body)
        return HTMLResponse(content=content)


@app.get("/hehe")
async def hehe():
    body = """
    <h1>Hehe</h1>
    <p>Hehe</p>
    """
    return HTMLResponse(content=html(css, body))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
