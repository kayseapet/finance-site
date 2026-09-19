import reflex as rx
from finance_app.data.content import ALL_ARTICLES, ArticleData
from finance_app.state.habitat_state import HabitatState


class ArticlePlayerState(rx.State):
    """Manages active article state and completion triggers."""

    @rx.var
    def active_article(self) -> ArticleData:
        """Finds the active article based on the current_article_id dynamic route param."""
        target_id = self.current_article_id
        for article in ALL_ARTICLES:
            article_id = getattr(article, "id", None) or article.get("id", "")
            if article_id == target_id or str(article_id).lower().replace(" ", "-") == target_id:
                return article
        return ALL_ARTICLES[0]

    # --- Robust Computed Property Getters ---
    @rx.var
    def article_title(self) -> str:
        art = self.active_article
        return getattr(art, "title", None) or (art.get("title") if isinstance(art, dict) else "Article Title")

    @rx.var
    def article_category(self) -> str:
        art = self.active_article
        return getattr(art, "category", None) or (art.get("category") if isinstance(art, dict) else "GENERAL")

    @rx.var
    def article_read_time(self) -> str:
        art = self.active_article
        return getattr(art, "read_time", None) or (art.get("read_time") if isinstance(art, dict) else "3 min read")

    @rx.var
    def article_content(self) -> str:
        art = self.active_article
        # Checks attribute, dict key, or provides fallback
        if hasattr(art, "content"):
            return art.content
        elif isinstance(art, dict) and "content" in art:
            return art["content"]
        return "Lesson content loading..."

    @rx.var
    def article_image_url(self) -> str:
        art = self.active_article
        if hasattr(art, "image_url"):
            return art.image_url
        filename = getattr(art, "image_filename", None) or (art.get("image_filename") if isinstance(art, dict) else "default_article.png")
        filename = str(filename).lstrip("/")
        return f"/{filename}"

    async def complete_article_and_return(self):
        """Awards +50 XP, triggers level-up check, and redirects to dashboard."""
        prev_stage = HabitatState.plant_stage

        # Award Growth XP
        HabitatState.growth_xp += 50
        HabitatState.last_action_log = (
            f"📚 Completed '{self.article_title}' (+50 XP)!"
        )

        # Check for level-up transition
        new_stage = HabitatState.plant_stage
        if new_stage > prev_stage:
            yield HabitatState.trigger_level_up_effects()

        # Redirect back to main dashboard
        yield rx.redirect("/")


def article_player_page() -> rx.Component:
    """Full view page for reading learning modules and claiming XP."""
    return rx.box(
        rx.vstack(
            # Top Navigation Header
            rx.hstack(
                rx.link(
                    rx.button(
                        "← Back to Habitat",
                        class_name="bg-[#064E3B] text-[#FAFAF9] font-bold text-xs px-4 py-2 rounded-none cursor-pointer border border-[#FAFAF9]",
                    ),
                    href="/",
                ),
                rx.badge(
                    "LEARNING MODULE",
                    class_name="bg-[#EAB308] text-[#064E3B] font-bold px-3 py-1 rounded-none text-xs uppercase tracking-wider",
                ),
                class_name="w-full justify-between items-center pb-4 border-b-2 border-[#064E3B]",
            ),
            
            # Article Card
            rx.box(
                rx.vstack(
                    rx.image(
                        src=ArticlePlayerState.article_image_url,
                        alt=ArticlePlayerState.article_title,
                        class_name="w-full h-56 md:h-72 object-cover border-b-2 border-[#064E3B] rounded-none",
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.badge(
                                ArticlePlayerState.article_category,
                                class_name="bg-[#064E3B] text-[#FAFAF9] font-bold rounded-none px-2.5 py-1 text-xs",
                            ),
                            rx.text(
                                f"⏱️ {ArticlePlayerState.article_read_time}",
                                class_name="text-xs font-bold text-[#FB923C]",
                            ),
                            class_name="items-center space-x-3",
                        ),
                        rx.heading(
                            ArticlePlayerState.article_title,
                            class_name="text-3xl font-black text-[#064E3B] tracking-tight",
                        ),
                        rx.text(
                            ArticlePlayerState.article_content,
                            class_name="text-base text-[#064E3B] leading-relaxed pt-3 border-t border-[#064E3B]/20 w-full",
                        ),
                        rx.box(
                            rx.button(
                                "🎉 Finish Lesson (+50 Growth XP)",
                                on_click=ArticlePlayerState.complete_article_and_return,
                                class_name="w-full bg-[#064E3B] hover:bg-[#FB923C] text-[#FAFAF9] font-black py-4 px-6 rounded-none text-sm uppercase tracking-wider cursor-pointer border border-[#064E3B]",
                            ),
                            class_name="w-full pt-6",
                        ),
                        class_name="p-6 space-y-4 w-full items-start",
                    ),
                    class_name="space-y-0 w-full",
                ),
                class_name="bg-[#FAFAF9] border-2 border-[#064E3B] rounded-none w-full max-w-3xl mx-auto overflow-hidden mt-6",
            ),
            class_name="max-w-4xl mx-auto space-y-4",
        ),
        class_name="min-h-screen bg-[#FAFAF9] p-6 md:p-10 font-sans",
    )