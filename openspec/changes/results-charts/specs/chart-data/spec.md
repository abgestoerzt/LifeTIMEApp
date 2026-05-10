# Spec: Chart Data Preparation

## Capability

Transform existing scoring data into JSON structures that Chart.js can consume directly. All transformation happens server-side; the template just passes data through.

## Gesamtverteilung chart data

Input: `PaarSession`
Output:
```json
{
  "management": {"person_a": <float 0-100>, "person_b": <float 0-100>},
  "ausfuehrung": {"person_a": <float 0-100>, "person_b": <float 0-100>},
  "label_a": "<username of partner_a>",
  "label_b": "<username of partner_b>"
}
```

Rules:
- Percentages always sum to 100 for each dimension
- Values are rounded to 1 decimal place
- `extern` and `trifft_nicht_zu` answers are excluded from both partners' scores (denominator is only ich/partner/beide answers)
- If there are no scoreable answers, return 50/50

## Kategorie chart data

Input: `PaarSession`
Output: list of objects, **sorted descending by imbalance**:
```json
[
  {
    "kategorie": "<name>",
    "icon": "<emoji>",
    "person_a": <float 0-100>,
    "person_b": <float 0-100>,
    "imbalance": <float — abs(person_a - person_b)>
  }
]
```

Rules:
- Only categories with at least one Antwort are included
- Sorted by `imbalance` descending (most unequal category first)
- Same percentage calculation rules as Gesamtverteilung

## Verlauf chart data

Input: `PaarSession`
Output:
```json
{
  "wochen": ["YYYY-MM-DD", ...],
  "person_a": [<float 0-100>, ...],
  "person_b": [<float 0-100>, ...]
}
```

Rules:
- At most 8 weeks, oldest first
- `person_a` and `person_b` values are the percentage of "ja" answers for that week
- A week with a CheckIn but zero CheckInAntworten returns 0
- A week with no CheckIn for that person returns `null` (Chart.js will render a gap in the line)
