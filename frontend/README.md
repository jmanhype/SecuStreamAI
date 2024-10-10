# SecuStreamAI Frontend

This is the frontend dashboard for **SecuStreamAI**, built with React and Material-UI. It provides real-time visualization and interaction with security event data processed by the backend services.

## Table of Contents

1. [Available Scripts](#available-scripts)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Environment Configuration](#environment-configuration)
5. [Running the Application](#running-the-application)
6. [Testing](#testing)
7. [Deployment](#deployment)
8. [Contributing](#contributing)
9. [License](#license)
10. [Contact](#contact)

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.<br>
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.<br>
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.<br>
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.<br>
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br>
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc.) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point, you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and medium deployments, and you shouldn't feel obligated to use this feature. However, we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Prerequisites

Before setting up the SecuStreamAI Frontend, ensure you have the following installed:

- [Node.js](https://nodejs.org/en/download/) (version 18 or higher)
- [npm](https://www.npmjs.com/get-npm) (comes with Node.js)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/SecuStreamAI.git
cd SecuStreamAI/frontend
```

### 2. Install Dependencies

Ensure you are in the `frontend/` directory and run:

```bash
npm install
```

## Environment Configuration

Create a `.env` file in the `frontend/` directory based on the example:

```bash
cp .env.example .env
```

### Setting Environment Variables

Open the `.env` file and set the necessary environment variables:

```env
REACT_APP_API_URL=http://localhost:8080/api/v1
# Add other environment variables as needed
```

**Note:** Replace placeholders with actual values as required by your application. Do not commit sensitive information like API keys to the repository.

## Running the Application

### Development Mode

Start the development server:

```bash
npm start
```

Open [http://localhost:3000](http://localhost:3000) to view the application in your browser. The page will reload when you make changes.

### Production Build

Create an optimized production build:

```bash
npm run build
```

The build artifacts will be stored in the `build/` directory.

## Testing

Run the test suite using:

```bash
npm test
```

This will launch the test runner in interactive watch mode.

## Deployment

### Docker Deployment

Ensure Docker is installed and running on your system.

1. **Build the Docker Image:**

   ```bash
   docker build -t yourusername/secustreamai-frontend:latest .
   ```

2. **Run the Docker Container:**

   ```bash
   docker run -d -p 3000:3000 yourusername/secustreamai-frontend:latest
   ```

### Integrate with Docker Compose

If you're using Docker Compose for the entire project, ensure the frontend service is defined in your `docker/docker-compose.yaml`:

```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
  ports:
    - "3000:3000"  # React development server port
  environment:
    - REACT_APP_API_URL=${API_V1_STR}
  volumes:
    - ./frontend:/app
    - /app/node_modules
  depends_on:
    - app  # Ensure the backend is up before the frontend
```

Then, build and start the services:

```bash
docker-compose up --build
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the repository.**
2. **Create a new branch** for your feature or bugfix.
3. **Commit your changes** with clear messages.
4. **Push your branch** and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or feedback, please contact [your.email@example.com](mailto:your.email@example.com).

## Acknowledgments

- [Create React App](https://github.com/facebook/create-react-app)
- [Material-UI](https://mui.com/)
- [Axios](https://axios-http.com/)