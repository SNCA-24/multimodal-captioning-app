const DEFAULT_API_BASE_URL = "http://127.0.0.1:5000";

const apiBaseUrl = (process.env.REACT_APP_API_BASE_URL || DEFAULT_API_BASE_URL).replace(/\/$/, "");

export function buildApiUrl(path) {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${apiBaseUrl}${normalizedPath}`;
}

export { apiBaseUrl };
