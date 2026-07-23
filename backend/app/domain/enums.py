import enum


class Modality(str, enum.Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"


class ContractType(str, enum.Enum):
    CLT = "clt"
    PJ = "pj"
    FREELANCER = "freelancer"
    INTERNSHIP = "internship"


class Level(str, enum.Enum):
    INTERNSHIP = "internship"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
