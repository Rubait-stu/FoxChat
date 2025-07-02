
# FoxChat: A Comprehensive Overview

FoxChat is a modern, feature-rich chat application built using Python and PyQt6 that allows users to interact with AI models or create anonymous local chats. The application has a sleek, user-friendly interface inspired by ChatGPT's design, with a focus on customization, privacy, and advanced features.

## Core Purpose and Functionality

FoxChat serves as a desktop chat interface with two primary modes:

1. **AI Chat Mode**: Allows users to communicate with AI models, primarily using the Deepseek model via the OpenRouter API. The application is designed to support multiple AI backends, though currently Deepseek is the main implemented model.

2. **Anonymous Chat Mode**: Enables users to create local-only conversations without sharing data online, useful for personal journaling, note-taking, or sandbox experiments.

## Technical Architecture

The application is built with a clean, modular architecture:

- **Frontend**: Built with PyQt6, featuring a responsive UI with customizable themes (light/dark modes)
- **Backend**: Python-based with API integrations for AI models
- **Data Storage**: Local JSON files for session management and configuration
- **API Integration**: Currently uses OpenRouter API to access the Deepseek AI model

## Key Features

### 1. Chat Interface
- Real-time AI text generation with streaming responses
- Markdown rendering for rich text formatting (bold, code blocks, lists, etc.)
- Copy functionality for messages
- Typing indicators during AI responses

### 2. Session Management
- Create, rename, and switch between multiple chat sessions
- Persistent storage of chat history in JSON format
- Session-specific model selection

### 3. File Handling
- File upload and preview capabilities
- Support for various file types (images, PDFs, documents, etc.)
- Drag and drop functionality for files and text
- Inline image previews in chat messages

### 4. UI/UX Features
- ChatGPT-inspired interface with sidebar navigation
- Theme switching between light and dark modes
- Responsive layout with collapsible sidebar
- Welcome message on startup

### 5. API Integration
- Currently uses Deepseek model via OpenRouter API
- API key stored in .env file for security
- Streaming API support for real-time text generation
- Error handling for API failures

## Technical Components

### Core Modules
1. **Main Window (`main_window.py`)**: The central component managing the application's state, handling user interactions, and coordinating between different UI components.

2. **API Manager (`api_manager.py`)**: Handles communication with AI APIs, including:
   - Query functions for different AI models
   - Streaming API support for real-time responses
   - Error handling for API calls

3. **Chat Area (`chat_area.py`)**: Manages the display of messages, including:
   - Message rendering with Markdown support
   - File previews
   - Typing indicators
   - Streaming message updates

4. **Input Panel (`input_panel.py`)**: Handles user input, including:
   - Text input with keyboard shortcuts
   - File attachment functionality
   - Drag and drop support

5. **Sidebar (`sidebar.py`)**: Provides navigation and session management:
   - Chat session list
   - Model selection
   - Chat mode switching
   - Settings access

6. **File Manager (`file_manager.py`)**: Manages persistent storage:
   - Session saving and loading
   - API profile management

### Advanced Features
1. **Markdown Rendering**: Uses Python's markdown library with extensions for rich text formatting
2. **File Preview**: Custom widget for displaying file previews with type detection
3. **Theme System**: QSS-based theming with light and dark mode support

## API Integration

FoxChat currently uses the OpenRouter API to access the Deepseek AI model. The API key is stored in the `.env` file for security. The application supports both standard and streaming API calls, with the latter providing real-time text generation for a more interactive experience.

## Data Storage

The application stores data locally in JSON format:
- Chat sessions are saved in the `sessions` directory
- API profiles are stored in `api_profiles.json`
- No cloud dependency or data sharing

## Current Limitations and Development Areas

According to the project documentation, several features are still under development:

1. **API Profile System**: While custom APIs can be created, there are issues with validation and UI for editing.
2. **Session Management**: Lacks export/import functionality and has minor UX issues.
3. **Error Handling**: Limited UI feedback for API failures and minimal runtime validation.
4. **Settings Panel**: Placeholder exists but not fully implemented.
5. **Theme Switching**: Recently implemented but may have edge cases.

## Conclusion

FoxChat is a powerful desktop chat application that combines the capabilities of AI-powered conversations with the privacy of local chat sessions. Its modular architecture, rich feature set, and focus on user experience make it suitable for a variety of use cases, from AI-assisted writing and coding to personal note-taking and journaling. The application continues to evolve with new features and improvements being actively developed.



