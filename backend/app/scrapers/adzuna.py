import re
from datetime import datetime, timezone
from typing import List, Optional

import httpx
from loguru import logger

from app.core.config import settings
from app.data.brazil_cities import CITY_TO_STATE
from app.domain.enums import ContractType, Level, Modality
from app.scrapers.base import BaseScraper, ScrapedJob

STATE_NAME_MAP = {
    "acre": "AC", "alagoas": "AL", "amapa": "AP", "amazonas": "AM",
    "bahia": "BA", "ceara": "CE", "distrito federal": "DF",
    "espirito santo": "ES", "goias": "GO", "maranhao": "MA",
    "mato grosso": "MT", "mato grosso do sul": "MS",
    "minas gerais": "MG", "para": "PA", "paraiba": "PB",
    "parana": "PR", "pernambuco": "PE", "piaui": "PI",
    "rio de janeiro": "RJ", "rio grande do norte": "RN",
    "rio grande do sul": "RS", "rondonia": "RO", "roraima": "RR",
    "santa catarina": "SC", "sao paulo": "SP", "sergipe": "SE",
    "tocantins": "TO", "roraima": "RR",
    "estado de s\u00e3o paulo": "SP", "estado de sao paulo": "SP",
    "estado do rio de janeiro": "RJ",
    "estado de minas gerais": "MG",
    "estado do parana": "PR", "estado do paran\u00e1": "PR",
    "estado do rio grande do sul": "RS",
    "estado da bahia": "BA",
    "estado de pernambuco": "PE",
    "estado do ceara": "CE", "estado do cear\u00e1": "CE",
    "estado de santa catarina": "SC",
    "estado de goias": "GO", "estado de goi\u00e1s": "GO",
    "estado do espirito santo": "ES",
}


def _normalize_state(s: str) -> str:
    s = s.lower().strip()
    s = s.replace("estado de ", "").replace("estado do ", "estado da ")
    s = s.replace("estado da ", "")
    accent_map = {"á": "a", "â": "a", "ã": "a", "à": "a",
                  "é": "e", "ê": "e", "í": "i", "ó": "o",
                  "ô": "o", "õ": "o", "ú": "u", "ü": "u",
                  "ç": "c"}
    for acc, plain in accent_map.items():
        s = s.replace(acc, plain)
    return s

TECH_SEARCH_TERMS = [
    "desenvolvedor", "programador", "engenheiro de software",
    "analista de sistemas", "devops", "frontend", "backend",
    "fullstack", "cientista de dados", "data science",
    "engenheiro de dados", "data engineer", "analista de dados",
    "suporte técnico", "suporte ti", "administrador de redes",
    "segurança da informação", "qa", "teste", "quality assurance",
    "product manager", "product owner", "scrum master",
    "arquiteto de software", "mobile", "react native",
    "flutter", "machine learning", "inteligência artificial",
    "cloud", "aws", "azure", "remoto", "home office",
    "estágio ti", "estágio tecnologia", "trainee ti",
    "infraestrutura", "analista de suporte", "consultor ti",
]


class AdzunaScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="adzuna")
        self.api_key = settings.ADZUNA_API_KEY
        self.app_id = settings.ADZUNA_APP_ID
        self.base_url = "https://api.adzuna.com/v1/api/jobs/br"
        self.client_kwargs = {
            "timeout": 30.0,
            "headers": {"User-Agent": "JobFinder/1.0"},
        }
        self.seen_ids: set[str] = set()

    async     def fetch(self) -> List[ScrapedJob]:
        if not self.api_key or not self.app_id:
            logger.warning("Adzuna API credentials not configured, skipping")
            return []

        jobs: List[ScrapedJob] = []
        params_base = {
            "app_id": self.app_id,
            "app_key": self.api_key,
            "results_per_page": 50,
            "max_days_old": 14,
        }

        try:
            async with httpx.AsyncClient(**self.client_kwargs) as client:
                for term in TECH_SEARCH_TERMS[:10]:
                    page = 1
                    while page <= 3:
                        try:
                            params = {**params_base, "what": term}
                            response = await client.get(
                                f"{self.base_url}/search/{page}",
                                params=params,
                            )
                            if response.status_code == 400:
                                break
                            response.raise_for_status()
                            data = response.json()
                            raw_jobs = data.get("results", [])
                            if not raw_jobs:
                                break

                            for item in raw_jobs:
                                item_id = str(item.get("id", ""))
                                if item_id in self.seen_ids:
                                    continue
                                self.seen_ids.add(item_id)

                                try:
                                    job = self._parse_job(item)
                                    if job:
                                        jobs.append(job)
                                except Exception as e:
                                    logger.warning(f"Failed to parse Adzuna job: {e}")
                                    continue

                            if len(raw_jobs) < 50:
                                break
                            page += 1
                        except Exception as e:
                            logger.warning(f"Adzuna search '{term}' page {page} failed: {e}")
                            break

        except httpx.RequestError as e:
            logger.error(f"Adzuna API request failed: {e}")

        logger.info(f"Adzuna: found {len(jobs)} Brazilian tech jobs")
        return jobs

    def _parse_location(self, item: dict) -> tuple[Optional[str], Optional[str]]:
        location = item.get("location") or {}
        display_name = location.get("display_name", "")
        area = location.get("area", [])

        city = None
        state = None

        if not display_name or _normalize_state(display_name) in ("brasil", "brazil"):
            if area and len(area) >= 3:
                for segment in reversed(area):
                    seg_normalized = _normalize_state(segment)
                    if seg_normalized in STATE_NAME_MAP:
                        state = STATE_NAME_MAP[seg_normalized]
                        break
                    if seg_normalized not in ("brasil", "brazil", "sudeste", "sul", "norte", "nordeste", "centro-oeste"):
                        city = segment
            return city, state

        parts = [p.strip() for p in display_name.split(",") if p.strip()]
        if len(parts) >= 2:
            city = parts[0]
            state_normalized = _normalize_state(parts[-1])
            state = STATE_NAME_MAP.get(state_normalized)

        if not state:
            for p in parts:
                pn = _normalize_state(p)
                if pn in STATE_NAME_MAP:
                    state = STATE_NAME_MAP[pn]
                    break

        if not state and city:
            state = CITY_TO_STATE.get(city)

        return city, state

    def _parse_job(self, item: dict) -> Optional[ScrapedJob]:
        title = item.get("title", "")
        if not title:
            return None

        description = item.get("description", "")
        text = f"{title} {description}".lower()

        city, state = self._parse_location(item)

        return ScrapedJob(
            external_id=str(item.get("id", "")),
            title=title,
            company_name=item.get("company", {}).get("display_name", "Unknown"),
            description=description,
            city=city,
            state=state,
            modality=self._detect_modality(text),
            contract_type=self._detect_contract_type(text),
            level=self._detect_level(text),
            published_at=self._parse_date(item.get("created")),
            application_url=item.get("redirect_url"),
            technologies=[],
            currency="BRL",
        )

    def _detect_modality(self, text: str) -> Modality:
        if "remoto" in text or "home office" in text or "remote" in text or "trabalho remoto" in text:
            return Modality.REMOTE
        if "hibrido" in text or "híbrido" in text or "presencial" in text:
            return Modality.HYBRID
        return Modality.REMOTE

    def _detect_contract_type(self, text: str) -> ContractType:
        if "freelance" in text or "freelancer" in text or "pj" in text or "contrato" in text:
            return ContractType.FREELANCER
        if "estagio" in text or "estágio" in text or "intern" in text:
            return ContractType.INTERNSHIP
        if "trainee" in text:
            return ContractType.INTERNSHIP
        if "clt" in text or "efetivo" in text:
            return ContractType.CLT
        return ContractType.CLT

    def _detect_level(self, text: str) -> Level:
        if "senior" in text or "sênior" in text:
            return Level.SENIOR
        if "pleno" in text:
            return Level.MID
        if "junior" in text or "júnior" in text or "jr" in text or "entry" in text:
            return Level.JUNIOR
        if "estagio" in text or "estágio" in text or "trainee" in text:
            return Level.JUNIOR
        return Level.MID

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None
