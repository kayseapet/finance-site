import reflex as rx
from finance_app.state.habitat_state import HabitatState


def impulse_sandbox_widget() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Card Header
            rx.hstack(
                rx.heading(
                    "🛡️ Emergency Shield Simulator",
                    class_name="text-lg font-black text-[#064E3B]",
                ),
                rx.badge(
                    rx.cond(HabitatState.is_healthy, "HEALTHY SOIL", "WILTED SOIL"),
                    class_name=rx.cond(
                        HabitatState.is_healthy,
                        "bg-[#064E3B] text-[#FAFAF9] font-bold rounded-none px-2 py-1 text-xs",
                        "bg-[#EF4444] text-[#FAFAF9] font-bold rounded-none px-2 py-1 text-xs",
                    ),
                ),
                class_name="w-full justify-between items-center border-b border-[#064E3B]/20 pb-2",
            ),
            
            # Progress Bar & Numeric Target
            rx.vstack(
                rx.hstack(
                    rx.text("Current Shield Cushion", class_name="text-xs font-bold text-[#064E3B] uppercase"),
                    rx.text(
                        f"${HabitatState.savings_balance:.2f} / ${HabitatState.emergency_target:.2f}",
                        class_name="text-sm font-black text-[#064E3B]",
                    ),
                    class_name="w-full justify-between items-center",
                ),
                # Dynamic Visual Progress Bar
                rx.box(
                    rx.box(
                        class_name="h-full bg-[#064E3B] transition-all duration-300",
                        style={"width": f"{HabitatState.cushion_percentage}%"},
                    ),
                    class_name="w-full h-3 bg-[#E5E7EB] border border-[#064E3B] rounded-none overflow-hidden",
                ),
                class_name="w-full space-y-1 my-2",
            ),

            # Interactive Scenario Buttons
            rx.vstack(
                rx.text(
                    "SIMULATE REAL-WORLD SCENARIOS:",
                    class_name="text-[10px] font-black text-[#064E3B] uppercase tracking-wider",
                ),
                rx.hstack(
                    rx.button(
                        "🎟️ Buy $120 Ticket",
                        on_click=HabitatState.sim_impulse_spend(120.00),
                        class_name="flex-1 bg-[#FAFAF9] hover:bg-[#FFEDD5] text-[#064E3B] font-bold py-2 px-3 border border-[#064E3B] rounded-none text-xs cursor-pointer",
                    ),
                    rx.button(
                        "🚨 $180 Dental Bill",
                        on_click=HabitatState.sim_impulse_spend(180.00),
                        class_name="flex-1 bg-[#FAFAF9] hover:bg-[#FFEDD5] text-[#EF4444] font-bold py-2 px-3 border border-[#064E3B] rounded-none text-xs cursor-pointer",
                    ),
                    class_name="w-full space-x-2",
                ),
                rx.button(
                    "💧 Replenish Cushion (+$100)",
                    on_click=HabitatState.sim_deposit_cushion(100.00),
                    class_name="w-full bg-[#064E3B] hover:bg-[#FB923C] text-[#FAFAF9] font-black py-2 px-3 border border-[#064E3B] rounded-none text-xs uppercase tracking-wider cursor-pointer mt-1",
                ),
                class_name="w-full space-y-1.5",
            ),

            # Live Action Ledger
            rx.box(
                rx.hstack(
                    rx.text("⚡ LIVE LOG:", class_name="text-[10px] font-black text-[#064E3B] uppercase"),
                    rx.text(
                        HabitatState.last_action_log,
                        class_name="text-[11px] font-mono text-[#064E3B] truncate",
                    ),
                    class_name="items-center space-x-2",
                ),
                class_name="w-full bg-[#FAFAF9] border border-[#064E3B] px-2.5 py-1 rounded-none my-1",
            ),
            class_name="space-y-3 w-full",
        ),
        class_name="bg-[#FAFAF9] border-2 border-[#064E3B] p-5 rounded-none w-full shadow-none",
    )