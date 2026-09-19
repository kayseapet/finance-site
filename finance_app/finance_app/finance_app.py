import reflex as rx
from finance_app.pages.dashboard import dashboard_page
from finance_app.pages.article_player import article_player_page

# Initialize the Reflex application
app = rx.App(
    style={
        "background_color": "#FAFAF9",
        "font_family": "sans-serif",
    }
)

# --- Register Routes ---

# 1. Main Dashboard Route
app.add_page(
    dashboard_page,
    route="/",
    title="SproutFinance | Dashboard",
)

# 2. Dynamic Learning Module Route
# Using [current_article_id] allows Reflex to map the URL parameter directly into ArticlePlayerState
app.add_page(
    article_player_page,
    route="/learn/[current_article_id]",
    title="SproutFinance | Learn Module",
)