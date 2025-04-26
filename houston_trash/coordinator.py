import logging
import aiohttp
import async_timeout
import re
from datetime import date, timedelta
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)


def strip_html_tags(text: str) -> str:
    """Remove HTML tags from a string."""
    if not text:
        return ""
    return re.sub(r"<.*?>", "", text, flags=re.DOTALL).strip()


def detect_delayed(text: str) -> bool:
    """Return True if 'delayed' is in text (case-insensitive)."""
    return bool(text and "delayed" in text.lower())


def build_dynamic_url(base_url: str) -> str:
    """
    Parse the given base_url, remove existing 'after'/'before' if present,
    then add after=<today> and before=<today+180days>, returning the final URL.
    """
    parsed = urlparse(base_url)
    qs = parse_qs(parsed.query)

    # Remove existing 'after'/'before' if present
    qs.pop("after", None)
    qs.pop("before", None)

    # Construct new dynamic range: from today to +180 days (approx 6 months)
    today_str = date.today().isoformat()
    future_str = (date.today() + timedelta(days=180)).isoformat()

    qs["after"] = [today_str]
    qs["before"] = [future_str]

    new_query = urlencode(qs, doseq=True)
    new_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))
    return new_url


class HoustonTrashDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator that fetches a multi-event calendar from Recollect for the next ~6 months."""

    def __init__(self, hass, base_url: str):
        self.base_url = base_url
        super().__init__(
            hass,
            _LOGGER,
            name="houston_trash_coordinator",
            update_interval=timedelta(hours=12),  # Re-fetch every 12 hours
        )

    async def _async_update_data(self):
        """Fetch and parse Recollect multi-event data for ~6 months into the future."""
        url = build_dynamic_url(self.base_url)
        _LOGGER.debug("Fetching Houston Trash data from: %s", url)

        try:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(30):
                    resp = await session.get(url)
                    resp.raise_for_status()
                    raw_json = await resp.json()
        except Exception as err:
            raise UpdateFailed(f"Error fetching Houston Trash data: {err}") from err

        # raw_json typically has "events" (array) and "zones" (dict)
        raw_events = raw_json.get("events", [])
        raw_zones = raw_json.get("zones", {})

        cleaned_events = []
        for evt in raw_events:
            day_str = evt.get("day")  # e.g. "2025-02-07"
            zone_id = evt.get("zone_id")
            flags = evt.get("flags", [])

            # map zone_id -> zone_name/zone_title from 'zones' if present
            zone_name = None
            zone_title = None
            if zone_id and str(zone_id) in raw_zones:
                z = raw_zones[str(zone_id)]
                zone_name = z.get("name")
                zone_title = z.get("title")

            # Clean each flag
            cleaned_flags = []
            for f in flags:
                subj = f.get("subject", "")
                html_msg = f.get("html_message", "")
                message = strip_html_tags(html_msg)
                is_delayed = detect_delayed(subj) or detect_delayed(message)

                cleaned_flags.append({
                    "name": f.get("name"),  # e.g. "waste", "recycle", "yard", "heavy"
                    "subject": subj,
                    "message": message,
                    "delayed": is_delayed
                })

            cleaned_events.append({
                "day": day_str,
                "zone_id": zone_id,
                "zone_name": zone_name,
                "zone_title": zone_title,
                "flags": cleaned_flags
            })

        return {
            "events": cleaned_events,
            "zones": raw_zones
        }
