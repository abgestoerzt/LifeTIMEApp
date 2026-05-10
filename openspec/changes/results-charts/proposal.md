# Results Charts

## What

Wire Chart.js to the actual scoring data so the results page and check-in trend page show meaningful visualizations instead of raw numbers.

Three charts:
1. **Gesamtverteilung** — two donut charts side by side (one for Managen, one for Ausführen), showing Person A % vs Person B %
2. **Kategorie-Ansicht** — horizontal bar chart per category, sorted by imbalance (most unequal first)
3. **Check-in Verlauf** — line chart showing the weekly "ja"-rate over the last 8 weeks

## Why

The scoring logic is complete and correct. The Konzept explicitly calls for visual charts (section 5). Without them the results page is a wall of numbers — hard to read and not emotionally resonant, which undermines the core purpose of the app (starting a conversation).

## Scope

**In scope:**
- Donut charts on `results/auswertung`
- Category bar charts on `results/auswertung`, sorted by imbalance
- Line/bar trend chart on `checkins/verlauf`
- All chart data passed from the view as inline JSON (no extra API endpoint needed)
- Color scheme: purple for Person A, green for Person B (matching the existing Tailwind redesign)

**Out of scope:**
- Interactive / drill-down charts
- Animations
- Chart export / download
- Mobile-specific chart variants (responsive sizing via Chart.js defaults is fine)
