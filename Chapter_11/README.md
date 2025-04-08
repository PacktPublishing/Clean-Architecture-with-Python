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

A feature flag (`USE_CLEAN_ARCHITECTURE`) controls which implementation is used by default, allowing you to compare both approaches.

## Project Structure

The application follows the Clean Architecture layers discussed in the book:

```
order_system/
├── domain/           # Domain entities, value objects, and repository interfaces
├── application/      # Use cases that orchestrate domain objects
├── interfaces/       # Controllers that adapt between external formats and use cases
├── infrastructure/   # Concrete implementations of repositories and services
├── web/              # Flask-specific code for the web interface
```

## Running the Application

### Prerequisites

- Python 3.13 or higher
- pip (Python package manager)

### Understanding the Interface

The home page displays two options:
- **Legacy Implementation**: Clicking this button will explicitly use the legacy implementation, regardless of the feature flag setting
- **Clean Architecture Implementation**: Clicking this button will explicitly use the Clean Architecture implementation

At the bottom of the home page, you'll see a "Current Mode" indicator showing which implementation would be used by default according to the feature flag setting. This is primarily for demonstration purposes to show how a feature flag approach might work in a real-world transformation.

Unlike the pattern described in Chapter 11 where a single endpoint might use a feature flag to choose between implementations, this demo app uses separate endpoints for clarity.

### Installation

1. Go to the `EcomApp` folder:
   ```
   cd EcomApp
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the application:
   ```
   python -m order_system.main
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

The application includes a feature flag system as described in Chapter 11, though its implementation differs slightly from the chapter's example:

1. In the companion app, we use separate routes for clarity (`/legacy/orders` and `/clean/orders`)
2. The feature flag (`USE_CLEAN_ARCHITECTURE`) primarily affects the "Current Mode" indicator on the home page

If you want to experiment with changing this setting:

1. You can change the `USE_CLEAN_ARCHITECTURE` environment variable:
   ```
   # Use clean architecture as default
   export USE_CLEAN_ARCHITECTURE=True
   
   # Use legacy implementation as default
   export USE_CLEAN_ARCHITECTURE=False
   ```

2. Or modify the default value in `config.py`

This feature flag demonstrates the pattern described in Chapter 11 where a system undergoing transformation might use configuration to control which implementation handles requests. In a real-world scenario, this would allow for gradual migration with the ability to quickly revert if issues arise.

## Educational Value

This application serves as a practical demonstration of the concepts discussed in Chapter 11. By examining the code and running the application, you can gain deeper insights into:

1. How Clean Architecture principles apply in a real Python application
2. The process of incrementally refactoring from legacy to clean code
3. The benefits of clear architectural boundaries and separation of concerns
4. Practical implementation of domain-driven design in Python

Experiment with the code, make changes, and observe how each implementation responds to those changes to deepen your understanding of Clean Architecture principles.