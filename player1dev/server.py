import os
import re
from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join
from typing import List, Optional
from urllib.request import Request

import jinja2
import markdown
from fastapi import Depends, FastAPI, HTTPException, Request, Security
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

assets = f"{os.getcwd()}/assets"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
templates = Jinja2Templates(directory=f"{os.getcwd()}/templates")

app = FastAPI()
app.mount("/assets", StaticFiles(directory=assets), name="/assets")


get_routes = lambda: app.routes


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


@app.post("/auth/login")
def login(username: str, password: str):
    user = authenticate_user(username, password)
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/sitemap.xml")
@app.head("/sitemap.xml")
def generate_sitemap(request: Request, routes: List[APIRoute] = Depends(get_routes)):
    url_root = str(request.url).replace(request.url.path, "")
    # domain_name = url_root.lstrip(request.url.scheme + "://")
    root = etree.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for route in routes:
        if route.path in [
            "/{slug:path}",
            "/assets",
            "/docs",
            "/docs/oauth2-redirect",
            "/openapi.json",
            "/redoc",
            "/sitemap.xml",
        ]:
            continue

        url = etree.SubElement(root, "url")
        etree.SubElement(
            url, "loc"
        ).text = f"{url_root.replace('http://', 'https://')}{route.path}"
    markdown_files_dir = "content"
    markdown_files = [
        f
        for f in listdir(markdown_files_dir)
        if isfile(join(markdown_files_dir, f)) and f.endswith(".md")
    ]

    for markdown_file in markdown_files:
        if markdown_file in ["home.md", "error404.md", "error500.md"]:
            continue
        url = etree.SubElement(root, "url")
        etree.SubElement(
            url, "loc"
        ).text = f"{url_root.replace('http://', 'https://')}/{markdown_file.replace('_', '/').replace('.md', '')}"

    return Response(
        content=etree.tostring(root).decode("utf8"), media_type="application/xml"
    )


@app.get("/{slug:path}")
@app.head("/{slug:path}")
def static_router(slug: str):
    """
    Compile static pages from Markdown files and custom HTML templates. The slug is the path to the file, with underscores replacing slashes. For example, the slug "about_us" will look for the file "content/about_us.md". In either case, it will look for a template with the same name, e.g. "templates/about_us.html". If neither is found, it will return a 404 error. If the Markdown file is newer than the HTML file, it will recompile the HTML file.
    """

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


# # to get a string like this run:
# # openssl rand -hex 32
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# # set up the database connection
# client = MongoClient("mongodb://localhost:27017/")
# db = client["mydatabase"]
# aliases_collection = db["aliases"]
# domains_collection = db["domains"]
# sendermaps_collection = db["sendermaps"]
# virtuals_collection = db["virtuals"]

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# app = FastAPI()

# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }


# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     username: str | None = None


# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None


# class UserInDB(User):
#     hashed_password: str


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user


# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# @app.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# @app.get("/users/me/", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user


# @app.get("/users/me/items/")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": "Foo", "owner": current_user.username}]
