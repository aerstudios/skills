export function getSetting(config: any, key: string) {
    return config[key];
}

const settings = {
    retries: 3,
    endpoint: "/api",
    telemetry: true,
};

const retries = getSetting(settings, "retries");
retries.toFixed(0);

const endpoint = getSetting(settings, "endpoint");
endpoint.toUpperCase();