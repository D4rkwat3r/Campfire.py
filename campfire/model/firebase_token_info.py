from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class FirebaseTokenInfo:
    access_token: str
    expires_in: str
    token_type: str
    refresh_token: str
    id_token: str
    user_id: str
    project_id: str
