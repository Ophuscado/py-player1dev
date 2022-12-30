import os
import re
from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join
from typing import List, Optional

import jinja2
import markdown
import schemas
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.responses import RedirectResponse, Response
from fastapi.routing import APIRoute
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import (
    Environment,
    FileSystemBytecodeCache,
    FileSystemLoader,
    select_autoescape,
)
from lxml import etree

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def authenticate_user(username: str, password: str):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_username(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid JWT token")
        return username
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid JWT token")


app.mount("/assets", StaticFiles(directory="assets"), name="assets")

templates = Jinja2Templates(directory="templates")

get_routes = lambda: app.routes


@app.post("/auth/login")
def login(username: str, password: str):
    user = authenticate_user(username, password)
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/sitemap.xml")
def generate_sitemap(routes: List[APIRoute] = Depends(get_routes)):
    root = etree.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for route in routes:
        url = etree.SubElement(root, "url")
        etree.SubElement(url, "loc").text = f"https://liverado.com{route.path}"
    markdown_files_dir = "content"
    markdown_files = [
        f
        for f in listdir(markdown_files_dir)
        if isfile(join(markdown_files_dir, f)) and f.endswith(".md")
    ]
    for markdown_file in markdown_files:
        url = etree.SubElement(root, "url")
        etree.SubElement(
            url, "loc"
        ).text = f"https://liverado.com/{markdown_file.replace('_', '/').rstrip('.md')}"
    return Response(
        content=etree.tostring(root).decode("utf8"), media_type="application/xml"
    )


@app.get("/{slug:path}")
def static_router(slug: str):
    """
    Compile static pages from Markdown files and custom HTML templates. The slug is the path to the file, with underscores replacing slashes. For example, the slug "about_us" will look for the file "content/about_us.md". In either case, it will look for a template with the same name, e.g. "templates/about_us.html". If neither is found, it will return a 404 error. If the Markdown file is newer than the HTML file, it will recompile the HTML file."""

    use_cache = False  # For debugging

    slug = "home" if slug == "" else slug  # / == home.md
    slug_path = slug.replace("_", "/")
    file_path = os.path.join(os.getcwd(), "content", slug_path + ".md")
    html_file_path = file_path.replace(".md", ".html").replace("content", "static")

    if os.path.exists(html_file_path) and use_cache:
        md_mod_time = datetime.fromtimestamp(os.path.getctime(file_path))
        html_mod_time = datetime.fromtimestamp(os.path.getctime(html_file_path))
        if html_mod_time > md_mod_time:
            with open(html_file_path, "r") as f:
                html = f.read()
                return Response(content=html, media_type="text/html")
    else:
        with open(file_path, "r") as f:
            md = f.read()
        markdown_html = markdown.markdown(
            md, extensions=["tables", "fenced_code", "codehilite", "toc"]
        )
        template_file_path = f"prerender-{slug}.html"
        templates = Environment(loader=FileSystemLoader(["templates"])).get_template(
            template_file_path
            if os.path.exists(f"templates/{template_file_path}")
            else "prerender-default.html",
        )
        jinja2_html = templates.render(
            content=markdown_html,
            **{
                key: value
                for key, value in re.findall(
                    r"<!--\s*(.*?):\s*(.*?)\s*-->", md, re.MULTILINE | re.DOTALL
                )
            },
        )
        with open(html_file_path, "w") as f:
            f.write(jinja2_html)
        return Response(content=jinja2_html, media_type="text/html")
