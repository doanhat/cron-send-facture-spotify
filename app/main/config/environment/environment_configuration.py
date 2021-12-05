import os

from dotenv import dotenv_values, load_dotenv

load_dotenv("env/.env")

THREAD_ID = int(os.getenv("FB_THREAD_ID"))
PROJECT_ID = os.getenv("PROJECT_ID")
CRE_SECRET_ID = os.getenv("CRE_SECRET_ID")
TOK_SECRET_ID = os.getenv("TOK_SECRET_ID")
SES_SECRET_ID = os.getenv("SES_SECRET_ID")
LOG_SECRET_ID = os.getenv("LOG_SECRET_ID")