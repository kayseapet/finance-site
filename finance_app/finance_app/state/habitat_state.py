import asyncio
import reflex as rx

class HabitatState(rx.State):
    # --- Core State Variables ---
    growth_xp: int = 0
    savings_balance: float = 350.00
    emergency_target: float = 300.00
    is_raining: bool = False
    show_sparkles: bool = False
    last_action_log: str = "System ready. No recent transactions."  # <--- ADD THIS LINE

    # --- Computed Variables ---
    @rx.var
    def plant_stage(self) -> int:
        if self.growth_xp >= 150:
            return 3
        elif self.growth_xp >= 100:
            return 2
        elif self.growth_xp >= 50:
            return 1
        return 0

    @rx.var
    def is_healthy(self) -> bool:
        return self.savings_balance >= self.emergency_target

    @rx.var
    def current_image(self) -> str:
        if self.plant_stage == 0:
            return "/state_00.png"
        health_prefix = "1" if self.is_healthy else "0"
        return f"/state_{health_prefix}{self.plant_stage}.png"

    @rx.var
    def cushion_percentage(self) -> float:
        if self.emergency_target <= 0:
            return 0.0
        pct = (self.savings_balance / self.emergency_target) * 100.0
        return max(0.0, min(100.0, pct))

    @rx.var
    def gardener_rank(self) -> str:
        ranks = [
            "🌱 Level 1 Seedling",
            "🌿 Level 2 Sprout",
            "🌺 Level 3 Budding",
            "👑 Level 4 Master Gardener",
        ]
        return ranks[min(self.plant_stage, 3)]

    # --- Actions ---
    async def add_savings(self, amount: float):
        self.savings_balance += amount
        self.is_raining = True
        self.last_action_log = f"💧 Deposited +${amount:.2f}! Shield replenished."
        yield
        await asyncio.sleep(2.0)
        self.is_raining = False

    def sim_impulse_spend(self, amount: float):
        if self.savings_balance >= amount:
            self.savings_balance -= amount
            self.last_action_log = f"⚠️ Spent ${amount:.2f}! Shield reduced."
        else:
            self.savings_balance = 0.0
            self.last_action_log = "🚨 Emergency fund depleted!"
            
        if not self.is_healthy:
            self.is_raining = False

    async def sim_deposit_cushion(self, amount: float):
        self.savings_balance += amount
        self.is_raining = True
        self.last_action_log = f"💧 Deposited +${amount:.2f}! Cushion replenished."
        yield
        await asyncio.sleep(2.0)
        self.is_raining = False

    async def trigger_level_up_effects(self):
        self.show_sparkles = True
        yield rx.toast.success(
            "🎉 YOU HAVE LEVELED UP! Your habitat is flourishing!",
            position="top-center",
            duration=4000,
            style={
                "background_color": "#064E3B",
                "color": "#FAFAF9",
                "border": "2px solid #EAB308",
                "border_radius": "0px",
                "font_weight": "bold"
            }
        )
        await asyncio.sleep(3.5)
        self.show_sparkles = False