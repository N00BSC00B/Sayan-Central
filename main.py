from fastapi import FastAPI
from starlette.responses import RedirectResponse, HTMLResponse
import json
import os
from jinja2 import Environment, FileSystemLoader
import tabulate

with open("assets/styles.css", "r") as f:
    css = f.read()

env = Environment(loader=FileSystemLoader('assets'))
index_template = env.get_template('index.html')

app = FastAPI()

with open("assets/mappings.json", "r") as f:
    url_mappings = json.load(f)


@app.get("/")
async def home():
    body = """
    <h1>Welcome to Sayan Central!</h1>
    <p><strong>Here are the list of my Projects:</strong></p>
    <table>
    <thead><tr><th>URL</th><th>Description</th></tr></thead>
    <tbody>
    """

    for key, value in url_mappings.items():
        body += f"<tr><td><a href='/{key}'>{key}</a></td><td>{value[1]}</td></tr>"
    body += "</tbody></table>"

    content = index_template.render(
        title="Sayan Central", body=body, css=css
    )

    return HTMLResponse(content=content)


@app.get("/wip")
async def hehe():
    body = """
    <h1>Work In Progress</h1>
    <p>This current project is under development and will be linked soon.</p>
    """
    content = index_template.render(
        title="Work in Progress", body=body, css=css
    )
    return HTMLResponse(content=content)


@app.get("/{short_url}")
async def redirect_to_original(short_url: str):

    if short_url in url_mappings:
        return RedirectResponse(url=url_mappings[short_url][0])
    else:
        body = f"""
        <h1>URL not found</h1>
        <p>URL for <strong>{short_url}</strong> not found</p>
        """
        content = index_template.render(
            title="URL not found", body=body, css=css
        )
        return HTMLResponse(content=content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
