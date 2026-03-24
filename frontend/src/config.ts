/**
 * Application configuration by environment.
 *
 * Set the ENV environment variable to switch environments:
 *   - "dev" (default)
 *   - "test"
 *   - "prod"
 */

type Environment = "dev" | "test" | "prod";

interface AppConfig {
  env: Environment;
  backendUrl: string;
}

const configs: Record<Environment, AppConfig> = {
  dev: {
    env: "dev",
    backendUrl: "http://localhost:8000",
  },
  test: {
    env: "test",
    backendUrl: "http://localhost:8000",
  },
  prod: {
    env: "prod",
    backendUrl: "http://localhost:8000",
  },
};

function getConfig(): AppConfig {
  const env = (process.env.ENV ?? "dev") as Environment;
  return configs[env] ?? configs.dev;
}

export const config = getConfig();
