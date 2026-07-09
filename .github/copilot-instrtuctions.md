# Chronica Copilot Instructions

## Project identity

Chronica is a local-first desktop time tracker built with Python and PySide6.
It focuses on personal time awareness, app/window usage analysis, and a character/dialogue layer.
Prioritize maintainability, local-first behavior, and coherent UI over quick demo-only code.

## Architecture rules

- Domain models must stay independent from PySide6, QtWidgets, and QML.
- UI code may depend on domain/view models, but domain code must not depend on UI code.
- QML is allowed for complex visual components such as the session timeline.
- QML should render data and emit UI events only.
- Business rules, aggregation, formatting, and data transformation should stay in Python.
- Do not access the database directly from widgets or QML.
- Prefer explicit view models / bridge objects between Python and QML.

## Expected data flow

Tracking / storage
→ repository
→ domain service / aggregation
→ view model / mapper
→ QtWidgets or QML bridge
→ UI rendering
→ UI signal
→ Python slot / controller

## PySide6 / QML rules

- Use PySide6 only.
- Do not introduce extra GUI frameworks.
- Prefer QQuickWidget when embedding a QML component into the existing QtWidgets app.
- QML files should live under `src/chronica/ui/qml/`.
- Python bridge classes should live under `src/chronica/ui/bridges/` or a nearby presentation-layer package.
- Do not move the whole app to QQmlApplicationEngine unless explicitly requested.

## Coding style

- Use type hints.
- Prefer dataclasses for simple value models.
- Use classes for stable domain concepts, stateful controllers, bridges, services, and cross-layer mappers.
- Use pure functions for simple formatting, calculation, path resolving, and boolean checks.
- Do not introduce Manager/Coordinator/Helper classes unless the responsibility is clearly named and justified.
- Keep changes small and reviewable.
- Do not rewrite unrelated files.
- Do not rename existing public classes or methods unless requested.

## Dialogue system rules

- `Line` and `DialogueTemplate` represent script/template-time data.
- `RenderedLine` and `RenderedDialogue` represent context-rendered playback data.
- `DialoguePlayer` handles playback lifecycle.
- Rendering and playback should remain separate responsibilities.

## Testing / validation

- Add tests for domain logic, aggregation, formatting, and mapping when changing behavior.
- For UI work, keep a small manual validation note in the final summary.
- Before making large edits, inspect the relevant files first and propose a short plan.
- After changes, summarize modified files, risks, and how to validate.

## AI behavior

- Read before editing.
- Plan before large edits.
- Preserve existing behavior unless the task explicitly asks to change it.
- Avoid speculative abstractions.
- Ask before introducing new dependencies.