"""
Views for Plex Checker web interface
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .plex_service import plex_service
from .models import SearchHistory
import logging

logger = logging.getLogger(__name__)


def index(request):
    """Main search page"""
    libraries = []
    try:
        libraries = plex_service.get_libraries()
    except Exception as e:
        logger.error(f"Failed to load libraries: {e}")
    
    recent_searches = SearchHistory.objects.all()[:10]
    
    context = {
        'libraries': libraries,
        'recent_searches': recent_searches
    }
    return render(request, 'plex_checker/index.html', context)


@require_http_methods(["POST"])
def search(request):
    """Handle search requests via AJAX"""
    title = request.POST.get('title', '').strip()
    search_type = request.POST.get('search_type', 'exact')
    section_id = request.POST.get('section_id')
    threshold = int(request.POST.get('threshold', 85))
    
    if not title:
        return JsonResponse({'error': 'Title is required'}, status=400)
    
    # Convert section_id to int if provided
    if section_id and section_id != 'all':
        try:
            section_id = int(section_id)
        except ValueError:
            section_id = None
    else:
        section_id = None
    
    results = []
    found = False
    actual_search_type = search_type
    
    try:
        if search_type == 'exact':
            # Try exact match first
            results = plex_service.search_exact(title, section_id)
            if results:
                found = True
                actual_search_type = 'exact'
            
        elif search_type == 'fuzzy':
            # Fuzzy search
            cache = plex_service.refresh_cache()
            results = plex_service.search_fuzzy(title, threshold, section_id, cache)
            if results:
                found = True
                actual_search_type = 'fuzzy'
            
        elif search_type == 'auto':
            # Auto: Try exact first, then fuzzy, then server
            results = plex_service.search_exact(title, section_id)
            if results:
                found = True
                actual_search_type = 'exact'
            else:
                # Try fuzzy
                cache = plex_service.refresh_cache()
                results = plex_service.search_fuzzy(title, threshold, section_id, cache)
                if results:
                    found = True
                    actual_search_type = 'fuzzy'
                else:
                    # Fallback to server search
                    results = plex_service.search_server(title)
                    if results:
                        found = True
                        actual_search_type = 'server'
        
        # Log search to database
        SearchHistory.objects.create(
            title=title,
            found=found,
            search_type=actual_search_type
        )
        
        return JsonResponse({
            'success': True,
            'results': results,
            'search_type': actual_search_type,
            'found': found,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Search error: {e}", exc_info=True)
        return JsonResponse({
            'error': str(e),
            'success': False
        }, status=500)


@require_http_methods(["POST"])
def refresh_cache(request):
    """Force refresh the Plex library cache"""
    try:
        cache = plex_service.refresh_cache(force=True)
        total_items = sum(len(lib['items']) for lib in cache['libraries'].values())
        
        return JsonResponse({
            'success': True,
            'message': f'Cache refreshed successfully. {total_items} items cached.',
            'libraries': len(cache['libraries'])
        })
    except Exception as e:
        logger.error(f"Cache refresh error: {e}", exc_info=True)
        return JsonResponse({
            'error': str(e),
            'success': False
        }, status=500)


def stats(request):
    """Display search statistics"""
    total_searches = SearchHistory.objects.count()
    found_count = SearchHistory.objects.filter(found=True).count()
    not_found_count = total_searches - found_count
    
    recent_searches = SearchHistory.objects.all()[:50]
    
    search_type_stats = {}
    for search_type in ['exact', 'fuzzy', 'server']:
        search_type_stats[search_type] = SearchHistory.objects.filter(
            search_type=search_type
        ).count()
    
    context = {
        'total_searches': total_searches,
        'found_count': found_count,
        'not_found_count': not_found_count,
        'recent_searches': recent_searches,
        'search_type_stats': search_type_stats
    }
    
    return render(request, 'plex_checker/stats.html', context)
