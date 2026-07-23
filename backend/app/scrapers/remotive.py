import re
from datetime import datetime
from typing import List, Optional

import httpx
from loguru import logger

from app.core.config import settings
from app.data.brazil_cities import CITY_TO_STATE
from app.domain.enums import ContractType, Level, Modality
from app.scrapers.base import BaseScraper, ScrapedJob


BRAZIL_KEYWORDS = ["brazil", "brasil", "são paulo", "sao paulo", "rio de janeiro",
                   "belo horizonte", "curitiba", "porto alegre", "salvador",
                   "brasília", "brasilia", "recife", "fortaleza", "campinas",
                   "santos", "florianópolis", "florianopolis", "jundiaí", "jundiai"]


class RemotiveScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="remotive")
        self.base_url = settings.REMOTIVE_BASE_URL
        self.client_kwargs = {
            "timeout": 30.0,
            "headers": {"User-Agent": "JobFinder/1.0"},
        }

    async def fetch(self) -> List[ScrapedJob]:
        jobs: List[ScrapedJob] = []
        url = f"{self.base_url}/remote-jobs"
        search_terms = ["Brazil", "Brasil", "remote Brazil", "São Paulo", "Rio de Janeiro", "home office Brazil"]

        try:
            async with httpx.AsyncClient(**self.client_kwargs) as client:
                seen_ids: set[str] = set()

                for term in search_terms:
                    try:
                        response = await client.get(url, params={"search": term})
                        response.raise_for_status()
                        data = response.json()

                        for item in data.get("jobs", []):
                            item_id = str(item.get("id", ""))
                            if item_id in seen_ids:
                                continue
                            seen_ids.add(item_id)

                            try:
                                job = self._parse_job(item)
                                if job:
                                    jobs.append(job)
                            except Exception as e:
                                logger.warning(f"Failed to parse Remotive job: {e}")
                                continue
                    except Exception as e:
                        logger.warning(f"Remotive search '{term}' failed: {e}")
                        continue

        except httpx.HTTPStatusError as e:
            logger.error(f"Remotive API HTTP error: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"Remotive API request failed: {e}")

        logger.info(f"Remotive: found {len(jobs)} Brazilian jobs")
        return jobs

    def _is_brazil_location(self, location: Optional[str]) -> bool:
        if not location:
            return False
        loc_lower = location.lower()
        return any(kw in loc_lower for kw in BRAZIL_KEYWORDS)

    def _parse_location(self, location: Optional[str], title: str = "") -> tuple[Optional[str], Optional[str]]:
        city = None
        state = None

        if title:
            match = re.search(r'\(([^)]+)\)', title)
            if match:
                city = match.group(1).strip()

        if not location:
            if city:
                state = CITY_TO_STATE.get(city)
            return city, state

        brazil_states_upper = {
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
            "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
            "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
        }

        parts = [p.strip() for p in re.split(r'[,;/-]', location) if p.strip()]
        for p in parts:
            pu = p.upper()
            if pu in brazil_states_upper:
                state = pu
            elif not city and pu != "BRAZIL" and p.lower() != "brasil" and not p.lower().startswith("remote"):
                city = p

        if not state and city:
            state = CITY_TO_STATE.get(city)

        return city, state

    def _parse_job(self, item: dict) -> Optional[ScrapedJob]:
        title = item.get("title", "")
        if not title:
            return None

        raw_location = item.get("candidate_required_location")
        if not self._is_brazil_location(raw_location):
            return None

        city, state = self._parse_location(raw_location, title)
        raw_tags = " ".join(item.get("tags", []) or []).lower()

        return ScrapedJob(
            external_id=str(item.get("id", "")),
            title=title,
            company_name=item.get("company_name", "Unknown"),
            company_logo=item.get("company_logo"),
            description=item.get("description", ""),
            city=city,
            state=state,
            modality=self._detect_modality(raw_tags),
            contract_type=self._detect_contract_type(raw_tags),
            level=self._detect_level(raw_tags),
            published_at=self._parse_date(item.get("publication_date")),
            application_url=item.get("url"),
            technologies=[t.strip() for t in item.get("tags", []) if t.strip()],
            currency="BRL",
        )

    def _detect_modality(self, text: str) -> Modality:
        if "remote" in text:
            return Modality.REMOTE
        if "hybrid" in text:
            return Modality.HYBRID
        return Modality.REMOTE

    def _detect_contract_type(self, text: str) -> ContractType:
        if "freelance" in text or "contract" in text:
            return ContractType.FREELANCER
        if "intern" in text:
            return ContractType.INTERNSHIP
        return ContractType.CLT

    def _detect_level(self, text: str) -> Level:
        if "senior" in text or "sr" in text:
            return Level.SENIOR
        if "junior" in text or "jr" in text or "entry" in text:
            return Level.JUNIOR
        if "intern" in text:
            return Level.INTERNSHIP
        if "mid" in text or "middle" in text:
            return Level.MID
        return Level.MID

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None
