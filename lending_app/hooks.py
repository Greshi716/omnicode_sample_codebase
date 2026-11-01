"""Lifecycle hooks for the library lending app (omnicode_core.hooks)."""

from omnicode_core.hooks import Allow, Block, HookEvent, hook

from lending_app.policy import contains_card_number, contains_destructive_sql


@hook("before_prompt")
def reject_payment_data(event: HookEvent):
    if contains_card_number(str(event.payload)):
        return Block("Payment card data must not appear in prompts.")
    return Allow()


@hook("before_tool")
def reject_destructive_sql(event: HookEvent):
    if contains_destructive_sql(event.payload.get("arguments", {})):
        return Block("Destructive DDL is not allowed in tool arguments.")
    return Allow()
