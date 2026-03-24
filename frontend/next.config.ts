import type { NextConfig } from "next";
import { config } from "./src/config";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${config.backendUrl}/api/:path*`,
      },
      {
        source: "/health",
        destination: `${config.backendUrl}/health`,
      },
    ];
  },
};

export default nextConfig;
