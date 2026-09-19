import reflex as rx
from finance_app.data.content import ALL_ARTICLES, ArticleData
from finance_app.state.habitat_state import HabitatState


class ArticlePlayerState(rx.State):
    """Manages active article state and completion triggers."""

    @rx.var
    def active_article(self) -> ArticleData:
        """Resolves active article based on dynamic URL route parameter."""
        target_id = self.current_article_id
        for article in ALL_ARTICLES:
            if (
                article.id == target_id
                or article.id.lower().replace(" ", "-") == target_id
            ):
                return article
        return ALL_ARTICLES[0]

    # --- Computed Safe Property Exposers for Reflex Binding ---
    @rx.var
    def title(self) -> str:
        return getattr(self.active_article, "title", "Article Title")

    @rx.var
    def category(self) -> str:
        return getattr(self.active_article, "category", "Savings")

    @rx.var
    def read_time(self) -> str:
        return getattr(self.active_article, "read_time", "3 min read")

    @rx.var
    def author_info(self) -> str:
        return getattr(self.active_article, "author_info", "SproutFinance Team")

    @rx.var
    def intro_text(self) -> str:
        return getattr(self.active_article, "intro_text", "")

    @rx.var
    def mid_text(self) -> str:
        return getattr(self.active_article, "mid_text", "")

    @rx.var
    def closing_text(self) -> str:
        return getattr(self.active_article, "closing_text", "")

    @rx.var
    def head_image_url(self) -> str:
        label = getattr(self.active_article, "head_image_label", "default_article.png")
        return f"/{label.lstrip('/')}"

    @rx.var
    def paragraph_photo_url(self) -> str:
        label = getattr(self.active_article, "paragraph_photo_label", "default_article.png")
        return f"/{label.lstrip('/')}"

    @rx.var
    def sources_list(self) -> list[str]:
        return getattr(self.active_article, "sources", [])

    async def complete_article_and_return(self):
        """Awards +50 XP, updates habitat action log, and returns to dashboard."""
        prev_stage = HabitatState.plant_stage
        
        # Award Growth XP
        HabitatState.growth_xp += 50
        HabitatState.last_action_log = f"📚 Read '{self.title}' (+50 XP)!"

        # Check for Level Up
        new_stage = HabitatState.plant_stage
        if new_stage > prev_stage:
            yield HabitatState.trigger_level_up_effects()

        # Redirect back to main dashboard
        yield rx.redirect("/")


def article_player_page() -> rx.Component:
    """Renders the full multi-section Article Reader matching the exact ArticleData schema."""
    return rx.box(
        rx.vstack(
            # --- 1. Navigation Header ---
            rx.hstack(
                rx.link(
                    rx.button(
                        "← Back to Habitat",
                        class_name="bg-[#064E3B] text-[#FAFAF9] font-bold text-xs px-4 py-2 rounded-none hover:bg-[#FB923C] transition-colors cursor-pointer border border-[#FAFAF9]",
                    ),
                    href="/",
                ),
                rx.badge(
                    "FINANCIAL EDUCATION MODULE",
                    class_name="bg-[#EAB308] text-[#064E3B] font-bold px-3 py-1 rounded-none text-xs uppercase tracking-wider",
                ),
                class_name="w-full justify-between items-center pb-4 border-b-2 border-[#064E3B]",
            ),

            # --- 2. Main Article Card ---
            rx.box(
                rx.vstack(
                    # Header Image (head_image_label)
                    rx.image(
                        src=ArticlePlayerState.head_image_url,
                        alt=ArticlePlayerState.title,
                        class_name="w-full h-56 md:h-72 object-cover border-b-2 border-[#064E3B] rounded-none",
                    ),
                    
                    # Article Meta Bar
                    rx.vstack(
                        rx.hstack(
                            rx.badge(
                                ArticlePlayerState.category,
                                class_name="bg-[#064E3B] text-[#FAFAF9] font-bold rounded-none px-2.5 py-1 text-xs uppercase",
                            ),
                            rx.text(
                                f"⏱️ {ArticlePlayerState.read_time}",
                                class_name="text-xs font-bold text-[#FB923C]",
                            ),
                            rx.text(
                                f"✍️ {ArticlePlayerState.author_info}",
                                class_name="text-xs font-bold text-[#064E3B]/70",
                            ),
                            class_name="items-center space-x-3 flex-wrap",
                        ),
                        
                        rx.heading(
                            ArticlePlayerState.title,
                            class_name="text-3xl font-black text-[#064E3B] tracking-tight pt-1",
                        ),

                        # Section 1: Intro Text
                        rx.text(
                            ArticlePlayerState.intro_text,
                            class_name="text-base text-[#064E3B] leading-relaxed pt-3 border-t border-[#064E3B]/20 w-full font-medium",
                        ),

                        # Paragraph Photo (paragraph_photo_label)
                        rx.box(
                            rx.image(
                                src=ArticlePlayerState.paragraph_photo_url,
                                alt="Section Illustration",
                                class_name="w-full h-48 md:h-64 object-cover border border-[#064E3B] my-2",
                            ),
                            class_name="w-full py-2",
                        ),

                        # Section 2: Mid Text
                        rx.text(
                            ArticlePlayerState.mid_text,
                            class_name="text-base text-[#064E3B] leading-relaxed font-medium w-full",
                        ),

                        # Section 3: Closing Text
                        rx.text(
                            ArticlePlayerState.closing_text,
                            class_name="text-base text-[#064E3B] leading-relaxed font-medium pt-2 w-full",
                        ),

                        # Section 4: Sources List
                        rx.vstack(
                            rx.text(
                                "📖 Sources & References:",
                                class_name="text-xs font-black text-[#064E3B] uppercase tracking-wider",
                            ),
                            rx.foreach(
                                ArticlePlayerState.sources_list,
                                lambda source: rx.text(
                                    f"• {source}",
                                    class_name="text-xs text-[#064E3B]/80 font-mono",
                                ),
                            ),
                            class_name="w-full bg-[#FFEDD5] p-4 border border-[#064E3B] mt-4 space-y-1 items-start",
                        ),

                        # Claim Reward Button
                        rx.box(
                            rx.button(
                                "🎉 Finish Lesson (+50 Growth XP)",
                                on_click=ArticlePlayerState.complete_article_and_return,
                                class_name="w-full bg-[#064E3B] hover:bg-[#FB923C] text-[#FAFAF9] font-black py-4 px-6 rounded-none text-sm uppercase tracking-wider cursor-pointer border border-[#064E3B] transition-colors",
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