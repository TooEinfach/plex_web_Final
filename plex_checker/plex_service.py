"""
Plex service module - adapted from plex_check.py CLI
Handles all Plex server interactions, caching, and searching
"""
import json
import time
import logging
from pathlib import Path
from django.conf import settings
from plexapi.server import PlexServer
from rapidfuzz import fuzz

logger = logging.getLogger(__name__)

CACHE_FILE = Path.home() / ".plex_cache.json"
CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 60 * 6)


class PlexService:
    """Service class for interacting with Plex server"""
    
    def __init__(self):
        self.plex_base = settings.PLEX_BASE
        self.plex_token = settings.PLEX_TOKEN
        self._server = None
    
    @property
    def server(self):
        """Lazy-load Plex server connection"""
        if self._server is None:
            if not self.plex_token:
                raise ValueError("PLEX_TOKEN not configured in settings or environment")
            try:
                self._server = PlexServer(self.plex_base, self.plex_token)
                logger.info(f"Connected to Plex server at {self.plex_base}")
            except Exception as e:
                logger.error(f"Failed to connect to Plex at {self.plex_base}: {e}")
                raise
        return self._server
    
    def load_cache(self):
        """Load cache from file"""
        if not CACHE_FILE.exists():
            return {"updated": 0, "libraries": {}}
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception as e:
            logger.warning(f"Failed to read cache file: {e}. Recreating cache.")
            return {"updated": 0, "libraries": {}}
    
    def save_cache(self, cache):
        """Save cache to file"""
        try:
            CACHE_FILE.write_text(json.dumps(cache), encoding="utf-8")
        except Exception as e:
            logger.warning(f"Failed to write cache file: {e}")
    
    def refresh_cache(self, force=False):
        """Refresh library cache from Plex server"""
        cache = self.load_cache()
        now = time.time()
        
        if not force and (now - cache.get("updated", 0) < CACHE_TTL):
            logger.debug("Using cached library data")
            return cache
        
        logger.info("Refreshing library cache from Plex...")
        libraries = {}
        
        try:
            sections = self.server.library.sections()
        except Exception as e:
            logger.error(f"Failed to list library sections: {e}")
            return cache
        
        for section in sections:
            try:
                items = []
                for item in section.all():
                    items.append({
                        "title": getattr(item, "title", None),
                        "year": getattr(item, "year", None),
                        "type": getattr(item, "type", None),
                        "ratingKey": getattr(item, "ratingKey", None)
                    })
                libraries[str(section.key)] = {
                    "title": section.title,
                    "type": section.type,
                    "items": items
                }
                logger.info(f"Cached {len(items)} items from library: {section.title}")
            except Exception as e:
                logger.warning(f"Failed to read section {getattr(section, 'title', section.key)}: {e}")
                continue
        
        cache = {"updated": now, "libraries": libraries}
        self.save_cache(cache)
        logger.info("Cache refresh complete")
        return cache
    
    def search_exact(self, title, section_id=None):
        """
        Search for exact title matches
        
        Args:
            title: Title to search for
            section_id: Optional library section ID to limit search
            
        Returns:
            List of exact matches with metadata
        """
        title_norm = title.strip().lower()
        
        try:
            if section_id is not None:
                section = self.server.library.sectionByID(section_id)
                results = section.search(title)
            else:
                results = self.server.search(title)
        except Exception:
            # Fallback to server-wide search if section lookup fails
            try:
                results = self.server.search(title)
            except Exception as e:
                logger.error(f"Search failed: {e}")
                return []
        
        matches = []
        for r in results:
            if getattr(r, "title", "").strip().lower() == title_norm:
                matches.append({
                    "title": r.title,
                    "year": getattr(r, "year", None),
                    "type": getattr(r, "type", None),
                    "ratingKey": getattr(r, "ratingKey", None),
                    "library": getattr(r, "librarySectionTitle", None),
                    "summary": getattr(r, "summary", "")[:200] if hasattr(r, "summary") else ""
                })
        
        return matches
    
    def search_fuzzy(self, title, threshold=80, section_id=None, cache=None):
        """
        Fuzzy search using cached library data
        
        Args:
            title: Title to search for
            threshold: Minimum similarity score (0-100)
            section_id: Optional library section ID to limit search
            cache: Optional pre-loaded cache (will refresh if not provided)
            
        Returns:
            List of fuzzy matches sorted by score
        """
        title_norm = title.strip().lower()
        
        if cache is None:
            cache = self.refresh_cache()
        
        items = []
        if section_id is not None:
            lib = cache["libraries"].get(str(section_id))
            if lib:
                items = lib["items"]
        else:
            for lib in cache["libraries"].values():
                items.extend(lib["items"])
        
        found = []
        for it in items:
            if not it.get("title"):
                continue
            score = fuzz.token_sort_ratio(title_norm, it["title"].strip().lower())
            if score >= threshold:
                found.append({
                    "title": it["title"],
                    "year": it.get("year"),
                    "score": score,
                    "type": it.get("type"),
                    "ratingKey": it.get("ratingKey")
                })
        
        return sorted(found, key=lambda x: x["score"], reverse=True)
    
    def search_server(self, title, limit=20):
        """
        Fallback server search (returns mixed results)
        
        Args:
            title: Title to search for
            limit: Maximum number of results to return
            
        Returns:
            List of server search results
        """
        try:
            results = self.server.search(title)
        except Exception as e:
            logger.error(f"Server search failed: {e}")
            return []
        
        formatted = []
        for r in results[:limit]:
            title_val = (getattr(r, "title", None) or 
                        getattr(r, "name", None) or 
                        getattr(r, "tag", None) or 
                        "<unknown>")
            formatted.append({
                "title": title_val,
                "year": getattr(r, "year", "n/a"),
                "type": getattr(r, "type", type(r).__name__),
                "library": getattr(r, "librarySectionTitle", "n/a"),
                "ratingKey": getattr(r, "ratingKey", "n/a")
            })
        
        return formatted
    
    def get_libraries(self):
        """Get list of all Plex libraries"""
        try:
            sections = self.server.library.sections()
            return [{
                "id": section.key,
                "title": section.title,
                "type": section.type
            } for section in sections]
        except Exception as e:
            logger.error(f"Failed to get libraries: {e}")
            return []


# Singleton instance
plex_service = PlexService()
