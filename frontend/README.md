# frontend

## Project setup

```
npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```

### Lints and fixes files

```
npm run lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

### Intall npm router so pages can be linked

'''
npm install vue-router
'''

#### This is the file structure I attempted to replicate from per internet adivice

#### modify this as necessary and only keep what you need.

#### Modularity is the key here. Read the comments and if you want to make a drastic

#### change from this. Consult front-end team!

my-app/
├── public/
│ ├── index.html # Main HTML template for the app
│ └── assets/ # Global static assets like images, icons, and fonts
│
├── src/
│ ├── assets/ # Component-specific static assets, e.g., logos, icons
│ ├── components/ # Reusable components
│ │ ├── common/ # Common UI components (buttons, inputs, cards)
│ │ ├── layout/ # Layout components (header, footer, sidebar)
│ │ ├── auth/ # Components for login, signup, password recovery
│ │ ├── user/ # Components for user profile and account features
│ │ ├── search/ # Components for search and filter functionality
│ │ └── landing/ # Landing page-specific components
│ │
│ ├── pages/ # Page components for Vue Router (e.g., landing, login, account)
│ │ ├── LandingPage.vue
│ │ ├── LoginPage.vue
│ │ ├── SignupPage.vue
│ │ ├── UserProfilePage.vue
│ │ └── SearchPage.vue
│ │
│ ├── App.vue # Root app component
│ ├── router/ # Vue Router setup for page navigation
│ │ └── index.js
│ │
│ ├── store/ # Vuex state management for global state
│ │ └── index.js
│ │
│ ├── services/ # API calls and external services
│ │ ├── authService.js # Authentication service (e.g., login, logout)
│ │ ├── userService.js # User-related service (e.g., profile info, update)
│ │ └── searchService.js # Search-related service
│ │
│ ├── utils/ # Utility functions and helpers (e.g., validation, formatting)
│ │ └── validation.js
│ │
│ └── main.js # Entry point for the Vue app
│
└── package.json # Dependencies and scripts for the project
