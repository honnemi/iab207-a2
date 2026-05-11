from flask import Blueprint, render_template, request

events_bp = Blueprint('events', __name__)

# Placeholder movie events data (static for now)
events_data = [
    {
        "id": 1,
        "title": "Avengers: Doomsday",
        "category": "Action",
        "date": "15 June 2026 - 19:00",
        "location": "Cinema City",
        "price": 25,
        "available_tickets": 120,
        "image": "avengers.jpg"
    },
    {
        "id": 2,
        "title": "Oppenheimer",
        "category": "Drama",
        "date": "20 May 2026 - 20:30",
        "location": "Grand Theatre",
        "price": 18,
        "available_tickets": 80,
        "image": "oppenheimer.jpg"
    },
    {
        "id": 3,
        "title": "Deadpool & Wolverine",
        "category": "Comedy",
        "date": "10 July 2026 - 21:00",
        "location": "Metro Cinema",
        "price": 22,
        "available_tickets": 150,
        "image": "deadpool.jpg"
    },
    {
        "id": 4,
        "title": "Dune: Part Three",
        "category": "Sci-Fi",
        "date": "05 June 2026 - 18:45",
        "location": "IMAX Theatre",
        "price": 30,
        "available_tickets": 95,
        "image": "dune.jpg"
    },
    {
        "id": 5,
        "title": "The Conjuring: Last Rites",
        "category": "Horror",
        "date": "25 May 2026 - 22:00",
        "location": "Horror House",
        "price": 20,
        "available_tickets": 60,
        "image": "conjuring.jpg"
    },
]


@events_bp.route('/events')
def browse_events():
    """Browse events with category filter and search functionality"""
    category = request.args.get('category')
    search = request.args.get('search', '').strip().lower()

    # Filter events based on category and search
    events = events_data

    if category:
        events = [e for e in events if e['category'] == category]

    if search:
        events = [e for e in events 
                  if search in e['title'].lower() or search in e['category'].lower()]

    # Get unique categories for filter dropdown
    categories = sorted(list(set(event['category'] for event in events_data)))

    return render_template('events.html', 
                           events=events, 
                           categories=categories,
                           selected_category=category,
                           search=search)