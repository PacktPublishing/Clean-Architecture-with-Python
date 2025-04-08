# Chapter 11

The code exampes from the chapter can be found in the order of appearance in the files with numeric indexes (ex:
`00_error_class.py`)

## Companion task management application

This folder contains a proof-of-concept implementation of the order processing system described in Chapter 11 of "Clean Architecture with Python." It demonstrates the transformation from a legacy application with architectural violations to a clean, well-structured system following Clean Architecture principles.

## Overview

The Order Processing System is a simple Flask application that allows users to:

1. View available products
2. Create orders with multiple items
3. Process payments (simulated)

The application provides two parallel implementations:

- **Legacy Implementation**: Demonstrates the architectural issues discussed in Chapter 11, with tangled dependencies, mixed business logic, and direct database access in route handlers.
- **Clean Architecture Implementation**: Shows the refactored application with proper separation of concerns, domain-driven design, and clean architectural boundaries.

## Running the Application

Ensure you have followed the instructions in the [Getting started](../README.md#2-getting-started) section to set up your environment.

### Understanding the Interface

The home page displays two options:
- **Legacy Implementation**: Clicking this button will explicitly use the legacy implementation, regardless of the feature flag setting
- **Clean Architecture Implementation**: Clicking this button will explicitly use the Clean Architecture implementation

At the bottom of the home page, you'll see a "Current Mode" indicator showing which implementation would be used by default according to the feature flag setting. This is primarily for demonstration purposes to show how a feature flag approach might work in a real-world transformation.

Unlike the pattern described in Chapter 11 where a single endpoint might use a feature flag to choose between implementations, this demo app uses separate endpoints for clarity.




### Running the Application

1. Start the application:
   ```
   python main.py
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

3. Use the interface to create orders using either the legacy or Clean Architecture implementation.

## Key Features to Explore

- **Parallel Implementations**: Both legacy and clean code coexist, demonstrating the transformation strategy from Chapter 11.
- **Domain Model**: Explore the rich domain model in `/domain/entities/` with proper encapsulation and business rules.
- **Repository Pattern**: See how the repository interfaces in the domain layer are implemented in the infrastructure layer without leaking implementation details.
- **Use Case Pattern**: Examine how application-specific business rules are orchestrated in the use cases.
- **Controller Pattern**: Observe how controllers handle the translation between external formats and internal models.

## About the Feature Flag

The application includes a feature flag system as described in Chapter 11, though its utilization differs from the chapter's example:

1. In the companion app, we use separate routes for clarity (`/legacy/orders` and `/clean/orders`) to make the choice of which application to use (legacy or clean architecture) explicit.
2. You can still set the feature flag (`USE_CLEAN_ARCHITECTURE`) but it will only affect the "Current Mode" indicator on the home page.
```bash
USE_CLEAN_ARCHITECTURE=False python main.py
```

This allows you switch between the two implementations, placing orders using the legacy or Clean Architecture implementation.