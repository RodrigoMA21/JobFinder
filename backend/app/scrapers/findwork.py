from datetime import datetime
from typing import List, Optional

import httpx
from loguru import logger

from app.core.config import settings
from app.domain.enums import ContractType, Level, Modality
from app.scrapers.base import BaseScraper, ScrapedJob


class FindworkScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="findwork")
        self.base_url = settings.FINDWORK_BASE_URL
        self.api_key = settings.FINDWORK_API_KEY
        headers = {"User-Agent": "JobFinder/1.0"}
        if self.api_key:
            headers["Authorization"] = f"Token {self.api_key}"
        self.client_kwargs = {
            "timeout": 30.0,
            "headers": headers,
        }

    async def fetch(self) -> List[ScrapedJob]:
        if not self.api_key:
            logger.warning("Findwork API key not configured, skipping")
            return []

        jobs: List[ScrapedJob] = []

        try:
            async with httpx.AsyncClient(**self.client_kwargs) as client:
                response = await client.get(f"{self.base_url}/jobs/")
                response.raise_for_status()
                data = response.json()

                for item in data.get("results", []):
                    try:
                        job = self._parse_job(item)
                        if job:
                            jobs.append(job)
                    except Exception as e:
                        logger.warning(f"Failed to parse Findwork job: {e}")
                        continue

        except httpx.HTTPStatusError as e:
            logger.error(f"Findwork API HTTP error: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"Findwork API request failed: {e}")

        return jobs

    def _parse_job(self, item: dict) -> Optional[ScrapedJob]:
        title = item.get("role", "") or item.get("title", "")
        if not title:
            return None

        text = f"{title} {item.get('description', '')}".lower()

        return ScrapedJob(
            external_id=item.get("id"),
            title=title,
            company_name=item.get("company_name", "Unknown"),
            description=item.get("description", ""),
            city=item.get("location"),
            modality=self._detect_modality(text),
            contract_type=self._detect_contract_type(text),
            level=self._detect_level(text),
            salary_min=item.get("salary_min"),
            salary_max=item.get("salary_max"),
            currency="USD",
            published_at=self._parse_date(item.get("date_posted")),
            application_url=item.get("url"),
            technologies=item.get("keywords", []),
        )

    def _detect_modality(self, text: str) -> Modality:
        if "remote" in text or "work from home" in text or "wfh" in text:
            return Modality.REMOTE
        if "hybrid" in text:
            return Modality.HYBRID
        return Modality.ONSITE

    def _detect_contract_type(self, text: str) -> ContractType:
        if "contract" in text or "freelance" in text:
            return ContractType.FREELANCER
        return ContractType.CLT

    def _detect_level(self, text: str) -> Level:
        if "senior" in text or "sr " in text:
            return Level.SENIOR
        if "junior" in text or "jr " in text or "entry" in text:
            return Level.JUNIOR
        if "intern" in text:
            return Level.INTERNSHIP
        return Level.MID

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None
