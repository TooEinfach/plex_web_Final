# Plex Checker Web UI - Interface Overview

## Main Search Page (/)

```
┌─────────────────────────────────────────────────────────────┐
│  🎬 Plex Checker                    [Search] [Stats]        │
└─────────────────────────────────────────────────────────────┘

                    Search Your Plex Library
    ┌───────────────────────────────────────────────────┐
    │  Movie or Show Title:                            │
    │  [________________________________]               │
    │                                                   │
    │  Search Type: [Auto ▼]  Library: [All ▼]        │
    │  Fuzzy Threshold: [85]                           │
    │                                                   │
    │  [🔍 Search]  [🔄 Refresh Cache]                 │
    └───────────────────────────────────────────────────┘

    ┌───────────────────────────────────────────────────┐
    │  ✓ Exact Match Results                    2       │
    ├───────────────────────────────────────────────────┤
    │  ┌─────────────────────────────────────────────┐ │
    │  │ The Matrix                                   │ │
    │  │ 1999 | movie | Movies | Score: 100          │ │
    │  │ Rating Key: 12345                            │ │
    │  └─────────────────────────────────────────────┘ │
    │                                                   │
    │  ┌─────────────────────────────────────────────┐ │
    │  │ The Matrix Reloaded                          │ │
    │  │ 2003 | movie | Movies | Score: 95           │ │
    │  │ Rating Key: 12346                            │ │
    │  └─────────────────────────────────────────────┘ │
    └───────────────────────────────────────────────────┘

    ┌───────────────────────────────────────────────────┐
    │  Recent Searches                                  │
    ├───────────────────────────────────────────────────┤
    │  The Matrix          EXACT - ✓ Found             │
    │  Inception           FUZZY - ✓ Found             │
    │  Unknown Movie       AUTO - ✗ Not Found          │
    └───────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  © 2026 Plex Checker | Connected to: http://10.0.0.208     │
└─────────────────────────────────────────────────────────────┘
```

## Statistics Page (/stats)

```
┌─────────────────────────────────────────────────────────────┐
│  🎬 Plex Checker                    [Search] [Stats]        │
└─────────────────────────────────────────────────────────────┘

                    Search Statistics

    ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
    │  156   │  │  142   │  │   14   │  │  91%   │
    │ Total  │  │ Found  │  │Not Fnd │  │Success │
    └────────┘  └────────┘  └────────┘  └────────┘

                 Searches by Type
    ┌────────┐  ┌────────┐  ┌────────┐
    │   89   │  │   52   │  │   15   │
    │ Exact  │  │ Fuzzy  │  │ Server │
    └────────┘  └────────┘  └────────┘

    ┌───────────────────────────────────────────────────┐
    │  Recent Search History                            │
    ├────────────┬──────┬──────────┬───────────────────┤
    │ Title      │ Type │ Result   │ Time              │
    ├────────────┼──────┼──────────┼───────────────────┤
    │ The Matrix │ EXACT│ ✓ Found  │ Jan 30, 2026 3:15│
    │ Inception  │ FUZZY│ ✓ Found  │ Jan 30, 2026 2:45│
    │ Star Wars  │ EXACT│ ✓ Found  │ Jan 30, 2026 2:30│
    └────────────┴──────┴──────────┴───────────────────┘

                [← Back to Search]
```

## Key Features

### Search Modes

1. **Auto Mode** (Recommended)
   - Tries exact match first
   - Falls back to fuzzy search if no exact match
   - Finally tries server search if needed
   - Most user-friendly option

2. **Exact Mode**
   - Only returns perfect title matches
   - Fast and precise
   - Best for known titles

3. **Fuzzy Mode**
   - Uses similarity scoring
   - Finds partial matches
   - Adjustable threshold (0-100)
   - Great for uncertain titles

### Library Filtering

- Search all libraries at once
- Or narrow to specific library:
  - Movies
  - TV Shows
  - Music
  - Photos
  - Any custom libraries

### Caching System

- Caches entire library for 6 hours
- Manual refresh available
- Dramatically speeds up fuzzy searches
- Shared with CLI tool

### Search History

- Automatic logging of all searches
- Tracks success/failure
- Shows search type used
- Timestamps for analysis

## Color Scheme

- Primary: Gold/Orange (#e5a00d) - Plex-inspired
- Secondary: Dark Gray (#282a2d)
- Success: Green (#4caf50)
- Warning: Orange (#ff9800)
- Danger: Red (#f44336)

## Responsive Design

- Desktop: Full-width layout with grid
- Tablet: Adjusted columns
- Mobile: Single column, stacked elements

## AJAX Integration

- No page reloads during search
- Loading spinner during operations
- Real-time results display
- Smooth user experience
