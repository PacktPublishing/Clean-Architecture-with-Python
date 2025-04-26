class ArchitectureConfig:
    """Defines Clean Architecture structure and rules."""

    # Ordered from innermost to outermost layer
    LAYER_HIERARCHY = [
        "domain",
        "application",
        "interfaces",
        "infrastructure",
    ]
