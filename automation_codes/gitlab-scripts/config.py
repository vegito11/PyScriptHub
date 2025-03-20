import os

BASE_URL = "https://gitlab.com/api/v4"
REL_BRANCH_PATTERN = r"^release\/[0-9]+\.[0-9]+(\.[0-9]+)?$"
# REL_BRANCH_PATTERN = r"^release/[0-9]+\.[0-9]+\.?[0-9]*$"
MR_LABELS = ["cascade", "automerge_bot"]
CONFLICT_LABELS = ["merge_conflict", "need_manual_merge"]
PROJECT_ID_DEFAULT = "62057396"
API_TOKEN_ENV_VAR = "CASCADE_API_TOKEN"
DEFAULT_FLOW="merge_trigger"
DEFAULT_ACTION="get_fwd_br"
POST_RELEASE_TARGETS=["main"]
# POST_RELEASE_TARGETS=["develop", "main"]
# POST_RELEASE_TARGETS=[]

HEADERS = {
    "PRIVATE-TOKEN": os.getenv(API_TOKEN_ENV_VAR),
    "Content-Type": "application/json"
}