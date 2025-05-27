# Chapter 11

## Chapter code excerpts
The code snippets from the chapter can be found in the order of appearance in the `chapter_code_excerpts` folder. Examples: `00_error_class.py`  
These are provided for reference and are not meant to be runnable.

## Companion task management application

This folder contains a proof-of-concept implementation of the order processing system described in Chapter 11 of "Clean Architecture with Python." It demonstrates the transformation from a legacy application with architectural violations to a clean, well-structured system following Clean Architecture principles.

## Overview

The Order Processing System is a simple Flask application that allows users to:

1. View available products
2. Create orders with multiple items
3. Process payments (simulated)

The application demonstrates the feature flag transformation pattern described in Chapter 11:

- **Single Route Implementation**: The `/orders` endpoint uses a feature flag to choose between legacy and clean implementations
- **Legacy Implementation**: Demonstrates the architectural issues discussed in Chapter 11, with tangled dependencies, mixed business logic, and direct database access in route handlers
- **Clean Architecture Implementation**: Shows the refactored application with proper separation of concerns, domain-driven design, and clean architectural boundaries


## Running the Application

Ensure you have followed the instructions in the [Getting started](../README.md#2-getting-started) section to set up your environment.

### Understanding the Interface

The home page displays two options:
- **Legacy Implementation**: Clicking this button will explicitly use the legacy implementation, regardless of the feature flag setting
- **Clean Architecture Implementation**: Clicking this button will explicitly use the Clean Architecture implementation


## Running the Application

Ensure you have followed the instructions in the [Getting started](../README.md#2-getting-started) section to set up your environment.

### Feature Flag Control

The application uses the `USE_CLEAN_ARCHITECTURE` environment variable to control which implementation handles requests. This demonstrates the transformation pattern from Chapter 11 where a single route chooses between implementations.

### Starting the Application

```bash
cd EcomApp

# Legacy Implementation
USE_CLEAN_ARCHITECTURE=false python main.py

# Clean Architecture Implementation  
USE_CLEAN_ARCHITECTURE=true python main.py

# On Windows
set USE_CLEAN_ARCHITECTURE=true && python main.py
```
